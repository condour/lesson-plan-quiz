import os, re, subprocess, html

SITE = "https://condour.github.io/lesson-plan-quiz/"
# Shown under the title on Slack/LinkedIn/etc. Aim for ~150 characters.
DESCRIPTION = ("A method for reviewing agent-written code: have the agent build a lesson "
               "plan, quiz you on what it shipped, and rewrite the parts you push back on.")

ART  = os.path.expanduser("~/article/knowing-is-half-the-battle.md")
IMGD = os.path.expanduser("~/article/images")
OUT  = os.path.expanduser("~/lesson-plan-quiz-repo/docs")
os.makedirs(os.path.join(OUT, "images"), exist_ok=True)

md = open(ART).read()
title = re.search(r'^#\s+(.+)$', md, re.M).group(1).strip()

# Prettier does not understand pandoc fenced divs: with proseWrap "never" it
# joins "::: caption / text / :::" onto a single line, which pandoc then emits
# as literal text. Normalise that back to the block form before parsing.
md = re.sub(r'^:::[ \t]*caption[ \t]+(?P<cap>.+?)[ \t]*:::[ \t]*$',
            lambda m: "::: caption\n" + m.group("cap") + "\n:::",
            md, flags=re.M)

body = subprocess.run(
    ["pandoc","-f","markdown+smart-implicit_figures","-t","html5","--no-highlight","--wrap=none"],
    input=md, capture_output=True, text=True, check=True).stdout

# The h1 stays where the markdown puts it, so anything above it (a hero image,
# say) keeps its position. `title` is used only for the <title> tag.

def figurize(m):
    alt, src = (m.group("alt") or ""), m.group("src")
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
    return media

# alt may be absent entirely: pandoc drops the attribute when the alt text is
# empty, as it is for a purely decorative image.
body = re.sub(r'<img\s+src="(?P<src>[^"]+)"(?:\s+alt="(?P<alt>[^"]*)")?[^>]*?/?>',
              figurize, body, flags=re.S)

# Captions are explicit: a ::: caption ::: fenced div, which pandoc renders as
# <div class="caption">. Where one directly follows an image or a code block,
# fold the pair into <figure>/<figcaption>.
#
# Both patterns below are structurally bounded - MEDIA cannot cross a ">" or a
# </picture>, and only whitespace may sit between the parts - so a match can
# never span from one element to a distant one.
MEDIA = r'(?P<m><picture>.*?</picture>|<img\b[^>]*>)'
CAP   = r'<div class="caption">\s*<p>(?P<cap>.*?)</p>\s*</div>'

body = re.sub(r'<p>\s*' + MEDIA + r'\s*</p>\s*' + CAP,
              lambda m: f'<figure>{m.group("m")}<figcaption>{m.group("cap")}</figcaption></figure>',
              body, flags=re.S)
body = re.sub(r'(?P<pre><pre\b.*?</pre>)\s*' + CAP,
              lambda m: f'<figure class="code">{m.group("pre")}'
                        f'<figcaption>{m.group("cap")}</figcaption></figure>',
              body, flags=re.S)
body = re.sub(r'<p>\s*' + MEDIA + r'\s*</p>',
              lambda m: f'<figure>{m.group("m")}</figure>', body, flags=re.S)

assert "FIG>>>" not in body, "stray figure marker survived"

first_img = re.search(r'<img[^>]+src="(?P<src>[^"]+)"', body)
og_image = SITE + first_img.group("src") if first_img else ""
og = ""
if og_image:
    og = (f'<meta property="og:image" content="{og_image}">\n'
          f'<meta name="twitter:image" content="{og_image}">\n'
          '<meta name="twitter:card" content="summary_large_image">\n')
else:
    og = '<meta name="twitter:card" content="summary">\n'

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(DESCRIPTION)}">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(DESCRIPTION)}">
{og}<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(DESCRIPTION)}">
<meta name="color-scheme" content="dark light">
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>
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
