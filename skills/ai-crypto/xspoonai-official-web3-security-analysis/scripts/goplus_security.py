#!/usr/bin/env python3
"""GoPlus Token Security Analysis."""

import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field

GOPLUS_API = "https://api.gopluslabs.io/api/v1"

CHAIN_IDS = {
    "ethereum": "1",
    "bsc": "56",
    "polygon": "137",
    "arbitrum": "42161",
    "base": "8453",
    "optimism": "10"
}


class TokenSecurityTool(BaseTool):
    """Analyze token security risks via GoPlus API."""

    name: str = "token_security"
    description: str = "Analyze token security risks via GoPlus"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "token_address": {"type": "string"},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["token_address"]
    })

    async def execute(self, token_address: str, chain: str = "ethereum") -> str:
        chain_id = CHAIN_IDS.get(chain, "1")
        url = f"{GOPLUS_API}/token_security/{chain_id}"
        params = {"contract_addresses": token_address.lower()}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    return f"Error: API returned {resp.status}"

                data = await resp.json()

        if data.get("code") != 1:
            return f"Error: {data.get('message', 'Unknown error')}"

        result = data.get("result", {}).get(token_address.lower(), {})
        return self._format_security_report(result, token_address)

    def _format_security_report(self, data: dict, address: str) -> str:
        """Format security analysis report."""
        risks = []
        warnings = []

        # Critical risks
        if data.get("is_honeypot") == "1":
            risks.append("HONEYPOT DETECTED")
        if data.get("is_blacklisted") == "1":
            risks.append("BLACKLISTED TOKEN")
        if data.get("can_take_back_ownership") == "1":
            risks.append("Owner can reclaim ownership")
        if data.get("hidden_owner") == "1":
            risks.append("Hidden owner detected")
        if data.get("selfdestruct") == "1":
            risks.append("Self-destruct function")

        # Warnings
        if data.get("is_proxy") == "1":
            warnings.append("Proxy contract (upgradeable)")
        if data.get("is_mintable") == "1":
            warnings.append("Mintable token")
        if data.get("external_call") == "1":
            warnings.append("External calls in contract")

        # Tax analysis
        buy_tax = float(data.get("buy_tax", "0") or "0") * 100
        sell_tax = float(data.get("sell_tax", "0") or "0") * 100

        if buy_tax > 10:
            warnings.append(f"High buy tax: {buy_tax:.1f}%")
        if sell_tax > 10:
            risks.append(f"High sell tax: {sell_tax:.1f}%")
        if sell_tax > 50:
            risks.append("EXTREME SELL TAX - LIKELY SCAM")

        risk_level = "HIGH" if risks else ("MEDIUM" if warnings else "LOW")

        report = f"""
TOKEN SECURITY REPORT
{'='*50}
Address: {address}
Risk Level: {risk_level}

Token Info:
- Name: {data.get('token_name', 'Unknown')}
- Symbol: {data.get('token_symbol', 'Unknown')}
- Holders: {data.get('holder_count', 'Unknown')}

Taxes:
- Buy Tax: {buy_tax:.1f}%
- Sell Tax: {sell_tax:.1f}%
"""

        if risks:
            report += f"\nCRITICAL RISKS:\n"
            for risk in risks:
                report += f"  - {risk}\n"

        if warnings:
            report += f"\nWARNINGS:\n"
            for warning in warnings:
                report += f"  - {warning}\n"

        return report


async def main():
    tool = TokenSecurityTool()
    # Example: Check USDC
    result = await tool.execute(
        token_address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        chain="ethereum"
    )
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
