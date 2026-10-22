# Architecture

## Context Layers

```text
Rules           AGENTS.md
Discovery       .agents/skills/*/SKILL.md
State           .agent-context/state/*.md
Memory          .agent-context/memory/{FACTS,HYPOTHESES,DISCOVERIES}.md
History         .agent-context/sessions/ -> .agent-context/archive/
Implementation  .agent-context/{scripts,templates,docs,integrations,tests}/
Evidence        application code, tests, and optional Git
```

## Lifecycle

```text
project-init -> context-start (bootstrap | resume) -> work -> handoff
                       ^                              |
                       +-------- next session --------+
```

Skills describe lifecycle operations and remain agent-discoverable; they never
store project facts. `.agent-context/` owns all implementation and persistent
context data. Business `docs/`, `scripts/`, and `tests/` remain application
space and are excluded from framework installation.

## Components

- `AGENTS.md`: durable behavior, source priority, and safety rules.
- `.agents/skills/`: small, vendor-neutral operational procedures.
- `.agent-context/state/`: canonical project state and decision index.
- `.agent-context/memory/`, `sessions/`, `archive/`, and `decisions/`: durable
  knowledge and structured history.
- `.agent-context/scripts/context_paths.py`: constants and upward root discovery.
- `.agent-context/scripts/context_start.py`: deterministic session routing.
- `.agent-context/scripts/validate_context.py` and `context_status.py`: health
  checks with explicit namespaced and legacy-layout reporting.
- `.agent-context/scripts/init-ai-context.sh`: dry-run-capable development and
  embedded profile installer that does not use business generic directories.
- `.agent-context/scripts/migrate_v21_to_v22.py`: guarded one-time V2.1 migration.

## Compatibility Boundary

The `.ai/` tree is retained only as V1 migration evidence. A V2.1 `.agent/`
tree is detected as legacy and must migrate once; tools do not dual-write.
See `.agent-context/docs/migration-v1-to-v2.md` and
`.agent-context/docs/migration-v2.1-to-v2.2.md`.

## Dependencies

Python tools use only the standard library. Git is optional: initialization,
routing, status, validation, and handoff procedures degrade explicitly when Git
evidence is unavailable.
