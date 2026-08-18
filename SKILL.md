---
name: lesson-plan-quiz
description: >-
  Builds a lesson plan and/or quiz that verifies understanding of a feature,
  commit, or PR before it ships, then commits it as a training doc under
  docs/training/ with a shared plaintext answers.md answer key.
  Use when the user asks to be quizzed on a change, wants to make sure they
  understand a PR/feature before releasing it, asks for a "lesson plan," or
  says things like "quiz me on this," "test my understanding," or "make sure
  I get this before I ship it."
---

# Lesson plan + quiz

Verifies the user's understanding via an interactive **multiple-choice**
quiz, then permanently records it as a training doc in `docs/training/` in
**the current repository**, alongside the code being studied. Keep training
docs in the repo that owns the code; don't scatter them elsewhere.

## Two question tiers (required)

| Tier | Where | What the reader has | Question style |
| --- | --- | --- | --- |
| **Lesson modules** | `00` … `NN-1` | Only the module text (code snippets quoted inline) | MC answerable **without** opening the repo |
| **Code-reading round** | Final module (`NN-code-reading-round.md` or `NN-boss-round.md`) | The actual codebase | MC that requires tracing logic in real files |

**Lesson modules must be self-contained.** Each module is a short tour: an
objective, key ideas, code snippets or diagrams inline, and 2–4 MC questions
whose correct answers are derivable from **that module's content alone**. Do
not point the reader at files they must open to answer — put the relevant
code or behavior in the lesson body.

**The final code-reading round is the exception.** Those questions require
opening the referenced files, reading two things side by side (two methods, a
doc vs. code, a schema vs. its consumer), and noticing where they agree or
disagree. They should require thinking, not a single grep hit. 

## Question rules (all tiers)

- **Multiple choice only** — lettered A/B/C/D (occasionally E). No
  open-ended "explain in your own words" prompts. This keeps grading
  unambiguous in chat and in the saved file.
- **Balanced distractors** — wrong options must be plausible and **similar
  in length and detail** to the correct one. Avoid the tell where the
  longest option is always right.
- **Cite real identifiers** — function/class/file names, config values,
  exact conditions. Prefer questions whose answer hinges on a specific line
  of logic over ones answerable from a comment alone.
- **Dead code and doc/code mismatches are fair game** — if the codebase has
  unimplemented features, misleading comments, or unused paths, quizzing on
  them is valuable. Do not sanitize the quiz to hide them unless the user
  asks.

## Workflow

1. **Scope it.** Confirm what's being tested: a commit (`git show <sha>`),
   a diff (`git diff main...HEAD`), or a feature/RFC. Read the actual
   diff/files before writing anything.
2. **Size it.** Target **~30–45 minutes** total for a multi-module plan.
   One commit/PR → a single quiz file (5–10 MC questions) is fine; still
   split into a short "lesson" section (self-contained prose + MC) and a
   "code-reading" section (MC requiring the repo) if the topic warrants it.
   A multi-system feature → numbered modules `00-big-picture.md` through
   `NN-code-reading-round.md` plus `README.md`. See
   [templates.md](templates.md).
3. **Write the lessons first.** For each module: objective → tour the
   mechanism (with inline snippets) → MC quiz. Verify each question is
   answerable from the module text before moving on.
4. **Write the code-reading round last.** Harder synthesis: trace a path
   end-to-end, compare two implementations, spot a schema/prompt mismatch.
   Not answerable from the lesson text alone.
5. **Run it live in chat.** Post questions with the answer key withheld.
   User answers by letter (e.g. `B` or `1-B, 2-C`). Grade immediately, cite
   the actual code for wrong answers, keep a running score.
6. **Always write the file too** — save under `docs/training/<topic_slug>/`
   per [templates.md](templates.md). Don't wait to be asked.
7. **Write the answer key to a single plaintext file.** Put ALL modules'
   answers in one `answers.md` in the same docs folder (e.g.
   `docs/training/<topic_slug>/answers.md`). Plaintext, no encoding, no ROT13.
   One line per question: `Q1: B — <brief reason>` (or just the letter). The
   agent withholds this file until the user has answered, then reveals/grades
   from it.
8. **Commit on a feature branch**, never `main`/`master`. Ensure staged
   files are formatted before committing.


## Quizzing the developer (running it live)

This is where the method pays off: the quiz is a **teaching conversation**, not
a one-way file dump. Run it live in chat, one question at a time, and treat the
interaction as the product.

**One at a time.** Post a single question with its options and stop. Wait for
the user's answer before moving on. Do not flood them with the whole module.
Pacing keeps the run focused and gives lateral thinking room.

**Show the full module text verbatim before quizzing.** Do NOT condense or
"summarize" the module into bullets — the quiz questions are written against
the module's actual prose and code blocks, and the reader may want to reference
specific wording. When starting a module, paste the module's full text (title,
objective, all prose, all code snippets) exactly as written, then begin the
questions one at a time. A condensed preview defeats the self-contained-module
design.

**Withhold the key.** Never reveal `answers.md` up front. The key is for
*after* the user commits to an answer, so they reconcile honestly rather than
pattern-matching the correct option.

**Grade immediately, cite the code.** When the user answers, tell them
right/wrong at once. For wrong answers, point at the *actual code* they missed
(specific file, function, line) — the correction is the lesson. Keep a running
score.

**Earn the right to push.** If the user answers by guessing instead of
reasoning, ask them to justify their choice briefly before grading. This
separates "knows it" from "got lucky." But keep it light — the goal is
understanding, not an interrogation.

**Answer by letter.** Ask the user to respond `B` or `1-B, 2-C`. Terse input,
fast flow.

**Encourage self-check before decode.** Have the user answer by letter first,
then decode that module's key and reconcile misses, then move on. (See the
sidebar section for run-time feedback while this happens.)

**Offer feedback at the end of EVERY module.** When the user has answered the
last multiple-choice question of a module, explicitly pause to offer a chance
for feedback on BOTH the code and the quiz itself — e.g. "Any thoughts on how
this is built, or on the questions?" Do not just announce the score and move
on to the next module. This is the natural seam for design critiques (the
sidebar's job) and for catching quiz-quality flaws (bad options, ambiguous
stems, misleading wording). Make the offer again at the end of the final
module / whole quiz too. Treat any feedback as a sidebar item and reconcile
it the same way.

## Pair this with the sidebar

While quizzing, keep the sidebar open so the user can flag design concerns
without derailing the run. The quiz catches *misunderstandings*; the sidebar
catches *design criticisms*. Both are legitimate, and both feed the rewrite
loop. See [the sidebar section](#sidebar-run-time-feedback) below.

## Sidebar (run-time feedback)

When running the quiz **live in chat**, use a sidebar so the user can flag
concerns without derailing the active module.

**Agent-visible.** The sidebar is a shared list the agent sees in real time.

When the user drops a note (e.g. `sidebar: <note>` or "put this on the
sidebar"), the agent MUST:

1. **Record** the note verbatim into a running sidebar list — no debate, no
   arguing it's out of scope.
2. **Highlight** any future lesson items or quiz questions that may depend on
   the resolution of the flagged issue (so the user knows what's affected
   downstream). Do not silently proceed into something the note invalidates.
3. **Suggest aborting** the run if the issue is foundational — meaning the
   thing being studied changes shape, so continuing would waste the remaining
   modules. It is a *suggestion*; the user decides. For everything else, keep
   the run going and reconcile later.

**Triage at reconcile.** At the agreed boundary (end-of-module, end-of-run, or
on-demand), work through each sidebar item and mark it:
- **Fix now** — rewrite the code or quiz to match the concern.
- **Accept** — inspect the agent's choice, understand the tradeoff, and
  consciously ratify it even if you'd have done it differently. This is not
  dismissal: you engaged with the design and chose to keep it. It's one of the
  most valuable outcomes, because it's expertise *making a judgment*, not
  blindly trusting the agent.
- **Defer** — park to a real issue list / follow-up session.
- **Dismiss** — not worth acting on.

**Interrupt-vs-sidebar heuristic.** Only interrupt immediately for
*foundation-level* flaws (upstream design that everything else depends on).
Sidebar everything else. The cost of derailing a focused run is high; the cost
of a temporarily-unresolved note is low.

## Answer key file (plaintext, no ROT13)

Store every module's answers in **one** plaintext `answers.md` in the same
docs folder as the lessons. Do NOT encrypt, do NOT use ROT13, do not embed the
answers inline in the lesson files.

Format (keep it terse; reasons are optional but helpful):

```markdown
# Answer key — <Topic>

## Module 00
- Q1: B — the server reads the pre-generated movies.json at startup.
- Q2: A — grading happens in /api/submit, never on the client.
- Q3: C — Vite proxies /api/* to the Express backend (4310).

## Module 01
- Q1: A — sort_by=vote_count.desc.
...
```

Why plaintext and separate:

- **No refusal surface.** Encoding answers (ROT13 or otherwise) sometimes
  triggers safety refusals for looking like obfuscation. Plaintext eliminates
  it entirely.
- **No formatter footguns.** Encoded blocks get corrupted by markdown
  formatters (list markers, line reflow). A plaintext answers file can't be.
- **Simpler.** One terse file, easy to maintain and read. The separation from
  the lesson (a different file) is what prevents accidental spoilers while
  skimming — same protection encoding gave, without the cleverness.

**Withholding.** When running the quiz live, do NOT show the answers file until
the user has committed to an answer. Grade from it as you go, then reveal.

**Lesson files should note** where the key lives, e.g. a line in each module:
"Answers are in `answers.md` — attempt the questions before reading it."

## Additional resources

- [templates.md](templates.md) — single-quiz and multi-module templates
- Any existing `docs/training/` entries in the current repo — use the most
  recent one as a structural reference

