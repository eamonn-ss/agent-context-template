from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_context import validate_project
from helpers import write_valid_context


def errors(root):
    return [issue.message for issue in validate_project(root) if issue.level == "ERROR"]


class ValidateContextTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        write_valid_context(self.root)

    def tearDown(self):
        self.temporary.cleanup()

    def test_valid_project_has_no_errors(self):
        self.assertEqual(errors(self.root), [])

    def test_missing_handoff_is_an_error(self):
        (self.root / ".agent/HANDOFF.md").unlink()
        self.assertTrue(any("HANDOFF.md" in message for message in errors(self.root)))

    def test_duplicate_decision_id_is_an_error(self):
        decisions = self.root / ".agent/decisions"
        decisions.mkdir()
        (decisions / "one.md").write_text("# DEC-0001: One\n", encoding="utf-8")
        (decisions / "two.md").write_text("# DEC-0001: Two\n", encoding="utf-8")
        self.assertTrue(any("duplicate decision ID DEC-0001" in message for message in errors(self.root)))

    def test_fact_without_evidence_is_an_error(self):
        (self.root / ".agent/memory/FACTS.md").write_text(
            "# Facts\n\n## F-002\n\n### Statement\n\nClaim.\n\n### Status\n\nVerified\n",
            encoding="utf-8",
        )
        self.assertTrue(any("F-002 is missing Evidence" in message for message in errors(self.root)))

    def test_fact_with_empty_evidence_fields_is_an_error(self):
        (self.root / ".agent/memory/FACTS.md").write_text(
            "# Facts\n\n## F-003\n\n### Statement\n\nClaim.\n\n"
            "### Evidence\n\n- file:\n- test:\n\n### Status\n\nVerified\n",
            encoding="utf-8",
        )
        self.assertTrue(any("F-003 is missing Evidence" in message for message in errors(self.root)))

    def test_missing_handoff_reference_is_an_error(self):
        (self.root / ".agent/HANDOFF.md").write_text(
            "# Handoff\n\nEvidence file: missing.txt\n", encoding="utf-8"
        )
        self.assertTrue(any("missing.txt" in message for message in errors(self.root)))


if __name__ == "__main__":
    unittest.main()
