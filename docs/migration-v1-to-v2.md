# Migrating from V1 `.ai/` to V2 `.agent/`

V1 remains in this template so existing repositories are not broken by an
upgrade. V2 does not require dual writes: migrate once, review the result, then
treat `.agent/` as canonical.

## Responsibility Mapping

| V1 | V2 | Action |
|---|---|---|
| `.ai/context.md` | `.agent/PROJECT.md` and memory | Split stable project identity from evidence-backed knowledge |
| `.ai/architecture.md` | `.agent/ARCHITECTURE.md` | Copy only current design; move durable choices to Decisions |
| `.ai/current.md` | `.agent/CURRENT_TASK.md` | Keep only current goal, status, blockers, and next action |
| `.ai/tasks/*.md` | `.agent/CURRENT_TASK.md` or issue tracker | Merge the active task; retain old task files as history if useful |
| `.ai/decisions/*.md` | `.agent/decisions/DEC-*.md` | Allocate unique DEC IDs; preserve status and rationale |
| `.ai/handoffs/*.md` | `.agent/HANDOFF.md` and sessions | Use newest verified handoff; summarize older useful history |
| `.ai/changelog.md` | Git and `.agent/sessions/` | Keep historical file; do not copy it wholesale into startup context |
| `.ai/archive/` | `.agent/archive/` | Move only targeted history when needed |
| `.ai/templates/` | `templates/` | Use the V2 state/decision/handoff schemas |

## Migration Procedure

1. Commit or otherwise preserve the V1 state and working tree.
2. Run the updated initializer; it adds missing V2 files without overwriting V1.
3. Replace template content in `.agent/` using the mapping above.
4. Classify knowledge explicitly as Fact, Hypothesis, Discovery, or Decision.
5. Run `python scripts/validate_context.py` and review
   `python scripts/context_status.py`.
6. Update local agent entry rules to point to `AGENTS.md` and `.agent/`.
7. Stop writing active state to `.ai/`. Retain or archive it according to project
   policy after the V2 state has been verified.

Do not automatically convert speculation in old handoffs into Facts. Preserve
unknowns as Hypotheses and attach a validation plan.
