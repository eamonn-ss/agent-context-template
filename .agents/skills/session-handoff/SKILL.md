---
name: session-handoff
description: Use when ending unfinished work, switching agents, or when a finished task is still marked active. Do not use when the handoff already matches the task and Git state.
---

# Session Handoff

Collect `git status --short`, `git diff --stat`, `git rev-parse HEAD`, and
`git log --oneline -5`. Leave the full diff in Git. Important Evidence is the
command, its exit code, and one result sentence. If a diff may contain a
secret, write only:

`Sensitive value detected in changed file; content omitted.`

`Done when` names the command and the observed result.

- Good: `python -m unittest discover -s .agent-context/tests -v` exits 0.
- Bad: "tests passed".

Update `.agent-context/state/HANDOFF.md` using the sections in
`.agent-context/templates/HANDOFF.template.md`. Git Evidence is:

```text
- commit: <full HEAD sha, or unavailable>
- worktree: clean
```

Use `dirty` when `git status --short` is not empty. Keep failed approaches,
including when none succeeded.

Write one `.agent-context/sessions/YYYY-MM-DD-NN.md` summary, not a transcript.
Update `CURRENT_TASK.md` to match verified state only.
