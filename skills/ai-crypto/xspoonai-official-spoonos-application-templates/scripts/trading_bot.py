#!/usr/bin/env python3
"""Trading Bot Agent Template."""

from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from spoon_ai.tools.base import BaseTool
from pydantic import Field


class PriceMonitorTool(BaseTool):
    """Monitor token prices across DEXs."""

    name: str = "price_monitor"
    description: str = "Get current token prices from DEX aggregators"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "token": {"type": "string", "description": "Token symbol or address"},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["token"]
    })

    async def execute(self, token: str, chain: str = "ethereum") -> str:
        # Implementation: fetch from 1inch, DEX aggregators
        return f"Price for {token} on {chain}: $50,000"


class SwapExecutorTool(BaseTool):
    """Execute token swaps with slippage protection."""

    name: str = "swap_executor"
    description: str = "Execute token swap via DEX aggregator"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "from_token": {"type": "string"},
            "to_token": {"type": "string"},
            "amount": {"type": "string"},
            "max_slippage": {"type": "number", "default": 1.0}
        },
        "required": ["from_token", "to_token", "amount"]
    })

    async def execute(self, from_token: str, to_token: str,
                      amount: str, max_slippage: float = 1.0) -> str:
        # Implementation: execute via 1inch/CoW Protocol
        return f"Swap executed: {amount} {from_token} -> {to_token}"


class PositionTrackerTool(BaseTool):
    """Track portfolio positions and PnL."""

    name: str = "position_tracker"
    description: str = "Track open positions and calculate PnL"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["list", "add", "close", "pnl"]}
        },
        "required": ["action"]
    })

    async def execute(self, action: str) -> str:
        if action == "list":
            return "Current positions: ETH: 1.5, USDC: 5000"
        elif action == "pnl":
            return "Total PnL: +$1,234.56 (24h: +2.5%)"
        return f"Action {action} completed"


class TradingAgent(SpoonReactMCP):
    """Automated DeFi trading agent."""

    name = "trading_bot"
    description = "Automated DeFi trading agent"

    system_prompt = """You are a DeFi trading assistant.

    CAPABILITIES:
    - Monitor token prices across DEXs
    - Execute swaps with slippage protection
    - Track portfolio positions and PnL

    RULES:
    - Always check price impact before swaps
    - Never exceed configured max slippage
    - Log all transactions for audit
    - Verify token security before trading
    """

    max_steps = 10

    def __init__(self):
        super().__init__(
            llm=ChatBot(model_name="gpt-4o"),
            tools=ToolManager([
                PriceMonitorTool(),
                SwapExecutorTool(),
                PositionTrackerTool()
            ])
        )


async def main():
    agent = TradingAgent()
    result = await agent.run("Check current ETH price and my positions")
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
