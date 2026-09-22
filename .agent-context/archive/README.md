# Session Archive

This directory contains structured session summaries moved by guarded compaction.
It is excluded from default bootstrap, resume, and status context.

Archiving is not deletion: migrate durable knowledge first, retain unique
evidence, and use `.agent-context/scripts/compact_sessions.py --apply` only after reviewing its
dry-run plan.
