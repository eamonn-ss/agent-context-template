---
name: context-bootstrap
description: Load an initialized repository's project-oriented context without scanning broad history or source trees; use project-init first when canonical state is still templated.
---

# Context Bootstrap

Build a compact, evidence-backed project view. This is the explicit advanced
entry for project orientation; `context-start` is the normal automatic router.

## Workflow

1. Read `AGENTS.md` and follow its source priority and safety rules.
2. Confirm `.agent-context/state/PROJECT.md` and
   `.agent-context/state/ARCHITECTURE.md` are initialized. If
   either is missing or contains template placeholders, stop and use
   `project-init`; bootstrap loads canonical context but does not create it.
3. Read Project, Architecture, Current Task, and Handoff from
   `.agent-context/state/`. Report missing files; do not invent their contents.
4. Run `python .agent-context/scripts/collect_git_state.py --json` when available. Otherwise
   inspect the branch, `git status --short`, and the latest five commits.
5. Read `.agent-context/state/DECISIONS.md` and only the decision records
   relevant to the current task. Read
   `.agent-context/memory/HYPOTHESES.md` for open items.
6. Resolve contradictions using `AGENTS.md`. Mark claims as unknown when they
   cannot be verified.

Return: Project, Architecture, Current Goal, Current Status, Active Branch,
Modified Files, Known Problems, Last Handoff, Open Decisions, Open Hypotheses,
and Recommended First Action.

Do not read all sessions, archives, source files, or Git diffs by default. When
exploring application source, exclude `.agent-context/` and `.agents/` so the
framework is not mistaken for product architecture. Go deeper only when the
current task or a detected contradiction requires it.
