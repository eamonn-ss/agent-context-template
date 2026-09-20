# Cursor Integration

Cursor enters through the repository `AGENTS.md`; the existing
`.cursor/rules/ai-context.mdc` reminds sessions to follow it.

- Discovery: keep the rule enabled and expose `.agents/skills/` to the workspace.
- First entry: ask Cursor to follow
  `.agents/skills/context-bootstrap/SKILL.md`.
- Resume: ask it to follow `.agents/skills/context-resume/SKILL.md`.
- Handoff: ask it to follow `.agents/skills/session-handoff/SKILL.md`.

Cursor-specific rules are adapters only. Do not copy canonical state or complete
Skill bodies into `.cursor/`. Review `.cursorignore` before enabling it so
`.agent/` is not accidentally hidden.
