# lesson-plan-quiz

Have an AI agent **teach you the code it just wrote** — with a lesson plan, a
multiple-choice quiz, and a commit history you can see the improvement in.

Developers are experts, and we can *remain* experts while automating the actual
job of writing code. This skill turns every PR into a classroom: the same agent
that shipped a feature builds a self-paced lesson plan that verifies you
actually understand it before you approve it.

> The companion explainer: *"Knowing is Half the Battle"* (link to article).

## What it does

When you ask (e.g. *"quiz me on this change"* / *"make me a lesson plan"* /
*"make sure I understand this before I ship it"*), the agent:

1. **Sizes** a lesson plan to the change — a single PR gets one quiz; a feature
   gets a multi-module course (`00-big-picture.md` … `NN-code-reading-round.md`),
   ~30–45 minutes total.
2. **Writes self-contained modules.** Each module teaches one concern with code
   quoted inline, then ends with multiple-choice questions answerable from that
   module alone.
3. **Adds a "final boss" round.** The last module forces you to actually open
   the code and trace logic across files — not just re-read the lesson.
4. **Runs it live in chat.** One question at a time, key withheld, graded
   immediately with cites to the real code.
5. **Takes feedback via a "sidebar."** Park design critiques as you go, reconcile
   them at the end — and the agent rewrites code *or* the quiz to match.
6. **Commits the training docs** so the knowledge lives beside the code.

The answer key is a single plaintext `answers.md` — withheld until you've
answered, so you reconcile honestly rather than pattern-matching.

## Files

- `SKILL.md` — the skill itself (frontmatter + full instructions)
- `templates.md` — single-quiz and multi-module templates
- `examples/` — a real worked example: the training docs generated for the
  `years` web game (4 modules + final boss + answers.md)

## Install

Place `SKILL.md` + `templates.md` in your agent's skills directory:

- **pi**: `~/.pi/agent/skills/lesson-plan-quiz/`
- **Claude Code**: `~/.claude/skills/lesson-plan-quiz/`
- **Cursor**: `.cursor/skills/lesson-plan-quiz/`

Then ask your agent to quiz you on a change.

## The method in one line

Automate the *writing* of code — never the *understanding*.