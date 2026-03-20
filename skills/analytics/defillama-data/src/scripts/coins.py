from __future__ import annotations

import argparse

from ._shared import Context, parse_json_value, split_csv


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("coins", help="币价与链上数据")
    coins_sub = parser.add_subparsers(dest="coins_command", required=True)

    current = coins_sub.add_parser("current", help="当前价格")
    current.add_argument("--coins", required=True, help="币种列表，逗号分隔")
    current.add_argument("--search-width", help="搜索窗口")
    current.set_defaults(func=_current)

    historical = coins_sub.add_parser("historical", help="历史价格")
    historical.add_argument("--timestamp", type=int, required=True, help="时间戳")
    historical.add_argument("--coins", required=True, help="币种列表，逗号分隔")
    historical.add_argument("--search-width", help="搜索窗口")
    historical.set_defaults(func=_historical)

    batch = coins_sub.add_parser("batch-historical", help="批量历史价格")
    batch.add_argument("--coins-json", required=True, help="JSON 字符串")
    batch.add_argument("--search-width", help="搜索窗口")
    batch.set_defaults(func=_batch_historical)

    chart = coins_sub.add_parser("chart", help="价格曲线")
    chart.add_argument("--coins", required=True, help="币种列表，逗号分隔")
    chart.add_argument("--start", type=int, help="开始时间戳")
    chart.add_argument("--end", type=int, help="结束时间戳")
    chart.add_argument("--span", type=int, help="时间间隔小时数")
    chart.add_argument("--period", help="周期（如 1d,7d）")
    chart.add_argument("--search-width", help="搜索窗口")
    chart.set_defaults(func=_chart)

    percentage = coins_sub.add_parser("percentage", help="区间涨跌幅")
    percentage.add_argument("--coins", required=True, help="币种列表，逗号分隔")
    percentage.add_argument("--timestamp", type=int, help="时间戳")
    percentage.add_argument("--look-forward", action="store_true", help="向前看")
    percentage.add_argument("--period", help="周期（如 3w）")
    percentage.set_defaults(func=_percentage)

    first = coins_sub.add_parser("first", help="最早价格")
    first.add_argument("--coins", required=True, help="币种列表，逗号分隔")
    first.set_defaults(func=_first)

    block = coins_sub.add_parser("block", help="时间戳对应区块")
    block.add_argument("--chain", required=True, help="链名")
    block.add_argument("--timestamp", type=int, required=True, help="时间戳")
    block.set_defaults(func=_block)


def _current(args: argparse.Namespace, context: Context):
    coins = split_csv(args.coins)
    return context.client.prices.getCurrentPrices(coins, searchWidth=args.search_width)


def _historical(args: argparse.Namespace, context: Context):
    coins = split_csv(args.coins)
    return context.client.prices.getHistoricalPrices(
        args.timestamp, coins, searchWidth=args.search_width
    )


def _batch_historical(args: argparse.Namespace, context: Context):
    coins_json = parse_json_value(args.coins_json)
    return context.client.prices.getBatchHistoricalPrices(
        coins_json, searchWidth=args.search_width
    )


def _chart(args: argparse.Namespace, context: Context):
    coins = split_csv(args.coins)
    options = {
        "start": args.start,
        "end": args.end,
        "span": args.span,
        "period": args.period,
        "searchWidth": args.search_width,
    }
    return context.client.prices.getChart(coins, options=options)


def _percentage(args: argparse.Namespace, context: Context):
    coins = split_csv(args.coins)
    options = {
        "timestamp": args.timestamp,
        "lookForward": True if args.look_forward else None,
        "period": args.period,
    }
    return context.client.prices.getPercentageChange(coins, options=options)


def _first(args: argparse.Namespace, context: Context):
    coins = split_csv(args.coins)
    return context.client.prices.getFirstPrices(coins)


def _block(args: argparse.Namespace, context: Context):
    return context.client.prices.getBlockAtTimestamp(args.chain, args.timestamp)
