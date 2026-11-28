"""Tests for scripts/validate_skill.py. Run: python -m unittest discover -s tests"""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import validate_skill  # noqa: E402

GOOD_DESCRIPTION = "Review a wallet signature request and return a sign / don't-sign verdict."


def _run(name: str, description: str) -> int:
    """Run the validator against a throwaway skill with the given raw field values."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "skill.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n# Skill\n",
            encoding="utf-8",
        )
        (root / "examples").mkdir()
        (root / "examples" / "example.md").write_text("# Example\n", encoding="utf-8")
        with mock.patch.object(validate_skill, "_repo_root", return_value=root):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return validate_skill.main()


class QuotedFrontmatterTest(unittest.TestCase):
    def test_plain_values_pass(self):
        self.assertEqual(_run("my-skill", GOOD_DESCRIPTION), 0)

    def test_quoted_values_pass(self):
        self.assertEqual(_run('"my-skill"', f'"{GOOD_DESCRIPTION}"'), 0)

    def test_quoted_empty_name_is_rejected(self):
        self.assertEqual(_run('""', GOOD_DESCRIPTION), 1)
        self.assertEqual(_run("''", GOOD_DESCRIPTION), 1)

    def test_quotes_do_not_count_toward_description_length(self):
        short = "x" * (validate_skill.MIN_DESCRIPTION_CHARS - 2)
        self.assertEqual(_run("my-skill", f'"{short}"'), 1)


if __name__ == "__main__":
    unittest.main()
