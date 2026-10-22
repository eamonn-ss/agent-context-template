# DEC-0004: AGENTS.md Is a Map

## Status

Accepted

## Context

`AGENTS.md` is loaded on every session. It had grown into a second copy of the
lifecycle procedures already stored in `.agents/skills/`. OpenAI's harness
engineering notes and Claude's skill guidance both treat the always-loaded file
as a short map: procedural detail belongs where it is read only when needed.

## Decision

Keep source priority, knowledge rules, safety rules, and validation commands in
`AGENTS.md`. Point session start, handoff, decisions, and compaction at the
matching Skill instead of restating those procedures.

## Alternatives Considered

- Leave the full procedure in `AGENTS.md`: duplicates Skills and competes with
  the task for context.
- Move safety and source priority into Skills too: those rules must apply even
  when no Skill is selected.

## Reason

Always-loaded text should be the rules that are wrong to omit. Repeatable
workflows already have Skill files.

## Consequences

### Benefits

- Session context stays smaller.
- Procedure changes happen in one Skill instead of two documents.

### Tradeoffs

- An agent that ignores Skills will not see the step-by-step lifecycle. The
  map still names the Skill to open.

## Evidence

- `AGENTS.md` sections 3 and 4 name Skills instead of copying their steps.
- Skill bodies remain under `.agents/skills/`.
