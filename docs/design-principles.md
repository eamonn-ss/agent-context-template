# Design Principles

1. Repository over chat: durable context is reviewable and versioned.
2. Evidence over memory: Git, code, and tests outrank remembered claims.
3. Minimum context first: retrieve deeper history only when the task requires it.
4. One writable truth: `.agent/` is canonical; integrations are adapters.
5. State is replaced, history is appended, and accepted decisions are superseded.
6. Facts require evidence; hypotheses retain uncertainty and validation plans.
7. Safe automation previews destructive-looking changes and degrades gracefully.
8. Markdown and standard tools remain useful without services or vendor lock-in.
