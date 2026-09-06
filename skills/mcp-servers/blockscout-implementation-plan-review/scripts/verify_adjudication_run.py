#!/usr/bin/env python3
"""Independently verify every completed finding adjudication in a run."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _adjudication_report import (
    BRIEF_NAME,
    REPORT_NAME,
    ReportValidationError,
    expected_candidate_files,
    parse_and_validate_report,
    render_brief,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--expected-count", type=int)
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    run_dir = args.run.resolve()
    if not run_dir.is_dir():
        print(f"ERROR run directory does not exist: {run_dir}", file=sys.stderr)
        return 2

    candidate_dirs = sorted(path for path in run_dir.iterdir() if path.is_dir() and path.name.startswith("finding-"))
    errors: list[str] = []
    if not candidate_dirs:
        errors.append(f"no finding-* candidate directories found below {run_dir}")
    if args.expected_count is not None and len(candidate_dirs) != args.expected_count:
        errors.append(f"expected {args.expected_count} candidate directories, found {len(candidate_dirs)}")

    summaries: list[str] = []
    completed_reports = 0
    for candidate_dir in candidate_dirs:
        report_path = candidate_dir / REPORT_NAME
        relative = candidate_dir.relative_to(run_dir)
        if not report_path.is_file():
            errors.append(f"{relative}: missing {REPORT_NAME}")
            continue
        completed_reports += 1
        try:
            report = parse_and_validate_report(report_path)
        except ReportValidationError as exc:
            errors.extend(f"{relative}: {message}" for message in exc.errors)
            continue
        except OSError as exc:
            errors.append(f"{relative}: {exc}")
            continue

        actual_entries = {path.name for path in candidate_dir.iterdir()}
        expected_files = expected_candidate_files()
        if actual_entries != expected_files:
            errors.append(
                f"{relative}: candidate entries must be exactly "
                f"{sorted(expected_files)!r}, got {sorted(actual_entries)!r}"
            )

        brief_path = candidate_dir / BRIEF_NAME
        if not brief_path.is_file():
            errors.append(f"{relative}: missing {BRIEF_NAME}")
        elif brief_path.is_symlink():
            errors.append(f"{relative}: {BRIEF_NAME} must not be a symbolic link")
        else:
            expected_brief = render_brief(report)
            try:
                actual_brief = brief_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                errors.append(f"{relative}: cannot read {BRIEF_NAME}: {exc}")
            else:
                if actual_brief != expected_brief:
                    errors.append(f"{relative}: {BRIEF_NAME} is stale or was edited; rerun finalize_adjudication.py")

        summaries.append(
            f"{relative}: disposition={report.result['disposition']} "
            f"severity={report.result['severity']} "
            f"confidence={report.result['confidence']} "
            f"sha256={report.sha256}"
        )

    if errors:
        print("ERROR adjudication run validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"OK reports={completed_reports} run={run_dir}")
    for summary in summaries:
        print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
