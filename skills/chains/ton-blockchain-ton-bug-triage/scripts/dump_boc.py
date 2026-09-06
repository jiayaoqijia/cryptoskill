"""Render a BoC cell tree through Fift for human inspection.

Use this when you need to inspect payload, StateInit, or transaction BoCs at
the cell level instead of treating them as opaque bytes.
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from ton_triage_lib import resolve_path, run_fift_script_command, runtime_from_args


SCRIPT_DIR = Path(__file__).resolve().parent
FIFT_DIR = SCRIPT_DIR / "fift"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Dump a BoC cell tree through Fift",
        epilog=(
            "Examples:\n"
            "  python3 dump_boc.py --wallet-env /tmp/run/wallet-env.txt --boc /tmp/contract/code.boc\n"
            "  python3 dump_boc.py --repo-root /path/to/repo --build /path/to/repo/build \\\n"
            "    --boc-hex b5ee9c72410101010004000000"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--wallet-env", help="Path to wallet-env.txt emitted by the network runner")
    parser.add_argument("--run-dir", help="Run directory containing wallet-env.txt")
    parser.add_argument("--repo-root", help="Path to the TON repo root")
    parser.add_argument("--build", help="Build directory containing create-state")
    parser.add_argument("--config", help="Unused here; accepted for wallet-env compatibility")
    parser.add_argument("--state-dir", help="Unused here; accepted for wallet-env compatibility")
    parser.add_argument("--boc", help="Path to a BoC file")
    parser.add_argument("--boc-hex", help="BoC bytes as a hex string")
    parser.add_argument("--out-file", help="Optional path to also save the dump text")

    args = parser.parse_args()
    if bool(args.boc) == bool(args.boc_hex):
        raise SystemExit("pass exactly one of --boc or --boc-hex")

    runtime = runtime_from_args(args, require_config=False)

    if args.boc:
        boc_path = resolve_path(Path.cwd(), args.boc)
        with tempfile.TemporaryDirectory(prefix="dump-boc-") as tmp_dir:
            completed = run_fift_script_command(
                runtime.repo_root,
                runtime.build_dir,
                FIFT_DIR / "dump_boc.fif",
                cwd=Path(tmp_dir),
                script_args=[str(boc_path)],
                capture_output=True,
            )
    else:
        boc_bytes = bytes.fromhex(args.boc_hex)
        with tempfile.TemporaryDirectory(prefix="dump-boc-") as tmp_dir:
            tmp_path = Path(tmp_dir)
            boc_path = tmp_path / "inline.boc"
            boc_path.write_bytes(boc_bytes)
            completed = run_fift_script_command(
                runtime.repo_root,
                runtime.build_dir,
                FIFT_DIR / "dump_boc.fif",
                cwd=tmp_path,
                script_args=[str(boc_path)],
                capture_output=True,
            )

    dump_text = completed.stdout
    if args.out_file:
        out_file = resolve_path(Path.cwd(), args.out_file)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(dump_text)

    print(dump_text, end="" if dump_text.endswith("\n") else "\n")


if __name__ == "__main__":
    main()
