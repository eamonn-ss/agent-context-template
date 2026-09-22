<p align="center">
  <strong>English</strong> |
  <a href="./README.zh-CN.md">简体中文</a>
</p>

# agent-context-template

## 1. Project Introduction

`agent-context-template` is a vendor-neutral lifecycle protocol for durable
project state, evidence-backed memory, session handoff, and recovery across
Codex, Cursor, Claude Code, and other coding agents. It requires only Markdown
and Python 3.10+; Git is useful evidence but remains optional.

## 2. Problem

Chats expire and assumptions drift. Earlier layouts also placed framework
`docs/`, `scripts/`, and `tests/` beside identically named business directories,
making an otherwise useful context system invasive in real repositories.

## 3. Core Idea

```text
Rules           AGENTS.md
Discovery       .agents/skills/
Context Root    .agent-context/
Canonical State .agent-context/state/
Evidence        application code, tests, and optional Git
```

Repository evidence outranks canonical prose; canonical state outranks memory,
handoffs, history, and agent-native memory.

## 4. Architecture

`.agents/` contains agent-discoverable capabilities only. `.agent-context/`
contains Context System state, memory, history, tooling, templates, docs,
integrations, and framework tests. This is the V2.2 boundary established by
DEC-0003.

## 5. Quick Start

Preview or install the embedded profile:

```bash
.agent-context/scripts/init-ai-context.sh --dry-run /path/to/project
.agent-context/scripts/init-ai-context.sh /path/to/project
```

The installed project keeps its existing application layout:

```text
your-project/
├── src/
├── docs/                  # your business docs
├── scripts/               # your business scripts
├── tests/                 # your business tests
├── .agents/
│   └── skills/
└── .agent-context/
    ├── state/
    ├── memory/
    ├── sessions/
    ├── archive/
    └── scripts/
```

Run `/project-init` once, `/context-start` at each new session, and
`/session-handoff` before ending meaningful unfinished work.

## 6. Context Lifecycle

`context-start` routes to `INIT_REQUIRED`, `BOOTSTRAP`, or `RESUME`. Bootstrap
loads a project view; resume continues an active task from canonical state and a
usable handoff. Facts require evidence, Decisions preserve rationale, and
compaction extracts durable knowledge before archiving history.

## 7. Skills

| Skill | Purpose |
|---|---|
| `project-init` | Initialize Project and Architecture on first adoption |
| `context-start` | Select initialization, bootstrap, or resume |
| `context-bootstrap` | Load a project-oriented view |
| `context-resume` | Continue an unfinished task |
| `session-handoff` | Transfer verified work across sessions/tools |
| `record-decision` | Add or supersede a durable decision |
| `context-compact` | Extract knowledge and archive eligible summaries |
| `project-status` | Report current canonical and Git evidence |

## 8. Namespace Isolation

Your project keeps its own `docs/`, `scripts/`, `tests/`, `templates/`, and
`integrations/`. Agent Context stays isolated in `.agent-context/`; the only
separate framework directory is `.agents/skills/`, retained for agent discovery.
Do not treat framework implementation as application source code.

## 9. Non-invasive Installation

The installer never overwrites existing files, modifies application source, or
writes framework assets into generic business directories. Existing `AGENTS.md`
is skipped. It reports an installed version, detects explicit V2.1 `.agent/`
markers, and supports a no-write `--dry-run` preview.

## 10. Development vs Embedded Profile

`--profile embedded` is the default and installs lifecycle Skills, state
scaffolds, runtime scripts, required templates, metadata, and thin optional
configuration. `--profile development` additionally installs framework docs,
integrations, and tests—but still inside `.agent-context/`.

## 11. Directory Structure

The template repository uses the complete development layout:

```text
.
├── AGENTS.md
├── .agents/skills/
└── .agent-context/
    ├── VERSION
    ├── state/        ├── memory/       ├── decisions/
    ├── sessions/     ├── archive/      ├── scripts/
    ├── templates/    ├── docs/         ├── integrations/
    └── tests/
```

The legacy `.ai/` tree remains only as V1 migration evidence.

## 12. Context Root Discovery

Python tools walk upward from the current directory to find `.agent-context/`.
They can therefore run from `src/module/` without assuming the shell is at the
repository root. `context_paths.py` centralizes Context, state, memory, session,
and archive paths.

## 13. V2.1 Migration

V2.1 `.agent/` state is detected but never dual-written. Preview and apply the
guarded one-time migration:

```bash
python .agent-context/scripts/migrate_v21_to_v22.py --dry-run
python .agent-context/scripts/migrate_v21_to_v22.py
```

Different destination content is a blocking conflict. See
[`migration-v2.1-to-v2.2.md`](.agent-context/docs/migration-v2.1-to-v2.2.md).

## 14. Vendor Integrations

Cursor, Codex, and Claude use root `AGENTS.md` plus `.agents/skills/`; integration
notes are thin adapters under
[`.agent-context/integrations/`](.agent-context/integrations/). Canonical state
never moves into vendor-native memory.

## 15. Validation / Testing

```bash
python .agent-context/scripts/context_start.py
python .agent-context/scripts/context_status.py
python .agent-context/scripts/validate_context.py
python .agent-context/scripts/compact_sessions.py
python -m unittest discover -s .agent-context/tests -v
```

No-Git projects remain supported and are reported as lacking Git evidence rather
than failing. Validator warnings do not fail; blocking errors return non-zero.

## 16. Roadmap

- V2.0: context lifecycle foundation.
- V2.1: first-run initialization, `context-start`, and bilingual documentation.
- V2.2: namespace isolation and non-invasive installation.
- V2.3: context freshness and state-drift detection.
- V2.4: optional local search/retrieval.
- V3: optional MCP Context Server.

See the full [protocol](.agent-context/docs/protocol.md),
[design principles](.agent-context/docs/design-principles.md), and
[V1 migration guide](.agent-context/docs/migration-v1-to-v2.md).
