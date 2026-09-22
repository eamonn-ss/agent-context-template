#!/usr/bin/env python3
"""Safely migrate an Agent Context V2.1 project to the V2.2 namespace."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Move:
    source: Path
    destination: Path


STATE_FILES = (
    "PROJECT.md",
    "ARCHITECTURE.md",
    "CURRENT_TASK.md",
    "DECISIONS.md",
    "HANDOFF.md",
    "TODO.md",
)
LEGACY_TREES = ("memory", "sessions", "archive", "decisions")
FRAMEWORK_FILES = {
    "scripts": (
        "collect_git_state.py",
        "compact_sessions.py",
        "context_start.py",
        "context_status.py",
        "validate_context.py",
        "check-context.sh",
        "init-ai-context.sh",
    ),
    "templates": (
        "PROJECT.template.md",
        "ARCHITECTURE.template.md",
        "CURRENT_TASK.template.md",
        "DECISIONS.template.md",
        "HANDOFF.template.md",
        "TODO.template.md",
        "FACTS.template.md",
        "HYPOTHESES.template.md",
        "DISCOVERIES.template.md",
        "DECISION.template.md",
        "SESSION.template.md",
    ),
}


def migration_plan(root: Path | str) -> list[Move]:
    base = Path(root).expanduser().resolve()
    context = base / ".agent-context"
    legacy = base / ".agent"
    moves: list[Move] = []
    for name in STATE_FILES:
        source = legacy / name
        if source.is_file():
            moves.append(Move(source, context / "state" / name))
    for name in LEGACY_TREES:
        source = legacy / name
        if source.is_dir():
            for path in sorted(item for item in source.rglob("*") if item.is_file()):
                moves.append(Move(path, context / name / path.relative_to(source)))
    for directory, names in FRAMEWORK_FILES.items():
        for name in names:
            source = base / directory / name
            if source.is_file():
                moves.append(Move(source, context / directory / name))
    return moves


def conflicts(plan: list[Move]) -> list[Move]:
    result: list[Move] = []
    for move in plan:
        if move.destination.exists():
            try:
                same = move.source.read_bytes() == move.destination.read_bytes()
            except OSError:
                same = False
            if not same:
                result.append(move)
    return result


def apply_migration(root: Path | str, plan: list[Move]) -> None:
    base = Path(root).expanduser().resolve()
    for move in plan:
        move.destination.parent.mkdir(parents=True, exist_ok=True)
        if move.destination.exists():
            move.source.unlink()  # identical content was verified during preflight
        else:
            shutil.move(str(move.source), str(move.destination))
    # Remove only empty legacy/context-owned directories; business files survive.
    candidates = [
        base / ".agent" / name for name in LEGACY_TREES
    ] + [base / ".agent", base / "scripts", base / "templates"]
    for directory in candidates:
        try:
            directory.rmdir()
        except OSError:
            pass
    version = base / ".agent-context" / "VERSION"
    version.parent.mkdir(parents=True, exist_ok=True)
    if not version.exists():
        version.write_text("2.2.0\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root")
    parser.add_argument("--dry-run", action="store_true", help="show the plan only")
    args = parser.parse_args()
    plan = migration_plan(args.root)
    bad = conflicts(plan)
    print(f"V2.1 -> V2.2 Migration ({'DRY RUN' if args.dry_run else 'APPLY'})")
    print("─" * 40)
    if not plan:
        print("Legacy V2.1 layout not detected; no files would move.")
        return 0
    for move in plan:
        print(f"MOVE {move.source.relative_to(args.root.resolve())} -> {move.destination.relative_to(args.root.resolve())}")
    if bad:
        for move in bad:
            print(f"CONFLICT {move.destination.relative_to(args.root.resolve())}", file=sys.stderr)
        print("Migration stopped; different destination content was not overwritten.", file=sys.stderr)
        return 2
    if args.dry_run:
        print("No files changed.")
        return 0
    apply_migration(args.root, plan)
    validator = args.root.resolve() / ".agent-context/scripts/validate_context.py"
    if validator.is_file():
        completed = subprocess.run([sys.executable, str(validator), "--root", str(args.root.resolve())])
        if completed.returncode:
            return completed.returncode
    print("Migration complete. V2.2 is now canonical; legacy paths are no longer written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
