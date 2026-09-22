# Migrating from V1 `.ai/` to V2.2 `.agent-context/`

V1 remains in this template so existing repositories are not broken by an
upgrade. V2 does not require dual writes: migrate once, review the result, then
treat `.agent-context/state/` as canonical.

## Responsibility Mapping

| V1 | V2 | Action |
|---|---|---|
| `.ai/context.md` | `.agent-context/state/PROJECT.md` and memory | Split stable identity from evidence-backed knowledge |
| `.ai/architecture.md` | `.agent-context/state/ARCHITECTURE.md` | Copy only current design; move durable choices to Decisions |
| `.ai/current.md` | `.agent-context/state/CURRENT_TASK.md` | Keep only the current goal and execution state |
| `.ai/tasks/*.md` | `.agent-context/state/CURRENT_TASK.md` or issue tracker | Merge only the active task |
| `.ai/decisions/*.md` | `.agent-context/decisions/DEC-*.md` | Allocate unique IDs; preserve rationale |
| `.ai/handoffs/*.md` | `.agent-context/state/HANDOFF.md` and sessions | Use the newest verified handoff |
| `.ai/changelog.md` | Git and `.agent-context/sessions/` | Retain as history, not startup context |
| `.ai/archive/` | `.agent-context/archive/` | Move only targeted history when needed |
| `.ai/templates/` | `.agent-context/templates/` | Use current schemas |

## Migration Procedure

1. Commit or otherwise preserve the V1 state and working tree.
2. Run the updated initializer; it adds missing V2 files without overwriting V1.
3. Replace template content in `.agent-context/state/` using the mapping above.
4. Classify knowledge explicitly as Fact, Hypothesis, Discovery, or Decision.
5. Run `python .agent-context/scripts/validate_context.py` and review
   `python .agent-context/scripts/context_status.py`.
6. Update local agent entry rules to point to `AGENTS.md` and `.agent-context/`.
7. Stop writing active state to `.ai/`. Retain or archive it according to project
   policy after the V2 state has been verified.

Do not automatically convert speculation in old handoffs into Facts. Preserve
unknowns as Hypotheses and attach a validation plan.
