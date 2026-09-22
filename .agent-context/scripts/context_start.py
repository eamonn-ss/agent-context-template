#!/usr/bin/env python3
"""Select the safe context-loading mode for a new agent session."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from context_paths import resolve_project_root, state_dir
from validate_context import contains_template_placeholder


TERMINAL_TASK_STATUSES = {
    "cancelled",
    "canceled",
    "closed",
    "complete",
    "completed",
    "done",
}
ACTIVE_TASK_STATUSES = {"active", "blocked", "in progress", "in-progress", "ready"}


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _section(text: str, name: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(name)}\s*$\s*([\s\S]*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1).strip() if match else ""


def _usable(text: str) -> bool:
    return bool(text.strip()) and not contains_template_placeholder(text)


def project_state_initialized(root: Path | str | None = None) -> bool:
    base = resolve_project_root(root)
    return all(
        _usable(_read(state_dir(base) / name))
        for name in ("PROJECT.md", "ARCHITECTURE.md")
    )


def active_task(root: Path | str | None = None) -> bool:
    text = _read(state_dir(resolve_project_root(root)) / "CURRENT_TASK.md")
    if not _usable(text):
        return False
    status = " ".join(_section(text, "Status").lower().split())
    if status in TERMINAL_TASK_STATUSES:
        return False
    return status in ACTIVE_TASK_STATUSES


def usable_handoff(root: Path | str | None = None) -> bool:
    text = _read(state_dir(resolve_project_root(root)) / "HANDOFF.md")
    if not _usable(text):
        return False
    return bool(
        _section(text, "Goal")
        and (_section(text, "Next Steps") or _section(text, "Suggested First Action"))
    )


def detect_mode(root: Path | str | None = None) -> dict[str, Any]:
    initialized = project_state_initialized(root)
    task_is_active = active_task(root)
    handoff_is_usable = usable_handoff(root)
    if not initialized:
        mode = "INIT_REQUIRED"
        message = "Project context has not been initialized.\nRun /project-init first."
    elif task_is_active and handoff_is_usable:
        mode = "RESUME"
        message = "Continue the active task using /context-resume."
    else:
        mode = "BOOTSTRAP"
        message = "Load the initialized project view using /context-bootstrap."
    return {
        "mode": mode,
        "message": message,
        "project_initialized": initialized,
        "active_task": task_is_active,
        "usable_handoff": handoff_is_usable,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="project root (auto-discovered by default)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    result = detect_mode(args.root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Mode: {result['mode']}")
        print(result["message"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
