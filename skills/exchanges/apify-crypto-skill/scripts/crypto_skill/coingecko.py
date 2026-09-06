from __future__ import annotations

from pydantic import ValidationError

from crypto_skill.client import run_actor_sync
from crypto_skill.constants import (
    COINGECKO_ACTOR_ID,
    DEFAULT_DATA_LIMIT,
    DEFAULT_HISTORICAL_DAYS,
    DEFAULT_SORT_ORDER,
    DEFAULT_VS_CURRENCY,
    SCRAPE_MODE_CATEGORIES,
    SCRAPE_MODE_COIN_DETAIL,
    SCRAPE_MODE_HISTORICAL,
    SCRAPE_MODE_MARKET_DATA,
    SCRAPE_MODE_SIMPLE_PRICES,
    SCRAPE_MODE_TRENDING,
)
from crypto_skill.exceptions import ActorDataError
from crypto_skill.models import MarketCoin


async def get_simple_prices(
    coin_ids: list[str], vs_currencies: list[str] | None = None
) -> list[MarketCoin]:
    """Fetch price data for specific coins from CoinGecko."""
    currencies = vs_currencies if vs_currencies is not None else [DEFAULT_VS_CURRENCY]
    actor_input = {
        "scrapeMode": SCRAPE_MODE_SIMPLE_PRICES,
        "coinIds": coin_ids,
        "vsCurrencies": currencies,
    }
    items = await run_actor_sync(COINGECKO_ACTOR_ID, actor_input)
    return _parse_market_coins(items)


async def get_market_data(
    vs_currency: str = DEFAULT_VS_CURRENCY,
    category: str | None = None,
    max_results: int = DEFAULT_DATA_LIMIT,
) -> list[MarketCoin]:
    """Fetch market data for top cryptocurrencies from CoinGecko."""
    actor_input: dict[str, object] = {
        "scrapeMode": SCRAPE_MODE_MARKET_DATA,
        "vsCurrency": vs_currency,
        "sortOrder": DEFAULT_SORT_ORDER,
        "maxResults": max_results,
    }
    if category is not None:
        actor_input["category"] = category
    items = await run_actor_sync(COINGECKO_ACTOR_ID, actor_input)
    return _parse_market_coins(items)


async def get_coin_detail(coin_id: str, include_details: bool = True) -> MarketCoin:
    """Fetch detailed data for a specific coin from CoinGecko."""
    actor_input = {
        "scrapeMode": SCRAPE_MODE_COIN_DETAIL,
        "coinIds": [coin_id],
        "includeDetails": include_details,
    }
    items = await run_actor_sync(COINGECKO_ACTOR_ID, actor_input)
    return _extract_single(items, coin_id)


async def get_historical(
    coin_id: str, days: int = DEFAULT_HISTORICAL_DAYS, vs_currency: str = DEFAULT_VS_CURRENCY
) -> MarketCoin:
    """Fetch data for a coin from CoinGecko (historical mode)."""
    actor_input = {
        "scrapeMode": SCRAPE_MODE_HISTORICAL,
        "coinIds": [coin_id],
        "days": days,
        "vsCurrency": vs_currency,
    }
    items = await run_actor_sync(COINGECKO_ACTOR_ID, actor_input)
    return _extract_single(items, coin_id)


async def get_trending() -> list[MarketCoin]:
    """Fetch currently trending cryptocurrencies from CoinGecko."""
    items = await run_actor_sync(COINGECKO_ACTOR_ID, {"scrapeMode": SCRAPE_MODE_TRENDING})
    return _parse_market_coins(items)


async def get_categories() -> list[MarketCoin]:
    """Fetch cryptocurrency data by categories from CoinGecko."""
    items = await run_actor_sync(COINGECKO_ACTOR_ID, {"scrapeMode": SCRAPE_MODE_CATEGORIES})
    return _parse_market_coins(items)


def _parse_market_coins(items: list[dict]) -> list[MarketCoin]:
    """Validate a list of dicts as MarketCoin models."""
    try:
        return [MarketCoin(**item) for item in items]
    except (ValidationError, TypeError) as exc:
        raise ActorDataError(f"Failed to parse MarketCoin: {exc}") from exc


def _extract_single(items: list[dict], identifier: str) -> MarketCoin:
    """Extract and validate a single MarketCoin from the dataset result."""
    if not items:
        raise ActorDataError(f"No data returned for {identifier}")
    try:
        return MarketCoin(**items[0])
    except (ValidationError, TypeError) as exc:
        raise ActorDataError(f"Failed to parse MarketCoin: {exc}") from exc
