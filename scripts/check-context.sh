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
  ".ai/index.md"
  ".ai/context.md"
  ".ai/architecture.md"
  ".ai/current.md"
  ".ai/changelog.md"
  ".ai/decisions/README.md"
  ".ai/tasks/README.md"
  ".ai/handoffs/README.md"
  ".ai/archive/README.md"
  ".ai/templates/README.md"
  ".ai/templates/TASK-000-template.md"
  ".ai/templates/ADR-0000-template.md"
  ".ai/templates/HANDOFF-template.md"
  ".ai/templates/new-task.md"
  ".ai/templates/session-start.md"
  ".ai/templates/session-end.md"
  ".cursor/rules/ai-context.mdc"
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

echo

# Template skeletons must not live in active registries.
while IFS= read -r -d '' stray; do
  echo "[WARN] template file in active dir: ${stray}"
  echo "       move to .ai/templates/ (or delete if obsolete)"
  warned=1
done < <(find .ai/tasks .ai/decisions .ai/handoffs \
  -type f \( -name '*-template.md' -o -name '*template.md' \) -print0 2>/dev/null)

# Bootstrap placeholders that commonly confuse new sessions.
placeholder_files=(
  ".ai/current.md"
  ".ai/context.md"
  ".ai/architecture.md"
)

for file in "${placeholder_files[@]}"; do
  [[ -f "${file}" ]] || continue
  if grep -qE 'TASK-XXX|<CURRENT_OBJECTIVE>|<PROJECT_NAME>|<PRIMARY_PROJECT_GOAL>|<WHAT_THIS_PROJECT_DOES>' "${file}"; then
    echo "[WARN] ${file} still contains bootstrap placeholders"
    echo "       fill these after adopting the template into a real project"
    warned=1
  fi
done

echo
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Git working tree:"
  git status --short
fi

if [[ "${STRICT}" -eq 1 && "${warned}" -ne 0 ]]; then
  echo
  echo "Strict mode: treating warnings as failures."
  failed=1
fi

exit "${failed}"
