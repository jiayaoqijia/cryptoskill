from __future__ import annotations

import argparse

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("unlocks", help="解锁/排放数据（Pro）")
    unlocks_sub = parser.add_subparsers(dest="unlocks_command", required=True)

    all_cmd = unlocks_sub.add_parser("all", help="全部解锁数据")
    all_cmd.set_defaults(func=_all)

    protocol_cmd = unlocks_sub.add_parser("protocol", help="协议解锁数据")
    protocol_cmd.add_argument("--protocol", required=True, help="协议 slug")
    protocol_cmd.set_defaults(func=_protocol)


def _all(args: argparse.Namespace, context: Context):
    return context.pro_client.emissions.getAll()


def _protocol(args: argparse.Namespace, context: Context):
    return context.pro_client.emissions.getByProtocol(args.protocol)
