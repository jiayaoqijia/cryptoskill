#!/usr/bin/env python3
"""Validate a timestamped implementation-plan review comments export."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BEGIN_RE = re.compile(r'^<!-- comment:begin slug="([a-z0-9]+(?:-[a-z0-9]+)*)" -->$')
END_RE = re.compile(r'^<!-- comment:end slug="([a-z0-9]+(?:-[a-z0-9]+)*)" -->$')
NUMBER_RE = re.compile(r"^(\d+)\.\s+\S")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Markdown export to validate.")
    parser.add_argument(
        "--expected-count",
        type=int,
        help="Require exactly this many comment blocks.",
    )
    return parser.parse_args()


def validate(path: Path, expected_count: int | None) -> list[str]:
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [f"cannot read {path}: {exc}"]

    blocks: list[tuple[str, int, list[str]]] = []
    seen_slugs: set[str] = set()
    active_slug: str | None = None
    active_start = 0
    active_body: list[str] = []

    for line_number, line in enumerate(lines, start=1):
        begin_match = BEGIN_RE.fullmatch(line)
        end_match = END_RE.fullmatch(line)

        if begin_match:
            slug = begin_match.group(1)
            if active_slug is not None:
                errors.append(f"line {line_number}: nested begin for {slug!r} inside {active_slug!r}")
                continue
            if slug in seen_slugs:
                errors.append(f"line {line_number}: duplicate slug {slug!r}")
            seen_slugs.add(slug)
            active_slug = slug
            active_start = line_number
            active_body = []
            continue

        if end_match:
            slug = end_match.group(1)
            if active_slug is None:
                errors.append(f"line {line_number}: end marker for {slug!r} has no begin")
                continue
            if slug != active_slug:
                errors.append(f"line {line_number}: end slug {slug!r} does not match {active_slug!r}")
            blocks.append((active_slug, active_start, active_body))
            active_slug = None
            active_start = 0
            active_body = []
            continue

        if active_slug is None:
            if line.strip():
                errors.append(f"line {line_number}: nonblank content outside a comment block")
        else:
            active_body.append(line)

    if active_slug is not None:
        errors.append(f"line {active_start}: comment {active_slug!r} has no end marker")

    if expected_count is not None and expected_count < 0:
        errors.append("--expected-count must be non-negative")
    elif expected_count is not None and len(blocks) != expected_count:
        errors.append(f"expected {expected_count} comment blocks, found {len(blocks)}")

    for index, (slug, start, body) in enumerate(blocks, start=1):
        first_content = next((line for line in body if line.strip()), None)
        if first_content is None:
            errors.append(f"line {start}: comment {slug!r} is empty")
            continue
        number_match = NUMBER_RE.match(first_content)
        if number_match is None:
            errors.append(f"line {start}: first content in comment {slug!r} must retain list numbering")
            continue
        number = int(number_match.group(1))
        if number != index:
            errors.append(f"line {start}: comment {slug!r} is numbered {number}, expected {index}")

    if not blocks and not errors:
        errors.append("no comment blocks found")

    return errors


def main() -> int:
    args = parse_args()
    errors = validate(args.path, args.expected_count)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    block_count = sum(1 for line in args.path.read_text(encoding="utf-8").splitlines() if BEGIN_RE.fullmatch(line))
    print(f"OK comments={block_count} path={args.path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
