# Module 3 — Client state and interaction (`App.jsx`)

**Objective:** Understand the four pieces of component state, how pick-up/drop
works in both orders, and how Submit is scored.

## The state model

```js
const [selectedMovieId, setSelectedMovieId] = useState(null); // movie picked up
const [selectedYearIdx, setSelectedYearIdx] = useState(null); // year picked up
const [assignments, setAssignments] = useState({});           // { [movieId]: yearIdx }
const [submitted, setSubmitted] = useState(false);
const [result, setResult] = useState(null);                   // server verdict for this round
const [score, setScore] = useState({ correct: 0, total: 0 });
```

Two subtle choices:

- `assignments` maps **movieId → yearIdx**, where `yearIdx` is an *index into
  `round.years`*, not the year value itself. The real year is looked up later
  with `round.years[assignments[movie.id]]`.
- `selectedMovieId` and `selectedYearIdx` are mutually exclusive by convention:
  each click handler clears the other selection first, so at most one thing is
  ever "picked up".

A small helper converts assignments into two lookup views, used by the year
cards to know which indexes are already taken:

```js
const assignedMovieYears = useMemo(() => {
  const byYear = {}, byMovie = {};
  for (const [mid, yIdx] of Object.entries(assignments)) {
    byMovie[mid] = Number(yIdx);
    byYear[Number(yIdx)] = mid;
  }
  return { byYear, byMovie };
}, [assignments]);
```

## Two click orders, one drop rule

The design brief allowed either "movie first, then year" or "year first, then
movie" — the code supports **both**. Symmetrically, each handler:

1. clears the *other* selection (`setSelectedMovieId(null)` / `setSelectedYearIdx(null)`);
2. checks if its counterpart is already picked up → if so, **drop** and assign;
3. otherwise, toggle itself as picked up.

Movie side:

```js
function handleMovieClick(movieId) {
  if (submitted) return;
  setSelectedYearIdx(null);                              // (1) clear lifted year
  if (movieId in assignments) {                          // already assigned?
    const next = { ...assignments };                     //     → un-assign
    delete next[movieId];
    setAssignments(next);
    return;
  }
  if (selectedYearIdx != null) {                         // (2) year is lifted?
    setAssignments((a) => ({ ...a, [movieId]: selectedYearIdx }));
    setSelectedMovieId(null); setSelectedYearIdx(null);
    return;
  }
  setSelectedMovieId(movieId === selectedMovieId ? null : movieId);  // (3) toggle
}
```

Year side:

```js
function handleYearClick(yearIdx) {
  if (submitted) return;
  setSelectedMovieId(null);                              // (1) clear lifted movie
  if (yearIdx in assignedMovieYears.byYear) return;      // taken → ignore
  if (selectedMovieId != null) {                         // (2) movie is lifted?
    setAssignments((a) => ({ ...a, [selectedMovieId]: yearIdx }));
    setSelectedMovieId(null); setSelectedYearIdx(null);
    return;
  }
  setSelectedYearIdx(yearIdx === selectedYearIdx ? null : yearIdx);   // (3) toggle
}
```

Because a year can map to only one movie, the year side *ignores* clicks on an
already-used year index, while the movie side *un-assigns* — an intentional
asymmetry. A movie you click again drops its match, freeing that year for reuse
elsewhere if it was already assigned.

## Submitting and scoring

Submit is enabled only when all four movies are matched. The client holds **no
true years**, so it can't grade its own work. It resolves each assignment
index to the display-year *value* it picked, POSTs that as `{ movieId:
chosenYear }` to `/api/submit`, and lets the server decide:

```js
async function submit() {
  const reported = {};
  for (const [movieId, yearIdx] of Object.entries(assignments)) {
    reported[movieId] = round.years[yearIdx]; // index -> display year value
  }
  const resp = await fetch('/api/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ assignments: reported }),
  });
  if (!resp.ok) throw new Error('failed to submit round');
  const res = await resp.json();
  setResult(res);
  setScore((s) => ({ correct: s.correct + res.correct, total: s.total + res.total }));
  setSubmitted(true);
}
```

Note there's **no round id** sent — the server grades statelessly by comparing
each reported year to the movie's true year on its pool. The response carries
the server's ready-made tally and per-movie verdict (`{ correct, total,
results }`). The client stores it in `result`, adds `res.correct` to the
running score, and `cardState(movie)` reads the server-declared outcome out of
`result.results[movie.id]` — `'correct'` / `'wrong'` (or `null` before submit)
to drive the green/red styling. The footer button switches from **Submit** to
**Next round** (which calls `startRound()` and resets all state).

## Quiz

Answer from **this module only**.

**Q1.** What exactly does `assignments` store as values?

- A. The chosen year value itself, e.g. `1996`.
- B. An index into `round.years` for the chosen year.
- C. The chosen movie's TMDB id.
- D. A boolean saying whether the movie has been matched.

**Q2.** A user clicks a **year first**, then clicks a **movie**. What happens?

- A. The movie is assigned to that year (drop works in this order too).
- B. Nothing — only movie-first order is supported.
- C. The year selection is cleared and the pick-up is cancelled.
- D. The movie replaces whatever was previously assigned to it.

**Q3.** After matching all four movies, you click one of them again. What happens?

- A. The game auto-submits.
- B. The movie is locked in and cannot change.
- C. Its assignment is deleted, un-matching it for the round.
- D. It jumps to the top of the movie list.

## Answer key

Answers are in `answers.md` — attempt the questions before reading it.