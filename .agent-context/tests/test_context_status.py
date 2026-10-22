from __future__ import annotations

import subprocess
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
        self.assertEqual(status["freshness"], "unknown")
        self.assertEqual(status["context_health"], "WARNING")
        self.assertEqual(status["open_hypotheses"], 1)

    def test_status_reports_missing_handoff_as_error(self):
        (self.root / ".agent-context/state/HANDOFF.md").unlink()
        status = build_status(self.root)
        self.assertEqual(status["handoff_action"], "Missing")
        self.assertEqual(status["context_health"], "ERROR")

    def test_handoff_action_is_the_first_line_only(self):
        (self.root / ".agent-context/state/HANDOFF.md").write_text(
            "# Session Handoff\n\n"
            "## Completed\n\n"
            "Moved every framework directory and rewrote the protocol.\n\n"
            "## Suggested First Action\n\n"
            "Exercise the V2.1 migration on a real consumer.\n"
            "- Then plan retrieval.\n",
            encoding="utf-8",
        )
        status = build_status(self.root)
        self.assertEqual(
            status["handoff_action"],
            "Exercise the V2.1 migration on a real consumer.",
        )
        self.assertNotIn("Moved every", status["handoff_action"])

    def test_git_repo_without_recorded_evidence_is_stale(self):
        self._commit_base()
        status = build_status(self.root)
        self.assertEqual(status["freshness"], "stale")
        self.assertEqual(status["context_health"], "WARNING")
        self.assertIn("record", status["freshness_reason"].lower())

    def test_matching_git_evidence_is_current(self):
        sha = self._commit_base()
        self._write_evidence(sha, "dirty", "Commit the release notes.")
        status = build_status(self.root)
        self.assertEqual(status["freshness"], "current")
        self.assertEqual(status["context_health"], "GOOD")

    def test_worktree_state_mismatch_is_stale(self):
        sha = self._commit_base()
        self._write_evidence(sha, "clean")
        status = build_status(self.root)
        self.assertEqual(status["freshness"], "stale")
        self.assertIn("did not record", status["freshness_reason"].lower())

    def test_committing_the_recorded_snapshot_stays_current(self):
        sha = self._commit_base()
        self._write_evidence(sha, "dirty")
        self._git("add", ".")
        self._git("commit", "-m", "handoff")
        status = build_status(self.root)
        self.assertEqual(status["freshness"], "current")

    def test_later_commit_without_new_evidence_is_stale(self):
        sha = self._commit_base()
        self._write_evidence(sha, "dirty")
        self._git("add", ".")
        self._git("commit", "-m", "handoff")
        (self.root / "note.txt").write_text("later\n", encoding="utf-8")
        self._git("add", "note.txt")
        self._git("commit", "-m", "later")
        status = build_status(self.root)
        self.assertEqual(status["freshness"], "stale")

    def test_done_when_without_command_and_result_is_stale(self):
        sha = self._commit_base()
        self._write_task("Done", "tests passed", "None")
        self._write_evidence(sha, "dirty")
        status = build_status(self.root)
        self.assertEqual(status["freshness"], "stale")
        self.assertIn("Done when", status["freshness_reason"])

    def test_finished_task_with_future_action_stays_current(self):
        sha = self._commit_base()
        self._write_task(
            "Done",
            "`python -m unittest discover -s .agent-context/tests -v` exits 0.",
            "Exercise the migration on a real consumer.",
        )
        self._write_evidence(sha, "dirty")
        status = build_status(self.root)
        self.assertEqual(status["freshness"], "current")

    def test_finished_task_asking_to_commit_on_clean_tree_is_stale(self):
        sha = self._commit_base()
        self._write_task(
            "Done",
            "`python -m unittest discover -s tests -v` exits 0.",
            "Review and commit the upgrade.",
        )
        self._write_evidence(sha, "dirty")
        self._git("add", ".")
        self._git("commit", "-m", "handoff")
        status = build_status(self.root)
        self.assertEqual(status["freshness"], "stale")
        self.assertIn("commit", status["freshness_reason"].lower())

    def test_dirty_handoff_listing_absent_file_is_stale(self):
        sha = self._commit_base()
        self._write_task(
            "Ready",
            "",
            "None",
        )
        (self.root / "note.txt").write_text("changed\n", encoding="utf-8")
        handoff = (
            "# Session Handoff\n\n## Git Evidence\n\n"
            f"- commit: {sha}\n- worktree: dirty\n\n"
            "## Modified Files\n\n- missing.txt\n\n"
            "## Suggested First Action\n\nNone\n"
        )
        (self.root / ".agent-context/state/HANDOFF.md").write_text(handoff, encoding="utf-8")
        status = build_status(self.root)
        self.assertEqual(status["freshness"], "stale")
        self.assertIn("modified files", status["freshness_reason"].lower())

    def test_dirty_handoff_directory_prefix_matches_git_status(self):
        sha = self._commit_base()
        self._write_task("Ready", "", "None")
        note = self.root / "notes" / "a.txt"
        note.parent.mkdir()
        note.write_text("changed\n", encoding="utf-8")
        handoff = (
            "# Session Handoff\n\n## Git Evidence\n\n"
            f"- commit: {sha}\n- worktree: dirty\n\n"
            "## Modified Files\n\n- notes/\n\n"
            "## Suggested First Action\n\nNone\n"
        )
        (self.root / ".agent-context/state/HANDOFF.md").write_text(handoff, encoding="utf-8")
        status = build_status(self.root)
        self.assertEqual(status["freshness"], "current")

    def _write_task(self, status: str, done_when: str, next_action: str) -> None:
        (self.root / ".agent-context/state/CURRENT_TASK.md").write_text(
            "# Current Task\n\n## Goal\n\nShip demo.\n\n"
            f"## Status\n\n{status}\n\n## Done when\n\n{done_when}\n\n"
            f"## Next Action\n\n{next_action}\n",
            encoding="utf-8",
        )

    def _git(self, *args: str) -> None:
        subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def _commit_base(self) -> str:
        subprocess.run(["git", "init", str(self.root)], check=True, capture_output=True)
        self._git("config", "user.email", "test@example.com")
        self._git("config", "user.name", "Test")
        self._git("add", ".")
        self._git("commit", "-m", "base")
        return subprocess.check_output(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"],
            text=True,
        ).strip()

    def _write_evidence(self, commit: str, worktree: str, action: str = "None") -> None:
        (self.root / ".agent-context/state/HANDOFF.md").write_text(
            "# Session Handoff\n\n## Git Evidence\n\n"
            f"- commit: {commit}\n- worktree: {worktree}\n\n"
            "## Suggested First Action\n\n"
            f"{action}\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
