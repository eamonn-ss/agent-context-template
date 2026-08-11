# Current Architecture

> Describe the architecture as it exists now. Historical architecture belongs in ADRs or Git history.
>
> After adopting this template into another project, replace this file with that system's architecture.

## System Overview

```text
Agent session
   ↓
AGENTS.md (protocol)
   ↓
.ai/index.md (navigation)
   ↓
Stable: context.md + architecture.md
   ↓
Decisions: decisions/*.md
   ↓
Active: current.md + tasks/*.md
   ↓
History: handoffs/ + changelog.md
   ↓
Code / Tests / Git (final facts)
```

## Major Components

### `AGENTS.md`

Responsibilities:

- Define restore-context protocol, source-of-truth order, and session hygiene

Must not:

- Store project-specific daily status

### `.ai/` context tree

Responsibilities:

- Hold navigable project memory with stable / active / history separation

Must not:

- Mix file templates into `tasks/`, `decisions/`, or `handoffs/` registries

### `scripts/init-ai-context.sh`

Responsibilities:

- Copy missing context files into a target project, including partial `.ai/` trees

### `scripts/check-context.sh`

Responsibilities:

- Verify required files exist; warn about stray templates and bootstrap placeholders

### `.cursor/rules/ai-context.mdc`

Responsibilities:

- Remind Cursor agents to follow `AGENTS.md` before non-trivial work

## Repository Map

```text
.
├── AGENTS.md
├── README.md
├── LICENSE
├── .cursor/rules/ai-context.mdc
├── .cursorignore.example
├── scripts/
│   ├── init-ai-context.sh
│   └── check-context.sh
└── .ai/
    ├── index.md
    ├── context.md
    ├── architecture.md
    ├── current.md
    ├── changelog.md
    ├── decisions/
    ├── tasks/
    ├── handoffs/
    ├── templates/
    └── archive/
```

## Data Flow

1. New session reads `AGENTS.md` → `.ai/index.md` → `.ai/current.md`.
2. Agent loads only task-relevant architecture, ADRs, and task files.
3. Agent verifies Git status / history before editing.
4. Session end updates task / `current.md` / changelog / handoff as needed.

## Important Interfaces

### Agent entry prompt

Input:

```text
Read AGENTS.md and restore project context before making changes.
```

Output:

```text
Brief restore summary, then proceed with the requested task
```

Contract:

- Do not explore the full repository by default when indexed context is sufficient

### Init script

Input:

```text
./scripts/init-ai-context.sh /path/to/project
```

Output:

```text
Missing files added; existing files skipped
```

Contract:

- Never overwrite existing target files
- Populate missing files even when `.ai/` already exists as an empty or partial directory

## Dependency Rules

- Agents may depend on `.ai/` documents and Git state.
- Context documents must not invent facts that contradict code or tests.
- Active registries (`tasks/`, `decisions/`, `handoffs/`) must not depend on chat-only claims.

## Configuration

| Configuration | Location | Notes |
|---|---|---|
| Agent protocol | `AGENTS.md` | Canonical entry |
| Cursor reminder | `.cursor/rules/ai-context.mdc` | `alwaysApply: true` |
| Ignore example | `.cursorignore.example` | Rename after review |

## Validation / Test Entry Points

```bash
./scripts/check-context.sh
./scripts/check-context.sh --strict
bash -n scripts/init-ai-context.sh scripts/check-context.sh
```

## Known Architectural Risks

- Unfilled bootstrap placeholders can be misread as active project state
- Overgrown `current.md` or `context.md` wastes tokens and drifts from Git truth
- Multiple agents editing the same high-conflict files without task branches
