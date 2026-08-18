# Module 2 — Round generation (`server.js`)

**Objective:** See how one `/api/round` call turns the loaded pool into a fair,
well-formed puzzle — and what guarantee the game depends on.

## Reading the pool once

At startup the server loads the whole pool into memory and shuts down if it's
missing:

```js
let movies = [];
try {
  const data = JSON.parse(await readFile(path.join(__dirname, 'movies.json'), 'utf8'));
  movies = data;
} catch (err) {
  console.error('Could not load movies.json — run "npm run fetch" first.');
  process.exit(1);
}
const PORT = process.env.PORT || 4310;
```

After this, `movies` is a module-level array, reused by every request.

## A cryptographic shuffle

The server brings its own shuffle rather than `Math.random`, for unbiased
ordering — a Fisher–Yates style loop seeded with `crypto.randomBytes`:

```js
function shuffled(arr) {
  const out = [...arr];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(crypto.randomBytes(4).readUInt32BE(0) / 0xffffffff * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}
```

## The one-to-one guarantee

`buildRound()` walks a shuffled copy of the pool, keeping a set of years it has
already used. A movie is kept only if its release year is **new**:

```js
function buildRound() {
  const picked = [];
  const usedYears = new Set();
  for (const m of shuffled(movies)) {
    if (usedYears.has(m.year)) continue;   // already have this year → skip
    picked.push(m);
    usedYears.add(m.year);
    if (picked.length === 4) break;        // four distinct years is enough
  }

  return {
    // No `year` fields and no roundId: the browser must not know the true
    // years, and grading needs no per-round state.
    movies: picked.map(({ id, title, poster }) => ({ id, title, poster })),
    years: shuffled(picked.map((m) => m.year)),   // shuffled display years
  };
}
```

Two deliberate consequences:

- **Distinct years.** No two movies in a round share a release year. That makes
  "title → year" a true one-to-one mapping, so the matching puzzle has a
  well-defined answer.
- **Stateless truth.** Each movie's real `year` is **never** included in the
  payload (`movies: [...]` keeps only `id`, `title`, `poster`), and there is no
  `roundId` or stored answer key. The true title→year mapping is simply the
  server's in-memory pool (`moviesById`). The four `years` sent are only the
  **shuffled display values**; the browser can't tell which year belongs to
  which movie until the server grades the round (via `POST /api/submit`,
  Module 3).

## Serving

```js
app.get('/api/round', (_req, res) => {
  res.set('Cache-Control', 'no-store');
  res.json(buildRound());
});
```

`Cache-Control: no-store` stops browsers/proxies from reusing a round. Finally
the server serves the built React bundle (`client/dist`) and, for anything not
under `/api`, returns `index.html` (SPA-style fallback).

## Grading (server-side, stateless)

Grading needs **no stored state**. The client resolves each of its picks to the
actual display-year *value* it chose and POSTs `{ movieId: chosenYear }` to
`/api/submit`. The server looks up each movie's true year on the pool it
already holds (`moviesById`) and compares — there is no round id and nothing
to remember between requests:

```js
const moviesById = new Map(); // id -> movie, built once from the pool

app.post('/api/submit', (req, res) => {
  const { assignments = {} } = req.body || {};
  let correct = 0;
  let total = 0;
  const results = {}; // movieId -> { correct, year: true release year }
  for (const [movieId, chosenYear] of Object.entries(assignments)) {
    const movie = moviesById.get(Number(movieId));
    if (!movie || chosenYear == null) continue;
    total++;
    const ok = Number(chosenYear) === movie.year;
    if (ok) correct++;
    results[movieId] = { correct: ok, year: movie.year };
  }

  res.json({ correct, total, results });
});
```

Because the answer lives on the pool itself rather than in any per-round
record, the route is **stateless and idempotent**: replaying the same body
yields the same grade. `app.use(express.json())` (added near the top of
`server.js`) parses the POST body, so the middleware is used. The response
returns the tally plus, per movie, whether the choice was right and the
**true** year — so the client can show the correct answer without ever having
been trusted with the truth up front.

## Quiz

Answer from **this module only**.

**Q1.** What invariant does `buildRound()` guarantee about the four chosen movies?

- A. They all have the same release year.
- B. They are the four highest-vote-count films in the pool.
- C. No two share a release year.
- D. They are always consecutive pages from TMDB.

**Q2.** Why does the round require each movie to have a *different* year?

- A. So the years look visually distinct on screen.
- B. So the title-to-year mapping is one-to-one and the puzzle is well-defined.
- C. So the client doesn't need the true year value.
- D. To make the puzzle deliberately impossible.

**Q3.** In the `/api/round` payload, which statement is true about how the true
release years are handled?

- A. Each movie object carries its real `year`, and `years` is a reordering of them.
- B. `years` is the only year source sent to the client; the movie→year truth
  lives on the server's in-memory pool and is looked up only at grade time.
- C. Both `years` and each true mapping are sent so the client can grade locally.
- D. `years` gets unrelated random integers; no year is tied to any movie.

## Answer key

Answers are in `answers.md` — attempt the questions before reading it.