---
name: context-start
description: Use at the start of every session. Do not use to create Project files, write a handoff, record a decision, or archive sessions.
---

# Context Start

Run `python .agent-context/scripts/context_start.py`, then
`python .agent-context/scripts/context_status.py`. If freshness is stale, report
the reason before following the section below. When the reason says the current
work is not recorded, the previous session did not close. Preserve uncommitted
work.

## INIT_REQUIRED

Project or Architecture is missing or still templated. Stop loading and run
`project-init`. Return:

```text
Mode: INIT_REQUIRED
Project context has not been initialized.
Run /project-init first.
```

## RESUME

Use only when the script selects RESUME. A completed or template task never
uses this section.

1. Read `.agent-context/state/CURRENT_TASK.md` and `HANDOFF.md`.
2. Run `python .agent-context/scripts/context_status.py`. If freshness is stale,
   report the Git mismatch before continuing.
3. Read `git diff --stat`. Open a full diff only for files that disagree with
   the handoff.
4. Read decisions and open hypotheses cited by the task.
5. Reconcile the handoff with code, tests, and Git before editing.

Report the goal, last completed work, blocker, modified files, failed attempts,
relevant decisions, and the next action.

## BOOTSTRAP

Use only when the script selects BOOTSTRAP. Do not create Project or
Architecture here.

1. Read Project, Architecture, Current Task if it is usable, Handoff, the
   decision index, and open hypotheses.
2. Run `python .agent-context/scripts/collect_git_state.py --json` when
   available. Otherwise read the branch, `git status --short`, and the latest
   five commits.
3. Do not read all sessions, archives, source files, or diffs. Exclude
   `.agent-context/` and `.agents/` when exploring application code.

Report the project, architecture, goal, status, branch, modified files,
problems, open decisions, open hypotheses, and the recommended first action.
