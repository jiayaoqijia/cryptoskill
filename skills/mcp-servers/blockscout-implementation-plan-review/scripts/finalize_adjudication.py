#!/usr/bin/env python3
"""Validate a finding adjudication report and generate or inspect its brief."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _adjudication_report import (
    BRIEF_NAME,
    ReportValidationError,
    parse_and_validate_report,
    render_brief,
    write_text_atomically,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--brief",
        type=Path,
        help=f"output path (default: sibling {BRIEF_NAME})",
    )
    action.add_argument(
        "--extract",
        metavar="SLUG",
        help="validate the report and print one section without its tags",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        report = parse_and_validate_report(args.report)
        if args.extract:
            try:
                section = report.section(args.extract)
            except KeyError:
                available = ", ".join(section.slug for section in report.sections)
                print(
                    f"ERROR unknown section slug {args.extract!r}; available: {available}",
                    file=sys.stderr,
                )
                return 2
            sys.stdout.write(section.content)
            return 0

        brief_path = (args.brief or report.path.with_name(BRIEF_NAME)).resolve()
        if brief_path.parent != report.path.parent:
            print(
                "ERROR brief must be a sibling of the full report",
                file=sys.stderr,
            )
            return 2
        write_text_atomically(brief_path, render_brief(report))
        print(f"OK brief={brief_path} source_sha256={report.sha256}")
        return 0
    except ReportValidationError as exc:
        print("ERROR invalid adjudication report:", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
