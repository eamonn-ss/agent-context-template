#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET="${1:-}"

if [[ -z "${TARGET}" ]]; then
  echo "Usage: $0 /path/to/project"
  exit 1
fi

mkdir -p "${TARGET}"

copy_if_missing() {
  local src="$1"
  local dst="$2"
  if [[ -e "${dst}" ]]; then
    echo "[SKIP] ${dst} already exists"
    return 0
  fi
  mkdir -p "$(dirname "${dst}")"
  cp -R "${src}" "${dst}"
  echo "[ADD]  ${dst}"
}

sync_tree_if_missing() {
  local src="$1"
  local dst="$2"
  mkdir -p "${dst}"
  local file rel
  while IFS= read -r -d '' file; do
    rel="${file#"${src}"/}"
    copy_if_missing "${file}" "${dst}/${rel}"
  done < <(find "${src}" -type f -print0)
}

copy_if_missing "${TEMPLATE_ROOT}/AGENTS.md" "${TARGET}/AGENTS.md"
sync_tree_if_missing "${TEMPLATE_ROOT}/.agents" "${TARGET}/.agents"

mkdir -p \
  "${TARGET}/.agent/decisions" \
  "${TARGET}/.agent/memory" \
  "${TARGET}/.agent/sessions" \
  "${TARGET}/.agent/archive"

copy_if_missing "${TEMPLATE_ROOT}/templates/PROJECT.template.md" "${TARGET}/.agent/PROJECT.md"
copy_if_missing "${TEMPLATE_ROOT}/templates/ARCHITECTURE.template.md" "${TARGET}/.agent/ARCHITECTURE.md"
copy_if_missing "${TEMPLATE_ROOT}/templates/CURRENT_TASK.template.md" "${TARGET}/.agent/CURRENT_TASK.md"
copy_if_missing "${TEMPLATE_ROOT}/templates/DECISIONS.template.md" "${TARGET}/.agent/DECISIONS.md"
copy_if_missing "${TEMPLATE_ROOT}/templates/HANDOFF.template.md" "${TARGET}/.agent/HANDOFF.md"
copy_if_missing "${TEMPLATE_ROOT}/templates/TODO.template.md" "${TARGET}/.agent/TODO.md"
copy_if_missing "${TEMPLATE_ROOT}/templates/FACTS.template.md" "${TARGET}/.agent/memory/FACTS.md"
copy_if_missing "${TEMPLATE_ROOT}/templates/HYPOTHESES.template.md" "${TARGET}/.agent/memory/HYPOTHESES.md"
copy_if_missing "${TEMPLATE_ROOT}/templates/DISCOVERIES.template.md" "${TARGET}/.agent/memory/DISCOVERIES.md"

sync_tree_if_missing "${TEMPLATE_ROOT}/templates" "${TARGET}/templates"
mkdir -p "${TARGET}/scripts"
for script in collect_git_state.py context_status.py validate_context.py compact_sessions.py check-context.sh; do
  copy_if_missing "${TEMPLATE_ROOT}/scripts/${script}" "${TARGET}/scripts/${script}"
done

copy_if_missing \
  "${TEMPLATE_ROOT}/.cursor/rules/ai-context.mdc" \
  "${TARGET}/.cursor/rules/ai-context.mdc"
copy_if_missing \
  "${TEMPLATE_ROOT}/.cursorignore.example" \
  "${TARGET}/.cursorignore.example"
copy_if_missing "${TEMPLATE_ROOT}/docs/protocol.md" "${TARGET}/docs/context-protocol.md"

echo
echo "Agent context V2 initialized without overwriting existing files."
echo "Next:"
echo "  1. Replace placeholders in .agent/*.md and .agent/memory/*.md"
echo "  2. Run python scripts/validate_context.py"
echo "  3. Ask an agent to follow context-bootstrap"
echo "  4. Commit the reviewed context skeleton"
