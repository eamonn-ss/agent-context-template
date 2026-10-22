# Cursor Integration

Cursor enters through the repository `AGENTS.md`; the existing
`.cursor/rules/ai-context.mdc` reminds sessions to follow it.

- Discovery: keep the rule enabled and expose `.agents/skills/` to the workspace.
- First adoption: ask Cursor to follow `.agents/skills/project-init/SKILL.md`.
- New session: ask it to follow `.agents/skills/context-start/SKILL.md`.
- Handoff: ask it to follow `.agents/skills/session-handoff/SKILL.md`.

Cursor-specific rules are adapters only. Do not copy canonical state or complete
Skill bodies into `.cursor/`. Review `.cursorignore` before enabling it so
`.agent-context/` is not accidentally hidden. `.agents/skills/` remains at the
project root for discovery; Context System implementation stays namespaced.
