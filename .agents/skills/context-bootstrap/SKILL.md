---
name: context-bootstrap
description: Establish minimum reliable project context when entering a repository for the first time, without scanning broad history or source trees.
---

# Context Bootstrap

Build a compact, evidence-backed starting view.

## Workflow

1. Read `AGENTS.md` and follow its source priority and safety rules.
2. Read `.agent/PROJECT.md`, `ARCHITECTURE.md`, `CURRENT_TASK.md`, and
   `HANDOFF.md`. Report missing files; do not invent their contents.
3. Run `python scripts/collect_git_state.py --json` when available. Otherwise
   inspect the branch, `git status --short`, and the latest five commits.
4. Read `.agent/DECISIONS.md` and only the decision records relevant to the
   current task. Read `.agent/memory/HYPOTHESES.md` for open items.
5. Resolve contradictions using `AGENTS.md`. Mark claims as unknown when they
   cannot be verified.

Return: Project, Architecture, Current Goal, Current Status, Active Branch,
Modified Files, Known Problems, Last Handoff, Open Decisions, Open Hypotheses,
and Recommended First Action.

Do not read all sessions, archives, source files, or Git diffs by default. Go
deeper only when the current task or a detected contradiction requires it.
