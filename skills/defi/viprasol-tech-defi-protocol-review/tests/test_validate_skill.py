"""Tests for scripts/validate_skill.py. Run: python -m unittest discover tests"""

import importlib.util
import unittest
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "validate_skill.py"
_spec = importlib.util.spec_from_file_location("validate_skill", _SCRIPT)
validate_skill = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_skill)


def _fields(name_value: str) -> dict:
    return validate_skill._parse_frontmatter(f"---\nname: {name_value}\n---\n")


class ParseFrontmatterTest(unittest.TestCase):
    def test_plain_value_is_kept(self):
        self.assertEqual(_fields("defi-protocol-review")["name"], "defi-protocol-review")

    def test_quoted_value_is_unquoted(self):
        self.assertEqual(_fields('"my-skill"')["name"], "my-skill")
        self.assertEqual(_fields("'my-skill'")["name"], "my-skill")

    def test_empty_quoted_value_is_empty(self):
        for empty in ('""', "''", '" "'):
            self.assertEqual(_fields(empty)["name"], "")

    def test_inner_or_unbalanced_quotes_are_kept(self):
        self.assertEqual(_fields('say "hi" now')["name"], 'say "hi" now')
        self.assertEqual(_fields('"open')["name"], '"open')


if __name__ == "__main__":
    unittest.main()
