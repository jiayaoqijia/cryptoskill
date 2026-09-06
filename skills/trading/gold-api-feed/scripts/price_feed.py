"""
Gold API Price Feed
Real-time precious metals and cryptocurrency prices
Compatible with Claude Code and OpenClaw MCP

API key required — get yours free at https://gold-api.com
Docs: https://gold-api.com/docs
"""

import os
import aiohttp
import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path

# Load .env file if present (works without python-dotenv)
def _load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())

_load_env()


@dataclass
class PriceData:
    """Price data structure"""
    symbol: str
    name: str
    price: float
    currency: str
    updated_at: datetime
    updated_readable: str


class GoldAPIFeed:
    """
    Real-time price feed from gold-api.com

    Requires a free API key from https://gold-api.com
    Set GOLD_API_KEY in your .env file (see .env.example)

    Features:
    - 60-second caching to prevent rate limiting
    - Support for XAU, XAG, BTC, ETH, XPD, XPT, HG
    - Async/await compatible
    - Graceful fallback to cached data on network errors
    """

    BASE_URL = "https://api.gold-api.com"
    CACHE_DURATION = 60  # seconds

    ASSETS = {
        "XAU": {"name": "Gold",      "type": "Precious Metal"},
        "XAG": {"name": "Silver",    "type": "Precious Metal"},
        "BTC": {"name": "Bitcoin",   "type": "Cryptocurrency"},
        "ETH": {"name": "Ethereum",  "type": "Cryptocurrency"},
        "XPD": {"name": "Palladium", "type": "Precious Metal"},
        "XPT": {"name": "Platinum",  "type": "Precious Metal"},
        "HG":  {"name": "Copper",    "type": "Industrial Metal"},
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the price feed.

        Args:
            api_key: Your gold-api.com API key.
                     If not provided, reads from GOLD_API_KEY environment variable.
                     Get your free key at https://gold-api.com
        """
        self.api_key = api_key or os.environ.get("GOLD_API_KEY")
        if not self.api_key or self.api_key == "your_api_key_here":
            raise ValueError(
                "\n\n[gold-api-feed] API key required.\n"
                "  1. Sign up for free at https://gold-api.com\n"
                "  2. Copy your API key from https://gold-api.com/docs\n"
                "  3. Add it to your .env file:\n"
                "       GOLD_API_KEY=your_key_here\n"
                "  See .env.example for the full template.\n"
            )
        self._cache: Dict[str, tuple] = {}

    def _headers(self) -> dict:
        return {
            "x-access-token": self.api_key,
            "Content-Type": "application/json",
        }

    async def get_price(self, symbol: str) -> Optional[PriceData]:
        """
        Fetch current price for a symbol.

        Args:
            symbol: Asset symbol (XAU, XAG, BTC, ETH, XPD, XPT, HG)

        Returns:
            PriceData or None if fetch failed
        """
        symbol = symbol.upper()
        now = datetime.now()

        # Return from cache if fresh
        if symbol in self._cache:
            cached_time, cached_data = self._cache[symbol]
            if (now - cached_time).total_seconds() < self.CACHE_DURATION:
                return cached_data

        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}/price/{symbol}"
                async with session.get(url, headers=self._headers(), timeout=10) as response:
                    if response.status == 401:
                        raise ValueError(
                            "Invalid API key. Get yours free at https://gold-api.com"
                        )
                    if response.status == 200:
                        data = await response.json()
                        price_data = PriceData(
                            symbol=data["symbol"],
                            name=data["name"],
                            price=float(data["price"]),
                            currency=data["currency"],
                            updated_at=datetime.fromisoformat(
                                data["updatedAt"].replace("Z", "+00:00")
                            ),
                            updated_readable=data["updatedAtReadable"],
                        )
                        self._cache[symbol] = (now, price_data)
                        return price_data

        except ValueError:
            raise
        except Exception as e:
            print(f"[gold-api-feed] Error fetching {symbol}: {e}")

        # Graceful fallback to stale cache
        if symbol in self._cache:
            return self._cache[symbol][1]

        return None

    async def get_all_prices(self) -> Dict[str, PriceData]:
        """Fetch prices for all supported assets concurrently."""
        tasks = [self.get_price(symbol) for symbol in self.ASSETS]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {
            symbol: result
            for symbol, result in zip(self.ASSETS, results)
            if isinstance(result, PriceData)
        }

    def format_price(self, data: PriceData) -> str:
        return f"{data.name} ({data.symbol}/USD): ${data.price:,.2f} (updated {data.updated_readable})"

    async def get_gold_price(self) -> Optional[PriceData]:
        return await self.get_price("XAU")

    async def get_bitcoin_price(self) -> Optional[PriceData]:
        return await self.get_price("BTC")

    async def get_silver_price(self) -> Optional[PriceData]:
        return await self.get_price("XAG")


# Sync wrappers
def get_price_sync(symbol: str) -> Optional[PriceData]:
    return asyncio.run(GoldAPIFeed().get_price(symbol))

def get_all_prices_sync() -> Dict[str, PriceData]:
    return asyncio.run(GoldAPIFeed().get_all_prices())


if __name__ == "__main__":
    async def test():
        feed = GoldAPIFeed()
        print("=== Gold API Price Feed ===\n")
        prices = await feed.get_all_prices()
        for symbol, data in prices.items():
            print(feed.format_price(data))

    asyncio.run(test())
