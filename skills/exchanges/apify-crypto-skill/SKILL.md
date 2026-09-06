---
name: crypto-skill
description: Fetch live cryptocurrency data from KuCoin and CoinGecko via Apify actors. Use when the user asks for crypto prices, OHLCV candlestick data, market cap rankings, trending coins, or any cryptocurrency market data. Provides 9 async Python functions for KuCoin (OHLCV, realtime prices) and CoinGecko (market data, trending, categories, coin details, historical data, simple prices).
---

# Crypto Skill

Async Python functions that fetch live cryptocurrency data via Apify actors. Requires `APIFY_API_TOKEN` environment variable.

## Setup

Install the package from the skill's bundled source:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/install.sh
```

Ensure `APIFY_API_TOKEN` is set (from `.env` or environment).

## Quick Start

```python
import asyncio
from crypto_skill import get_ohlcv, get_realtime_price, get_market_data, get_trending

async def main():
    # KuCoin OHLCV candles
    candles = await get_ohlcv("BTC/USDT", "15m", limit=10)
    for c in candles:
        print(f"{c.date} O={c.open} H={c.high} L={c.low} C={c.close}")

    # Current price
    price = await get_realtime_price("ETH/USDT")
    print(f"{price.symbol} = ${price.price:,.2f}")

    # Top coins by market cap
    coins = await get_market_data(max_results=5)
    for c in coins:
        print(f"{c.name} ${c.current_price:,.2f} Rank #{c.market_cap_rank}")

    # Trending coins
    trending = await get_trending()
    for c in trending[:5]:
        print(f"{c.name} 24h: {c.price_change_percentage_24h:.2f}%")

asyncio.run(main())
```

## Available Functions

### KuCoin (via Crypto Data Scraper actor)

| Function | Returns | Use for |
|----------|---------|---------|
| `get_ohlcv(symbol, timeframe, limit=100)` | `list[OHLCVCandle]` | Candlestick chart data |
| `get_realtime_price(symbol)` | `RealtimePrice` | Current price of a pair |
| `get_all_coins_ohlcv(timeframe, limit=100)` | `list[OHLCVCandle]` | All coins OHLCV (slow) |

**Timeframes:** `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`

### CoinGecko (via Crypto Intelligence actor)

All return `MarketCoin` or `list[MarketCoin]`.

| Function | Returns | Use for |
|----------|---------|---------|
| `get_simple_prices(coin_ids, vs_currencies=None)` | `list[MarketCoin]` | Specific coin prices |
| `get_market_data(vs_currency, category, max_results)` | `list[MarketCoin]` | Top coins ranked |
| `get_coin_detail(coin_id, include_details=True)` | `MarketCoin` | Single coin deep data |
| `get_historical(coin_id, days=30, vs_currency)` | `MarketCoin` | Coin historical mode |
| `get_trending()` | `list[MarketCoin]` | Currently trending coins |
| `get_categories()` | `list[MarketCoin]` | Coins by categories |

## Error Handling

```python
from crypto_skill import get_ohlcv, ApifyAuthError, ApifyTimeoutError, ActorDataError

try:
    candles = await get_ohlcv("BTC/USDT", "15m")
except ApifyAuthError:
    print("Set APIFY_API_TOKEN environment variable")
except ApifyTimeoutError:
    print("Actor run exceeded 300s — try smaller limit")
except ActorDataError as e:
    print(f"Unexpected response format: {e}")
```

## Detailed API Reference

For complete function signatures, model fields, and coin ID lists, see [api-reference.md](references/api-reference.md).
