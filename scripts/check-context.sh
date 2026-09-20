#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "${ROOT}"
STRICT=0
if [[ "${1:-}" == "--strict" ]]; then
  STRICT=1
fi

required=(
  "AGENTS.md"
  ".agent/PROJECT.md"
  ".agent/ARCHITECTURE.md"
  ".agent/CURRENT_TASK.md"
  ".agent/DECISIONS.md"
  ".agent/HANDOFF.md"
  ".agent/TODO.md"
  ".agent/memory/FACTS.md"
  ".agent/memory/HYPOTHESES.md"
  ".agent/memory/DISCOVERIES.md"
  ".agents/skills/context-bootstrap/SKILL.md"
  ".agents/skills/context-resume/SKILL.md"
  ".agents/skills/session-handoff/SKILL.md"
  ".agents/skills/record-decision/SKILL.md"
  ".agents/skills/context-compact/SKILL.md"
  ".agents/skills/project-status/SKILL.md"
  "scripts/validate_context.py"
)

failed=0
warned=0
for file in "${required[@]}"; do
  if [[ -f "${file}" ]]; then
    echo "[OK]   ${file}"
  else
    echo "[MISS] ${file}"
    failed=1
  fi
done

if [[ -f scripts/validate_context.py ]]; then
  echo
  if ! python scripts/validate_context.py; then
    failed=1
  fi
fi

if grep -R -qE '<[A-Z][A-Z0-9_ -]{2,}>|TASK-XXX|\{\{[^}]+\}\}' \
  .agent --include='*.md' 2>/dev/null; then
  echo "[WARN] canonical context still contains template placeholders"
  warned=1
fi

echo
echo "Git working tree:"
git status --short 2>/dev/null || echo "(not a Git repository)"

if [[ "${STRICT}" -eq 1 && "${warned}" -ne 0 ]]; then
  echo "Strict mode: treating warnings as failures."
  failed=1
fi
exit "${failed}"
