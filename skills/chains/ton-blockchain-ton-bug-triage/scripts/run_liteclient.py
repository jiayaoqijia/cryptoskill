"""Run a lite-client command using wallet-env.txt or explicit runtime paths.

Use this as the fallback observation path when tonlib-based helpers crash or
when you need a raw lite-client response for debugging.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from ton_triage_lib import format_command, resolve_path, runtime_from_args


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a lite-client command using wallet-env.txt or explicit repo/build/config inputs"
    )
    parser.add_argument("--wallet-env", help="Path to wallet-env.txt emitted by the network runner")
    parser.add_argument("--run-dir", help="Run directory containing wallet-env.txt")
    parser.add_argument("--repo-root", help="Path to the TON repo root")
    parser.add_argument("--build", help="Build directory containing lite-client")
    parser.add_argument("--config", help="Lite-client config JSON path")
    parser.add_argument("--state-dir", help="Unused here; accepted for wallet-env compatibility")
    parser.add_argument(
        "--lite-db",
        help="Optional lite-client DB directory override; defaults to LITECLIENT_DB from wallet-env when present",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="lite-client batch timeout in seconds",
    )
    parser.add_argument(
        "liteclient_args",
        nargs=argparse.REMAINDER,
        help="lite-client command tokens passed after '--'",
    )

    args = parser.parse_args()
    passthrough = args.liteclient_args
    if passthrough[:1] == ["--"]:
        passthrough = passthrough[1:]
    if not passthrough:
        raise SystemExit("pass a lite-client command after '--'")

    runtime = runtime_from_args(args)
    if runtime.config_path is None:
        raise SystemExit("lite-client config was not resolved; pass --config or use --wallet-env/--run-dir")

    lite_client = runtime.build_dir / "lite-client" / "lite-client"
    if not lite_client.exists():
        raise SystemExit(
            f"lite-client not found in build dir; build it with ninja -C {runtime.build_dir} lite-client"
        )

    if args.lite_db:
        lite_db = resolve_path(Path.cwd(), args.lite_db)
    else:
        lite_db = runtime.lite_db
    if lite_db is not None:
        lite_db.mkdir(parents=True, exist_ok=True)

    command = " ".join(passthrough)
    cmd = [str(lite_client), "-C", str(runtime.config_path), "-t", str(args.timeout), "-c", command]
    if lite_db is not None:
        cmd[1:1] = ["-D", str(lite_db)]

    cwd = runtime.workdir if runtime.workdir is not None else Path.cwd().resolve()
    print(f"running: {format_command(cmd)}", flush=True)
    print(f"cwd: {cwd}", flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


if __name__ == "__main__":
    main()
