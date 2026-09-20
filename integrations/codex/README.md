# Codex Integration

Codex uses root `AGENTS.md` as the protocol entry and project Skills under
`.agents/skills/` as the shared operational procedures.

- Discovery: open the repository root so `AGENTS.md` and project Skills are in
  scope.
- First entry: invoke or request `context-bootstrap`.
- Resume: invoke or request `context-resume`.
- Handoff: invoke or request `session-handoff` before switching sessions/tools.

Codex must still verify Git state and honor normal approval boundaries. Native
memory and prior chat never override the repository source priority.
