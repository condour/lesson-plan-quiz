# Module 4 — Final round (requires opening the code)

Unlike modules 0–3, these questions are **not** answerable from the lesson text
alone. Open the actual files and trace the logic side by side.

**Open:**

- `client/src/App.jsx` — the two handlers `handleMovieClick` / `handleYearClick`,
  the render body, and `submit()`.
- `server.js` — the route wiring (`/api/round`, `/api/submit`, static files).

Work through the trace before answering.

## Quiz

**Q1.** Trace `handleYearClick`. Suppose a movie has been picked up
(`selectedMovieId` set) and the user clicks a year button whose index another
movie **already** uses. What is the exact result?

- A. The new movie overwrites that year's assignment on the card.
- B. The click is ignored (early return) and the movie stays picked up.
- C. Both movies become assigned to the same year and the UI shows a clash.
- D. The earlier movie is un-assigned to make room.

**Q2.** Trace `handleMovieClick` in the *opposite* starting state: a year has
just been picked up (`selectedYearIdx` set), and the user clicks a movie that
**already has** an assignment. Which branch runs, and what ends up where?

- A. `setSelectedYearIdx(null)` runs first, then the "un-assign" branch — the
  movie's assignment is deleted and the lifted year is dropped.
- B. The lifted year overwrites the movie's existing assignment.
- C. The movie is picked up alongside its old assignment, so it appears twice.
- D. The handler returns immediately and nothing changes.

**Q3.** Open `client/src/App.jsx` and find the `.result` span on the movie cards.
For a **wrong** match, it shows the movie's true year. Where does that year
value actually come from?

- A. `assignments` — the year the user picked, looked up in `round.years`.
- B. `result.results[m.id].year` — the true year the server returns in its
  grading response, having only now revealed it to the client.
- C. `round.movies[m.id].year` — a year field pre-loaded on each movie.
- D. A year read straight back out of `movies.json` on the client.

**Q4.** Read `server.js`, focusing on `app.use(express.json())` and the list of
routes (`/api/round`, static files). Does the JSON body-parsing middleware
actually get a request body to parse?

- A. No — `/api/round` is a GET and static serving sends files, so
  `express.json()` is never handed a request body.
- B. Yes — the client POSTs `{ assignments }` (movieId → chosen year value) as
  JSON to `/api/submit` for server-side grading, so the middleware is required.
- C. Yes — the client POSTs JSON straight to `/api/round`.
- D. Yes — WebSocket upgrades send JSON that the middleware reads.

## Answer key

Answers are in `answers.md` — attempt the questions before reading it.