# Module 1 — The data pipeline (`fetch-movies.js`)

**Objective:** Follow how a raw TMDB response becomes the cleaned `movies.json`
pool, and what rules govern which movies make the cut.

## Entry point

`main()` is a guard + orchestration wrapper:

```js
async function main() {
  if (existsSync(OUT_FILE)) {
    console.log(`movies.json already exists (${OUT_FILE}) — delete it first to re-download.`);
    const existing = JSON.parse(await readFile(OUT_FILE, 'utf8'));
    console.log(`Found ${existing.length} cached movies.`);
    process.exit(0);
  }
  // ...otherwise call download() and writeFile(OUT_FILE, JSON.stringify(movies, null, 2))
}
```

Note the **one-time contract**: if `movies.json` already exists, the script
bails out instead of clobbering the cache. To refresh, delete the file and
re-run.

## Honing in on "well-known"

TMDB orders by a field we choose. The script asks for `vote_count.desc`, i.e.
the movies with the most ratings first — a proxy for films people actually
recognise:

```js
url.searchParams.set('sort_by', 'vote_count.desc');
```

`download()` walks pages (20 results each) and stops once it has collected
`DESIRED_COUNT` (**1000**) cleaned movies, with a `MAX_PAGES` (120) safety
cap and a 250 ms `sleep` between pages to be polite to the API.

## The filter that decides "is this keepable"

Per raw result `r`, all of these must hold to be pushed into the pool:

```js
if (r.adult || r.video) continue;                                   // (1) not adult/short video

const year = parseInt(String(r.release_date || '').slice(0, 4), 10); // (2) parse first 4 chars
if (!Number.isFinite(year) || year < MIN_YEAR) continue;            // must be a real number >= MIN_YEAR

if (seenById.has(r.id) || seenByTitle.has(r.title)) continue;        // (3) no duplicates
seenById.add(r.id);
seenByTitle.add(r.title);
```

- **(1)** rejects adult content and videos that aren't real theatrical films.
- **(2)** `MIN_YEAR === 1950` — and note it's **`>=`**, so a movie released in
  1950 itself passes; anything earlier is dropped.
- **(3)** a row is dropped if its `id` **or** its exact `title` has already been
  seen. Two different films that share a title collapse to one row — and
  because rows arrive ordered by `vote_count.desc`, the higher-vote title is
  seen first and kept.

Because we keep removing movies, we may paginate past page 1; the log reports
`page N: <kept> movies` as it goes. After reaching the goal it trims to the
first 1000 with `movies.slice(0, DESIRED_COUNT)`.

Each kept row is reduced to exactly what the game needs:

```js
movies.push({ id: r.id, title: r.title, year, vote_count: r.vote_count, poster: r.poster_path || null });
```

## Quiz

Answer from **this module only**.

**Q1.** How does the script choose which movies to prioritise while downloading?

- A. It sets `sort_by=vote_count.desc`, so the most-voted films arrive first.
- B. It sorts by the release date, newest first.
- C. It requests the smallest `vote_average` first to find obscure films.
- D. It picks a random page of TMDB each loop to maximise variety.

**Q2.** The year filter is `year < MIN_YEAR → continue` with `MIN_YEAR = 1950`.
Which statement is exactly true?

- A. Only films released strictly after 1950 are kept.
- B. Films released in 1950 and later are kept (1950 passes).
- C. The filter also rejects every film with a poster.
- D. The filter rejects all films released before 2010.

**Q3.** A second TMDB row arrives whose title has already been seen by the
dedup filter. What happens at that exact point in `download()`?

- A. It is added to `seenByTitle` immediately, then filtered out later.
- B. It is skipped by a guard-first `continue` before it is ever added to a set
  or kept in the pool.
- C. It overwrites the earlier row that already had the title.
- D. The first row is removed to make room for the second.

**Q4.** Two different films share the exact same title but different vote
counts. Which single row ends up in `movies.json`?

- A. Both rows survive, doubling that title's appearances.
- B. The one with the lower `vote_count`.
- C. The one with the higher `vote_count` (it arrives first under
  `vote_count.desc` ordering).
- D. Neither — the title is dropped entirely.

## Answer key

Answers are in `answers.md` — attempt the questions before reading it.