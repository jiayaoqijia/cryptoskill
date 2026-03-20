from __future__ import annotations

import argparse

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("stablecoins", help="稳定币数据")
    stable_sub = parser.add_subparsers(dest="stable_command", required=True)

    list_cmd = stable_sub.add_parser("list", help="稳定币列表")
    list_cmd.add_argument("--include-prices", action="store_true", help="包含价格")
    list_cmd.set_defaults(func=_list)

    charts_all = stable_sub.add_parser("charts-all", help="全部稳定币历史市值")
    charts_all.set_defaults(func=_charts_all)

    charts_chain = stable_sub.add_parser("charts-chain", help="指定链稳定币历史市值")
    charts_chain.add_argument("--chain", required=True, help="链名")
    charts_chain.set_defaults(func=_charts_chain)

    detail = stable_sub.add_parser("detail", help="稳定币详情")
    detail.add_argument("--asset", required=True, help="稳定币 ID")
    detail.set_defaults(func=_detail)

    chains = stable_sub.add_parser("chains", help="链上稳定币市值")
    chains.set_defaults(func=_chains)

    prices = stable_sub.add_parser("prices", help="稳定币历史价格")
    prices.set_defaults(func=_prices)

    dominance = stable_sub.add_parser("dominance", help="稳定币市值占比")
    dominance.add_argument("--chain", required=True, help="链名")
    dominance.add_argument("--stablecoin-id", type=int, help="稳定币 ID")
    dominance.set_defaults(func=_dominance)


def _list(args: argparse.Namespace, context: Context):
    include_prices = True if args.include_prices else None
    return context.client.stablecoins.getStablecoins(includePrices=include_prices)


def _charts_all(args: argparse.Namespace, context: Context):
    return context.client.stablecoins.getAllCharts()


def _charts_chain(args: argparse.Namespace, context: Context):
    return context.client.stablecoins.getChartsByChain(args.chain)


def _detail(args: argparse.Namespace, context: Context):
    return context.client.stablecoins.getStablecoin(args.asset)


def _chains(args: argparse.Namespace, context: Context):
    return context.client.stablecoins.getChains()


def _prices(args: argparse.Namespace, context: Context):
    return context.client.stablecoins.getPrices()


def _dominance(args: argparse.Namespace, context: Context):
    return context.pro_client.stablecoins.getDominance(
        args.chain, stablecoinId=args.stablecoin_id
    )
