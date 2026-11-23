#!/usr/bin/env python3
"""Bulletproof validator for the financial-statement-analysis Agent Skill.

Pure Python standard library — no third-party dependencies.

Checks:
  1. skill.md exists and opens with a YAML-style `---` frontmatter block.
  2. Frontmatter contains a non-empty `name:` field.
  3. Frontmatter contains a `description:` field of at least 40 characters.
  4. examples/ exists and contains at least one .md file.

Exit code 0 on success, 1 on any failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MIN_DESCRIPTION_CHARS = 40


def _repo_root() -> Path:
    # scripts/validate_skill.py -> repo root is the parent of scripts/
    return Path(__file__).resolve().parent.parent


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Extract a simple key: value frontmatter block delimited by --- lines."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("skill.md must start with a '---' frontmatter delimiter")

    fields: dict[str, str] = {}
    closed = False
    block_key = None  # key whose value is a `>` / `|` block scalar being read
    for line in lines[1:]:
        if line.strip() == "---":
            closed = True
            break
        if block_key and (line[:1] in (" ", "	") or not line.strip()):
            fields[block_key] = f"{fields[block_key]} {line.strip()}".strip()
            continue
        block_key = None
        if ":" in line:
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            if re.fullmatch(r"[>|][-+0-9]*", value):
                block_key, value = key, ""
            fields[key] = value

    if not closed:
        raise ValueError("frontmatter block is not closed with a second '---'")
    return fields


def main() -> int:
    root = _repo_root()
    errors: list[str] = []

    skill_path = root / "skill.md"
    if not skill_path.is_file():
        print(f"FAIL: missing {skill_path.name}", file=sys.stderr)
        return 1

    text = skill_path.read_text(encoding="utf-8")
    try:
        fields = _parse_frontmatter(text)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    name = fields.get("name", "")
    if not name:
        errors.append("frontmatter is missing a non-empty 'name:' field")

    description = fields.get("description", "")
    if len(description) < MIN_DESCRIPTION_CHARS:
        errors.append(
            f"frontmatter 'description:' must be >= {MIN_DESCRIPTION_CHARS} "
            f"chars (got {len(description)})"
        )

    examples_dir = root / "examples"
    if not examples_dir.is_dir():
        errors.append("missing examples/ directory")
    else:
        md_examples = list(examples_dir.glob("*.md"))
        if not md_examples:
            errors.append("examples/ must contain at least one .md file")

    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        return 1

    print("OK: skill.md frontmatter valid (name + description).")
    print(f"OK: name = {name!r}")
    print(f"OK: description length = {len(description)} chars.")
    print(f"OK: examples/ has {len(list(examples_dir.glob('*.md')))} markdown file(s).")
    print("validate_skill.py: all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
