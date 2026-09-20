# TASK-001: V2 Context Lifecycle Framework

**Status:** Done  
**Priority:** P0  
**Created:** `2026-09-19`  
**Updated:** `2026-09-19`

## Goal

Upgrade the repository from a static `.ai/` context skeleton to a vendor-neutral,
Skills-driven project context lifecycle framework.

## Scope

- Add canonical V2 state, memory, session history, and decision records under `.agent/`.
- Add six context lifecycle Skills under `.agents/skills/`.
- Add Git collection, status, validation, and compaction Python tools with tests.
- Add Cursor, Codex, and Claude integration guidance and V1 migration documentation.
- Preserve the useful V1 `.ai/` materials as a compatibility and migration layer.

## Out of Scope

- LLM APIs, vector databases, hosted services, web UI, MCP servers, or orchestration.
- Automatic promotion of hypotheses to facts.
- Long-term synchronization between V1 `.ai/` state and V2 `.agent/` state.

## Relevant Files

- `AGENTS.md`
- `.agent/`
- `.agents/skills/`
- `scripts/`
- `tests/`
- `docs/`
- `integrations/`

## Dependencies

- `DEC-0001` in `.agent/decisions/`

## Acceptance Criteria

- [x] All six requested Skills exist and validate.
- [x] Canonical state and memory responsibilities are explicit.
- [x] Four Python tools handle missing files and non-Git directories safely.
- [x] Core tests cover required edge cases and pass.
- [x] README, protocol, integrations, and migration guide describe real behavior.
- [x] Final validator and status commands run successfully.

## Plan

1. Establish the compatible V2 architecture and canonical state.
2. Implement Skills and deterministic tools.
3. Add memory/history structures and compaction safeguards.
4. Add vendor integrations and user documentation.
5. Test, validate, and record final evidence.

## Work Log

### 2026-09-19

- Audited the complete V1 repository and identified reusable and conflicting components.
- Chose a compatibility migration: `.agent/` is V2 canonical; `.ai/` remains read-only legacy material until migration.
- Implemented the complete V2 framework and verified its initializer in an
  isolated target directory.

## Verified Results

- `python -m unittest discover -s tests -v`: 13 tests pass.
- `python scripts/validate_context.py`: PASS with no warnings.
- `python scripts/context_status.py`: GOOD.
- Six Skill structure validations pass.
- `bash -n` and Python compilation checks pass.

## Open Questions / Risks

- Existing adopters must migrate once rather than maintain `.ai/` and `.agent/` in parallel.

## Next Action

Review and commit the V2 upgrade.
