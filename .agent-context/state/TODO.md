# Roadmap

## V2.2

- [x] Isolate state and implementation beneath `.agent-context/`.
- [x] Keep agent-discoverable Skills under `.agents/skills/`.
- [x] Verify migration, embedded installation, documentation, and all tests.

## V2.3

- [x] Compare recorded handoff Git evidence with HEAD and the worktree.
- [x] Flag a finished task whose Done when lacks a command and result, whose next
  action still asks to commit on a clean worktree, or whose dirty handoff lists
  files Git does not show.

## V2.4

- Evaluate an optional index of decision IDs, fact IDs, and paths. Keep Markdown
  as the source of truth; do not add embeddings.

## V3

- Evaluate an optional MCP Context Server while preserving local inspectability.
