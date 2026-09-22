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
| State | `.agent-context/state/*.md` | Current canonical project state |
| Memory | `.agent-context/memory/` | Facts, hypotheses, discoveries |
| History | `.agent-context/sessions/`, `.agent-context/archive/` | Structured past activity |
| Implementation | `.agent-context/scripts/`, `docs/`, `templates/` | Context tooling and assets |
| Evidence | code, tests, Git | Verifiable implementation truth |

Skills do not store facts. History does not override current state. Native agent
memory is a convenience, never a canonical project source.

## 4. Context Lifecycle

```text
first adoption: project-init -> canonical project context

new session: context-start -> INIT_REQUIRED | BOOTSTRAP | RESUME
                              |               |           |
                         project-init     project view  continue task
                                              \          /
                                               work -> handoff
```

Each transition leaves enough repository evidence that another tool can verify
and continue without the original chat.

## 5. Canonical Sources

For factual conflicts use: code/tests/Git, canonical `.agent-context/state/`, verified
Facts, accepted Decisions, current Handoff, recent Sessions, Archive, then native
memory. Current explicit user requirements still govern requested scope and may
authorize a change to project state; record and verify the resulting change.

## 6. Project Initialization

`project-init` performs minimum repository discovery and creates real canonical
Project and Architecture state for first adoption. It examines high-signal files
such as README and build manifests before shallow source exploration, records
only evidence-backed Facts, and leaves uncertainty as a Hypothesis or Unknown.

It does not create Current Task when no active engineering task has been
defined. `project-init != context-bootstrap`: initialization creates canonical
project context; bootstrap loads canonical project context that already exists.

Files that merely exist are not necessarily initialized. Missing, empty, or
placeholder-bearing Project and Architecture files require initialization.

## 7. Context Start Routing

`context-start` is the default new-session entry. It checks Project,
Architecture, Current Task, Handoff, and available Git state, then selects:

| Mode | Condition | Action |
|---|---|---|
| `INIT_REQUIRED` | Project or Architecture is missing or templated | Run `project-init` |
| `RESUME` | Current Task is active and Handoff is usable | Run `context-resume` |
| `BOOTSTRAP` | Project is initialized without a valid active task/handoff pair | Run `context-bootstrap` |

Template Current Task and Handoff files are unusable. Terminal task statuses do
not resume even when an older handoff remains present.

## 8. Bootstrap vs Resume

Bootstrap is project-oriented: it prioritizes Project, Architecture, status,
decisions, and hypotheses, while keeping Git inspection shallow. Resume is
task-oriented: it prioritizes Current Task, Handoff, task-relevant Git diffs,
failed attempts, blockers, and the next action. Both remain available as
advanced explicit entry points; `context-start` normally chooses between them.

## 9. First-run Lifecycle

```text
/project-init        # once, after adopting the framework
/context-start       # every new session
development
/session-handoff     # before ending or switching agents
/context-start       # next session, normally RESUME
```

## 10. Session Start

Use `context-start` unless intentionally forcing bootstrap or resume. Do not scan
all source or historical files unless evidence is insufficient.

## 11. During Session

Keep current state concise. Verify claims with code, tests, commands, issues, or
commits. Record durable choices as Decisions and uncertain explanations as
Hypotheses. Do not update every context file mechanically after every edit.

## 12. Session Handoff

A handoff must combine current task state with `git status --short`, diff stat,
relevant diff evidence, and recent commits. It records completed work, modified
files, decisions, current problems, attempts, failed approaches, evidence, open
questions, next steps, and one suggested first action. Suspected secret values
are never copied.

## 13. Resume

The next agent treats Handoff as a snapshot, not truth. It reconciles that
snapshot with Git, tests, Current Task, and relevant Decisions. Drift is reported
before work continues. Uncommitted changes are preserved unless the user
explicitly authorizes their removal.

## 14. Memory Model

- Facts have a unique ID, statement, evidence, and Verified status.
- Hypotheses have a unique ID, evidence, validation plan, and one of Open,
  Testing, Verified, or Rejected.
- Discoveries capture useful observations not yet mature enough for a Fact or
  Decision.

Verification of a hypothesis adds a separate Fact and retains the hypothesis as
history. No compaction or agent inference may silently promote it.

## 15. Decision Model

Decisions use unique `DEC-NNNN` records with Status, Context, Decision,
Alternatives, Reason, Consequences, and Evidence. Valid statuses are Proposed,
Accepted, Superseded, Deprecated, and Rejected. Replacement creates a new ID and
marks the old record `Superseded by DEC-XXXX`; accepted history is not rewritten.

## 16. History and Archive

Session history is a structured summary, not a transcript. Recent summaries are
available for targeted retrieval; archived summaries are excluded from startup.
Git remains the exact change history, while sessions explain operational context
such as failed attempts and next steps.

## 17. Compaction

Compaction extracts durable knowledge into Project/Architecture/Current Task,
Decisions, Facts, Hypotheses, or Discoveries. Only after extraction may a session
be marked `Compaction: Ready`. The script previews by default, protects recent
sessions, and only moves explicit Ready candidates on `--apply`. It never edits
canonical knowledge or code automatically.

## 18. Vendor Integration

The core protocol is vendor-neutral. Files under `.agent-context/integrations/` explain how a
tool finds `AGENTS.md` and invokes shared Skills; they must not duplicate the
workflow. Tool-specific automation remains optional.

## 19. Namespace Isolation and Embedded Installation

`.agents/skills/` is the agent-discoverable layer. `.agent-context/` is the
Context Root and owns state, memory, history, scripts, templates, framework
documentation, integrations, and framework tests. Business `docs/`, `scripts/`,
`tests/`, `templates/`, and `integrations/` remain application-owned and are
never installation targets.

The development profile includes framework development assets inside the
Context Root. The embedded profile installs only lifecycle Skills, state
scaffolds, runtime tools, necessary templates, and optional thin configuration.
It never modifies application source and never silently replaces `AGENTS.md`.

Tools discover the Context Root by walking upward from the current directory,
so repository-root execution is not required. Git remains optional evidence.

## 20. Legacy Layout Migration

A `.agent/PROJECT.md` marker without namespaced state identifies V2.1. Tools
report that migration is required; they do not dual-write. The guarded migration
tool previews by default when `--dry-run` is supplied, preflights destination
conflicts, and never migrates arbitrary content from generic business
directories. See `migration-v2.1-to-v2.2.md`.

## 21. Future MCP Integration

A future optional MCP server may expose project context, task, decision search,
history search, memory recording, and handoff creation. It must preserve Markdown
and Git as inspectable sources, remain optional, and enforce the same evidence,
uncertainty, safety, and authorization boundaries.
