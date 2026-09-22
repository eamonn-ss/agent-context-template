# Verified Facts

Facts require evidence. Verification of a hypothesis creates a separate fact;
the hypothesis record remains as history.

## F-001

### Statement

The framework runs without an LLM API or persistent service.

### Evidence

- file: `.agent-context/state/ARCHITECTURE.md`
- command: `python .agent-context/scripts/validate_context.py`
- test: `python -m unittest discover -s .agent-context/tests -v`

### Status

Verified

## F-002

### Statement

V2.0 and V2.1 used `.agent/` as canonical project state and `.agents/skills/`
for lifecycle procedures.

### Evidence

- file: `.agent-context/decisions/DEC-0001-canonical-v2-layout.md`
- decision: `DEC-0001`

### Status

Superseded by F-003

## F-003

### Statement

V2.2 uses `.agent-context/` for Context System state and implementation while
retaining `.agents/skills/` as the agent-discoverable layer.

### Evidence

- file: `.agent-context/state/ARCHITECTURE.md`
- decision: `DEC-0003`
- test: `python -m unittest discover -s .agent-context/tests -v`

### Status

Verified
