#!/usr/bin/env python3
"""DeFi Yield Finder using DeFiLlama API."""

import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field

DEFI_LLAMA_API = "https://yields.llama.fi"


class YieldFinderTool(BaseTool):
    """Find best DeFi yields across protocols."""

    name: str = "yield_finder"
    description: str = "Find best DeFi yields across protocols via DeFiLlama"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "token": {"type": "string", "description": "Token symbol"},
            "chain": {"type": "string", "default": "all"},
            "min_tvl": {"type": "number", "default": 1000000},
            "top_n": {"type": "integer", "default": 5}
        },
        "required": ["token"]
    })

    async def execute(self, token: str, chain: str = "all",
                      min_tvl: float = 1000000, top_n: int = 5) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{DEFI_LLAMA_API}/pools") as resp:
                if resp.status != 200:
                    return "Error fetching yields"

                data = await resp.json()
                pools = data.get("data", [])

        # Filter by token and criteria
        filtered = [
            p for p in pools
            if token.upper() in p.get("symbol", "").upper()
            and p.get("tvlUsd", 0) >= min_tvl
            and (chain == "all" or p.get("chain", "").lower() == chain.lower())
        ]

        # Sort by APY
        filtered.sort(key=lambda x: x.get("apy", 0), reverse=True)

        if not filtered:
            return f"No yields found for {token} with TVL >= ${min_tvl:,.0f}"

        result = f"Top {top_n} yields for {token}:\n\n"
        for i, pool in enumerate(filtered[:top_n], 1):
            result += f"""{i}. {pool.get('project', 'Unknown')} ({pool.get('chain', 'Unknown')})
   - APY: {pool.get('apy', 0):.2f}%
   - TVL: ${pool.get('tvlUsd', 0):,.0f}
   - Pool: {pool.get('symbol', 'Unknown')}

"""

        return result


async def main():
    tool = YieldFinderTool()
    result = await tool.execute(token="USDC", chain="ethereum", top_n=5)
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
