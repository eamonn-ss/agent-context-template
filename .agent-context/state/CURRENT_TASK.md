# Current Task

## ID

TASK-004

## Goal

Make handoff freshness depend on recorded Git evidence, and keep only the
Skills that prevent an agent from loading or writing the wrong context.

## Status

Done

## Scope

- Compare a handoff's recorded commit and worktree with current Git state.
- Point session procedures at Skills from `AGENTS.md`.
- Require handoffs to record commands, exit codes, and results.
- Add `Done when` to the task template.
- Keep five Skills. Put bootstrap and resume inside `context-start`.

## Blockers

None.

## Verified Results

- `python -m unittest discover -s .agent-context/tests -v` exits 0.
- Freshness is `stale` when Git evidence is missing, current work is unrecorded,
  a later commit is made without updating the handoff, Done when lacks a command
  and result, a finished task still asks to commit, or a dirty handoff lists
  files Git does not show.
- Committing the handoff that records its parent commit stays `current` on a
  clean worktree.

## Done when

`python -m unittest discover -s .agent-context/tests -v` exits 0.

## Next Action

Exercise the migration on a preserved real V2.1 consumer before release.
