from __future__ import annotations

from datetime import date
from typing import Any

from .base import ModuleResult, build_result


SOURCES = {
    "market_history": "CoinMarketCap global metrics historical",
    "top_assets": "CoinGecko /coins/markets; CoinPaprika fallback",
    "exchanges": "CoinMarketCap exchange/quotes/latest",
    "btc_eth_24h": "Binance Global; Binance.US fallback",
}


def collect(engine: Any, target: date) -> ModuleResult:
    gaps: list[str] = []
    warnings: list[str] = []
    market = engine._fetch_market_day(target, gaps, lookback_days=2)
    top_assets, capability = engine._fetch_top_assets(gaps)
    exchanges = engine._fetch_exchanges(gaps)
    top2_trend = engine._fetch_top2_24h_trend(gaps)
    top2_intraday = engine._fetch_top2_1h_series(target, gaps, hours=24)
    breadth = engine._build_breadth_snapshot(market.get("market_cap"), market.get("btc_dom"), top_assets)
    return build_result(
        "market",
        target,
        {
            "market": market,
            "top_assets": top_assets,
            "coingecko_capability": capability,
            "exchanges": exchanges,
            "top2_trend": top2_trend,
            "top2_intraday": top2_intraday,
            "breadth_snapshot": breadth,
        },
        gaps,
        warnings,
        SOURCES,
    )
