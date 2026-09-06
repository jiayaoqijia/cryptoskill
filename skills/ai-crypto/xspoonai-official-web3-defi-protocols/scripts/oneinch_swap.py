#!/usr/bin/env python3
"""1inch DEX Aggregator Integration."""

import os
import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field

ONEINCH_API = "https://api.1inch.dev"

CHAIN_IDS = {
    "ethereum": 1,
    "polygon": 137,
    "arbitrum": 42161,
    "optimism": 10,
    "base": 8453,
    "bsc": 56
}


class OneInchSwapTool(BaseTool):
    """1inch DEX aggregator for optimal swap routing."""

    name: str = "oneinch_swap"
    description: str = "Get swap quotes and execute via 1inch aggregator"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["quote", "swap"]},
            "from_token": {"type": "string", "description": "Source token address"},
            "to_token": {"type": "string", "description": "Destination token address"},
            "amount": {"type": "string", "description": "Amount in wei"},
            "chain": {"type": "string", "default": "ethereum"},
            "slippage": {"type": "number", "default": 1}
        },
        "required": ["action", "from_token", "to_token", "amount"]
    })

    async def execute(self, action: str, from_token: str, to_token: str,
                      amount: str, chain: str = "ethereum", slippage: float = 1) -> str:
        chain_id = CHAIN_IDS.get(chain, 1)
        api_key = os.getenv("ONEINCH_API_KEY")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        if action == "quote":
            url = f"{ONEINCH_API}/swap/v6.0/{chain_id}/quote"
            params = {
                "src": from_token,
                "dst": to_token,
                "amount": amount
            }
        else:
            url = f"{ONEINCH_API}/swap/v6.0/{chain_id}/swap"
            params = {
                "src": from_token,
                "dst": to_token,
                "amount": amount,
                "from": os.getenv("WALLET_ADDRESS"),
                "slippage": slippage
            }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    return f"Error: {error}"

                data = await resp.json()

                if action == "quote":
                    return self._format_quote(data)
                else:
                    return self._format_swap(data)

    def _format_quote(self, data: dict) -> str:
        src_decimals = data.get("srcToken", {}).get("decimals", 18)
        dst_decimals = data.get("dstToken", {}).get("decimals", 18)

        return f"""
1inch Quote:
- From: {data.get('srcToken', {}).get('symbol', 'Unknown')}
- To: {data.get('dstToken', {}).get('symbol', 'Unknown')}
- Input: {int(data.get('srcAmount', 0)) / 10**src_decimals:.6f}
- Output: {int(data.get('dstAmount', 0)) / 10**dst_decimals:.6f}
- Gas: {data.get('gas', 'N/A')}
"""

    def _format_swap(self, data: dict) -> str:
        return f"Swap transaction prepared: {data.get('tx', {})}"


async def main():
    tool = OneInchSwapTool()

    # Example: quote USDC -> WETH on Ethereum
    result = await tool.execute(
        action="quote",
        from_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
        to_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",    # WETH
        amount="1000000000",  # 1000 USDC
        chain="ethereum"
    )
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
