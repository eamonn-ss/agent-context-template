# Claude / Claude Code Integration

Use `AGENTS.md` as the shared protocol even if the local Claude setup also uses a
tool-specific instruction file. That adapter should point to the shared files,
not duplicate them.

- Discovery: instruct Claude to read `AGENTS.md` and the requested Skill under
  `.agents/skills/`.
- First adoption: follow `project-init/SKILL.md`.
- New session: follow `context-start/SKILL.md`.
- Advanced explicit entry: use `context-bootstrap` for project orientation or
  `context-resume` to force task continuation.
- Handoff: follow `session-handoff/SKILL.md`.

Claude-specific hooks or commands are optional. They must preserve
`.agent-context/state/` as
canonical, avoid loading all history, and enforce the same secret-handling rules.
