"""Run a get-method through tonlib and print the decoded result.

Use this for activation checks, wallet seqno inspection, and contract-specific
state reads after deploy or trigger transactions.
"""

from __future__ import annotations

import argparse
import asyncio
import json

from ton_triage_lib import (
    build_tonlib_client,
    first_stack_number,
    run_get_method,
    runtime_from_args,
    stack_entry_to_json,
)


async def _run(args: argparse.Namespace) -> None:
    runtime = runtime_from_args(args)
    client = await build_tonlib_client(runtime, verbosity=args.verbosity, request_timeout=args.request_timeout)
    try:
        normalized, _info, result = await run_get_method(
            client,
            args.address,
            args.method,
            stack_numbers=args.stack_number,
            request_timeout=args.request_timeout,
        )
    finally:
        await client.aclose()

    output = {
        "address_input": args.address,
        "address_serialized": normalized.serialized,
        "address_raw": normalized.raw,
        "method": args.method,
        "gas_used": result.gas_used,
        "exit_code": result.exit_code,
        "stack": [stack_entry_to_json(entry) for entry in result.stack],
    }
    top_number = first_stack_number(result)
    if top_number is not None:
        output["top_number"] = top_number
    print(json.dumps(output, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a get-method through tonlib and print JSON")
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
    parser.add_argument("--method", required=True, help="Get-method name or numeric id")
    parser.add_argument(
        "--stack-number",
        type=int,
        action="append",
        default=[],
        help="Integer stack argument; repeat as needed",
    )
    parser.add_argument("--verbosity", type=int, default=0, help="Tonlib verbosity level")
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=5.0,
        help="Per-request timeout for tonlib address loading and get-method execution",
    )

    args = parser.parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
