from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from compact_sessions import apply_plan, compaction_plan

class CompactSessionsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.sessions = self.root / ".agent-context/sessions"
        self.sessions.mkdir(parents=True)

    def tearDown(self):
        self.temporary.cleanup()

    def test_compaction_only_selects_old_ready_sessions(self):
        (self.sessions / "2026-01-01-01.md").write_text("**Compaction:** Ready\n", encoding="utf-8")
        (self.sessions / "2026-01-02-01.md").write_text("**Compaction:** Keep\n", encoding="utf-8")
        (self.sessions / "2026-01-03-01.md").write_text("**Compaction:** Ready\n", encoding="utf-8")
        plan = compaction_plan(self.root, keep=1)
        self.assertEqual(plan["archive"], ["2026-01-01-01.md"])
        self.assertEqual(plan["skipped_not_ready"], ["2026-01-02-01.md"])
        self.assertEqual(plan["protected_recent"], ["2026-01-03-01.md"])

    def test_apply_moves_without_deleting_summary(self):
        name = "2026-01-01-01.md"
        (self.sessions / name).write_text("**Compaction:** Ready\n", encoding="utf-8")
        plan = compaction_plan(self.root, keep=0)
        moved = apply_plan(self.root, plan)
        self.assertEqual(moved, [name])
        self.assertFalse((self.sessions / name).exists())
        self.assertTrue((self.root / ".agent-context/archive" / name).is_file())


if __name__ == "__main__":
    unittest.main()
