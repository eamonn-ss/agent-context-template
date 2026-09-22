from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / ".agent-context/scripts"
sys.path.insert(0, str(SCRIPTS))

from context_paths import find_context_root, find_project_root
from migrate_v21_to_v22 import apply_migration, conflicts, migration_plan


class ContextRootDiscoveryTests(unittest.TestCase):
    def test_discovery_walks_up_from_nested_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".agent-context").mkdir()
            nested = root / "src/package/module"
            nested.mkdir(parents=True)
            self.assertEqual(find_context_root(nested), root / ".agent-context")
            self.assertEqual(find_project_root(nested), root)


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        project = self.root / ".agent/PROJECT.md"
        project.parent.mkdir()
        project.write_text("# Project\n\nLegacy\n", encoding="utf-8")
        memory = self.root / ".agent/memory/FACTS.md"
        memory.parent.mkdir()
        memory.write_text("# Facts\n", encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def test_dry_run_reports_plan_without_changes(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPTS / "migrate_v21_to_v22.py"), "--root", str(self.root), "--dry-run"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertIn("DRY RUN", completed.stdout)
        self.assertTrue((self.root / ".agent/PROJECT.md").is_file())
        self.assertFalse((self.root / ".agent-context/state/PROJECT.md").exists())

    def test_success_moves_legacy_state_once(self):
        plan = migration_plan(self.root)
        self.assertEqual(conflicts(plan), [])
        apply_migration(self.root, plan)
        self.assertFalse((self.root / ".agent").exists())
        self.assertTrue((self.root / ".agent-context/state/PROJECT.md").is_file())
        self.assertTrue((self.root / ".agent-context/memory/FACTS.md").is_file())
        self.assertEqual((self.root / ".agent-context/VERSION").read_text(), "2.2.0\n")

    def test_conflict_is_detected_before_any_move(self):
        destination = self.root / ".agent-context/state/PROJECT.md"
        destination.parent.mkdir(parents=True)
        destination.write_text("# Different\n", encoding="utf-8")
        plan = migration_plan(self.root)
        self.assertEqual(len(conflicts(plan)), 1)
        self.assertTrue((self.root / ".agent/PROJECT.md").is_file())


class EmbeddedInstallationTests(unittest.TestCase):
    def test_business_directories_and_existing_agents_file_are_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "sample-project"
            originals = {
                "docs/business.md": "business docs\n",
                "scripts/deploy.sh": "business script\n",
                "tests/test_product.py": "business test\n",
                "AGENTS.md": "business agent rules\n",
            }
            for relative, content in originals.items():
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            completed = subprocess.run(
                ["bash", str(SCRIPTS / "init-ai-context.sh"), str(target)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            for relative, content in originals.items():
                self.assertEqual((target / relative).read_text(encoding="utf-8"), content)
            self.assertTrue((target / ".agents/skills/context-start/SKILL.md").is_file())
            self.assertTrue((target / ".agent-context/state/PROJECT.md").is_file())
            self.assertTrue((target / ".agent-context/scripts/context_paths.py").is_file())
            self.assertFalse((target / ".git").exists())
            self.assertFalse((target / ".agent-context/tests").exists())

            routed = subprocess.run(
                [sys.executable, str(target / ".agent-context/scripts/context_start.py"), "--root", str(target)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(routed.returncode, 0, routed.stderr)
            self.assertIn("Mode: INIT_REQUIRED", routed.stdout)

    def test_dry_run_creates_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "preview"
            completed = subprocess.run(
                ["bash", str(SCRIPTS / "init-ai-context.sh"), "--dry-run", str(target)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertFalse(target.exists())


class SkillIsolationTests(unittest.TestCase):
    def test_all_skills_use_namespaced_canonical_paths(self):
        for skill in sorted((ROOT / ".agents/skills").glob("*/SKILL.md")):
            text = skill.read_text(encoding="utf-8")
            self.assertNotIn("`.agent/", text, skill.name)
        project_init = (ROOT / ".agents/skills/project-init/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Always exclude `.agent-context/`, `.agents/`", project_init)


if __name__ == "__main__":
    unittest.main()
