from __future__ import annotations

import argparse
from urllib.parse import quote

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("bridges", help="跨链桥数据（Pro）")
    bridges_sub = parser.add_subparsers(dest="bridges_command", required=True)

    list_cmd = bridges_sub.add_parser("list", help="桥列表")
    list_cmd.add_argument("--include-chains", action="store_true", help="包含链数据")
    list_cmd.set_defaults(func=_list)

    detail = bridges_sub.add_parser("detail", help="桥详情")
    detail.add_argument("--id", type=int, required=True, help="桥 ID")
    detail.set_defaults(func=_detail)

    volume_chain = bridges_sub.add_parser("volume-chain", help="按链桥交易量")
    volume_chain.add_argument("--chain", required=True, help="链名")
    volume_chain.add_argument("--id", type=int, help="桥 ID")
    volume_chain.set_defaults(func=_volume_chain)

    day_stats = bridges_sub.add_parser("day-stats", help="日统计")
    day_stats.add_argument("--timestamp", type=int, required=True, help="时间戳")
    day_stats.add_argument("--chain", required=True, help="链名")
    day_stats.add_argument("--id", type=int, help="桥 ID")
    day_stats.set_defaults(func=_day_stats)

    transactions = bridges_sub.add_parser("transactions", help="桥交易列表")
    transactions.add_argument("--id", type=int, required=True, help="桥 ID")
    transactions.add_argument("--starttimestamp", type=int, help="开始时间戳")
    transactions.add_argument("--endtimestamp", type=int, help="结束时间戳")
    transactions.add_argument("--sourcechain", help="来源链")
    transactions.add_argument("--address", help="地址")
    transactions.add_argument("--limit", type=int, help="数量限制")
    transactions.set_defaults(func=_transactions)


def _list(args: argparse.Namespace, context: Context):
    options = None
    if args.include_chains:
        options = {"includeChains": True}
    return context.pro_client.bridges.getAll(options)


def _detail(args: argparse.Namespace, context: Context):
    return context.pro_client.bridges.getById(args.id)


def _volume_chain(args: argparse.Namespace, context: Context):
    if args.id is None:
        return context.pro_client.bridges.getVolumeByChain(args.chain)
    params = {"id": args.id}
    return context.pro_client._client.get(
        f"/bridgevolume/{quote(args.chain)}",
        base="bridges",
        params=params,
    )


def _day_stats(args: argparse.Namespace, context: Context):
    if args.id is None:
        return context.pro_client.bridges.getDayStats(args.timestamp, args.chain)
    params = {"id": args.id}
    return context.pro_client._client.get(
        f"/bridgedaystats/{args.timestamp}/{quote(args.chain)}",
        base="bridges",
        params=params,
    )


def _transactions(args: argparse.Namespace, context: Context):
    options = {}
    if args.limit is not None:
        options["limit"] = args.limit
    if args.starttimestamp is not None:
        options["startTimestamp"] = args.starttimestamp
    if args.endtimestamp is not None:
        options["endTimestamp"] = args.endtimestamp
    if args.sourcechain:
        options["sourceChain"] = args.sourcechain
    if args.address:
        options["address"] = args.address
    return context.pro_client.bridges.getTransactions(args.id, options or None)
