# Repository Agent Protocol

This file is the canonical entry point for AI coding agents working in this repository.

## 1. Restore Context Before Work

Before making non-trivial changes:

1. Read `.ai/index.md`.
2. Read `.ai/current.md`.
3. Read only the context documents relevant to the current task.
4. Run or inspect:
   - `git status`
   - recent Git history
   - existing uncommitted changes
5. Check whether an active task file already exists (ignore `*-template.md`).

Do not begin with a full-repository exploration unless the indexed context is missing, stale, or demonstrably insufficient.

## 2. Source of Truth

When information conflicts, use this priority:

1. Current explicit user requirements
2. Current executable code behavior
3. Tests and verified runtime evidence
4. Accepted ADRs in `.ai/decisions/`
5. `.ai/architecture.md`
6. `.ai/context.md`
7. `.ai/current.md`
8. Handoffs / changelog
9. Previous chat history

Do not treat assumptions, old experiments, or chat statements as current facts without verification.

## 3. Scope Discipline

Before editing:

- Identify the active task.
- Identify in-scope files.
- Identify out-of-scope areas.
- Check for uncommitted changes from another session.

Do not silently refactor unrelated modules.

Do not overwrite another agent's work merely to make the code match your preferred style.

## 4. Decision Discipline

Before changing architecture, interfaces, dependencies, storage formats, public APIs, deployment assumptions, or core algorithms:

1. Search `.ai/decisions/`.
2. Determine whether an existing ADR governs the choice.
3. If reversing an accepted decision, document:
   - why the old assumptions changed;
   - migration impact;
   - compatibility impact.

Important decisions belong in ADRs, not only in chat.

## 5. Work State

Use `.ai/current.md` for the latest global working state.

Use `.ai/tasks/TASK-NNN-short-title.md` for task-specific state.

Copy skeletons from `.ai/templates/`. Files named `*-template.md` are not active work.

`current.md` must remain concise and should answer:

- What are we doing now?
- What is blocked?
- What changed recently?
- What should happen next?

## 6. Validation

Before claiming completion:

- Run relevant tests, checks, builds, or evaluation commands when available.
- Distinguish verified results from assumptions.
- Record important validation evidence in the active task or handoff.
- Never mark a task Done solely because code was written.

## 7. Session Handoff

At the end of a meaningful work session:

1. Update the active task status.
2. Update `.ai/current.md` if global state changed.
3. Append meaningful changes to `.ai/changelog.md`.
4. Create/update a handoff when unfinished work remains.
5. Add an ADR only when a durable technical decision was made.

Do not update every context file mechanically.

## 8. Context Hygiene

Keep repository memory useful:

- Stable facts → `context.md`
- Current system design → `architecture.md`
- Durable decisions → `decisions/`
- Current global state → `current.md`
- Task execution → `tasks/`
- Cross-session continuation → `handoffs/`
- Historical summary → `changelog.md`

Remove or archive stale active information rather than letting contradictory states accumulate.

## 9. Communication

When starting from a fresh session, summarize before major changes:

- understood goal;
- current state;
- relevant constraints;
- files likely involved;
- risks or conflicts discovered.

For small, obvious tasks, keep this brief.
