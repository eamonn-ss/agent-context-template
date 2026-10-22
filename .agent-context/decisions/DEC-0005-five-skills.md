# DEC-0005: Five Necessary Skills

## Status

Accepted

## Context

DEC-0002 kept `context-bootstrap` and `context-resume` as separately invocable
Skills. A status Skill also restated `context_status.py`. Agents could choose
the wrong entry because three Skills began the same session job.

## Decision

Keep five Skills: `context-start`, `project-init`, `session-handoff`,
`record-decision`, and `context-compact`. `context-start` contains the
BOOTSTRAP and RESUME steps. Status is the read-only `context_status.py`
command. This narrows the separate-entry sentence in DEC-0002. The three-mode
router remains.

## Alternatives Considered

- Keep eight Skills and only tighten descriptions: the wrong Skill remains
  invocable.
- Fold handoff, decisions, and compaction into `context-start`: those writes
  are easy to get wrong and are not part of session start.

## Reason

A Skill should exist only where skipping it lets an agent load the wrong
context or overwrite canonical history. Routing modes are one procedure.

## Consequences

### Benefits

- Session start has one discovery entry.
- Status cannot drift from the script that computes it.

### Tradeoffs

- Forcing resume or bootstrap means reading a section of `context-start`, not
  invoking a separate Skill.

## Evidence

- `.agents/skills/` contains those five Skills.
- `context_start.py` points both load modes back at `context-start`.
