#!/usr/bin/env python3
"""Preview or archive session summaries explicitly marked ready for compaction."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from context_paths import archive_dir, resolve_project_root, sessions_dir


READY_MARKER = "**Compaction:** Ready"


def compaction_plan(root: Path | str | None = None, keep: int = 5) -> dict[str, list[str]]:
    base = resolve_project_root(root)
    source = sessions_dir(base)
    sessions = sorted(source.glob("*.md")) if source.is_dir() else []
    eligible_pool = sessions[: max(0, len(sessions) - max(0, keep))]
    ready: list[str] = []
    skipped: list[str] = []
    for path in eligible_pool:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            skipped.append(path.name)
            continue
        (ready if READY_MARKER in text else skipped).append(path.name)
    protected = [path.name for path in sessions[len(eligible_pool) :]]
    return {"archive": ready, "skipped_not_ready": skipped, "protected_recent": protected}


def apply_plan(root: Path | str | None, plan: dict[str, list[str]]) -> list[str]:
    base = resolve_project_root(root)
    source = sessions_dir(base)
    archive = archive_dir(base)
    archive.mkdir(parents=True, exist_ok=True)
    moved: list[str] = []
    for name in plan["archive"]:
        destination = archive / name
        if destination.exists():
            raise FileExistsError(f"archive destination already exists: {destination}")
        shutil.move(str(source / name), str(destination))
        moved.append(name)
    return moved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="project root (auto-discovered by default)")
    parser.add_argument("--keep", type=int, default=5, help="number of newest sessions to protect")
    parser.add_argument("--apply", action="store_true", help="move eligible sessions after preview")
    args = parser.parse_args()
    plan = compaction_plan(args.root, args.keep)
    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"Session Compaction ({mode})")
    print("─" * 32)
    print(f"Archive: {', '.join(plan['archive']) if plan['archive'] else 'None'}")
    print(f"Skipped (not Ready): {', '.join(plan['skipped_not_ready']) if plan['skipped_not_ready'] else 'None'}")
    print(f"Protected recent: {', '.join(plan['protected_recent']) if plan['protected_recent'] else 'None'}")
    if args.apply:
        moved = apply_plan(args.root, plan)
        print(f"Moved: {', '.join(moved) if moved else 'None'}")
    else:
        print("No files changed. Re-run with --apply after reviewing canonical knowledge migration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
