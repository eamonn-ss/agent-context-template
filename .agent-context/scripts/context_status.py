#!/usr/bin/env python3
"""Show a concise V2 project context status."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from collect_git_state import collect_git_state
from context_paths import (
    CONTEXT_DIRNAME,
    legacy_v21_detected,
    memory_dir,
    resolve_project_root,
    sessions_dir,
    state_dir,
)
from validate_context import validate_project


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _section(text: str, name: str, fallback: str = "Unknown") -> str:
    match = re.search(
        rf"^##\s+{re.escape(name)}\s*$\s*([\s\S]*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    if not match:
        return fallback
    lines = [line.strip().lstrip("- ") for line in match.group(1).splitlines() if line.strip()]
    return " ".join(lines) if lines else fallback


def _count_status(text: str, status: str) -> int:
    return len(re.findall(rf"^###\s+Status\s*$\s*{status}\s*$", text, re.MULTILINE | re.IGNORECASE))


def build_status(root: Path | str | None = None) -> dict[str, object]:
    base = resolve_project_root(root)
    state = state_dir(base)
    project = _read(state / "PROJECT.md")
    task = _read(state / "CURRENT_TASK.md")
    handoff_path = state / "HANDOFF.md"
    handoff = _read(handoff_path)
    hypotheses = _read(memory_dir(base) / "HYPOTHESES.md")
    decisions = _read(state / "DECISIONS.md")
    session_path = sessions_dir(base)
    sessions = sorted(path.name for path in session_path.glob("*.md")) if session_path.is_dir() else []
    git = collect_git_state(base)
    issues = validate_project(base)
    errors = sum(issue.level == "ERROR" for issue in issues)
    warnings = sum(issue.level == "WARNING" for issue in issues)
    health = "ERROR" if errors else "WARNING" if warnings or not git["is_git_repository"] else "GOOD"
    modified = _unique_paths(git)
    proposed = len(re.findall(r"\|\s*DEC-\d{4}\s*\|\s*Proposed\s*\|", decisions, re.IGNORECASE))
    return {
        "project": _section(project, "Name"),
        "current_task": _section(task, "Goal"),
        "task_status": _section(task, "Status"),
        "branch": git["branch"] or "Unavailable",
        "modified_files": modified,
        "last_handoff": _section(handoff, "Completed", "Missing") if handoff else "Missing",
        "open_decisions": proposed,
        "open_hypotheses": _count_status(hypotheses, "Open"),
        "recent_sessions": sessions[-3:],
        "context_health": health,
        "errors": errors,
        "warnings": warnings,
        "context_layout": "V2.2 namespaced",
        "context_root": CONTEXT_DIRNAME,
        "legacy_layout": "detected" if legacy_v21_detected(base) else "not detected",
    }


def _unique_paths(git: dict[str, object]) -> list[str]:
    values: list[str] = []
    for key in ("modified_files", "untracked_files", "deleted_files", "staged_files"):
        values.extend(str(item) for item in git[key])  # type: ignore[union-attr]
    return list(dict.fromkeys(values))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="project root (auto-discovered by default)")
    args = parser.parse_args()
    status = build_status(args.root)
    print("Agent Context Status")
    print("─" * 32)
    print(f"Context Layout: {status['context_layout']}")
    print(f"Context Root: {status['context_root']}")
    print(f"Legacy Layout: {status['legacy_layout']}")
    print(f"Project: {status['project']}")
    print(f"Current task: {status['current_task']}")
    print(f"Task status: {status['task_status']}")
    print(f"Branch: {status['branch']}")
    modified = status["modified_files"]
    print(f"Modified files: {', '.join(modified) if modified else 'None'}")
    print(f"Last handoff: {status['last_handoff']}")
    print(f"Open decisions: {status['open_decisions']}")
    print(f"Open hypotheses: {status['open_hypotheses']}")
    sessions = status["recent_sessions"]
    print(f"Recent sessions: {', '.join(sessions) if sessions else 'None'}")
    print(f"Context health: {status['context_health']}")
    return 1 if status["context_health"] == "ERROR" else 0


if __name__ == "__main__":
    raise SystemExit(main())
