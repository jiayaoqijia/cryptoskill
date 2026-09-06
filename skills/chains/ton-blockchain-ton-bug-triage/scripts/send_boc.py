"""Send an already-built external message BoC through tonlib.

Use this when another tool already produced the serialized external message and
you only need transport, seqno observation, or replay.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
from pathlib import Path

from ton_triage_lib import (
    build_tonlib_client,
    get_masterchain_info_with_timeout,
    raw_send_message_with_timeout,
    resolve_path,
    runtime_from_args,
    wait_for_mc_advance,
)


async def _run(args: argparse.Namespace) -> None:
    runtime = runtime_from_args(args)
    boc_path = resolve_path(Path.cwd(), args.boc)
    body = boc_path.read_bytes()

    print(f"repo root: {runtime.repo_root}")
    print(f"build dir: {runtime.build_dir}")
    print(f"config: {runtime.config_path}")
    print(f"boc: {boc_path} ({len(body)} bytes)")
    print(f"boc sha256: {hashlib.sha256(body).hexdigest()}")

    client = await build_tonlib_client(runtime, verbosity=args.verbosity, request_timeout=args.request_timeout)
    try:
        before_seqno = None
        if args.show_seqno:
            info = await get_masterchain_info_with_timeout(client, args.request_timeout)
            if info.last is not None:
                before_seqno = info.last.seqno
                print(f"mc seqno before: {before_seqno}")
        elif args.wait_mc_advance:
            info = await get_masterchain_info_with_timeout(client, args.request_timeout)
            if info.last is not None:
                before_seqno = info.last.seqno

        await raw_send_message_with_timeout(client, body, args.request_timeout)
        print("raw_send_message: ok")

        if args.wait_mc_advance and before_seqno is not None:
            advanced = await wait_for_mc_advance(
                client,
                before_seqno=before_seqno,
                wait_timeout=args.wait_timeout,
                request_timeout=args.request_timeout,
            )
            print(f"mc seqno advanced to: {advanced}")
        elif args.wait_seconds > 0:
            await asyncio.sleep(args.wait_seconds)

        if args.show_seqno:
            info = await get_masterchain_info_with_timeout(client, args.request_timeout)
            if info.last is not None:
                print(f"mc seqno after: {info.last.seqno}")
    finally:
        await client.aclose()


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a raw BOC message through tonlib")
    parser.add_argument("--wallet-env", help="Path to wallet-env.txt emitted by the network runner")
    parser.add_argument("--run-dir", help="Run directory containing wallet-env.txt")
    parser.add_argument("--repo-root", help="Path to the TON repo root")
    parser.add_argument("--build", help="Build directory containing tonlibjson")
    parser.add_argument("--config", help="Lite-client config JSON path")
    parser.add_argument("--state-dir", help="Optional state dir for helper defaults")
    parser.add_argument("--boc", required=True, help="Path to the serialized BOC message to send")
    parser.add_argument(
        "--wait-seconds",
        type=float,
        default=0.0,
        help="Optional delay after sending before a final seqno read",
    )
    parser.add_argument(
        "--wait-mc-advance",
        action="store_true",
        help="Wait until masterchain seqno advances after the send; useful as a liveness hint, not proof of inclusion",
    )
    parser.add_argument(
        "--wait-timeout",
        type=float,
        default=10.0,
        help="Timeout for --wait-mc-advance",
    )
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=5.0,
        help="Per-request timeout for tonlib calls such as getMasterchainInfo and raw_send_message",
    )
    parser.add_argument(
        "--verbosity",
        type=int,
        default=0,
        help="Tonlib verbosity level",
    )
    parser.add_argument(
        "--show-seqno",
        action="store_true",
        help="Print masterchain seqno before and after the send",
    )

    args = parser.parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
