# agent-context-template

`agent-context-template` is a vendor-neutral project context lifecycle protocol
for persistent state, session handoff, project memory, and context recovery
across AI coding agents such as Codex, Cursor, and Claude Code.

Chat sessions are temporary. The repository is durable context. Git, code, and
tests are verifiable evidence.

## Problem

New sessions repeatedly explore the same project, tools lose decisions and failed
attempts, assumptions slowly become “facts,” and growing transcripts waste tokens.
Native agent memory also cannot be the sole source for shared project truth.

## Core Idea

```text
Rules   tell agents what to respect
Skills  define how context operations run
State   says what is true now
Memory  separates facts, hypotheses, and discoveries
History records structured past work
Git     supplies objective evidence
```

## Architecture

```text
AGENTS.md                          Rules and source priority
.agents/skills/                    Vendor-neutral operations
.agent/*.md                        Canonical state
.agent/memory/                     Long-lived knowledge
.agent/sessions/ -> archive/       Bounded structured history
scripts/                           Deterministic evidence and validation
integrations/                      Thin vendor adapters
```

V2 uses `.agent/` as its only writable canonical state. The old `.ai/` tree is
retained for safe V1 migration, not parallel state maintenance.

## Quick Start

```bash
./scripts/init-ai-context.sh /path/to/project
cd /path/to/project
python scripts/validate_context.py
```

Customize `.agent/PROJECT.md`, `ARCHITECTURE.md`, `CURRENT_TASK.md`, and
`HANDOFF.md`, then ask your agent to run `context-bootstrap`.

## Context Lifecycle

1. `context-bootstrap` loads the minimum context on first entry.
2. Normal work records evidence-backed Facts and durable Decisions when needed.
3. `session-handoff` reconciles state with Git and preserves failed attempts.
4. `context-resume` verifies the handoff and continues in another session/tool.
5. `context-compact` extracts knowledge before archiving eligible old sessions.

The archive is never loaded by default.

## Skills

| Skill | Use |
|---|---|
| `context-bootstrap` | First entry with minimum context |
| `context-resume` | Continue verified unfinished work |
| `session-handoff` | Transfer state across sessions or tools |
| `record-decision` | Add or supersede a durable decision |
| `context-compact` | Extract knowledge and archive safe history |
| `project-status` | Answer “where is this project now?” |

Skills live under `.agents/skills/` and contain procedures, never project facts.

## Directory Structure

```text
.
├── AGENTS.md
├── .agents/skills/
├── .agent/
│   ├── PROJECT.md
│   ├── ARCHITECTURE.md
│   ├── CURRENT_TASK.md
│   ├── DECISIONS.md
│   ├── HANDOFF.md
│   ├── TODO.md
│   ├── decisions/
│   ├── memory/
│   ├── sessions/
│   └── archive/
├── scripts/
├── templates/
├── integrations/
├── docs/
└── tests/
```

## Cursor Usage

Keep `.cursor/rules/ai-context.mdc` enabled, then ask Cursor to follow the desired
Skill. The rule points to the shared protocol instead of duplicating it. Details:
[`integrations/cursor/README.md`](integrations/cursor/README.md).

## Codex Usage

Open the repository root so Codex sees `AGENTS.md` and project Skills. Invoke
`context-bootstrap`, `context-resume`, or `session-handoff` as appropriate.
Details: [`integrations/codex/README.md`](integrations/codex/README.md).

## Claude Usage

Tell Claude or Claude Code to use `AGENTS.md` and the selected Skill as the shared
protocol. Any Claude-specific instruction should remain a thin pointer. Details:
[`integrations/claude/README.md`](integrations/claude/README.md).

## Example Workflow

```text
Session A / Cursor
  context-bootstrap -> development -> record-decision -> session-handoff
                                                        |
Session B / Codex                                      v
  context-resume <- handoff + Git verification -> development -> handoff
                                                               |
Session C / Claude                                            v
  context-resume <- canonical state + handoff + Git evidence
```

The transfer is cross-session, cross-agent, and cross-tool because shared
repository files—not a vendor chat—carry the state.

## Automation

```bash
python scripts/collect_git_state.py --json
python scripts/context_status.py
python scripts/validate_context.py
python scripts/compact_sessions.py          # dry run
python scripts/compact_sessions.py --apply  # explicit Ready sessions only
python -m unittest discover -s tests -v
```

Tools use Python 3.10+ standard library only and handle missing Git/context files
without tracebacks. Validator warnings do not fail; blocking errors return 1.

## Design Principles

- Load minimum required context first; retrieve deeper history only when needed.
- Prefer code, tests, and Git over prose or remembered context.
- Facts require evidence; hypotheses retain explicit uncertainty.
- Replace current state, append structured history, supersede decisions.
- Never store credentials or copy suspected secrets into handoffs.
- Keep core protocol vendor-neutral and integrations thin.

See [`docs/protocol.md`](docs/protocol.md) for the complete lifecycle and
[`docs/design-principles.md`](docs/design-principles.md) for the compact rationale.

## Migration

Existing V1 repositories can keep `.ai/` while adopting V2, then stop writing V1
state after verification. The exact mapping and safe sequence are in
[`docs/migration-v1-to-v2.md`](docs/migration-v1-to-v2.md).

## Roadmap

- V2.1: optional ripgrep retrieval and SQLite FTS.
- V2.2: optional semantic retrieval, embeddings, and vector storage.
- V3: optional MCP context server (`get_project_context`, decision/history
  search, memory recording, and handoff creation).

These are deliberately absent from V2, which requires only Markdown, Git,
Skills, Python scripts, and the protocol.
