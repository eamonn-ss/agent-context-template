# Session Handoff

## Goal

Replace sentence-matching freshness with recorded Git evidence, and stop
duplicating lifecycle procedures in the always-loaded map.

## Git Evidence

- commit: 40c9ea25ce5ddf402639bc517a4adb02597d71f8
- worktree: dirty

## Completed

- Status compares the handoff commit and worktree with HEAD. A handoff committed
  on top of the commit it records stays current when the worktree is clean.
- Skill descriptions state when to use them and when not to.
- Handoffs record the command, exit code, and result. The full diff stays in Git.
- Task template has `Done when`. `AGENTS.md` points at Skills. DEC-0004 records
  that choice.
- Five Skills remain. DEC-0005 folds bootstrap and resume into `context-start`
  and leaves status to `context_status.py`.

## Modified Files

- `.agent-context/scripts/context_status.py`
- `.agent-context/tests/test_context_status.py`
- `.agents/skills/`
- `AGENTS.md`
- `.agent-context/decisions/DEC-0004-agents-md-is-a-map.md`
- `.agent-context/docs/protocol.md`
- `.agent-context/templates/CURRENT_TASK.template.md`
- `.agent-context/templates/HANDOFF.template.md`
- `.agent-context/state/`

## Technical Decisions

- DEC-0004: `AGENTS.md` keeps priority, knowledge, safety, and validation. Skills
  own the procedures.

## Current Problem

None.

## Attempts Made

- Keyword matching on "commit" was replaced before it shipped as the durable
  check, because wording missed non-English handoffs and ignored real Git drift.

## Failed Approaches

None.

## Important Evidence

- `python -m unittest discover -s .agent-context/tests -v` exits 0. 40 tests passed.

## Open Questions

None.

## Next Steps

- Exercise the migration on a preserved real V2.1 consumer before release.
- Stale prose that Git cannot check is still open.

## Suggested First Action

Exercise the migration on a preserved real V2.1 consumer before release.
