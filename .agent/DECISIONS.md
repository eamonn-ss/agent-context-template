# Decision Index

Decision records are immutable history stored under `.agent/decisions/`. Do not
silently rewrite an accepted decision; create a new ID and mark the old record
`Superseded by DEC-XXXX`.

| ID | Status | Title |
|---|---|---|
| DEC-0001 | Accepted | [Canonical V2 Layout](decisions/DEC-0001-canonical-v2-layout.md) |

Allowed statuses: Proposed, Accepted, Superseded, Deprecated, Rejected.
