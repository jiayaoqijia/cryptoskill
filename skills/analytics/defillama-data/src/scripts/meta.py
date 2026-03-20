from __future__ import annotations

import argparse

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("meta", help="账号与配额（Pro）")
    meta_sub = parser.add_subparsers(dest="meta_command", required=True)

    usage = meta_sub.add_parser("usage", help="API 使用量")
    usage.set_defaults(func=_usage)


def _usage(args: argparse.Namespace, context: Context):
    return context.pro_client.account.getUsage()
