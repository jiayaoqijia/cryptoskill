"""Tests for scripts/validate_skill.py. Run: python -m unittest discover tests"""

import importlib.util
import unittest
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "validate_skill.py"
_spec = importlib.util.spec_from_file_location("validate_skill", _SCRIPT)
validate_skill = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_skill)


class ParseFrontmatterTest(unittest.TestCase):
    def test_inline_values(self):
        fields = validate_skill._parse_frontmatter("---\nname: x\ndescription: hello\n---\n")
        self.assertEqual(fields["name"], "x")
        self.assertEqual(fields["description"], "hello")

    def test_folded_and_literal_block_descriptions(self):
        for indicator in (">", ">-", "|", "|-"):
            text = (
                "---\nname: x\n"
                f"description: {indicator}\n  First line of text,\n  second: line.\n"
                "version: 1.0.0\n---\n"
            )
            fields = validate_skill._parse_frontmatter(text)
            self.assertEqual(fields["description"], "First line of text, second: line.")
            self.assertEqual(fields["version"], "1.0.0")
            self.assertNotIn("second", fields)


if __name__ == "__main__":
    unittest.main()
