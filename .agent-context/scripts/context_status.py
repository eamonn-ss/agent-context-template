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


MISSING_GIT_EVIDENCE = "handoff does not record Git evidence"
GIT_EVIDENCE_MISMATCH = "handoff Git evidence does not match HEAD"
UNCLOSED = "previous session did not record the current work"
DONE_WHEN = "Done when has no command and result"
MODIFIED_FILES = "handoff modified files are not in git status"
UNFINISHED_COMMIT = "finished task still asks to commit"
_FINISHED = {"done", "completed", "complete"}
_COMMAND = re.compile(r"`[^`]+`|\b(?:python|pytest|npm|pnpm|yarn|cargo|go|bash|sh|make)\b", re.IGNORECASE)
_RESULT = re.compile(r"\b(?:exits?|exit code|passed|failed)\b|通过|退出", re.IGNORECASE)
_COMMIT_ASK = re.compile(r"\bcommit\b|提交", re.IGNORECASE)
_UNFINISHED = re.compile(
    r"\b(?:todo|fixme|wip|in progress|not done|unfinished)\b|未完成|待实现|继续实现|尚未",
    re.IGNORECASE,
)
_NONE_LINE = re.compile(r"^(?:none|n/?a|no further action|nothing)\.?$", re.IGNORECASE)


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


def _section_lines(text: str, name: str) -> list[str]:
    match = re.search(
        rf"^##\s+{re.escape(name)}\s*$\s*([\s\S]*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    if not match:
        return []
    return [
        line.strip().lstrip("- ").strip()
        for line in match.group(1).splitlines()
        if line.strip()
    ]


def _git_evidence(handoff: str) -> tuple[str, str]:
    commit = ""
    worktree = ""
    for line in _section_lines(handoff, "Git Evidence"):
        label, _, value = line.partition(":")
        if label.lower() == "commit":
            commit = value.strip()
        elif label.lower() == "worktree":
            worktree = value.strip().lower()
    return commit, worktree


def _same_commit(recorded: str, actual: object) -> bool:
    if not recorded or not isinstance(actual, str) or not actual:
        return False
    short, full = sorted((recorded, actual), key=len)
    return len(short) >= 7 and full.startswith(short)


def _worktree_label(git: dict[str, object]) -> str:
    dirty = any(
        git[key] for key in ("modified_files", "untracked_files", "deleted_files", "staged_files")
    )
    return "dirty" if dirty else "clean"


def _parent_commit(git: dict[str, object]) -> str:
    commits = git.get("recent_commits")
    head = git.get("head_commit")
    if not isinstance(commits, list) or not isinstance(head, str) or len(commits) < 2:
        return ""
    latest = commits[0]
    parent = commits[1]
    if not isinstance(latest, dict) or not isinstance(parent, dict):
        return ""
    if latest.get("commit") != head:
        return ""
    parent_commit = parent.get("commit")
    return parent_commit if isinstance(parent_commit, str) else ""


def _task_status(task: str) -> str:
    return " ".join(_section(task, "Status").lower().split())


def _git_reason(handoff: str, git: dict[str, object]) -> str:
    recorded, worktree = _git_evidence(handoff)
    if worktree not in {"clean", "dirty"} or len(recorded) < 7:
        return MISSING_GIT_EVIDENCE
    actual = _worktree_label(git)
    if _same_commit(recorded, git.get("head_commit")) and worktree == actual:
        return ""
    # A handoff cannot store the hash of the commit that adds that handoff.
    if actual == "clean" and worktree == "dirty" and _same_commit(recorded, _parent_commit(git)):
        return ""
    if actual == "dirty":
        return UNCLOSED
    return GIT_EVIDENCE_MISMATCH


def _done_when_reason(task: str) -> str:
    if _task_status(task) not in _FINISHED:
        return ""
    body = "\n".join(_section_lines(task, "Done when"))
    if _COMMAND.search(body) and _RESULT.search(body):
        return ""
    return DONE_WHEN


def _status_paths(git: dict[str, object]) -> list[str]:
    paths: list[str] = []
    for key in ("modified_files", "untracked_files", "deleted_files", "staged_files"):
        values = git.get(key)
        if isinstance(values, list):
            paths.extend(str(item) for item in values)
    return paths


def _path_covered(listed: str, actuals: list[str]) -> bool:
    listed = listed.strip("`").rstrip("/")
    if not listed:
        return True
    for actual in actuals:
        candidate = actual.rstrip("/")
        if candidate == listed or candidate.startswith(listed + "/") or listed.startswith(candidate + "/"):
            return True
    return False


def _modified_file_reason(handoff: str, git: dict[str, object]) -> str:
    recorded, worktree = _git_evidence(handoff)
    if worktree != "dirty" or _worktree_label(git) != "dirty":
        return ""
    if not _same_commit(recorded, git.get("head_commit")):
        return ""
    actuals = _status_paths(git)
    for line in _section_lines(handoff, "Modified Files"):
        if " " in line or line.lower() in {"none", "n/a", "unknown"} or line.startswith("<"):
            continue
        if not _path_covered(line, actuals):
            return MODIFIED_FILES
    return ""


def _unfinished_reason(task: str, handoff: str, git: dict[str, object]) -> str:
    if _task_status(task) not in _FINISHED:
        return ""
    actual = _worktree_label(git) if git["is_git_repository"] else "clean"
    lines = _section_lines(task, "Next Action") + _section_lines(handoff, "Suggested First Action")
    for line in lines:
        if _NONE_LINE.match(line):
            continue
        if _COMMIT_ASK.search(line) and actual == "clean":
            return UNFINISHED_COMMIT
        if _UNFINISHED.search(line):
            return "finished task still has an unfinished next action"
    return ""


def _freshness(task: str, handoff: str, git: dict[str, object]) -> tuple[str, str]:
    reasons: list[str] = []
    if git["is_git_repository"]:
        git_reason = _git_reason(handoff, git)
        if git_reason:
            reasons.append(git_reason)
        file_reason = _modified_file_reason(handoff, git)
        if file_reason:
            reasons.append(file_reason)
    done_when = _done_when_reason(task)
    if done_when:
        reasons.append(done_when)
    unfinished = _unfinished_reason(task, handoff, git)
    if unfinished:
        reasons.append(unfinished)
    if not reasons and not git["is_git_repository"]:
        return "unknown", ""
    if reasons:
        return "stale", "; ".join(reasons)
    return "current", ""


def _handoff_action(path: Path, handoff: str) -> str:
    if not path.is_file():
        return "Missing"
    for name in ("Suggested First Action", "Next Steps"):
        lines = _section_lines(handoff, name)
        if lines:
            return lines[0]
    return "None"


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
    freshness, freshness_reason = _freshness(task, handoff, git)
    issues = validate_project(base)
    errors = sum(issue.level == "ERROR" for issue in issues)
    warnings = sum(issue.level == "WARNING" for issue in issues)
    health = (
        "ERROR"
        if errors
        else "WARNING"
        if warnings or not git["is_git_repository"] or freshness == "stale"
        else "GOOD"
    )
    modified = _unique_paths(git)
    proposed = len(re.findall(r"\|\s*DEC-\d{4}\s*\|\s*Proposed\s*\|", decisions, re.IGNORECASE))
    return {
        "project": _section(project, "Name"),
        "current_task": _section(task, "Goal"),
        "task_status": _section(task, "Status"),
        "branch": git["branch"] or "Unavailable",
        "modified_files": modified,
        "handoff_action": _handoff_action(handoff_path, handoff),
        "freshness": freshness,
        "freshness_reason": freshness_reason,
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
    print(f"Handoff action: {status['handoff_action']}")
    if status["freshness"] == "stale":
        print(f"Freshness: stale — {status['freshness_reason']}")
    else:
        print(f"Freshness: {status['freshness']}")
    print(f"Open decisions: {status['open_decisions']}")
    print(f"Open hypotheses: {status['open_hypotheses']}")
    sessions = status["recent_sessions"]
    print(f"Recent sessions: {', '.join(sessions) if sessions else 'None'}")
    print(f"Context health: {status['context_health']}")
    return 1 if status["context_health"] == "ERROR" else 0


if __name__ == "__main__":
    raise SystemExit(main())
