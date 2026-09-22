from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from context_start import detect_mode, project_state_initialized
from helpers import write_valid_context


class ContextStartTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        write_valid_context(self.root)

    def tearDown(self):
        self.temporary.cleanup()

    def _write_handoff(self, status: str = "Active") -> None:
        (self.root / ".agent-context/state/CURRENT_TASK.md").write_text(
            "# Current Task\n\n## Goal\n\nShip demo.\n\n## Status\n\n"
            f"{status}\n",
            encoding="utf-8",
        )
        (self.root / ".agent-context/state/HANDOFF.md").write_text(
            "# Session Handoff\n\n## Goal\n\nShip demo.\n\n"
            "## Next Steps\n\n- Continue implementation.\n",
            encoding="utf-8",
        )

    def test_project_init_detects_template_project_state(self):
        (self.root / ".agent-context/state/PROJECT.md").write_text(
            "# Project\n\n## Name\n\n<PROJECT_NAME>\n", encoding="utf-8"
        )
        self.assertFalse(project_state_initialized(self.root))

    def test_init_required_for_template_project_state(self):
        (self.root / ".agent-context/state/ARCHITECTURE.md").write_text(
            "# Architecture\n\nPLACEHOLDER\n", encoding="utf-8"
        )
        self.assertEqual(detect_mode(self.root)["mode"], "INIT_REQUIRED")

    def test_init_required_when_project_state_is_missing(self):
        (self.root / ".agent-context/state/PROJECT.md").unlink()
        self.assertEqual(detect_mode(self.root)["mode"], "INIT_REQUIRED")

    def test_bootstrap_without_active_handoff(self):
        self.assertEqual(detect_mode(self.root)["mode"], "BOOTSTRAP")

    def test_resume_with_active_task_and_usable_handoff(self):
        self._write_handoff()
        self.assertEqual(detect_mode(self.root)["mode"], "RESUME")

    def test_completed_task_does_not_resume(self):
        self._write_handoff(status="Done")
        self.assertEqual(detect_mode(self.root)["mode"], "BOOTSTRAP")

    def test_template_handoff_is_not_usable(self):
        self._write_handoff()
        (self.root / ".agent-context/state/HANDOFF.md").write_text(
            "# Session Handoff\n\n## Goal\n\n<GOAL>\n\n## Next Steps\n\n<NEXT_STEP>\n",
            encoding="utf-8",
        )
        result = detect_mode(self.root)
        self.assertFalse(result["usable_handoff"])
        self.assertEqual(result["mode"], "BOOTSTRAP")

    def test_template_current_task_is_not_active(self):
        self._write_handoff()
        (self.root / ".agent-context/state/CURRENT_TASK.md").write_text(
            "# Current Task\n\n## ID\n\nTASK-<NNN>\n\n"
            "## Goal\n\n<ONE_VERIFIABLE_OUTCOME>\n\n## Status\n\nActive\n",
            encoding="utf-8",
        )
        result = detect_mode(self.root)
        self.assertFalse(result["active_task"])
        self.assertEqual(result["mode"], "BOOTSTRAP")


if __name__ == "__main__":
    unittest.main()
