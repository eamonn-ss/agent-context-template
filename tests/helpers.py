from __future__ import annotations

from pathlib import Path


def write_valid_context(root: Path) -> None:
    files = {
        ".agent/PROJECT.md": "# Project\n\n## Name\n\nDemo\n",
        ".agent/ARCHITECTURE.md": "# Architecture\n\nCurrent design.\n",
        ".agent/CURRENT_TASK.md": "# Current Task\n\n## Goal\n\nShip demo.\n\n## Status\n\nReady\n",
        ".agent/DECISIONS.md": "# Decision Index\n\nNo decisions.\n",
        ".agent/HANDOFF.md": "# Session Handoff\n\n## Completed\n\nNone yet.\n",
        ".agent/TODO.md": "# Roadmap\n\nNo planned work.\n",
        ".agent/memory/FACTS.md": (
            "# Facts\n\n## F-001\n\n### Statement\n\nIt works.\n\n"
            "### Evidence\n\n- test: unit suite\n\n### Status\n\nVerified\n"
        ),
        ".agent/memory/HYPOTHESES.md": (
            "# Hypotheses\n\n## H-001\n\n### Hypothesis\n\nMaybe.\n\n"
            "### Evidence\n\nNone yet.\n\n### Validation\n\nTest it.\n\n"
            "### Status\n\nOpen\n"
        ),
        ".agent/memory/DISCOVERIES.md": "# Discoveries\n\nNone.\n",
    }
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
