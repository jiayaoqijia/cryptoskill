from __future__ import annotations

import argparse

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("tvl", help="TVL 数据")
    tvl_sub = parser.add_subparsers(dest="tvl_command", required=True)

    protocols = tvl_sub.add_parser("protocols", help="列出所有协议 TVL")
    protocols.set_defaults(func=_protocols)

    protocol = tvl_sub.add_parser("protocol", help="协议详情")
    protocol.add_argument("--protocol", required=True, help="协议 slug")
    protocol.set_defaults(func=_protocol)

    tvl_value = tvl_sub.add_parser("tvl", help="协议当前 TVL")
    tvl_value.add_argument("--protocol", required=True, help="协议 slug")
    tvl_value.set_defaults(func=_tvl)

    chains = tvl_sub.add_parser("chains", help="链 TVL 列表")
    chains.set_defaults(func=_chains)

    historical = tvl_sub.add_parser("historical-chain-tvl", help="历史链 TVL")
    historical.add_argument("--chain", help="链名（可选）")
    historical.set_defaults(func=_historical_chain_tvl)

    token_protocols = tvl_sub.add_parser("token-protocols", help="持仓该代币的协议")
    token_protocols.add_argument("--symbol", required=True, help="代币 symbol")
    token_protocols.set_defaults(func=_token_protocols)

    inflows = tvl_sub.add_parser("inflows", help="协议资金流入流出")
    inflows.add_argument("--protocol", required=True, help="协议 slug")
    inflows.add_argument("--start", required=True, type=int, help="开始时间戳")
    inflows.add_argument("--end", required=True, type=int, help="结束时间戳")
    inflows.add_argument("--tokens-exclude", help="排除的 token 列表字符串")
    inflows.set_defaults(func=_inflows)

    chain_assets = tvl_sub.add_parser("chain-assets", help="链资产分布")
    chain_assets.set_defaults(func=_chain_assets)


def _protocols(args: argparse.Namespace, context: Context):
    return context.client.tvl.getProtocols()


def _protocol(args: argparse.Namespace, context: Context):
    return context.client.tvl.getProtocol(args.protocol)


def _tvl(args: argparse.Namespace, context: Context):
    return context.client.tvl.getTvl(args.protocol)


def _chains(args: argparse.Namespace, context: Context):
    return context.client.tvl.getChains()


def _historical_chain_tvl(args: argparse.Namespace, context: Context):
    return context.client.tvl.getHistoricalChainTvl(args.chain)


def _token_protocols(args: argparse.Namespace, context: Context):
    return context.pro_client.tvl.getTokenProtocols(args.symbol)


def _inflows(args: argparse.Namespace, context: Context):
    return context.pro_client.tvl.getInflows(
        args.protocol,
        args.start,
        args.end,
        tokens_to_exclude=args.tokens_exclude,
    )


def _chain_assets(args: argparse.Namespace, context: Context):
    return context.pro_client.tvl.getChainAssets()
