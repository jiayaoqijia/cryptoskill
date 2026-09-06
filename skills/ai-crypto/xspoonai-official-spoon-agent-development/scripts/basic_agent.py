#!/usr/bin/env python3
"""Basic SpoonReactAI agent example."""

from spoon_ai.agents import SpoonReactAI
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from spoon_ai.tools.base import BaseTool
from pydantic import Field


class PriceTool(BaseTool):
    """Custom tool for fetching crypto prices."""
    name: str = "get_crypto_price"
    description: str = "Get the current price of a cryptocurrency"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "Cryptocurrency symbol (e.g., BTC, ETH)"
            }
        },
        "required": ["symbol"]
    })

    async def execute(self, symbol: str) -> str:
        # Replace with actual API call
        return f"Price of {symbol}: $50000"


class CryptoAnalysisAgent(SpoonReactAI):
    """Agent specialized for cryptocurrency analysis."""

    name: str = "crypto_analyst"
    description: str = "An AI agent specialized in crypto market analysis"
    max_steps: int = 15
    tool_choice: str = "required"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm = ChatBot(model_name="gpt-4o", llm_provider="openai")
        self.available_tools = ToolManager([PriceTool()])
        self.system_prompt = """You are a cryptocurrency market analyst.
Your role is to:
- Analyze market trends and provide insights
- Fetch real-time price data using available tools
- Explain technical indicators clearly
- Always include risk warnings in trading advice"""


async def main():
    agent = CryptoAnalysisAgent()
    await agent.initialize()
    result = await agent.run("What's the current price of Bitcoin?")
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
