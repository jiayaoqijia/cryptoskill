import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_skill.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_skill", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


VALID_BODY = """---
name: sample-skill
description: Use when reviewing a cryptographic claim for correctness and evidence quality.
---

# Sample Skill

## Scope
In scope: review a supplied claim. Out of scope: invent missing evidence.

## Required Inputs
The claim and its cited source.

## Success Criteria
Return a claim classification, evidence assessment, and uncertainty statement.

## Failure Modes
Stop when the source or claim text is unavailable.

## Workflow
Classify the claim, inspect evidence, and report limitations.
"""


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_skill(self, folder_name="sample-skill", body=VALID_BODY):
        skill_dir = self.root / folder_name
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
        return skill_dir

    def test_accepts_valid_skill(self):
        report = self.validator.validate_skill(self.write_skill())
        self.assertTrue(report.ok, report.format_text())

    def test_rejects_missing_frontmatter(self):
        report = self.validator.validate_skill(
            self.write_skill(body="# Sample\n\nNo frontmatter.")
        )
        self.assertFalse(report.ok)
        self.assertIn("frontmatter", report.format_text().lower())

    def test_rejects_folder_name_mismatch(self):
        report = self.validator.validate_skill(self.write_skill(folder_name="other-name"))
        self.assertFalse(report.ok)
        self.assertIn("folder", report.format_text().lower())

    def test_rejects_non_discriminating_description(self):
        body = VALID_BODY.replace(
            "Use when reviewing a cryptographic claim for correctness and evidence quality.",
            "Helps with research.",
        )
        report = self.validator.validate_skill(self.write_skill(body=body))
        self.assertFalse(report.ok)
        self.assertIn("use when", report.format_text().lower())

    def test_rejects_missing_contract_section(self):
        body = VALID_BODY.replace("## Failure Modes", "## Limitations")
        report = self.validator.validate_skill(self.write_skill(body=body))
        self.assertFalse(report.ok)
        self.assertIn("failure modes", report.format_text().lower())


if __name__ == "__main__":
    unittest.main()
