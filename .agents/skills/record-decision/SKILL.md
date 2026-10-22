---
name: record-decision
description: Use when an architecture, interface, data-format, dependency, or compatibility choice must outlive the session. Do not use for routine implementation details.
---

# Record Decision

1. Search `.agent-context/decisions/` and `.agent-context/state/DECISIONS.md`.
2. Allocate the next unused `DEC-NNNN`. Never reuse or overwrite an ID.
3. Create `.agent-context/decisions/DEC-NNNN-short-title.md` with Status,
   Context, Decision, Alternatives Considered, Reason, Consequences, and Evidence.
4. Use only Proposed, Accepted, Superseded, Deprecated, or Rejected.
5. When replacing a decision, mark the old record `Superseded by DEC-NNNN` and
   link both ways. Keep its original rationale and evidence.
6. Add the record to `.agent-context/state/DECISIONS.md` and run
   `python .agent-context/scripts/validate_context.py`.

A written proposal is not accepted until its status says Accepted.
