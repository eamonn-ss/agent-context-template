from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ReadmeTests(unittest.TestCase):
    def test_english_readme_links_chinese_readme(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn('href="./README.zh-CN.md"', text)

    def test_chinese_readme_links_english_readme(self):
        text = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn('href="./README.md"', text)

    def test_readmes_have_matching_numbered_sections(self):
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        for number in range(1, 17):
            self.assertIn(f"## {number}.", english)
            self.assertIn(f"## {number}.", chinese)

    def test_namespace_and_profiles_are_documented(self):
        for name in ("README.md", "README.zh-CN.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn(".agent-context/", text)
            self.assertIn("Namespace Isolation", text)
            self.assertIn("Development vs Embedded Profile", text)


if __name__ == "__main__":
    unittest.main()
