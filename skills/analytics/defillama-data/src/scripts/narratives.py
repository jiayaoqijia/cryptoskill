from __future__ import annotations

import argparse

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("narratives", help="叙事表现（Pro）")
    narratives_sub = parser.add_subparsers(dest="narratives_command", required=True)

    fdv = narratives_sub.add_parser("fdv-performance", help="FDV 表现")
    fdv.add_argument("--period", required=True, help="周期（例如 30）")
    fdv.set_defaults(func=_fdv_performance)


def _fdv_performance(args: argparse.Namespace, context: Context):
    return context.pro_client.etfs.getFdvPerformance(args.period)
