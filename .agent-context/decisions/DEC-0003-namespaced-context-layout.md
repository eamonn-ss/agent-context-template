# DEC-0003: Namespaced Context Layout

## Status

Accepted

## Context

V2.1 separated discoverable Skills from canonical state, but embedded the
framework through generic top-level `docs/`, `scripts/`, `templates/`, `tests/`,
and `integrations/` directories. Existing business repositories commonly own
those names, making installation invasive and product/framework boundaries
ambiguous. This decision supersedes
[DEC-0001](DEC-0001-canonical-v2-layout.md).

## Decision

Keep only agent-discoverable capabilities in `.agents/skills/`. Place canonical
state, memory, history, scripts, templates, framework documentation,
integrations, and tests beneath `.agent-context/`; canonical state specifically
lives in `.agent-context/state/`. Embedded installation adds only required
runtime assets and never writes framework files into business `docs/`,
`scripts/`, `tests/`, `templates/`, or `integrations/`. V2.1 layouts migrate
once and are detected but never maintained through dual writes.

## Alternatives Considered

- Keep the V2.1 layout: avoids migration but remains invasive in real projects.
- Put Skills under `.agent-context/`: provides one physical root but breaks the
  standard discovery location used by coding agents.
- Support permanent `.agent/` and `.agent-context/state/` dual writes: improves
  superficial compatibility but creates contradictory canonical sources.

## Reason

A dedicated implementation namespace makes framework ownership explicit while
retaining compatible Skill discovery and a single canonical source of truth.

## Consequences

### Benefits

- Business directories remain untouched by embedded installation.
- Framework paths are recognizable and independently migratable.
- Tools can discover the project root from any descendant directory.

### Tradeoffs

- V2.1 adopters must perform a reviewed one-time migration.
- Every Skill, tool, integration, and documentation link changes once.
- `.agents/` and `.agent-context/` remain two intentional top-level entries.

## Evidence

- Requirement: `agent-context-template-v2.2-codex-task.md`.
- Implementation: `.agent-context/scripts/context_paths.py` and
  `.agent-context/scripts/init-ai-context.sh`.
- Verification: `.agent-context/tests/` covers migration, discovery, and
  non-invasive embedded installation.
