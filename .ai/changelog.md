# Semantic Changelog

> Git records exact diffs. This file records why meaningful changes mattered.

## Unreleased

### Added

- `.ai/templates/README.md` documenting where skeletons belong
- `check-context.sh --strict` to fail on bootstrap/stray-template warnings
- Init now also copies `scripts/check-context.sh` and `.cursorignore.example`

### Changed

- Filled template-repo `context.md`, `architecture.md`, and `current.md` with real meta-project facts (Active Task: None)
- README quick-start paths now use this repo root (`.`) instead of a wrong directory name
- Registry READMEs and `index.md` point skeletons exclusively to `.ai/templates/`
- README Chat Session prompts now match `session-start` / `session-end` and real `.ai/` paths

### Fixed

- README Session-end prompt no longer references non-existent `current_task.md` / `handoff.md` / `decisions.md`
- `init-ai-context.sh` no longer skips an entire empty/partial `.ai/` directory; it merges missing files
- Active registries no longer host `*-template.md` files that agents could mistake for real work

### Learned

- File-existence checks alone are insufficient; placeholder and stray-template warnings catch adoption footguns

### Removed
