# DEC-0001: Canonical V2 Layout

## Status

Accepted

## Context

V1 stores protocol navigation and project state in `.ai/`. V2 needs an explicit
separation between executable Skills (`.agents/skills/`) and project state,
memory, and history (`.agent/`). Deleting V1 files would make the upgrade unsafe
for existing adopters, while permanent dual writes would create contradictory
sources of truth.

## Decision

Use `.agent/` as the only canonical V2 state tree and `.agents/skills/` for
vendor-neutral lifecycle procedures. Preserve `.ai/` in this template as a
documented V1 compatibility layer, but do not require ongoing synchronization.
Adopters perform a one-time, reviewable migration.

## Alternatives Considered

- Continue extending `.ai/`: lower migration cost, but conflicts with the V2
  state/Skills boundary and requested cross-agent convention.
- Delete `.ai/`: simpler final tree, but needlessly breaks existing users.
- Maintain both trees indefinitely: superficially compatible, but creates two
  writable sources of truth.

## Reason

One canonical tree prevents drift while keeping the old material available for
safe migration and comparison.

## Consequences

### Benefits

- Clear Rules / Skills / State / Memory / History ownership.
- Vendor integrations share the same core protocol.
- Existing V1 content is not destroyed.

### Tradeoffs

- The template repository temporarily contains both V1 and V2 directories.
- Existing adopters need a documented one-time migration.

## Evidence

- Repository audit on 2026-09-19 found all active V1 state under `.ai/` and no
  `.agent/` or `.agents/skills/` implementation.
- Migration mapping is documented in `docs/migration-v1-to-v2.md`.
