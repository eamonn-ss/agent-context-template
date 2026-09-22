#!/usr/bin/env python3
"""Shared path discovery for the namespaced Agent Context layout."""

from __future__ import annotations

from pathlib import Path


CONTEXT_DIRNAME = ".agent-context"
CONTEXT_ROOT = Path(CONTEXT_DIRNAME)
STATE_ROOT = CONTEXT_ROOT / "state"
MEMORY_ROOT = CONTEXT_ROOT / "memory"
SESSIONS_ROOT = CONTEXT_ROOT / "sessions"
ARCHIVE_ROOT = CONTEXT_ROOT / "archive"


def _start_directory(start: Path | str | None = None) -> Path:
    path = Path.cwd() if start is None else Path(start)
    path = path.expanduser().resolve()
    return path.parent if path.is_file() else path


def find_context_root(start: Path | str | None = None) -> Path:
    """Find ``.agent-context`` at or above *start*."""
    current = _start_directory(start)
    for candidate in (current, *current.parents):
        if candidate.name == CONTEXT_DIRNAME and candidate.is_dir():
            return candidate
        context = candidate / CONTEXT_DIRNAME
        if context.is_dir():
            return context
    raise FileNotFoundError(
        f"{CONTEXT_DIRNAME} not found from {current}; run the installer first"
    )


def find_project_root(start: Path | str | None = None) -> Path:
    return find_context_root(start).parent


def resolve_project_root(root: Path | str | None = None) -> Path:
    """Resolve an explicit project root, or discover one from the current path."""
    if root is None:
        return find_project_root()
    path = Path(root).expanduser().resolve()
    if path.name == CONTEXT_DIRNAME:
        return path.parent
    return path


def context_root(root: Path | str | None = None) -> Path:
    return resolve_project_root(root) / CONTEXT_DIRNAME


def state_dir(root: Path | str | None = None) -> Path:
    return context_root(root) / "state"


def memory_dir(root: Path | str | None = None) -> Path:
    return context_root(root) / "memory"


def sessions_dir(root: Path | str | None = None) -> Path:
    return context_root(root) / "sessions"


def archive_dir(root: Path | str | None = None) -> Path:
    return context_root(root) / "archive"


def legacy_v21_detected(root: Path | str | None = None) -> bool:
    """Detect V2.1 by its dedicated canonical-state markers, not generic dirs."""
    legacy = resolve_project_root(root) / ".agent"
    return any(
        (legacy / name).is_file()
        for name in ("PROJECT.md", "ARCHITECTURE.md", "CURRENT_TASK.md")
    )
