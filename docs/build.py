import os, re, subprocess, html

ART  = os.path.expanduser("~/article/knowing-is-half-the-battle.md")
IMGD = os.path.expanduser("~/article/images")
OUT  = os.path.expanduser("~/lesson-plan-quiz-repo/docs")
os.makedirs(os.path.join(OUT, "images"), exist_ok=True)

md = open(ART).read()
title = re.search(r'^#\s+(.+)$', md, re.M).group(1).strip()

body = subprocess.run(
    ["pandoc","-f","markdown+smart-implicit_figures","-t","html5","--no-highlight","--wrap=none"],
    input=md, capture_output=True, text=True, check=True).stdout

# drop the h1 (the template renders it) and pair each image with its caption
body = re.sub(r'<h1[^>]*>.*?</h1>\s*', '', body, count=1, flags=re.S)

def figurize(m):
    alt, src = m.group("alt"), m.group("src")
    name = os.path.basename(src)
    stem, ext = os.path.splitext(name)
    light = os.path.join(IMGD, stem + "-light" + ext)
    if os.path.exists(light):
        media = ('<picture>'
                 f'<source srcset="images/{stem}{ext}" media="(prefers-color-scheme: dark)">'
                 f'<img src="images/{stem}-light{ext}" alt="{alt}" loading="lazy">'
                 '</picture>')
    else:
        media = f'<img class="shot" src="images/{name}" alt="{alt}" loading="lazy">'
    return "<<<FIG>>>" + media + "<<<ENDFIG>>>"

body = re.sub(r'<img\s+src="(?P<src>[^"]+)"\s+alt="(?P<alt>[^"]*)"[^>]*?/?>', figurize, body, flags=re.S)


# Captions are explicit: a ::: caption ::: fenced div. Pandoc renders it as
# <div class="caption">. When one directly follows an image or code block,
# fold the pair into <figure>/<figcaption>; otherwise style it where it stands.
CAP = r'<div class="caption">\s*<p>(?P<cap>.*?)</p>\s*</div>'
body = re.sub(r'<p><<<FIG>>>(?P<m>.*?)<<<ENDFIG>>></p>\s*' + CAP,
              lambda m: f'<figure>{m.group("m")}<figcaption>{m.group("cap")}</figcaption></figure>',
              body, flags=re.S)
body = re.sub(r'(?P<pre><pre\b.*?</pre>)\s*' + CAP,
              lambda m: f'<figure class="code">{m.group("pre")}'
                        f'<figcaption>{m.group("cap")}</figcaption></figure>',
              body, flags=re.S)
body = re.sub(r'<p><<<FIG>>>(.*?)<<<ENDFIG>>></p>',
              lambda m: f'<figure>{m.group(1)}</figure>', body, flags=re.S)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="color-scheme" content="dark light">
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>
<h1>{html.escape(title)}</h1>
{body}
</main>
</body>
</html>
"""
open(os.path.join(OUT, "index.html"), "w").write(page)

# copy images (skip the render sources)
import shutil
n = 0
for f in sorted(os.listdir(IMGD)):
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")):
        shutil.copy2(os.path.join(IMGD, f), os.path.join(OUT, "images", f)); n += 1
print("title:", title)
print("images copied:", n)
print("figures:", page.count("<figure>"), " pictures:", page.count("<picture>"))
