# Project Context Lifecycle Protocol

## 1. Goals

Provide a small, repository-owned context system that survives chat boundaries,
works across coding agents, distinguishes evidence from uncertainty, and makes
handoffs independently verifiable.

## 2. Non-goals

This protocol is not an agent runtime, transcript store, database, replacement
for Git/tests, cloud memory service, or guarantee that generated prose is true.
V2 has no LLM API, vector database, UI, account, or MCP server dependency.

## 3. Context Layers

| Layer | Location | Responsibility |
|---|---|---|
| Rules | `AGENTS.md` | Long-lived behavior and safety |
| Skills | `.agents/skills/` | Repeatable lifecycle operations |
| State | `.agent/*.md` | Current canonical project state |
| Memory | `.agent/memory/` | Facts, hypotheses, discoveries |
| History | `.agent/sessions/`, `.agent/archive/` | Structured past activity |
| Evidence | code, tests, Git | Verifiable implementation truth |

Skills do not store facts. History does not override current state. Native agent
memory is a convenience, never a canonical project source.

## 4. Context Lifecycle

```text
bootstrap -> work -> validate -> handoff -> resume
                 \-> decision/memory       |
                         ^                 |
                         +-- compaction <--+
```

Each transition leaves enough repository evidence that another tool can verify
and continue without the original chat.

## 5. Canonical Sources

For factual conflicts use: code/tests/Git, canonical `.agent/` state, verified
Facts, accepted Decisions, current Handoff, recent Sessions, Archive, then native
memory. Current explicit user requirements still govern requested scope and may
authorize a change to project state; record and verify the resulting change.

## 6. Session Start

On first entry, bootstrap from `AGENTS.md`, Project, Architecture, Current Task,
Handoff, and concise Git state. On continuation, emphasize Current Task,
Handoff, relevant decisions, `git diff --stat`, and task-relevant diffs. Do not
scan all source or historical files unless evidence is insufficient.

## 7. During Session

Keep current state concise. Verify claims with code, tests, commands, issues, or
commits. Record durable choices as Decisions and uncertain explanations as
Hypotheses. Do not update every context file mechanically after every edit.

## 8. Session Handoff

A handoff must combine current task state with `git status --short`, diff stat,
relevant diff evidence, and recent commits. It records completed work, modified
files, decisions, current problems, attempts, failed approaches, evidence, open
questions, next steps, and one suggested first action. Suspected secret values
are never copied.

## 9. Resume

The next agent treats Handoff as a snapshot, not truth. It reconciles that
snapshot with Git, tests, Current Task, and relevant Decisions. Drift is reported
before work continues. Uncommitted changes are preserved unless the user
explicitly authorizes their removal.

## 10. Memory Model

- Facts have a unique ID, statement, evidence, and Verified status.
- Hypotheses have a unique ID, evidence, validation plan, and one of Open,
  Testing, Verified, or Rejected.
- Discoveries capture useful observations not yet mature enough for a Fact or
  Decision.

Verification of a hypothesis adds a separate Fact and retains the hypothesis as
history. No compaction or agent inference may silently promote it.

## 11. Decision Model

Decisions use unique `DEC-NNNN` records with Status, Context, Decision,
Alternatives, Reason, Consequences, and Evidence. Valid statuses are Proposed,
Accepted, Superseded, Deprecated, and Rejected. Replacement creates a new ID and
marks the old record `Superseded by DEC-XXXX`; accepted history is not rewritten.

## 12. History and Archive

Session history is a structured summary, not a transcript. Recent summaries are
available for targeted retrieval; archived summaries are excluded from startup.
Git remains the exact change history, while sessions explain operational context
such as failed attempts and next steps.

## 13. Compaction

Compaction extracts durable knowledge into Project/Architecture/Current Task,
Decisions, Facts, Hypotheses, or Discoveries. Only after extraction may a session
be marked `Compaction: Ready`. The script previews by default, protects recent
sessions, and only moves explicit Ready candidates on `--apply`. It never edits
canonical knowledge or code automatically.

## 14. Vendor Integration

The core protocol is vendor-neutral. Files under `integrations/` explain how a
tool finds `AGENTS.md` and invokes shared Skills; they must not duplicate the
workflow. Tool-specific automation remains optional.

## 15. Future MCP Integration

A future optional MCP server may expose project context, task, decision search,
history search, memory recording, and handoff creation. It must preserve Markdown
and Git as inspectable sources, remain optional, and enforce the same evidence,
uncertainty, safety, and authorization boundaries.
