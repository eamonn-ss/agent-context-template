# V1 AI Context Index

> Compatibility reference only. V2 agents start at `../AGENTS.md` and use
> `../.agent/` as canonical state. See `../docs/migration-v1-to-v2.md`.

This file is the navigation map for project context.

Do not read every context file by default. Read the minimum set needed for the task.

## Always Read

| File | Purpose |
|---|---|
| `../AGENTS.md` | Agent working protocol |
| `current.md` | Current project state |

## Stable Context

| File | Read When |
|---|---|
| `context.md` | You need project goals, environment, constraints, terminology |
| `architecture.md` | You need module boundaries, data flow, interfaces, dependencies |

## Decisions

Directory:

```text
decisions/
```

Read relevant ADRs before changing:

- architecture;
- interfaces;
- dependencies;
- data formats;
- algorithms;
- infrastructure;
- deployment assumptions.

Index: `decisions/README.md`

Ignore `*-template.md` — skeletons live under `templates/`.

## Tasks

Directory:

```text
tasks/
```

Each active piece of work should have a task file.

Index: `tasks/README.md`

Ignore `*-template.md` — skeletons live under `templates/`.

## Handoffs

Directory:

```text
handoffs/
```

Read the latest relevant handoff when resuming unfinished work.

Index: `handoffs/README.md`

Ignore `*-template.md` — skeletons live under `templates/`.

## History

| File | Purpose |
|---|---|
| `changelog.md` | Human/AI-readable semantic project history |
| `archive/` | Old state documents no longer needed in normal context |

## Templates

Reusable skeletons and session prompts:

```text
templates/
├── TASK-000-template.md
├── ADR-0000-template.md
├── HANDOFF-template.md
├── new-task.md
├── session-start.md
└── session-end.md
```

Copy a skeleton into the matching registry directory before using it. Do not edit templates in place as if they were active work.
