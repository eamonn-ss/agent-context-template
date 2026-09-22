# Migrating from V2.1 to V2.2

V2.2 isolates Context System assets beneath `.agent-context/` while preserving
`.agents/skills/` as the discovery layer. It does not use permanent dual writes.

## Path Mapping

| V2.1 | V2.2 |
|---|---|
| `.agent/PROJECT.md` | `.agent-context/state/PROJECT.md` |
| `.agent/ARCHITECTURE.md` | `.agent-context/state/ARCHITECTURE.md` |
| `.agent/CURRENT_TASK.md` | `.agent-context/state/CURRENT_TASK.md` |
| `.agent/HANDOFF.md` | `.agent-context/state/HANDOFF.md` |
| `.agent/memory/` | `.agent-context/memory/` |
| `.agent/sessions/` | `.agent-context/sessions/` |
| `.agent/archive/` | `.agent-context/archive/` |
| `.agent/decisions/` | `.agent-context/decisions/` |
| framework `scripts/` | `.agent-context/scripts/` |
| framework `templates/` | `.agent-context/templates/` |
| framework `integrations/` | `.agent-context/integrations/` |

Business directories with the same generic names are not migration targets.

## Migration Command

Preserve or commit the working tree, install/copy the V2.2 runtime files, then
preview and apply:

```bash
python .agent-context/scripts/migrate_v21_to_v22.py --root /path/to/project --dry-run
python .agent-context/scripts/migrate_v21_to_v22.py --root /path/to/project
```

The tool detects explicit `.agent/` state markers, displays every planned move,
and stops before changing anything when destination content differs. After an
applied migration it runs the namespaced validator.

## Manual Fallback

If a conflict is reported, compare the named source and destination, preserve
the version that reflects current project truth, and manually move the remaining
V2.1 state using the table above. Do not move arbitrary business files from
top-level `docs/`, `scripts/`, or `tests/`. Finish with:

```bash
python .agent-context/scripts/validate_context.py --root /path/to/project
python .agent-context/scripts/context_status.py --root /path/to/project
```

## Compatibility Notes

The validator and installer recognize V2.1 from canonical `.agent/` markers;
the mere presence of business `docs/`, `scripts/`, or `tests/` never triggers a
legacy warning. V2.2 tools report migration requirements instead of silently
reading and writing both layouts.

## Rollback Notes

Before applying, keep a Git commit or filesystem backup. To roll back, restore
that snapshot as a unit. Do not partially recreate `.agent/` while continuing
to write `.agent-context/state/`, because that produces two apparent sources of
truth.
