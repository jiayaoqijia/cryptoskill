"""Summarize node liveness, crash markers, and extra log matches for a run.

Use this after Workflow B runs to collect a quick process-and-log overview
before digging through individual validator logs by hand.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from ton_triage_lib import resolve_path


DEFAULT_PATTERN_LABELS = [
    r"Signal:",
    r"\bFATAL\b",
    r"\bCHECK\b",
    r"\babort\b",
    r"\bterminate(?:d|s|ing)?\b",
]
DEFAULT_PATTERNS = [re.compile(pattern) for pattern in DEFAULT_PATTERN_LABELS]


def _tail_lines(path: Path, *, limit: int = 20) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(errors="ignore").splitlines()
    return lines[-limit:]


def _matching_lines(
    path: Path,
    patterns: list[re.Pattern[str]],
    *,
    limit: int = 50,
) -> list[dict[str, object]]:
    if not path.exists():
        return []
    matches: list[dict[str, object]] = []
    for number, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
        if any(pattern.search(line) for pattern in patterns):
            matches.append({"line": number, "text": line})
            if len(matches) >= limit:
                break
    return matches


def _validator_processes() -> list[tuple[int, str]]:
    completed = subprocess.run(
        ["ps", "-axo", "pid=,args="],
        check=True,
        text=True,
        capture_output=True,
    )
    result: list[tuple[int, str]] = []
    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        pid_raw, _, args = line.partition(" ")
        if not args or "validator-engine" not in args:
            continue
        try:
            pid = int(pid_raw)
        except ValueError:
            continue
        result.append((pid, args))
    return result


def _node_status(node_dir: Path, processes: list[tuple[int, str]]) -> tuple[str, list[int]]:
    config_json = str((node_dir / "config.json").resolve())
    global_config = str((node_dir / "config.global.json").resolve())
    matches = [
        pid
        for pid, args in processes
        if config_json in args or global_config in args
    ]
    if len(matches) == 1:
        return "running", matches
    if len(matches) > 1:
        return "ambiguous", matches
    return "stopped", []


def _node_summary(
    node_dir: Path,
    default_patterns: list[re.Pattern[str]],
    extra_patterns: list[str],
    processes: list[tuple[int, str]],
) -> dict[str, object]:
    log_path = node_dir / "log"
    error_log_path = node_dir / "error" / "log.txt"
    status, matched_pids = _node_status(node_dir, processes)
    extra_pattern_regexes = [re.compile(re.escape(pattern)) for pattern in extra_patterns]
    return {
        "node_dir": str(node_dir),
        "status": status,
        "matched_pids": matched_pids,
        "log_path": str(log_path),
        "error_log_path": str(error_log_path),
        "crash_markers": _matching_lines(log_path, default_patterns),
        "error_log_markers": _matching_lines(error_log_path, default_patterns),
        "extra_pattern_matches": _matching_lines(log_path, extra_pattern_regexes),
        "error_log_extra_pattern_matches": _matching_lines(error_log_path, extra_pattern_regexes),
        "log_tail": _tail_lines(log_path),
        "error_log_tail": _tail_lines(error_log_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize node liveness, crash markers, and extra log matches for a tontester run directory",
        epilog=(
            "Examples:\n"
            "  python3 summarize_run.py --run-dir /tmp/tontester-mixed/run-abc123\n"
            "  python3 summarize_run.py --run-dir /tmp/tontester-basic/run-def456 \\\n"
            "    --extra-pattern 'withholding proposal' --out /tmp/run-summary.json"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--run-dir", required=True, help="Run directory emitted by run_basic_network.py or run_mixed_network.py")
    parser.add_argument("--out", help="Optional JSON output path")
    parser.add_argument(
        "--extra-pattern",
        action="append",
        default=[],
        help="Extra literal log pattern to collect; repeat as needed",
    )

    args = parser.parse_args()
    run_dir = resolve_path(Path.cwd(), args.run_dir)
    processes = _validator_processes()
    nodes = sorted(path for path in run_dir.glob("node[0-9]*") if path.is_dir())

    result = {
        "run_dir": str(run_dir),
        "wallet_env_present": (run_dir / "wallet-env.txt").exists(),
        "liteclient_config_present": (run_dir / "liteclient.config.json").exists(),
        "default_patterns": DEFAULT_PATTERN_LABELS,
        "extra_patterns": args.extra_pattern,
        "nodes": {
            node_dir.name: _node_summary(node_dir, DEFAULT_PATTERNS, args.extra_pattern, processes)
            for node_dir in nodes
        },
    }

    rendered = json.dumps(result, indent=2)
    if args.out:
        out_path = resolve_path(Path.cwd(), args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered + "\n")

    print(rendered)


if __name__ == "__main__":
    main()
