---
name: project-init
description: Initialize real canonical project context for an existing repository on first adoption; do not use for routine session startup.
---

# Project Init

Create evidence-backed `.agent-context/state/PROJECT.md` and
`.agent-context/state/ARCHITECTURE.md` when canonical project state is missing
or still contains template placeholders.

## Verify First-run State

1. Read `AGENTS.md` and inspect current Git status so existing work is preserved.
2. Run `python .agent-context/scripts/context_start.py --json` when available. `INIT_REQUIRED`
   confirms initialization is needed; otherwise do not replace established
   canonical context merely to normalize wording.
3. Treat missing, empty, or placeholder-bearing Project or Architecture files
   as uninitialized. Markers include `<PROJECT_NAME>`, `<TODO>`, `PLACEHOLDER`,
   `TASK-<NNN>`, `<UNCERTAIN_CLAIM>`, and equivalent scaffold tokens.

## Repository Discovery

Inspect only the most informative files that exist, starting with README files,
`docs/`, `pyproject.toml`, `package.json`, `CMakeLists.txt`, `Cargo.toml`,
`requirements*`, `configs/`, and shallow views of application `src/`, `scripts/`,
and `tests/`. Always exclude `.agent-context/`, `.agents/`, `.git/`,
`node_modules/`, `.venv/`, `venv/`, `__pycache__/`, `build/`, `dist/`, and
`coverage/`. The discovery target is the business repository, not this context
implementation. Do not scan the whole repository or its history by default.

Establish, where evidence permits: project purpose, main architecture, key
modules, entry points, runtime dependencies, build/run/test workflow, external
systems, and repository constraints. Label unsupported details `Unknown`.

## Write Canonical Context

- Create `.agent-context/state/` and `.agent-context/memory/` if needed.
- Write a concise `.agent-context/state/PROJECT.md` describing purpose, users, goals,
  non-goals, and runtime.
- Write `.agent-context/state/ARCHITECTURE.md` describing the current system, components,
  important flow, interfaces, and dependencies.
- Preserve non-template user content and unrelated uncommitted changes.
- Add a Fact only when its entry includes concrete file, command, test, commit,
  or decision evidence. Put uncertain claims in Hypotheses with a validation
  plan, or leave them `Unknown`.
- If no active engineering task was explicitly provided, do not create or fill
  `.agent-context/state/CURRENT_TASK.md` and do not invent a handoff.

Run `python .agent-context/scripts/validate_context.py` when the installed context skeleton
supports it, then report evidence, unknowns, and files changed. When no active
task exists, end with:

```text
No active engineering task is defined.
Describe a task before creating CURRENT_TASK.
```
