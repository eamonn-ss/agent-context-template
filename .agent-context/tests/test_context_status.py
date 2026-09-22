from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from context_status import build_status
from helpers import write_valid_context


class ContextStatusTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        write_valid_context(self.root)

    def tearDown(self):
        self.temporary.cleanup()

    def test_status_is_friendly_outside_git(self):
        status = build_status(self.root)
        self.assertEqual(status["project"], "Demo")
        self.assertEqual(status["branch"], "Unavailable")
        self.assertEqual(status["context_health"], "WARNING")
        self.assertEqual(status["open_hypotheses"], 1)

    def test_status_reports_missing_handoff_as_error(self):
        (self.root / ".agent-context/state/HANDOFF.md").unlink()
        status = build_status(self.root)
        self.assertEqual(status["last_handoff"], "Missing")
        self.assertEqual(status["context_health"], "ERROR")


if __name__ == "__main__":
    unittest.main()
