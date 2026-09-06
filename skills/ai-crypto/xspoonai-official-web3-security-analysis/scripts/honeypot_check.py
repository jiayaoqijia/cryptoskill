#!/usr/bin/env python3
"""Honeypot.is Token Detection."""

import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field

HONEYPOT_API = "https://api.honeypot.is/v2"

CHAIN_IDS = {
    "ethereum": 1,
    "bsc": 56,
    "polygon": 137,
    "arbitrum": 42161,
    "base": 8453
}


class HoneypotCheckTool(BaseTool):
    """Check if a token is a honeypot."""

    name: str = "honeypot_check"
    description: str = "Check if token is a honeypot via honeypot.is"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "token_address": {"type": "string"},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["token_address"]
    })

    async def execute(self, token_address: str, chain: str = "ethereum") -> str:
        url = f"{HONEYPOT_API}/IsHoneypot"

        payload = {
            "address": token_address,
            "chainId": CHAIN_IDS.get(chain, 1)
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    return f"Error: {resp.status}"

                data = await resp.json()

        honeypot = data.get("honeypotResult", {})
        simulation = data.get("simulationResult", {})

        is_honeypot = honeypot.get("isHoneypot", False)

        report = f"""
HONEYPOT ANALYSIS
{'='*40}
Token: {token_address}
Chain: {chain}

Result: {"HONEYPOT DETECTED" if is_honeypot else "NOT A HONEYPOT"}

Simulation:
- Buy Tax: {simulation.get('buyTax', 0):.1f}%
- Sell Tax: {simulation.get('sellTax', 0):.1f}%
- Buy Gas: {simulation.get('buyGas', 'N/A')}
- Sell Gas: {simulation.get('sellGas', 'N/A')}
"""

        if is_honeypot:
            report += f"\nReason: {honeypot.get('honeypotReason', 'Unknown')}"

        return report


async def main():
    tool = HoneypotCheckTool()
    result = await tool.execute(
        token_address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        chain="ethereum"
    )
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
