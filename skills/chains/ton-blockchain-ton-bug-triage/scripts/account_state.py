"""Fetch raw account state through tonlib and optionally dump code/data BoCs.

Use this to confirm activation, inspect current balance and last transaction,
or export code/data artifacts for follow-up debugging.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from ton_triage_lib import (
    build_tonlib_client,
    normalize_account_address,
    raw_get_account_state_with_timeout,
    resolve_path,
    runtime_from_args,
)


async def _run(args: argparse.Namespace) -> None:
    runtime = runtime_from_args(args)
    out_dir = resolve_path(Path.cwd(), args.out_dir) if args.out_dir else None

    client = await build_tonlib_client(runtime, verbosity=args.verbosity, request_timeout=args.request_timeout)
    try:
        normalized = await normalize_account_address(client, args.address, request_timeout=args.request_timeout)
        state = await raw_get_account_state_with_timeout(
            client,
            normalized.serialized,
            args.request_timeout,
        )
    finally:
        await client.aclose()

    code = state.code or b""
    data = state.data or b""
    result = {
        "address_input": args.address,
        "address_serialized": normalized.serialized,
        "address_raw": normalized.raw,
        "code_len": len(code),
        "data_len": len(data),
    }

    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "account-state.json").write_text(state.to_json())
        (out_dir / "code.boc").write_bytes(code)
        (out_dir / "data.boc").write_bytes(data)
        result["out_dir"] = str(out_dir)

    print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch raw account state through tonlib")
    parser.add_argument("--wallet-env", help="Path to wallet-env.txt emitted by the network runner")
    parser.add_argument("--run-dir", help="Run directory containing wallet-env.txt")
    parser.add_argument("--repo-root", help="Path to the TON repo root")
    parser.add_argument("--build", help="Build directory containing tonlibjson")
    parser.add_argument("--config", help="Lite-client config JSON path")
    parser.add_argument("--state-dir", help="Optional state dir for helper defaults")
    parser.add_argument(
        "--address",
        required=True,
        help="TON account address accepted by tonlib; use --address=<value> for raw forms like -1:...",
    )
    parser.add_argument("--out-dir", help="Optional output directory for dumped code/data/state")
    parser.add_argument("--verbosity", type=int, default=0, help="Tonlib verbosity level")
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=5.0,
        help="Per-request timeout for tonlib address/state queries",
    )

    args = parser.parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
