from __future__ import annotations

import argparse
from urllib.parse import quote

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("token-liquidity", help="代币流动性（Pro）")
    token_sub = parser.add_subparsers(dest="token_command", required=True)

    historical = token_sub.add_parser("historical", help="代币流动性历史")
    historical.add_argument("--token", required=True, help="代币 symbol")
    historical.set_defaults(func=_historical)


def _historical(args: argparse.Namespace, context: Context):
    token = quote(args.token)
    return context.pro_client._client.get(
        f"/historicalLiquidity/{token}",
        requires_auth=True,
    )
