from __future__ import annotations

import argparse

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("perps", help="永续合约数据")
    perps_sub = parser.add_subparsers(dest="perps_command", required=True)

    open_interest = perps_sub.add_parser("open-interest", help="未平仓量")
    open_interest.add_argument("--include-total-data-chart", action="store_true")
    open_interest.add_argument("--include-total-data-chart-breakdown", action="store_true")
    open_interest.set_defaults(func=_open_interest)

    derivatives_overview = perps_sub.add_parser(
        "derivatives-overview", help="衍生品概览（Pro）"
    )
    derivatives_overview.set_defaults(func=_derivatives_overview)

    derivatives_summary = perps_sub.add_parser(
        "derivatives-summary", help="衍生品协议概览（Pro）"
    )
    derivatives_summary.add_argument("--protocol", required=True, help="协议 slug")
    derivatives_summary.set_defaults(func=_derivatives_summary)


def _open_interest(args: argparse.Namespace, context: Context):
    params = {
        "excludeTotalDataChart": not args.include_total_data_chart,
        "excludeTotalDataChartBreakdown": not args.include_total_data_chart_breakdown,
    }
    return context.client._client.get("/overview/open-interest", params=params)


def _derivatives_overview(args: argparse.Namespace, context: Context):
    return context.pro_client.volumes.getDerivativesOverview()


def _derivatives_summary(args: argparse.Namespace, context: Context):
    return context.pro_client.volumes.getDerivativesSummary(args.protocol)
