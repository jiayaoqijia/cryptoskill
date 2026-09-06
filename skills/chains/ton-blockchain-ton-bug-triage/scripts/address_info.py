"""Normalize a TON account address through tonlib.

Use this when you need to convert between raw and serialized forms or inspect
address metadata such as bounceability and testnet bits.
"""

from __future__ import annotations

import argparse
import asyncio
import json

from ton_triage_lib import build_tonlib_client, normalize_account_address, runtime_from_args


async def _run(args: argparse.Namespace) -> None:
    runtime = runtime_from_args(args)

    client = await build_tonlib_client(runtime, verbosity=args.verbosity, request_timeout=args.request_timeout)
    try:
        normalized = await normalize_account_address(client, args.address, request_timeout=args.request_timeout)
    finally:
        await client.aclose()

    print(
        json.dumps(
            {
                "address_input": normalized.input_value,
                "address_serialized": normalized.serialized,
                "address_raw": normalized.raw,
                "workchain_id": normalized.workchain_id,
                "bounceable": normalized.bounceable,
                "testnet": normalized.testnet,
                "addr_hex": normalized.addr_hex,
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize and inspect a TON account address through tonlib")
    parser.add_argument("--wallet-env", help="Path to wallet-env.txt emitted by the network runner")
    parser.add_argument("--run-dir", help="Run directory containing wallet-env.txt")
    parser.add_argument("--repo-root", help="Path to the TON repo root")
    parser.add_argument("--build", help="Build directory containing tonlibjson")
    parser.add_argument("--config", help="Lite-client config JSON path")
    parser.add_argument("--state-dir", help="Optional state dir for helper defaults")
    parser.add_argument(
        "--address",
        required=True,
        help="TON account address in any tonlib-accepted form; use --address=<value> for raw forms like -1:...",
    )
    parser.add_argument("--verbosity", type=int, default=0, help="Tonlib verbosity level")
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=5.0,
        help="Per-request timeout for tonlib address normalization",
    )

    args = parser.parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
