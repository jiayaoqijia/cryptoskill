#!/usr/bin/env python3
"""BaseTool implementation examples."""

import aiohttp
from typing import Optional, Any
from spoon_ai.tools.base import BaseTool, ToolResult, ToolFailure
from pydantic import Field


class CoinGeckoTool(BaseTool):
    """Tool for fetching cryptocurrency prices from CoinGecko."""

    name: str = "get_crypto_price"
    description: str = "Get current cryptocurrency price from CoinGecko API"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "coin_id": {
                "type": "string",
                "description": "CoinGecko coin ID (e.g., 'bitcoin', 'ethereum')"
            },
            "currency": {
                "type": "string",
                "description": "Target currency (e.g., 'usd', 'eur')",
                "default": "usd"
            }
        },
        "required": ["coin_id"]
    })

    base_url: str = "https://api.coingecko.com/api/v3"
    timeout: int = 30

    async def execute(self, coin_id: str, currency: str = "usd") -> str:
        url = f"{self.base_url}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": currency,
            "include_24hr_change": "true"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as resp:
                    if resp.status != 200:
                        return f"Error: API returned status {resp.status}"

                    data = await resp.json()

                    if coin_id not in data:
                        return f"Error: Coin '{coin_id}' not found"

                    price = data[coin_id][currency]
                    change = data[coin_id].get(f"{currency}_24h_change", 0)

                    return (
                        f"{coin_id.upper()} Price: ${price:,.2f} {currency.upper()}\n"
                        f"24h Change: {change:+.2f}%"
                    )

        except aiohttp.ClientError as e:
            return f"Network error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"


class SafeTool(BaseTool):
    """Tool with comprehensive error handling."""

    name: str = "safe_operation"
    description: str = "Safely execute operations with validation"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "data": {"type": "string"}
        },
        "required": ["data"]
    })

    async def execute(self, **kwargs) -> Any:
        # Input validation
        error = self._validate_inputs(**kwargs)
        if error:
            return ToolFailure(error)

        try:
            result = await self._do_operation(**kwargs)
            return ToolResult(output=result)
        except ValueError as e:
            return ToolFailure(f"Invalid input: {e}")
        except ConnectionError as e:
            return ToolFailure(f"Connection failed: {e}")
        except Exception as e:
            return ToolFailure(f"Unexpected error: {e}")

    def _validate_inputs(self, **kwargs) -> Optional[str]:
        required = self.parameters.get("required", [])
        for field in required:
            if field not in kwargs:
                return f"Missing required field: {field}"
        return None

    async def _do_operation(self, **kwargs) -> Any:
        return f"Processed: {kwargs.get('data')}"


async def main():
    # Test CoinGecko tool
    price_tool = CoinGeckoTool()
    result = await price_tool.execute(coin_id="bitcoin")
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
