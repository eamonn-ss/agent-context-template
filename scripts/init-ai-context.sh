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

# Copy each file under src into dst, skipping paths that already exist.
# Safe when dst is missing, empty, or only partially populated.
sync_tree_if_missing() {
  local src="$1"
  local dst="$2"

  if [[ ! -d "${src}" ]]; then
    echo "[MISS] ${src}"
    return 1
  fi

  mkdir -p "${dst}"

  local file rel
  while IFS= read -r -d '' file; do
    rel="${file#"${src}"/}"
    copy_if_missing "${file}" "${dst}/${rel}"
  done < <(find "${src}" -type f -print0)
}

copy_if_missing "${TEMPLATE_ROOT}/AGENTS.md" "${TARGET}/AGENTS.md"
sync_tree_if_missing "${TEMPLATE_ROOT}/.ai" "${TARGET}/.ai"

mkdir -p "${TARGET}/.cursor/rules"
copy_if_missing \
  "${TEMPLATE_ROOT}/.cursor/rules/ai-context.mdc" \
  "${TARGET}/.cursor/rules/ai-context.mdc"

copy_if_missing \
  "${TEMPLATE_ROOT}/.cursorignore.example" \
  "${TARGET}/.cursorignore.example"

mkdir -p "${TARGET}/scripts"
copy_if_missing \
  "${TEMPLATE_ROOT}/scripts/check-context.sh" \
  "${TARGET}/scripts/check-context.sh"

echo
echo "AI project context initialized."
echo "Next:"
echo "  1. Edit .ai/context.md"
echo "  2. Edit .ai/architecture.md"
echo "  3. Edit .ai/current.md"
echo "  4. Run ./scripts/check-context.sh"
echo "  5. Commit the context skeleton to Git"
