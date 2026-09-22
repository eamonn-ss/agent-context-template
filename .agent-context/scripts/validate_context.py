#!/usr/bin/env python3
"""Validate the V2 project context tree without requiring third-party packages."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from context_paths import (
    context_root,
    legacy_v21_detected,
    memory_dir,
    resolve_project_root,
    state_dir,
)


REQUIRED = (
    ".agent-context/state/PROJECT.md",
    ".agent-context/state/ARCHITECTURE.md",
    ".agent-context/state/CURRENT_TASK.md",
    ".agent-context/state/DECISIONS.md",
    ".agent-context/state/HANDOFF.md",
    ".agent-context/state/TODO.md",
    ".agent-context/memory/FACTS.md",
    ".agent-context/memory/HYPOTHESES.md",
    ".agent-context/memory/DISCOVERIES.md",
)
HYPOTHESIS_STATUSES = {"Open", "Testing", "Verified", "Rejected"}
PLACEHOLDER = re.compile(
    r"<[A-Z][A-Z0-9_ -]{2,}>|\{\{[^}]+\}\}|TASK-(?:XXX|<NNN>)|\bPLACEHOLDER\b",
)


@dataclass(frozen=True)
class Issue:
    level: str
    message: str


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def contains_template_placeholder(text: str) -> bool:
    """Return whether canonical content still contains scaffold markers."""
    return bool(PLACEHOLDER.search(text))


def _blocks(text: str, heading_pattern: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(heading_pattern, text, re.MULTILINE))
    return [
        (match.group(1), text[match.end() : matches[index + 1].start() if index + 1 < len(matches) else None])
        for index, match in enumerate(matches)
    ]


def validate_project(root: Path | str | None = None) -> list[Issue]:
    base = resolve_project_root(root)
    issues: list[Issue] = []
    if legacy_v21_detected(base):
        issues.append(
            Issue("WARNING", "Legacy V2.1 layout detected. Migration is required.")
        )
    for relative in REQUIRED:
        path = base / relative
        if not path.is_file():
            issues.append(Issue("ERROR", f"missing required file: {relative}"))

    canonical_files = [base / relative for relative in REQUIRED if (base / relative).is_file()]
    for path in canonical_files:
        text = _read(path)
        if contains_template_placeholder(text):
            issues.append(Issue("WARNING", f"template placeholder found: {path.relative_to(base)}"))

    current = state_dir(base) / "CURRENT_TASK.md"
    if current.is_file():
        body = re.sub(r"^#+.*$", "", _read(current), flags=re.MULTILINE).strip()
        if not body:
            issues.append(Issue("ERROR", ".agent-context/state/CURRENT_TASK.md has no task content"))

    decision_ids: dict[str, Path] = {}
    decisions_dir = context_root(base) / "decisions"
    if decisions_dir.is_dir():
        for path in sorted(decisions_dir.glob("*.md")):
            matches = re.findall(r"^#\s+(DEC-\d{4})\b", _read(path), re.MULTILINE)
            if not matches:
                issues.append(Issue("WARNING", f"decision has no DEC-NNNN heading: {path.relative_to(base)}"))
                continue
            for decision_id in matches:
                if decision_id in decision_ids:
                    first = decision_ids[decision_id].relative_to(base)
                    issues.append(Issue("ERROR", f"duplicate decision ID {decision_id}: {first} and {path.relative_to(base)}"))
                else:
                    decision_ids[decision_id] = path

    facts = memory_dir(base) / "FACTS.md"
    if facts.is_file():
        for fact_id, block in _blocks(_read(facts), r"^##\s+(F-\d+)\s*$"):
            evidence = re.search(r"^###\s+Evidence\s*$([\s\S]*?)(?=^###\s+|\Z)", block, re.MULTILINE)
            evidence_body = evidence.group(1).strip() if evidence else ""
            useful = []
            for line in evidence_body.splitlines():
                value = line.strip().lstrip("- ").strip()
                if value in {"", "None", "N/A"}:
                    continue
                if re.fullmatch(r"(?:file|line|command|test|commit|decision):\s*", value, re.IGNORECASE):
                    continue
                useful.append(value)
            if not useful:
                issues.append(Issue("ERROR", f"fact {fact_id} is missing Evidence"))

    hypotheses = memory_dir(base) / "HYPOTHESES.md"
    if hypotheses.is_file():
        for hypothesis_id, block in _blocks(_read(hypotheses), r"^##\s+(H-\d+)\s*$"):
            match = re.search(r"^###\s+Status\s*$\s*([^\n]+)", block, re.MULTILINE)
            status = match.group(1).strip() if match else ""
            if status not in HYPOTHESIS_STATUSES:
                issues.append(Issue("ERROR", f"hypothesis {hypothesis_id} has invalid status: {status or '(missing)'}"))

    handoff = state_dir(base) / "HANDOFF.md"
    if handoff.is_file():
        text = _read(handoff)
        references = re.findall(r"(?:file:\s*|\[[^]]*\]\()([^\s)]+)", text)
        for raw in references:
            if raw.startswith(("http://", "https://", "#")) or "<" in raw:
                continue
            candidate = Path(raw.strip("`"))
            resolved = candidate if candidate.is_absolute() else base / candidate
            if not resolved.exists():
                issues.append(Issue("ERROR", f"HANDOFF references missing file: {raw}"))

    if not issues:
        issues.append(Issue("PASS", "context structure and content checks passed"))
    elif not any(issue.level == "ERROR" for issue in issues):
        issues.append(Issue("PASS", "no blocking context errors"))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="project root (auto-discovered by default)")
    args = parser.parse_args()
    issues = validate_project(args.root)
    symbols = {"PASS": "✓ PASS", "WARNING": "⚠ WARNING", "ERROR": "✗ ERROR"}
    print("Agent Context Validation")
    print("─" * 32)
    for issue in issues:
        print(f"{symbols[issue.level]}  {issue.message}")
    return 1 if any(issue.level == "ERROR" for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
