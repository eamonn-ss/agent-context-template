# Architecture Decision Records

Use one ADR per durable technical decision.

Naming:

```text
ADR-0001-short-title.md
ADR-0002-short-title.md
```

Create new ADRs by copying:

```text
.ai/templates/ADR-0000-template.md
```

Do not keep `*-template.md` files in this directory.

Status values:

- Proposed
- Accepted
- Superseded
- Rejected
- Deprecated

Create an ADR when a decision affects future contributors, for example:

- architecture;
- public interfaces;
- persistence formats;
- external dependencies;
- model/algorithm selection;
- deployment strategy;
- compatibility guarantees.

Do not create ADRs for:

- trivial implementation details;
- temporary debugging choices;
- every code edit.

When a decision changes, prefer marking the previous ADR `Superseded` and linking the new ADR rather than rewriting history.
