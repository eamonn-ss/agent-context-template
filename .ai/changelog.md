# Semantic Changelog

> Git records exact diffs. This file records why meaningful changes mattered.

## Unreleased

### Added

- V2 canonical state, memory, decisions, and session history under `.agent/`
- Six vendor-neutral lifecycle Skills under `.agents/skills/`
- Git collection, context status, validation, and guarded compaction Python tools
- Dependency-free tests for Git, validation, status, and compaction edge cases
- Protocol, design, V1 migration, and Cursor/Codex/Claude integration guides
- V2 reusable state, decision, handoff, memory, and session templates
- `.ai/templates/README.md` documenting where skeletons belong
- `check-context.sh --strict` to fail on bootstrap/stray-template warnings
- Init now also copies `scripts/check-context.sh` and `.cursorignore.example`

### Changed

- `AGENTS.md` now defines Rules / Skills / State / Memory / History and the V2
  canonical source priority
- README now documents the complete cross-session, cross-agent V2 lifecycle
- Init and check scripts now install and validate V2 without overwriting files
- Cursor rules now point to `.agent/` state and shared project Skills
- `.ai/` is now an explicit V1 migration layer; `.agent/` is V2 canonical
- Filled template-repo `context.md`, `architecture.md`, and `current.md` with real meta-project facts (Active Task: None)
- README quick-start paths now use this repo root (`.`) instead of a wrong directory name
- Registry READMEs and `index.md` point skeletons exclusively to `.ai/templates/`
- README Chat Session prompts now match `session-start` / `session-end` and real `.ai/` paths

### Fixed

- Git porcelain collection preserves leading status spaces and dotted paths
- Context tools report missing Git/files cleanly instead of raising tracebacks
- README Session-end prompt no longer references non-existent `current_task.md` / `handoff.md` / `decisions.md`
- `init-ai-context.sh` no longer skips an entire empty/partial `.ai/` directory; it merges missing files
- Active registries no longer host `*-template.md` files that agents could mistake for real work

### Learned

- Guarded compaction can remain deterministic by requiring explicit Ready markers
- Standard-library tests keep the template usable when pytest is unavailable
- File-existence checks alone are insufficient; placeholder and stray-template warnings catch adoption footguns

### Removed
