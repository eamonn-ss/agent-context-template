from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from collect_git_state import collect_git_state


class CollectGitStateTests(unittest.TestCase):
    def test_non_git_directory_is_reported_without_exception(self):
        with tempfile.TemporaryDirectory() as directory:
            state = collect_git_state(directory)
        self.assertFalse(state["is_git_repository"])
        self.assertEqual(state["modified_files"], [])
        self.assertIn("error", state)

    def test_empty_git_repository_and_untracked_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
            (root / "note.txt").write_text("hello", encoding="utf-8")
            state = collect_git_state(root)
        self.assertTrue(state["is_git_repository"])
        self.assertIsNone(state["head_commit"])
        self.assertEqual(state["recent_commits"], [])
        self.assertEqual(state["untracked_files"], ["note.txt"])

    def test_unstaged_status_preserves_leading_space_and_dot_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            path = root / ".cursor/rule.md"
            path.parent.mkdir()
            path.write_text("before", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", ".cursor/rule.md"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "initial"], check=True, capture_output=True)
            path.write_text("after", encoding="utf-8")
            state = collect_git_state(root)
        self.assertEqual(state["modified_files"], [".cursor/rule.md"])
        self.assertEqual(state["staged_files"], [])


if __name__ == "__main__":
    unittest.main()
