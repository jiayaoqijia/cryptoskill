#!/usr/bin/env python3
# /// script
# dependencies = ["defillama-sdk==0.1.4"]
# ///

from __future__ import annotations

import argparse
import os
import sys
from typing import Any, Callable, Optional

from defillama_sdk import (
    ApiError,
    ApiKeyRequiredError,
    DefiLlamaError,
    NotFoundError,
    RateLimitError,
)

from scripts import (
    bridges,
    coins,
    dat,
    etfs,
    fees,
    main_page,
    meta,
    narratives,
    perps,
    stablecoins,
    token_liquidity,
    tvl,
    unlocks,
    volumes,
    yields,
)
from scripts._shared import Context, build_clients, dump_json


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="DefiLlama API CLI (via defillama-sdk).",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("DEFILLAMA_API_KEY"),
        help="Pro API key (可选，默认读取 DEFILLAMA_API_KEY).",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="输出紧凑 JSON（默认 pretty JSON）。",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    tvl.register(subparsers)
    stablecoins.register(subparsers)
    coins.register(subparsers)
    yields.register(subparsers)
    volumes.register(subparsers)
    fees.register(subparsers)
    perps.register(subparsers)
    unlocks.register(subparsers)
    main_page.register(subparsers)
    token_liquidity.register(subparsers)
    etfs.register(subparsers)
    narratives.register(subparsers)
    bridges.register(subparsers)
    meta.register(subparsers)
    dat.register(subparsers)

    return parser


def _print_error(message: str) -> None:
    print(message, file=sys.stderr)


def _handle_error(error: Exception) -> int:
    if isinstance(error, RateLimitError):
        _print_error("rate limited; 放缓速率或提供 API plan key。")
        return 1
    if isinstance(error, ApiKeyRequiredError):
        _print_error("API PLAN REQUIRED; 设置 DEFILLAMA_API_KEY 或升级订阅。")
        return 1
    if isinstance(error, NotFoundError):
        _print_error(str(error))
        return 1
    if isinstance(error, ApiError):
        _print_error(f"API error {error.status_code}: {error}")
        return 1
    if isinstance(error, DefiLlamaError):
        _print_error(str(error))
        return 1
    _print_error(f"Unexpected error: {error}")
    return 1


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    client, pro_client = build_clients(args.api_key)
    context = Context(
        client=client,
        pro_client=pro_client,
        compact=args.compact,
    )

    handler: Callable[[argparse.Namespace, Context], Any] = args.func
    try:
        result = handler(args, context)
    except Exception as exc:
        return _handle_error(exc)

    dump_json(result, compact=args.compact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
