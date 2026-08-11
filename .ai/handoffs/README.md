# Session Handoffs

Use handoffs when unfinished work must continue in another Agent session.

Naming:

```text
YYYY-MM-DD-TASK-001.md
```

Create new handoffs by copying:

```text
.ai/templates/HANDOFF-template.md
```

Do not keep `*-template.md` files in this directory.

A handoff is a snapshot, not the source of current truth.

When resuming work:

1. Read the relevant handoff.
2. Verify it against current code, task state, and Git.
3. Continue from verified state.

Do not assume an old handoff is still current.
