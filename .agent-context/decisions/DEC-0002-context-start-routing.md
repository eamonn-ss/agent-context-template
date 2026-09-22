# DEC-0002: Automatic Session Start Routing

## Status

Accepted

## Context

V2 required users to choose project bootstrap or task resume before every new
session, and neither operation owned first-adoption initialization. File
existence alone is insufficient because the installer intentionally creates
template canonical files.

## Decision

Add `project-init` as the first-adoption operation and `context-start` as the
default new-session router. Route from Project/Architecture initialization,
active Current Task, and usable Handoff state. Keep `context-bootstrap` and
`context-resume` as explicit advanced entries. Centralize deterministic mode
detection in `scripts/context_start.py` and reuse validator placeholder logic.

## Alternatives Considered

- Keep manual bootstrap/resume selection: fewer files, but exposes an avoidable
  lifecycle decision to every user and leaves first adoption ambiguous.
- Merge initialization into bootstrap: simpler naming, but mixes writing new
  canonical truth with loading existing truth.
- Route only by file existence: fails for freshly copied template skeletons.

## Reason

The three-mode router makes normal startup predictable while preserving explicit
control and evidence boundaries for advanced use.

## Consequences

### Benefits

- Normal users need only project-init, context-start, and session-handoff.
- Template files cannot accidentally trigger task continuation.
- Routing behavior is independently testable without an agent runtime.

### Tradeoffs

- The framework includes one additional standard-library script.
- Active task statuses and minimum usable-handoff structure form a maintained
  compatibility surface.

## Evidence

- requirement: `agent-context-template-v2.1-codex-task.md`
- implementation: `scripts/context_start.py`
- tests: `python -m unittest discover -s tests -v`
