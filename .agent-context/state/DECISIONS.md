# Decision Index

Decision records are immutable history stored under `.agent-context/decisions/`. Do not
silently rewrite an accepted decision; create a new ID and mark the old record
`Superseded by DEC-XXXX`.

| ID | Status | Title |
|---|---|---|
| DEC-0001 | Superseded | [Canonical V2 Layout](../decisions/DEC-0001-canonical-v2-layout.md) |
| DEC-0002 | Accepted | [Automatic Session Start Routing](../decisions/DEC-0002-context-start-routing.md) |
| DEC-0003 | Accepted | [Namespaced Context Layout](../decisions/DEC-0003-namespaced-context-layout.md) |
| DEC-0004 | Accepted | [AGENTS.md Is a Map](../decisions/DEC-0004-agents-md-is-a-map.md) |
| DEC-0005 | Accepted | [Five Necessary Skills](../decisions/DEC-0005-five-skills.md) |

Allowed statuses: Proposed, Accepted, Superseded, Deprecated, Rejected.
