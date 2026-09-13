#!/usr/bin/env python3
"""Generate CHANGELOG.md from git history since the last tag."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict

CATEGORIES = {
    "feat": "Added",
    "fix": "Fixed",
    "refactor": "Changed",
    "chore": "Changed",
    "docs": "Changed",
    "perf": "Changed",
    "style": "Changed",
    "test": "Changed",
    "build": "Changed",
    "ci": "Changed",
    "revert": "Removed",
    "remove": "Removed",
    "delete": "Removed",
}

CONVENTIONAL = re.compile(r"^(?P<type>[a-zA-Z]+)(?:\([^)]+\))?!?:\s*(?P<msg>.+)$")


def git(*args: str) -> str:
    p = subprocess.run(["git", *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr.strip() or f"git {' '.join(args)} failed")
    return p.stdout.strip()


def last_tag() -> str:
    p = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True,
        text=True,
    )
    if p.returncode == 0:
        return p.stdout.strip()
    return ""


def commits_since(tag: str) -> list[str]:
    if tag:
        out = git("log", f"{tag}..HEAD", "--pretty=format:%s")
    else:
        out = git("log", "--pretty=format:%s")
    return [line.strip() for line in out.splitlines() if line.strip()]


def classify(subject: str) -> tuple[str, str]:
    m = CONVENTIONAL.match(subject)
    if not m:
        return "Changed", subject
    ctype = m.group("type").lower()
    msg = m.group("msg").strip()
    return CATEGORIES.get(ctype, "Changed"), msg


def build(tag: str, commits: list[str]) -> str:
    buckets: dict[str, list[str]] = defaultdict(list)
    for c in commits:
        cat, msg = classify(c)
        buckets[cat].append(msg)
    header = f"## {tag}..HEAD" if tag else "## Unreleased"
    lines = [header, ""]
    for cat in ("Added", "Fixed", "Changed", "Removed"):
        items = buckets.get(cat) or []
        if not items:
            continue
        lines.append(f"### {cat}")
        lines.extend(f"- {i}" for i in items)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stdout", action="store_true", help="Print instead of writing CHANGELOG.md")
    ap.add_argument("--out", default="CHANGELOG.md", help="Output path")
    args = ap.parse_args()
    tag = last_tag()
    commits = commits_since(tag)
    if not commits:
        print("No commits since last tag.", file=sys.stderr)
        sys.exit(0)
    text = build(tag, commits)
    if args.stdout:
        print(text)
    else:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote {args.out} ({len(commits)} commits)")


if __name__ == "__main__":
    main()
