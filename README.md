# lesson-plan-quiz

Have an AI agent **teach you the code it just wrote** — with a lesson plan, a
multiple-choice quiz, and a commit history you can see the improvement in.

Developers are experts, and we can *remain* experts while automating the actual
job of writing code. This skill turns every PR into a classroom: the same agent
that shipped a feature builds a self-paced lesson plan that verifies you
actually understand it before you approve it.

> The companion explainer: *"Pop Quiz, Hotshot: A Method for Agent-driven Code
> Review"* — <https://condour.github.io/lesson-plan-quiz/>

## What it does

When you ask (e.g. *"quiz me on this change"* / *"make me a lesson plan"* /
*"make sure I understand this before I ship it"*), the agent:

1. **Scopes the change** — a commit, a diff, or a feature — and reads the actual
   code before writing anything.
2. **Decides what to teach.** Which concepts matter, what the architecture is,
   which trade-offs were made, and what you already know. Those answers drive
   the outline, not the shape of the diff.
3. **Sizes** the plan — a single PR gets one quiz; a feature gets a multi-module
   course (`00-big-picture.md` … `NN-code-reading-round.md`), ~30–45 minutes.
4. **Writes self-contained modules.** Each module teaches one concern with code
   quoted inline, then ends with multiple-choice questions answerable from that
   module alone. (Multi-select is allowed, as long as the question says how many
   answers to pick.)
5. **Adds a "final boss" round.** The last module forces you to actually open
   the code and trace logic across files — not just re-read the lesson.
6. **Runs it live in chat.** The full module text first, then one question at a
   time, key withheld, graded immediately with cites to the real code. It pauses
   at the end of every module to ask what you thought — of the code *and* of the
   questions.
7. **Takes feedback via a "sidebar."** Park a concern without derailing the run.
   The list is agent-visible, so it records the note verbatim, flags later lesson
   content and questions that depend on how the note resolves, and tells you when
   something is foundational enough to abort over. Reconcile at a boundary you
   pick — end of module, end of run, or on demand — and triage each item:
   **fix now**, **accept**, **defer**, or **dismiss**.
8. **Commits the training docs** on a feature branch, so the knowledge lives
   beside the code.

The answer key is a single plaintext `answers.md` — withheld until you've
answered, so you reconcile honestly rather than pattern-matching.

## Files

- `SKILL.md` — the skill itself (frontmatter + full instructions)
- `templates.md` — single-quiz and multi-module templates
- `examples/years-web-game/` — a real worked example: the training docs
  generated for the `years` web game (four lesson modules, a code-reading round,
  and a shared `answers.md`)
- `docs/` — the companion article, published via GitHub Pages

## Install

Place `SKILL.md` + `templates.md` in your agent's skills directory:

- **pi**: `~/.pi/agent/skills/lesson-plan-quiz/`
- **Claude Code**: `~/.claude/skills/lesson-plan-quiz/`
- **Cursor**: `.cursor/skills/lesson-plan-quiz/`

Then ask your agent to quiz you on a change.

## The method in one line

Automate the *writing* of code — never the *understanding*.
