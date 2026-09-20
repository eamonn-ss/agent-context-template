---
name: context-resume
description: Resume unfinished repository work from canonical task, handoff, decisions, and current Git evidence at the start of a new session.
---

# Context Resume

Continue verified work without trusting the prior conversation alone.

## Workflow

1. Read `AGENTS.md`, `.agent/CURRENT_TASK.md`, and `.agent/HANDOFF.md`.
2. Collect current Git state and `git diff --stat`. Inspect the full diff only
   for files relevant to the task or when the summary and worktree disagree.
3. Read decisions referenced by the task/handoff. Check open hypotheses that
   affect the next action.
4. Treat the handoff as a snapshot: reconcile it with code, tests, and Git.
5. If the prior state is stale, say exactly what changed before continuing.

Return: Current Goal, Last Completed Work, Current Blocking Issue, Modified
Files, Known Failed Attempts, Important Decisions, Next Steps, and Suggested
First Action.

Do not load `.agent/archive/` or every session by default. Never overwrite
uncommitted work merely because it is absent from the handoff.
