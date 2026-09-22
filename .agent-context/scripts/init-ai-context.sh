#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXT_SOURCE="$(cd "${SCRIPT_DIR}/.." && pwd)"
TEMPLATE_ROOT="$(cd "${CONTEXT_SOURCE}/.." && pwd)"
TARGET=""
PROFILE="embedded"
DRY_RUN=0

usage() {
  echo "Usage: $0 [--dry-run] [--profile embedded|development] /path/to/project"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --profile) shift; PROFILE="${1:-}" ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
    *)
      if [[ -n "${TARGET}" ]]; then
        echo "Only one target project may be provided." >&2
        exit 1
      fi
      TARGET="$1"
      ;;
  esac
  shift
done

if [[ -z "${TARGET}" || ( "${PROFILE}" != "embedded" && "${PROFILE}" != "development" ) ]]; then
  usage >&2
  exit 1
fi

TARGET="$(cd "$(dirname "${TARGET}")" && pwd)/$(basename "${TARGET}")"
if [[ "${DRY_RUN}" -eq 0 ]]; then
  mkdir -p "${TARGET}"
fi

copy_if_missing() {
  local src="$1"
  local dst="$2"
  if [[ -e "${dst}" ]]; then
    echo "[SKIP] ${dst} already exists"
    return 0
  fi
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    echo "[ADD]  ${dst}"
    return 0
  fi
  mkdir -p "$(dirname "${dst}")"
  cp -R "${src}" "${dst}"
  echo "[ADD]  ${dst}"
}

sync_tree_if_missing() {
  local src="$1"
  local dst="$2"
  local file rel
  while IFS= read -r -d '' file; do
    rel="${file#"${src}"/}"
    copy_if_missing "${file}" "${dst}/${rel}"
  done < <(find "${src}" -type f ! -path '*/__pycache__/*' -print0)
}

if [[ -f "${TARGET}/.agent-context/VERSION" ]]; then
  echo "Existing Agent Context version: $(tr -d '\r\n' < "${TARGET}/.agent-context/VERSION")"
fi

legacy=0
if [[ -f "${TARGET}/.agent/PROJECT.md" && ! -f "${TARGET}/.agent-context/state/PROJECT.md" ]]; then
  legacy=1
  echo "Legacy V2.1 layout detected. Migration is required."
fi

copy_if_missing "${TEMPLATE_ROOT}/AGENTS.md" "${TARGET}/AGENTS.md"
sync_tree_if_missing "${TEMPLATE_ROOT}/.agents" "${TARGET}/.agents"
sync_tree_if_missing "${CONTEXT_SOURCE}/scripts" "${TARGET}/.agent-context/scripts"
sync_tree_if_missing "${CONTEXT_SOURCE}/templates" "${TARGET}/.agent-context/templates"
copy_if_missing "${CONTEXT_SOURCE}/VERSION" "${TARGET}/.agent-context/VERSION"

if [[ "${legacy}" -eq 0 ]]; then
  copy_if_missing "${CONTEXT_SOURCE}/templates/PROJECT.template.md" "${TARGET}/.agent-context/state/PROJECT.md"
  copy_if_missing "${CONTEXT_SOURCE}/templates/ARCHITECTURE.template.md" "${TARGET}/.agent-context/state/ARCHITECTURE.md"
  copy_if_missing "${CONTEXT_SOURCE}/templates/CURRENT_TASK.template.md" "${TARGET}/.agent-context/state/CURRENT_TASK.md"
  copy_if_missing "${CONTEXT_SOURCE}/templates/DECISIONS.template.md" "${TARGET}/.agent-context/state/DECISIONS.md"
  copy_if_missing "${CONTEXT_SOURCE}/templates/HANDOFF.template.md" "${TARGET}/.agent-context/state/HANDOFF.md"
  copy_if_missing "${CONTEXT_SOURCE}/templates/TODO.template.md" "${TARGET}/.agent-context/state/TODO.md"
  copy_if_missing "${CONTEXT_SOURCE}/templates/FACTS.template.md" "${TARGET}/.agent-context/memory/FACTS.md"
  copy_if_missing "${CONTEXT_SOURCE}/templates/HYPOTHESES.template.md" "${TARGET}/.agent-context/memory/HYPOTHESES.md"
  copy_if_missing "${CONTEXT_SOURCE}/templates/DISCOVERIES.template.md" "${TARGET}/.agent-context/memory/DISCOVERIES.md"
fi

if [[ "${DRY_RUN}" -eq 0 ]]; then
  mkdir -p "${TARGET}/.agent-context/decisions" "${TARGET}/.agent-context/sessions" "${TARGET}/.agent-context/archive"
fi

copy_if_missing "${TEMPLATE_ROOT}/.cursor/rules/ai-context.mdc" "${TARGET}/.cursor/rules/ai-context.mdc"
copy_if_missing "${TEMPLATE_ROOT}/.cursorignore.example" "${TARGET}/.cursorignore.example"

if [[ "${PROFILE}" == "development" ]]; then
  sync_tree_if_missing "${CONTEXT_SOURCE}/docs" "${TARGET}/.agent-context/docs"
  sync_tree_if_missing "${CONTEXT_SOURCE}/integrations" "${TARGET}/.agent-context/integrations"
  sync_tree_if_missing "${CONTEXT_SOURCE}/tests" "${TARGET}/.agent-context/tests"
fi

echo
if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo "Agent Context V2.2 ${PROFILE} profile preview complete."
else
  echo "Agent Context V2.2 ${PROFILE} profile installation complete."
fi
echo "Business docs/, scripts/, tests/, templates/, integrations/, and source files were not touched."
if [[ "${legacy}" -eq 1 ]]; then
  echo "Next: python .agent-context/scripts/migrate_v21_to_v22.py --root \"${TARGET}\" --dry-run"
else
  echo "Next: ask an agent to run /project-init"
  echo "Validate: python .agent-context/scripts/validate_context.py --root \"${TARGET}\""
fi
