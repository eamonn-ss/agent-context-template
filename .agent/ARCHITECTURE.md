# Architecture

## Context Layers

```text
Rules     AGENTS.md
Skills    .agents/skills/*/SKILL.md
State     .agent/PROJECT.md, ARCHITECTURE.md, CURRENT_TASK.md, DECISIONS.md,
          HANDOFF.md, TODO.md
Memory    .agent/memory/{FACTS,HYPOTHESES,DISCOVERIES}.md
History   .agent/sessions/ -> .agent/archive/
Evidence  code, tests, and Git
```

## Lifecycle

```text
bootstrap -> work -> record decision/fact -> handoff -> resume
                          ^                            |
                          +---- compact history ------+
```

Skills describe how agents perform lifecycle operations; they never store
project facts. Canonical state describes the latest project truth. Session files
are structured historical summaries and are not loaded by default.

## Components

- `AGENTS.md`: durable behavior, source priority, and safety rules.
- `.agents/skills/`: small, vendor-neutral operational procedures.
- `.agent/`: canonical V2 project state, memory, decisions, and history.
- `scripts/collect_git_state.py`: objective, structured Git evidence.
- `scripts/context_status.py`: concise human-readable status.
- `scripts/validate_context.py`: structural and semantic checks.
- `scripts/compact_sessions.py`: guarded dry-run-first session archiving.
- `integrations/`: discovery guidance only; core logic remains shared.

## Compatibility Boundary

The `.ai/` tree is retained for V1 migration. It is not a second V2 source of
truth. V2 work updates `.agent/`; see `docs/migration-v1-to-v2.md`.

## Dependencies

The Python tools use only the standard library. Git is optional for status and
validation: absence is reported cleanly rather than causing a traceback.
