#!/usr/bin/env python3
"""Portable structural validator for Agent Skills-style directories."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, NamedTuple


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_HEADINGS = (
    "scope",
    "required inputs",
    "success criteria",
    "failure modes",
    "workflow",
)


class Issue(NamedTuple):
    severity: str
    message: str


class Report:
    def __init__(self, path: Path, issues: List[Issue]):
        self.path = path
        self.issues = issues

    @property
    def ok(self) -> bool:
        return not any(issue.severity == "ERROR" for issue in self.issues)

    def format_text(self) -> str:
        status = "PASS" if self.ok else "FAIL"
        lines = [f"{status}: {self.path}"]
        if not self.issues:
            lines.append("  No structural findings.")
        else:
            lines.extend(
                f"  [{issue.severity}] {issue.message}" for issue in self.issues
            )
        return "\n".join(lines)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | tuple[None, None]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, None

    fields: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in {"name", "description"}:
            fields[key] = value
    return fields, text[match.end() :]


def normalized_headings(body: str) -> set[str]:
    headings = set()
    for line in body.splitlines():
        match = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if match:
            headings.add(match.group(1).strip().lower())
    return headings


def validate_links(skill_dir: Path, body: str) -> List[Issue]:
    issues: List[Issue] = []
    for destination in LINK_RE.findall(body):
        destination = destination.strip()
        if destination.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative = destination.split("#", 1)[0]
        if not relative:
            continue
        if re.match(r"^[A-Za-z]:[\\/]", relative) or relative.startswith(("/", "~")):
            issues.append(Issue("ERROR", f"Non-portable absolute link: {destination}"))
            continue
        if not (skill_dir / relative).exists():
            issues.append(Issue("ERROR", f"Broken relative link: {destination}"))
    return issues


def validate_skill(path: str | Path) -> Report:
    skill_dir = Path(path).resolve()
    issues: List[Issue] = []
    skill_file = skill_dir / "SKILL.md"

    if not skill_dir.is_dir():
        return Report(skill_dir, [Issue("ERROR", "Skill path is not a directory.")])
    if not skill_file.is_file():
        return Report(skill_dir, [Issue("ERROR", "SKILL.md is missing.")])

    try:
        text = skill_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return Report(skill_dir, [Issue("ERROR", "SKILL.md is not UTF-8 text.")])

    fields, body = parse_frontmatter(text)
    if fields is None:
        return Report(skill_dir, [Issue("ERROR", "YAML frontmatter is missing or malformed.")])

    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        issues.append(Issue("ERROR", "Frontmatter field 'name' is missing."))
    elif not NAME_RE.fullmatch(name) or len(name) > 64:
        issues.append(
            Issue("ERROR", "Name must be lowercase hyphen-case and at most 64 characters.")
        )
    elif name != skill_dir.name:
        issues.append(
            Issue("ERROR", f"Frontmatter name '{name}' does not match folder '{skill_dir.name}'.")
        )

    if not description:
        issues.append(Issue("ERROR", "Frontmatter field 'description' is missing."))
    else:
        if not description.startswith("Use when "):
            issues.append(Issue("ERROR", "Description must start with 'Use when '."))
        if len(description) > 1024:
            issues.append(Issue("ERROR", "Description exceeds 1024 characters."))

    headings = normalized_headings(body or "")
    for required in REQUIRED_HEADINGS:
        if required not in headings:
            issues.append(Issue("ERROR", f"Required section is missing: {required.title()}."))

    if body is not None:
        issues.extend(validate_links(skill_dir, body))
        if "[[" in body or "]]" in body:
            issues.append(Issue("ERROR", "SKILL.md contains unresolved scaffold tokens."))

    return Report(skill_dir, issues)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python validate_skill.py PATH/TO/SKILL", file=sys.stderr)
        return 2
    report = validate_skill(argv[1])
    print(report.format_text())
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
