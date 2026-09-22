#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ROOT="$(cd "${CONTEXT_ROOT}/.." && pwd)"
cd "${ROOT}"
STRICT=0
if [[ "${1:-}" == "--strict" ]]; then STRICT=1; fi

required=(
  "AGENTS.md"
  ".agent-context/VERSION"
  ".agent-context/state/PROJECT.md"
  ".agent-context/state/ARCHITECTURE.md"
  ".agent-context/state/CURRENT_TASK.md"
  ".agent-context/state/DECISIONS.md"
  ".agent-context/state/HANDOFF.md"
  ".agent-context/state/TODO.md"
  ".agent-context/memory/FACTS.md"
  ".agent-context/memory/HYPOTHESES.md"
  ".agent-context/memory/DISCOVERIES.md"
  ".agents/skills/context-bootstrap/SKILL.md"
  ".agents/skills/context-start/SKILL.md"
  ".agents/skills/context-resume/SKILL.md"
  ".agents/skills/project-init/SKILL.md"
  ".agents/skills/session-handoff/SKILL.md"
  ".agents/skills/record-decision/SKILL.md"
  ".agents/skills/context-compact/SKILL.md"
  ".agents/skills/project-status/SKILL.md"
  ".agent-context/scripts/validate_context.py"
  ".agent-context/scripts/context_start.py"
)

failed=0
warned=0
for file in "${required[@]}"; do
  if [[ -f "${file}" ]]; then echo "[OK]   ${file}"; else echo "[MISS] ${file}"; failed=1; fi
done

echo
if ! python .agent-context/scripts/validate_context.py --root "${ROOT}"; then failed=1; fi

if grep -R -qE '<[A-Z][A-Z0-9_ -]{2,}>|TASK-(XXX|<NNN>)|\{\{[^}]+\}\}|\bPLACEHOLDER\b' \
  .agent-context/state .agent-context/memory --include='*.md' 2>/dev/null; then
  echo "[WARN] canonical context still contains template placeholders"
  warned=1
fi

echo
echo "Git working tree:"
git status --short 2>/dev/null || echo "(Git evidence unavailable)"
if [[ "${STRICT}" -eq 1 && "${warned}" -ne 0 ]]; then failed=1; fi
exit "${failed}"
