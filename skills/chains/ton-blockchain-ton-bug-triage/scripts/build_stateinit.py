"""Build a deployable StateInit BoC from code, data, and optional libraries.

Use this after compiling contract code and before deployment or zerostate-style
address calculation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ton_triage_lib import (
    resolve_path,
    run_fift_script_command,
    runtime_from_args,
    wallet_address_from_base,
)


SCRIPT_DIR = Path(__file__).resolve().parent
FIFT_DIR = SCRIPT_DIR / "fift"


def _parse_marker(output: str, marker: str) -> str | None:
    prefix = f"{marker}: "
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    return None


def _validate_name(value: str) -> str:
    if value in {"", ".", ".."}:
        raise argparse.ArgumentTypeError("name must be a simple non-empty filename base")
    path = Path(value)
    if path.name != value:
        raise argparse.ArgumentTypeError("name must not contain directory separators")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a deployable StateInit BoC from code plus optional data and libraries",
        epilog=(
            "Examples:\n"
            "  python3 build_stateinit.py --wallet-env /tmp/run/wallet-env.txt \\\n"
            "    --code-boc /tmp/contract/code.boc --out-dir /tmp/contract-build\n"
            "  python3 build_stateinit.py --repo-root /path/to/repo --build /path/to/repo/build \\\n"
            "    --code-boc code.boc --data-boc data.boc --library-boc libs.boc \\\n"
            "    --workchain 0 --name target --out-dir /tmp/target-stateinit"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--wallet-env", help="Path to wallet-env.txt emitted by the network runner")
    parser.add_argument("--run-dir", help="Run directory containing wallet-env.txt")
    parser.add_argument("--repo-root", help="Path to the TON repo root")
    parser.add_argument("--build", help="Build directory containing create-state")
    parser.add_argument("--config", help="Unused here; accepted for wallet-env compatibility")
    parser.add_argument("--state-dir", help="Unused here; accepted for wallet-env compatibility")
    parser.add_argument("--code-boc", required=True, help="Compiled contract code BoC")
    parser.add_argument("--data-boc", help="Optional initial data BoC")
    parser.add_argument(
        "--library-boc",
        help="Optional library-dictionary root cell BoC; pass a prebuilt HashmapE root, not raw library code",
    )
    parser.add_argument("--workchain", type=int, default=0, help="Destination workchain id")
    parser.add_argument("--name", type=_validate_name, default="contract", help="Filename base for emitted artifacts")
    parser.add_argument("--out-dir", required=True, help="Output directory for the emitted StateInit and address files")

    args = parser.parse_args()
    runtime = runtime_from_args(args, require_config=False)

    out_dir = resolve_path(Path.cwd(), args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    code_boc = resolve_path(Path.cwd(), args.code_boc)
    data_boc = resolve_path(Path.cwd(), args.data_boc) if args.data_boc else None
    library_boc = resolve_path(Path.cwd(), args.library_boc) if args.library_boc else None

    completed = run_fift_script_command(
        runtime.repo_root,
        runtime.build_dir,
        FIFT_DIR / "build_stateinit.fif",
        cwd=out_dir,
        script_args=[
            str(args.workchain),
            str(code_boc),
            str(data_boc) if data_boc is not None else "-",
            str(library_boc) if library_boc is not None else "-",
            args.name,
        ],
        capture_output=True,
    )

    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")

    contract_base = out_dir / args.name
    stateinit_boc = contract_base.with_name(f"{args.name}-stateinit.boc")
    address_file = contract_base.with_suffix(".addr")

    result = {
        "workchain": args.workchain,
        "code_boc": str(code_boc),
        "data_boc": str(data_boc) if data_boc is not None else None,
        "library_boc": str(library_boc) if library_boc is not None else None,
        "stateinit_boc": str(stateinit_boc),
        "address_file": str(address_file),
        "address_raw": wallet_address_from_base(contract_base),
        "address_non_bounceable": _parse_marker(completed.stdout, "contract address non-bounceable"),
        "address_bounceable": _parse_marker(completed.stdout, "contract address bounceable"),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
