# Project

## Name

agent-context-template

## Purpose

A vendor-neutral project context lifecycle framework for persistent state,
session handoff, project memory, and context recovery across AI coding agents.

## Users

Engineers and AI coding agents working in Git repositories with Codex, Cursor,
Claude Code, or another tool that can read repository files and run commands.

## Goals

- Restore useful context without broad repository exploration.
- Transfer verified work across sessions, agents, and tools.
- Keep facts, hypotheses, decisions, current state, and history distinct.
- Prefer Git and executable evidence over remembered conversation.

## Non-goals

- An agent runtime, orchestrator, database, hosted memory service, or UI.
- A replacement for Git, tests, code review, or human judgment.
- Automatic inference that promotes hypotheses into facts.

## Runtime

Markdown, Git, and Python 3.10+. No service or LLM API is required.
