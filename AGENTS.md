# Repository Agent Protocol

This is the vendor-neutral entry point for AI coding agents in this repository.
User requirements govern scope; the priority below governs claims about project
state. Canonical state lives under `.agent-context/state/`. This file is the
map. Procedures live in `.agents/skills/`. See DEC-0004.

## 1. Context Protocol

```text
Rules   = this file: durable behavior
Skills  = .agents/skills/: how to perform context operations
State   = .agent-context/state/: current canonical project state
Memory  = .agent-context/memory/: evidence-backed knowledge and uncertainty
History = .agent-context/sessions/ and archive/: what happened before
Git     = objective working-tree and commit evidence
```

The `.ai/` tree is retained only for V1 migration. Do not maintain parallel V2
state there. See `.agent-context/docs/migration-v1-to-v2.md`.

`.agents/` contains Agent Skills only. `.agent-context/` owns canonical state,
memory, history, tooling, framework docs, templates, integrations, and tests.
Do not treat `.agent-context/` implementation files as application source, and
do not move business `docs/`, `scripts/`, or `tests/` into it.

## 2. Canonical Source Priority

When project information conflicts, use this order:

1. Current code, tests, and Git state
2. Canonical project state in `.agent-context/state/`
3. Verified facts in `.agent-context/memory/FACTS.md`
4. Accepted decisions in `.agent-context/decisions/`
5. Current `.agent-context/state/HANDOFF.md`
6. Recent structured session summaries
7. Archived session history
8. Agent-native memory or previous chat

Never let remembered context override repository evidence. Report unresolved
conflicts rather than silently choosing a convenient version.

## 3. Where To Look

- Start a session with `.agents/skills/context-start/SKILL.md`. It selects
  initialization, the project view, or task continuation.
- Answer a status question by running `python .agent-context/scripts/context_status.py`.
  Do not write state files for that question.
- End meaningful unfinished work with `.agents/skills/session-handoff/SKILL.md`.
- Record architecture, interface, or compatibility choices with
  `.agents/skills/record-decision/SKILL.md`.
- Archive old sessions with `.agents/skills/context-compact/SKILL.md`.
- Do not load every source file, session, or archive entry by default.
- Preserve uncommitted work from other sessions.

## 4. Knowledge Rules

- Facts require evidence. Hypotheses keep their uncertainty and a validation plan.
- Do not promote a hypothesis, delete unique evidence, or rewrite an accepted
  decision in place.
- Compaction extracts knowledge before archiving. It does not concatenate history.

## 5. Safety Rules

- Never store credentials, tokens, passwords, private keys, `.env` values, or
  other secrets in context files.
- If a diff appears to contain a secret, omit the value and report only that
  sensitive content was detected.
- Do not overwrite user or other-agent changes to match preferred style.
- Do not run destructive operations without explicit authorization and verified
  targets.

## 6. Validation

Use these entry points before completion:

```bash
python .agent-context/scripts/validate_context.py
python .agent-context/scripts/context_status.py
python -m unittest discover -s .agent-context/tests -v
```
