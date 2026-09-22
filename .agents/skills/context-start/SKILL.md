---
name: context-start
description: Route a new repository session to initialization, project bootstrap, or active-task resume using canonical state and current Git evidence.
---

# Context Start

Use this as the default entry point for every new session after the framework is
installed. It routes to an existing lifecycle Skill; it does not replace their
evidence and safety rules.

## Route

1. Read `AGENTS.md` and preserve current uncommitted work.
2. Inspect Project, Architecture, Current Task, and Handoff under
   `.agent-context/state/`, plus concise Git state when Git is available.
3. Run `python .agent-context/scripts/context_start.py` when available. Otherwise apply the
   same rules below, treating missing, empty, or placeholder-bearing files as
   unusable.

### `INIT_REQUIRED`

Select when Project or Architecture is missing or still contains scaffold
placeholders. Return exactly these leading lines and stop normal loading:

```text
Mode: INIT_REQUIRED
Project context has not been initialized.
Run /project-init first.
```

### `RESUME`

Select only when Current Task is usable and active and Handoff is usable.
Return `Mode: RESUME`, then follow `../context-resume/SKILL.md`. Prioritize the
task, handoff, current Git changes, failed attempts, blockers, relevant
decisions, and next action.

### `BOOTSTRAP`

Select when project context is initialized but no valid active-task/handoff pair
exists, including when the previous task is complete. Return `Mode: BOOTSTRAP`,
then follow `../context-bootstrap/SKILL.md`. Prioritize Project, Architecture,
Current Task if usable, project status, decisions, and hypotheses.

A template Current Task is never active, a template Handoff is never usable,
and a completed task never routes to Resume.
