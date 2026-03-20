from __future__ import annotations

import argparse

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("yields", help="收益率数据（Pro）")
    yields_sub = parser.add_subparsers(dest="yields_command", required=True)

    pools = yields_sub.add_parser("pools", help="收益池列表")
    pools.set_defaults(func=_pools)

    pools_old = yields_sub.add_parser("pools-old", help="旧版收益池")
    pools_old.set_defaults(func=_pools_old)

    pools_borrow = yields_sub.add_parser("pools-borrow", help="借贷池")
    pools_borrow.set_defaults(func=_pools_borrow)

    pool_chart = yields_sub.add_parser("pool-chart", help="收益池历史曲线")
    pool_chart.add_argument("--pool", required=True, help="Pool ID")
    pool_chart.set_defaults(func=_pool_chart)

    lend_borrow_chart = yields_sub.add_parser("lend-borrow-chart", help="借贷曲线")
    lend_borrow_chart.add_argument("--pool", required=True, help="Pool ID")
    lend_borrow_chart.set_defaults(func=_lend_borrow_chart)

    perps = yields_sub.add_parser("perps", help="永续资金费率")
    perps.set_defaults(func=_perps)

    lsd_rates = yields_sub.add_parser("lsd-rates", help="LSD 利率")
    lsd_rates.set_defaults(func=_lsd_rates)


def _pools(args: argparse.Namespace, context: Context):
    return context.pro_client.yields.getPools()


def _pools_old(args: argparse.Namespace, context: Context):
    return context.pro_client.yields.getPoolsOld()


def _pools_borrow(args: argparse.Namespace, context: Context):
    return context.pro_client.yields.getBorrowPools()


def _pool_chart(args: argparse.Namespace, context: Context):
    return context.pro_client.yields.getPoolChart(args.pool)


def _lend_borrow_chart(args: argparse.Namespace, context: Context):
    return context.pro_client.yields.getLendBorrowChart(args.pool)


def _perps(args: argparse.Namespace, context: Context):
    return context.pro_client.yields.getPerps()


def _lsd_rates(args: argparse.Namespace, context: Context):
    return context.pro_client.yields.getLsdRates()
