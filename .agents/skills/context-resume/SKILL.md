---
name: context-resume
description: Explicitly continue an unfinished task from canonical task, handoff, decisions, and current Git evidence; context-start normally selects this mode automatically.
---

# Context Resume

Continue verified task work without trusting the prior conversation alone. This
is the explicit advanced entry when task continuation is intentionally forced;
`context-start` is the normal automatic router.

## Workflow

1. Read `AGENTS.md`, `.agent-context/state/CURRENT_TASK.md`, and
   `.agent-context/state/HANDOFF.md`.
2. Collect current Git state and `git diff --stat`. Inspect the full diff only
   for files relevant to the task or when the summary and worktree disagree.
3. Read decisions referenced by the task/handoff. Check open hypotheses that
   affect the next action.
4. Treat the handoff as a snapshot: reconcile it with code, tests, and Git.
5. If the prior state is stale, say exactly what changed before continuing.

Return: Current Goal, Last Completed Work, Current Blocking Issue, Modified
Files, Known Failed Attempts, Important Decisions, Next Steps, and Suggested
First Action.

Do not load `.agent-context/archive/` or every session by default. Exclude
`.agent-context/` and `.agents/` from application-source exploration. Never
overwrite uncommitted work merely because it is absent from the handoff.
