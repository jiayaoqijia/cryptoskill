from __future__ import annotations

import os
from datetime import date
from typing import Any

from .base import ModuleResult, build_result


SOURCES = {
    "fear_greed": "Alternative.me /fng/; CoinMarketCap fallback",
    "optional_trader_positions": "OKX CLI smart-money endpoints",
    "optional_news_sentiment": "OKX CLI news sentiment endpoint",
}


def collect(engine: Any, target: date) -> ModuleResult:
    gaps: list[str] = []
    warnings: list[str] = []
    fng, fng_series = engine._fetch_fng(target, gaps, lookback_days=2)
    traders, signals, attempted, positions = engine._fetch_okx_smartmoney(warnings)
    news_enabled = (os.getenv("OKX_NEWS_SENTIMENT_ENABLED", "0").strip() or "0").lower() in {"1", "true", "yes", "on"}
    news = engine._fetch_okx_news_sentiment(warnings) if news_enabled else {"rows": []}
    return build_result(
        "sentiment",
        target,
        {
            "fng": fng,
            "fng_series": fng_series,
            "smartmoney_traders": traders,
            "smartmoney_signals": signals,
            "smartmoney_signal_attempted": attempted,
            "smartmoney_positions": positions,
            "okx_news_sentiment": news,
        },
        gaps,
        warnings,
        SOURCES,
    )
