# Templates

Two shapes, chosen by scope (see SKILL.md). Both use **multiple-choice only**.
Both live under `docs/training/<topic_slug>/` in the repo.

## A. Single quiz (one commit/PR)

One file: `docs/training/<topic_slug>/quiz.md`.

Split into two sections when the topic has both "concepts from the diff"
and "details only visible in code":

```markdown
# <Feature/PR Title> — Quiz

A short self-check on <PR #NNNN / commit SHA> (`<repo>`, branch
`<branch-name>`): <one-sentence description>.

**Objective:** <what the reader should understand after completing this>.

## Lesson

<Self-contained tour of the change: what problem it solves, key mechanisms,
important snippets quoted inline. The reader should not need to open the repo
to follow this section.>

## Quiz — from the lesson

Answer from the **Lesson** section above only.

**Q1.** <Question stem>

- A. <option>
- B. <option>
- C. <option>
- D. <option>

**Q2.** ...

## Code-reading round

Open the repo. These questions are **not** answerable from the lesson alone.

**Files to open:**

- `<path/to/file.ts>` — <what to trace>

**Q3.** <Question requiring reading/tracing in those files>

- A. <option — plausible, similar length to correct answer>
- B. <option>
- C. <option>
- D. <option>

## Answer key

Answers live in a **separate plaintext `answers.md`** in the same folder.
Withhold it until the user has answered; grade from it and then reveal. No
encoding.

See [answers.md](#about-the-answer-keys) for the shared format.
```

For a small, fully-described change, a single "Quiz" section (all MC) without
a separate code-reading block is OK — but default to two tiers when the PR
touches non-obvious control flow.

## B. Multi-module lesson plan (preferred for features)

Directory: `docs/training/<topic_slug>/` with `README.md`, modules
`00-big-picture.md` … `NN-code-reading-round.md`.

**Time budget:** ~30–45 minutes total including reading and answering.

**`README.md`:**

```markdown
# <Feature Title> — Training

A self-paced walkthrough of <feature> (<RFC/ticket ref>) in the current
repository.

**Time budget:** ~30–45 minutes end to end.

## How to use this

Work through modules **in order**. Modules 0–N-1 each teach one concern
(with code quoted inline) and end with multiple-choice questions answerable
from **that module's text alone**. The final module requires opening the
actual codebase.

| #   | File                       | Topic                    |
| --- | -------------------------- | ------------------------ |
| 0   | `00-big-picture.md`        | <topic>                  |
| 1   | `01-<topic>.md`            | <topic>                  |
| ... |                            |                          |
| N   | `NN-code-reading-round.md` | Requires opening the code |

## About the answer keys

All modules share **one** plaintext `answers.md` in the same folder, grouped by
module. It is not encoded. It is withheld while quizzing and revealed/graded
from after the user answers.

```markdown
# Answer key — <Topic>

## Module 00
- Q1: B — the server reads the pre-generated movies.json at startup.
- Q2: A — grading happens in /api/submit, never on the client.

## Module 01
- Q1: A — sort_by=vote_count.desc.
...
```

## Suggested workflow

1. Read a module top to bottom.
2. Answer its MC questions (letters only).
3. Have the agent grade you from `answers.md`, then reconcile any misses.
4. Move to the next module. Do the code-reading round last.
```

**Each lesson module (`00` … `NN-1`):**

```markdown
# Module N — <Topic>

**Objective:** <one sentence>.

## <Tour the mechanism>

<Key ideas, flow diagrams, and **code snippets quoted inline**. Everything
needed to answer the quiz below must appear in this module.>

## Quiz

All questions are multiple choice. Answer from **this module only** — you
should not need to open the repo.

**Q1.** <stem>

- A. <option>
- B. <option>
- C. <option>
- D. <option>

## Answer key

See `answers.md` (shared, plaintext) for this module's answers, since last.

```

**Final module (`NN-code-reading-round.md`):**

```markdown
# Module N — Final round (requires opening the code)

Unlike modules 0–N-1, these questions are **not** answerable from the lesson
text or a single grep hit. Each requires reading two things side by side —
two methods, a doc vs. the code, a description vs. its schema — and
noticing where they disagree or interact.

**Q1.** <stem that names specific files/functions to open and trace>

- A. <plausible distractor, similar length to correct answer>
- B. <option>
- C. <option>
- D. <option>

## Answer key

See `answers.md` (shared, plaintext) for this module's answers, since last.

```
