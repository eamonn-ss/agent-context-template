---
name: session-handoff
description: Create a reliable cross-session or cross-agent handoff grounded in current task state, decisions, validation evidence, and Git changes.
---

# Session Handoff

Use before ending substantial unfinished work, switching agents/tools, or when
context is becoming unreliable.

## Evidence First

Inspect `.agent/CURRENT_TASK.md`, `.agent/DECISIONS.md`, and the relevant records.
Collect `git status --short`, `git diff --stat`, `git diff`, and
`git log --oneline -5`. Summarize diffs; never paste suspected credentials,
tokens, private keys, `.env` values, or other secrets. Instead write:

`Sensitive value detected in changed file; content omitted.`

## Write

Update `.agent/HANDOFF.md` with Goal, Completed, Modified Files, Technical
Decisions, Current Problem, Attempts Made, Failed Approaches, Important Evidence,
Open Questions, Next Steps, and Suggested First Action. Preserve failed
approaches even when none succeeded.

Create one structured summary in `.agent/sessions/YYYY-MM-DD-NN.md` containing
Objective, Completed, Decisions, Files Changed, Problems, Failed Attempts,
Discoveries, and Next Step. Do not copy chat transcripts.

Update `CURRENT_TASK.md` to match verified state. Record commands and actual
results, distinguish completed from merely written, and leave unrelated state
untouched.
