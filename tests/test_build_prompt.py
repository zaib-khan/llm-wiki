"""Checks for content preservation and refusal to publish incomplete sources."""

from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
BUILD = runpy.run_path(str(ROOT / "scripts/build_prompt.py"))


class PromptBuildTests(unittest.TestCase):
    def test_fenced_headings_are_preserved_as_content(self):
        text = ("Introduction\n\n## 1. First\n\n```markdown\n## 99. Example\n"
                "### 9.8 Example\n```\n\n~~~\n## 2. Also an example\n~~~\n"
                "\n## 3. Last\nFin — é\n")
        sections = BUILD["split_sections"](text)
        self.assertEqual(list(sections), ["intro", "1", "3"])
        self.assertEqual("".join(sections.values()), text)

    def test_duplicate_section_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate section"):
            BUILD["split_sections"]("## 1. First\n## 1. Duplicate\n")

    def test_unclosed_fence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unclosed code fence"):
            BUILD["split_sections"]("## 1. First\n```\nExample\n")

    def test_missing_section_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "prompt", root / "prompt")
            (root / "prompt/02-structure.md").write_text("## 5. Architecture\n")
            with self.assertRaisesRegex(ValueError, "missing sections.*6"):
                BUILD["assemble"](root)

    def test_cli_check_does_not_overwrite_stale_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "prompt", root / "prompt")
            (root / "scripts").mkdir()
            script = root / "scripts/build_prompt.py"
            shutil.copyfile(ROOT / "scripts/build_prompt.py", script)
            output = root / BUILD["OUTPUT"]
            output.write_bytes(b"Existing content\n")
            command = [sys.executable, str(script)]
            checked = subprocess.run(command + ["--check"], capture_output=True)
            self.assertEqual(checked.returncode, 1)
            self.assertEqual(output.read_bytes(), b"Existing content\n")
            built = subprocess.run(command, capture_output=True)
            self.assertEqual(built.returncode, 0, built.stderr)
            self.assertEqual(output.read_bytes(), (ROOT / BUILD["OUTPUT"]).read_bytes())
            checked = subprocess.run(command + ["--check"], capture_output=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)


if __name__ == "__main__":
    unittest.main()
