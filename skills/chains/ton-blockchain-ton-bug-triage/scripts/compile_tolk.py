"""Compile a Tolk contract and materialize its code BoC.

Use this when Workflow A starts from a `.tolk` source and you want a checked
path that refuses to use a stale `tolk` binary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ton_triage_lib import (
    ensure_tolk_matches_repo,
    resolve_path,
    run_fift_script_command,
    run_subprocess,
    runtime_from_args,
)


def _validate_name(value: str) -> str:
    if value in {"", ".", ".."}:
        raise argparse.ArgumentTypeError("name must be a simple non-empty filename base")
    path = Path(value)
    if path.name != value:
        raise argparse.ArgumentTypeError("name must not contain directory separators")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile a Tolk contract and materialize its code BoC",
        epilog=(
            "Examples:\n"
            "  python3 compile_tolk.py --repo-root /path/to/repo --build /path/to/repo/build \\\n"
            "    --source /tmp/counter.tolk --out-dir /tmp/counter-build\n"
            "  python3 compile_tolk.py --wallet-env /tmp/run/wallet-env.txt \\\n"
            "    --source contracts/trigger.tolk --name trigger --out-dir /tmp/trigger-build"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--wallet-env", help="Path to wallet-env.txt emitted by the network runner")
    parser.add_argument("--run-dir", help="Run directory containing wallet-env.txt")
    parser.add_argument("--repo-root", help="Path to the TON repo root")
    parser.add_argument("--build", help="Build directory containing tolk and create-state")
    parser.add_argument("--config", help="Unused here; accepted for wallet-env compatibility")
    parser.add_argument("--state-dir", help="Unused here; accepted for wallet-env compatibility")
    parser.add_argument("--source", required=True, help="Path to the .tolk source file")
    parser.add_argument("--out-dir", required=True, help="Output directory for compiler artifacts")
    parser.add_argument("--name", type=_validate_name, help="Filename base for emitted artifacts; defaults to the source stem")

    args = parser.parse_args()
    runtime = runtime_from_args(args, require_config=False)

    source = resolve_path(Path.cwd(), args.source)
    out_dir = resolve_path(Path.cwd(), args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    name = args.name or source.stem

    build_info = ensure_tolk_matches_repo(runtime.repo_root, runtime.build_dir)

    fift_out = out_dir / f"{name}.fif"
    code_boc = out_dir / f"{name}.code.boc"

    completed = run_subprocess(
        [
            str(build_info.binary),
            "-o",
            str(fift_out),
            "-b",
            str(code_boc),
            str(source),
        ],
        cwd=out_dir,
        capture_output=True,
    )
    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.stderr:
        print(completed.stderr, end="" if completed.stderr.endswith("\n") else "\n")

    fift_completed = run_fift_script_command(
        runtime.repo_root,
        runtime.build_dir,
        fift_out,
        cwd=out_dir,
        capture_output=True,
    )
    if fift_completed.stdout:
        print(fift_completed.stdout, end="" if fift_completed.stdout.endswith("\n") else "\n")

    print(
        json.dumps(
            {
                "source": str(source),
                "tolk_binary": str(build_info.binary),
                "tolk_version": build_info.version,
                "build_commit": build_info.build_commit,
                "build_date": build_info.build_date,
                "fift_output": str(fift_out),
                "code_boc": str(code_boc),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
