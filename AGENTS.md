# Repository Agent Protocol

This is the vendor-neutral entry point for AI coding agents in this repository.
User requirements govern scope; the priority below governs claims about project
state. V2.2 canonical state lives under `.agent-context/state/`.

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

## 3. Session Start Rules

- If canonical Project or Architecture state is missing or still templated,
  follow `.agents/skills/project-init/SKILL.md`.
- Otherwise prefer `.agents/skills/context-start/SKILL.md` for every new
  session; it routes automatically to project bootstrap or task resume.
- Use `context-resume` explicitly only when task continuation is intentionally
  forced. Use `context-bootstrap` explicitly for project-level orientation.
- Read `CURRENT_TASK.md` and `HANDOFF.md` before broad exploration.
- Inspect branch, recent commits, working-tree status, and relevant diffs.
- Do not load all source files, sessions, or archive entries by default.
- Check for uncommitted work and preserve changes from other sessions.

## 4. During Work Rules

- Keep scope tied to the current task; do not silently refactor unrelated code.
- Prefer executable evidence over prose and label unverified claims.
- Record architecture/interface/dependency/data-format decisions using the
  `record-decision` Skill. Do not silently rewrite accepted history.
- Store stable verified claims as Facts with evidence. Keep uncertain claims as
  Hypotheses with a validation plan. A verified hypothesis creates a separate
  Fact; retain the hypothesis history.
- Keep discoveries separate until they merit a Fact or Decision.
- Run relevant tests or checks before calling work complete.

## 5. Session End Rules

For meaningful unfinished work, follow the `session-handoff` Skill:

- reconcile task state with Git and tests;
- update `CURRENT_TASK.md` and `HANDOFF.md`;
- preserve failed attempts and concrete evidence;
- create a structured session summary, never a chat transcript;
- update decisions or memory only when their standards are met.

## 6. History and Compaction

- Recent summaries live in `.agent-context/sessions/`; old summaries live in
  `.agent-context/archive/` and are not default context.
- Compaction means extracting knowledge into canonical state/memory before
  archiving. It must not concatenate history into an ever-growing summary.
- Never promote a hypothesis, delete unique evidence, overwrite unfinished
  state, or modify product code during compaction.

## 7. Safety Rules

- Never store credentials, tokens, passwords, private keys, `.env` values, or
  other secrets in context files.
- If a diff appears to contain a secret, omit the value and report only that
  sensitive content was detected.
- Do not overwrite user or other-agent changes to match preferred style.
- Do not run destructive operations without explicit authorization and verified
  targets.

## 8. Validation

Use these entry points before completion:

```bash
python .agent-context/scripts/validate_context.py
python .agent-context/scripts/context_status.py
python -m unittest discover -s .agent-context/tests -v
```
