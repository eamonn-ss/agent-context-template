---
name: project-init
description: Use when canonical Project or Architecture files are missing or still templated. Do not use at ordinary session start or to continue a task.
---

# Project Init

Create `.agent-context/state/PROJECT.md` and `ARCHITECTURE.md` only when
`context-start` reports `INIT_REQUIRED`. If it does not, stop. Do not rewrite
initialized files to normalize wording.

Read README files and build manifests, then only enough application source to
support those claims. Always exclude `.agent-context/`, `.agents/`, `.git/`,
`node_modules/`, `.venv/`, `venv/`, `__pycache__/`, `build/`, `dist/`, and
`coverage/`. Do not scan history by default. Label gaps `Unknown`.

Write purpose, users, goals, non-goals, and runtime in `PROJECT.md`. Write the
current components, flow, interfaces, and dependencies in `ARCHITECTURE.md`.
A Fact needs file, command, test, commit, or decision evidence. Uncertain
claims stay Hypotheses or `Unknown`. Do not create `CURRENT_TASK.md` or a
handoff unless the user named an active task.

Run `python .agent-context/scripts/validate_context.py`. When no task was
given, end with:

```text
No active engineering task is defined.
Describe a task before creating CURRENT_TASK.
```
