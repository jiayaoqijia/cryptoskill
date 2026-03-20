from __future__ import annotations

import argparse

from ._shared import Context


def _build_overview_options(args: argparse.Namespace):
    options = {}
    if args.data_type:
        options["dataType"] = args.data_type
    if args.include_total_data_chart:
        options["excludeTotalDataChart"] = False
    if args.include_total_data_chart_breakdown:
        options["excludeTotalDataChartBreakdown"] = False
    return options or None


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("fees", help="费用与收入数据")
    fees_sub = parser.add_subparsers(dest="fees_command", required=True)

    overview = fees_sub.add_parser("overview", help="总体费用概览")
    overview.add_argument("--data-type", help="dailyFees/dailyRevenue/dailyHoldersRevenue")
    overview.add_argument("--include-total-data-chart", action="store_true")
    overview.add_argument("--include-total-data-chart-breakdown", action="store_true")
    overview.set_defaults(func=_overview)

    overview_chain = fees_sub.add_parser("overview-chain", help="链费用概览")
    overview_chain.add_argument("--chain", required=True, help="链名")
    overview_chain.add_argument("--data-type", help="dailyFees/dailyRevenue/dailyHoldersRevenue")
    overview_chain.add_argument("--include-total-data-chart", action="store_true")
    overview_chain.add_argument("--include-total-data-chart-breakdown", action="store_true")
    overview_chain.set_defaults(func=_overview_chain)

    summary = fees_sub.add_parser("summary", help="协议费用概览")
    summary.add_argument("--protocol", required=True, help="协议 slug")
    summary.add_argument("--data-type", help="dailyFees/dailyRevenue/dailyHoldersRevenue")
    summary.set_defaults(func=_summary)


def _overview(args: argparse.Namespace, context: Context):
    options = _build_overview_options(args)
    return context.client.fees.getOverview(options)


def _overview_chain(args: argparse.Namespace, context: Context):
    options = _build_overview_options(args)
    return context.client.fees.getOverviewByChain(args.chain, options)


def _summary(args: argparse.Namespace, context: Context):
    options = {"dataType": args.data_type} if args.data_type else None
    return context.client.fees.getSummary(args.protocol, options)
