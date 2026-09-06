from __future__ import annotations

from pydantic import AliasGenerator, BaseModel, ConfigDict

# --- KuCoin Models ---


class OHLCVCandle(BaseModel):
    """OHLCV candlestick data from KuCoin.

    Actor returns capitalized keys (Date, Open, High, Low, Close, Volume).
    The date field is a string like "2026-03-16 23:15:00".
    Symbol is injected from the request input since the actor doesn't return it.
    """

    model_config = ConfigDict(
        extra="ignore",
        alias_generator=AliasGenerator(validation_alias=str.capitalize),
        populate_by_name=True,
    )

    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    symbol: str = ""


class RealtimePrice(BaseModel):
    model_config = ConfigDict(extra="ignore")

    symbol: str
    price: float
    date: str


# --- CoinGecko Models ---
# The CoinGecko actor returns the same market-data format for all scrape modes.
# MarketCoin is the universal output model.


class MarketCoin(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    symbol: str
    name: str
    current_price: float
    market_cap: float
    market_cap_rank: int
    total_volume: float
    high_24h: float | None = None
    low_24h: float | None = None
    price_change_24h: float | None = None
    price_change_percentage_24h: float | None = None
    circulating_supply: float | None = None
    total_supply: float | None = None
    max_supply: float | None = None
    ath: float | None = None
    atl: float | None = None
    last_updated: str | None = None
