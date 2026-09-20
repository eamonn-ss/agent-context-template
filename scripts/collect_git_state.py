#!/usr/bin/env python3
"""Collect the small, objective subset of Git state needed for context work."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, Sequence


def _git(repo: Path, args: Sequence[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        return 127, "git executable not found"
    if result.returncode == 0:
        # Porcelain status uses leading spaces as data; only trim line endings.
        return result.returncode, result.stdout.rstrip("\r\n")
    return result.returncode, result.stderr.strip()


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _parse_porcelain(output: str) -> dict[str, list[str]]:
    modified: list[str] = []
    untracked: list[str] = []
    deleted: list[str] = []
    staged: list[str] = []
    records = output.split("\0")
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        code = record[:2]
        path = record[3:] if len(record) > 3 else ""
        if code[0] in {"R", "C"} and index < len(records):
            # Porcelain -z emits the destination first; consume the source name.
            index += 1
        if code == "??":
            untracked.append(path)
            continue
        if "D" in code:
            deleted.append(path)
        else:
            modified.append(path)
        if code[0] not in {" ", "?"}:
            staged.append(path)
    return {
        "modified_files": _unique(modified),
        "untracked_files": _unique(untracked),
        "deleted_files": _unique(deleted),
        "staged_files": _unique(staged),
    }


def collect_git_state(repo: Path | str = ".", recent_count: int = 5) -> dict[str, Any]:
    requested = Path(repo).resolve()
    code, top = _git(requested, ["rev-parse", "--show-toplevel"])
    empty: dict[str, Any] = {
        "repository": str(requested),
        "is_git_repository": False,
        "branch": None,
        "head_commit": None,
        "modified_files": [],
        "untracked_files": [],
        "deleted_files": [],
        "staged_files": [],
        "recent_commits": [],
        "diff_stat": [],
    }
    if code != 0:
        empty["error"] = top or "not a Git repository"
        return empty

    root = Path(top).resolve()
    state = {**empty, "repository": str(root), "is_git_repository": True}

    _, branch = _git(root, ["branch", "--show-current"])
    state["branch"] = branch or "(detached HEAD)"

    head_code, head = _git(root, ["rev-parse", "HEAD"])
    if head_code == 0:
        state["head_commit"] = head

    status_code, status = _git(root, ["status", "--porcelain=v1", "-z"])
    if status_code == 0:
        state.update(_parse_porcelain(status))

    log_code, log = _git(
        root,
        ["log", f"-{recent_count}", "--format=%H%x1f%h%x1f%s"],
    )
    if log_code == 0 and log:
        state["recent_commits"] = [
            {"commit": full, "short": short, "subject": subject}
            for full, short, subject in
            (line.split("\x1f", 2) for line in log.splitlines())
        ]

    if state["head_commit"]:
        diff_code, diff = _git(root, ["diff", "--stat", "HEAD"])
    else:
        diff_code, diff = _git(root, ["diff", "--stat"])
    if diff_code == 0 and diff:
        state["diff_stat"] = diff.splitlines()
    return state


def _human(state: dict[str, Any]) -> str:
    if not state["is_git_repository"]:
        return f"Repository: {state['repository']}\nGit: unavailable ({state.get('error', 'unknown error')})"
    lines = [
        f"Repository: {state['repository']}",
        f"Branch: {state['branch']}",
        f"HEAD: {state['head_commit'] or '(no commits)'}",
    ]
    for label, key in (
        ("Modified files", "modified_files"),
        ("Untracked files", "untracked_files"),
        ("Deleted files", "deleted_files"),
        ("Staged files", "staged_files"),
    ):
        values = state[key]
        lines.append(f"{label}: {', '.join(values) if values else 'None'}")
    lines.append("Recent commits:")
    lines.extend(
        f"  {item['short']} {item['subject']}" for item in state["recent_commits"]
    )
    if not state["recent_commits"]:
        lines.append("  None")
    lines.append("Diff stat:")
    lines.extend(f"  {line}" for line in state["diff_stat"] or ["None"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="repository path")
    parser.add_argument("--recent", type=int, default=5, help="recent commit count")
    args = parser.parse_args()
    state = collect_git_state(args.repo, max(0, args.recent))
    print(json.dumps(state, indent=2, ensure_ascii=False) if args.json else _human(state))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
