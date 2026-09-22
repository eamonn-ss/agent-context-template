---
name: record-decision
description: Record or supersede a durable project decision with a unique ID, alternatives, consequences, and verifiable evidence.
---

# Record Decision

Use for changes to architecture, interfaces, dependencies, data formats, public
APIs, deployment assumptions, compatibility, or core algorithms. Do not create
a decision for routine implementation details.

1. Search `.agent-context/decisions/` and
   `.agent-context/state/DECISIONS.md` for governing records.
2. Allocate the next unused `DEC-NNNN`; never reuse or silently overwrite an ID.
3. Create `.agent-context/decisions/DEC-NNNN-short-title.md` with Status, Context,
   Decision, Alternatives Considered, Reason, Consequences (Benefits and
   Tradeoffs), and Evidence.
4. Use only Proposed, Accepted, Superseded, Deprecated, or Rejected.
5. If replacing a decision, mark the old record `Superseded by DEC-NNNN` and
   link both directions. Preserve its original rationale and evidence.
6. Add the new record to `.agent-context/state/DECISIONS.md` and run the validator.

State uncertainty explicitly. A proposal is not accepted merely because it was
written down.
