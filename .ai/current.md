# Current Project State

> This is the short-lived global state. Keep it concise and overwrite stale information.

**Last updated:** 2026-08-11

## Current Objective

Maintain this AI project-context template: keep protocol docs, scripts, and skeletons consistent and safe for adoption.

## Active Task

None

## Current Status

- Template skeleton is complete under `.ai/`, `AGENTS.md`, and Cursor rule
- Reusable file templates live only in `.ai/templates/`
- Init and check scripts support partial installs and placeholder warnings

## Current Blockers

- None

## Recent Verified Findings

- `./scripts/check-context.sh` validates required files and warns on bootstrap leftovers
- `./scripts/init-ai-context.sh` merges missing files into an existing/empty `.ai/` tree

## Working Tree Notes

- Repository may still have uncommitted template files; check `git status` before editing

## Next Action

Adopt into a real project with `./scripts/init-ai-context.sh /path/to/project`, or commit this template skeleton if publishing.

## Do Not Accidentally Change

- Layered context protocol in `AGENTS.md`
- Source-of-truth priority order
- Separation of stable (`context.md`) vs active (`current.md` / `tasks/`) state
