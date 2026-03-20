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
    parser = subparsers.add_parser("volumes", help="交易量数据")
    volumes_sub = parser.add_subparsers(dest="volumes_command", required=True)

    dex_overview = volumes_sub.add_parser("dex-overview", help="DEX 概览")
    dex_overview.add_argument("--data-type", help="dailyVolume/totalVolume")
    dex_overview.add_argument("--include-total-data-chart", action="store_true")
    dex_overview.add_argument("--include-total-data-chart-breakdown", action="store_true")
    dex_overview.set_defaults(func=_dex_overview)

    dex_chain = volumes_sub.add_parser("dex-overview-chain", help="DEX 链概览")
    dex_chain.add_argument("--chain", required=True, help="链名")
    dex_chain.add_argument("--data-type", help="dailyVolume/totalVolume")
    dex_chain.add_argument("--include-total-data-chart", action="store_true")
    dex_chain.add_argument("--include-total-data-chart-breakdown", action="store_true")
    dex_chain.set_defaults(func=_dex_overview_chain)

    dex_summary = volumes_sub.add_parser("dex-summary", help="DEX 协议概览")
    dex_summary.add_argument("--protocol", required=True, help="协议 slug")
    dex_summary.add_argument("--data-type", help="dailyVolume/totalVolume")
    dex_summary.set_defaults(func=_dex_summary)

    options_overview = volumes_sub.add_parser("options-overview", help="期权概览")
    options_overview.add_argument("--data-type", help="dailyPremiumVolume/dailyNotionalVolume")
    options_overview.add_argument("--include-total-data-chart", action="store_true")
    options_overview.add_argument("--include-total-data-chart-breakdown", action="store_true")
    options_overview.set_defaults(func=_options_overview)

    options_chain = volumes_sub.add_parser("options-overview-chain", help="期权链概览")
    options_chain.add_argument("--chain", required=True, help="链名")
    options_chain.add_argument("--data-type", help="dailyPremiumVolume/dailyNotionalVolume")
    options_chain.add_argument("--include-total-data-chart", action="store_true")
    options_chain.add_argument("--include-total-data-chart-breakdown", action="store_true")
    options_chain.set_defaults(func=_options_overview_chain)

    options_summary = volumes_sub.add_parser("options-summary", help="期权协议概览")
    options_summary.add_argument("--protocol", required=True, help="协议 slug")
    options_summary.add_argument("--data-type", help="dailyPremiumVolume/dailyNotionalVolume")
    options_summary.set_defaults(func=_options_summary)


def _dex_overview(args: argparse.Namespace, context: Context):
    options = _build_overview_options(args)
    return context.client.volumes.getDexOverview(options)


def _dex_overview_chain(args: argparse.Namespace, context: Context):
    options = _build_overview_options(args)
    return context.client.volumes.getDexOverviewByChain(args.chain, options)


def _dex_summary(args: argparse.Namespace, context: Context):
    options = {"dataType": args.data_type} if args.data_type else None
    return context.client.volumes.getDexSummary(args.protocol, options)


def _options_overview(args: argparse.Namespace, context: Context):
    options = _build_overview_options(args)
    return context.client.volumes.getOptionsOverview(options)


def _options_overview_chain(args: argparse.Namespace, context: Context):
    options = _build_overview_options(args)
    return context.client.volumes.getOptionsOverviewByChain(args.chain, options)


def _options_summary(args: argparse.Namespace, context: Context):
    options = {"dataType": args.data_type} if args.data_type else None
    return context.client.volumes.getOptionsSummary(args.protocol, options)
