# Verified Facts

Facts require evidence. Verification of a hypothesis creates a separate fact;
the hypothesis record remains as history.

## F-001

### Statement

The framework runs without an LLM API or persistent service.

### Evidence

- file: `.agent/ARCHITECTURE.md`
- command: `python scripts/validate_context.py`
- test: `pytest`

### Status

Verified

## F-002

### Statement

V2 uses `.agent/` as canonical project state and `.agents/skills/` for lifecycle
procedures.

### Evidence

- file: `.agent/decisions/DEC-0001-canonical-v2-layout.md`
- decision: `DEC-0001`

### Status

Verified
