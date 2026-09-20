---
name: context-compact
description: Extract durable knowledge from recent structured sessions and safely archive eligible history without changing code or promoting uncertainty.
---

# Context Compact

Compaction is knowledge extraction, not concatenated summarization.

1. Review recent `.agent/sessions/` summaries and select old candidates; do not
   read the complete archive by default.
2. For each candidate, migrate still-useful content to the correct canonical
   destination: current state, a decision, an evidence-backed fact, an explicit
   hypothesis, or a discovery.
3. Never promote a hypothesis to fact automatically, overwrite unfinished task
   state, remove unique evidence, or modify product code.
4. Mark a session `**Compaction:** Ready` only after its useful knowledge has
   been migrated and its open work is represented canonically.
5. Preview with `python scripts/compact_sessions.py`; review the plan, then run
   with `--apply` only when the proposed archive set is correct.
6. Run `python scripts/validate_context.py` afterward.

Sessions marked `Keep` or lacking an explicit `Ready` marker remain active.
