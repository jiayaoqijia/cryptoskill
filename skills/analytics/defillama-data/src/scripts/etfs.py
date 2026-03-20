from __future__ import annotations

import argparse

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("etfs", help="ETF 数据（Pro）")
    etfs_sub = parser.add_subparsers(dest="etfs_command", required=True)

    overview = etfs_sub.add_parser("overview", help="比特币 ETF 概览")
    overview.set_defaults(func=_overview)

    overview_eth = etfs_sub.add_parser("overview-eth", help="以太坊 ETF 概览")
    overview_eth.set_defaults(func=_overview_eth)

    history = etfs_sub.add_parser("history", help="比特币 ETF 流入流出历史")
    history.set_defaults(func=_history)

    history_eth = etfs_sub.add_parser("history-eth", help="以太坊 ETF 流入流出历史")
    history_eth.set_defaults(func=_history_eth)


def _overview(args: argparse.Namespace, context: Context):
    return context.pro_client.etfs.getOverview()


def _overview_eth(args: argparse.Namespace, context: Context):
    return context.pro_client.etfs.getOverviewEth()


def _history(args: argparse.Namespace, context: Context):
    return context.pro_client.etfs.getHistory()


def _history_eth(args: argparse.Namespace, context: Context):
    return context.pro_client.etfs.getHistoryEth()
