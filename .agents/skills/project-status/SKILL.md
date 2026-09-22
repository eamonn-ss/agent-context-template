---
name: project-status
description: Answer where a project currently stands using canonical task and handoff state, Git, decisions, hypotheses, TODOs, and recent sessions.
---

# Project Status

Run `python .agent-context/scripts/context_status.py` when available, then verify any surprising
result against its source file.

Read only:

- `.agent-context/state/CURRENT_TASK.md` and `.agent-context/state/HANDOFF.md`
- current Git status
- `.agent-context/state/DECISIONS.md`
- open entries in `.agent-context/memory/HYPOTHESES.md`
- `.agent-context/state/TODO.md`
- the newest relevant session summary when needed

Do not load the complete archive. Report the current goal and status, blockers,
modified files, last handoff, open decisions/hypotheses, near-term TODOs, context
health, and the most useful next action. Separate verified evidence from stale or
missing state.
