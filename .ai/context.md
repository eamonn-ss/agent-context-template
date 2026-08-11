# Project Context

> Stable facts only. Do not put daily progress here.
>
> After copying this template into another project, replace the sections below with that project's facts.

## Project

**Name:** AI Project Context Template

**One-line description:**

A reusable repository-level context system for AI coding agents (Cursor, Codex, Claude Code, Copilot, and similar).

## Primary Goal

Give agents durable project memory outside chat sessions: protocol, stable facts, architecture, decisions, active tasks, and handoffs — without dumping the entire `.ai/` tree into every prompt.

## Users / Runtime Environment

- Target user: engineers and AI coding agents working in a Git repository
- Deployment environment: any local or remote Git workspace
- Operating system: OS-agnostic (Bash scripts assume a POSIX shell)
- Language/runtime: Markdown + Bash; no application runtime required

## Core Technology

- Markdown context documents under `.ai/`
- `AGENTS.md` as the agent entry protocol
- Optional Cursor rule: `.cursor/rules/ai-context.mdc`
- Helper scripts: `scripts/init-ai-context.sh`, `scripts/check-context.sh`

## Hard Constraints

1. Chat history is not the source of truth; prefer code, tests, ADRs, then context files.
2. Keep active state short; put durable decisions in ADRs, not in `current.md`.
3. Do not require agents to read every file under `.ai/` — navigate from `index.md`.
4. Never treat `*-template.md` files as active tasks, ADRs, or handoffs.

## Non-Goals

- Not an application framework or agent runtime
- Not a replacement for Git history, CI, or tests
- Not a mandate to update every context file after every edit

## Domain Terms

| Term | Meaning |
|---|---|
| ADR | Architecture Decision Record in `.ai/decisions/` |
| Active task | Execution-state file in `.ai/tasks/` (not a template) |
| Handoff | Cross-session snapshot in `.ai/handoffs/` |
| Bootstrap placeholder | Unfilled token such as angle-bracket PROJECT_NAME meant to be replaced |

## External Systems

| System | Purpose | Interface |
|---|---|---|
| Git | Fact history and working-tree coordination | CLI |
| Cursor / other agents | Consumers of `AGENTS.md` + `.ai/` | File reads / rules |

## Known Invariants

Things agents should assume unless explicitly changed:

- Source-of-truth priority is defined in `AGENTS.md`
- File templates live only under `.ai/templates/`
- `current.md` is overwritten with latest state; `changelog.md` is append-only
