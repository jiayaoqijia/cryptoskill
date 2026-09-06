#!/usr/bin/env python3
"""Tenderly Transaction Simulation."""

import os
import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field

TENDERLY_API = "https://api.tenderly.co/api/v1"

CHAIN_IDS = {
    "ethereum": "1",
    "polygon": "137",
    "arbitrum": "42161",
    "optimism": "10",
    "base": "8453"
}


class TransactionSimulatorTool(BaseTool):
    """Simulate transactions before execution using Tenderly."""

    name: str = "simulate_transaction"
    description: str = "Simulate transaction before execution via Tenderly"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "to": {"type": "string", "description": "Target contract"},
            "data": {"type": "string", "description": "Calldata (hex)"},
            "value": {"type": "string", "default": "0"},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["to", "data"]
    })

    async def execute(self, to: str, data: str, value: str = "0",
                      chain: str = "ethereum") -> str:
        account = os.getenv("TENDERLY_ACCOUNT")
        project = os.getenv("TENDERLY_PROJECT")
        api_key = os.getenv("TENDERLY_API_KEY")

        if not all([account, project, api_key]):
            return "Error: Missing Tenderly configuration"

        url = f"{TENDERLY_API}/account/{account}/project/{project}/simulate"

        headers = {
            "X-Access-Key": api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "network_id": CHAIN_IDS.get(chain, "1"),
            "from": os.getenv("WALLET_ADDRESS"),
            "to": to,
            "input": data,
            "value": value,
            "gas": 8000000,
            "gas_price": "0",
            "save_if_fails": True
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    return f"Simulation failed: {error}"

                result = await resp.json()

        return self._format_simulation(result)

    def _format_simulation(self, result: dict) -> str:
        """Format simulation results."""
        tx = result.get("transaction", {})

        status = "SUCCESS" if tx.get("status") else "FAILED"
        gas_used = tx.get("gas_used", 0)

        report = f"""
TRANSACTION SIMULATION
{'='*40}
Status: {status}
Gas Used: {gas_used:,}
"""

        # Asset changes
        tx_info = tx.get("transaction_info", {})
        asset_changes = tx_info.get("asset_changes", [])

        if asset_changes:
            report += "\nAsset Changes:\n"
            for change in asset_changes:
                direction = "+" if change.get("type") == "Transfer" else "-"
                amount = change.get("amount", 0)
                symbol = change.get("token_info", {}).get("symbol", "ETH")
                report += f"  {direction}{amount} {symbol}\n"

        # Logs/Events
        logs = tx.get("logs", [])
        if logs:
            report += f"\nEvents Emitted: {len(logs)}\n"
            for log in logs[:5]:
                report += f"  - {log.get('name', 'Unknown')}\n"

        # Error info
        if not tx.get("status"):
            error_info = tx.get("error_info", {})
            report += f"\nError: {error_info.get('error_message', 'Unknown error')}"

        return report


async def main():
    tool = TransactionSimulatorTool()
    # This requires actual tx data and Tenderly credentials
    print("TransactionSimulatorTool ready - requires Tenderly credentials")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
