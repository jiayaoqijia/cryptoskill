from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .contracts import ExecutionAdapter, MarketDataAdapter, NewsAdapter


@dataclass(frozen=True)
class MockExecutionAdapter(ExecutionAdapter):
    name: str = "mock-execution"

    def place_order(self, order: dict[str, Any]) -> dict[str, Any]:
        avg_fill_price = order.get("limit_price")
        if avg_fill_price is None:
            avg_fill_price = 100.0
        return {
            "venue": self.name,
            "status": "filled",
            "symbol": order.get("symbol"),
            "side": order.get("side"),
            "qty": order.get("qty"),
            "avg_fill_price": avg_fill_price,
        }


@dataclass(frozen=True)
class MockMarketDataAdapter(MarketDataAdapter):
    name: str = "mock-market-data"

    def get_latest_quote(self, symbol: str) -> dict[str, Any]:
        return {"symbol": symbol, "bid": 99.5, "ask": 100.5, "last": 100.0}


@dataclass(frozen=True)
class MockNewsAdapter(NewsAdapter):
    name: str = "mock-news"

    def get_headlines(self, topic: str, limit: int = 10) -> list[dict[str, Any]]:
        return [
            {"topic": topic, "headline": f"Mock headline {i + 1}", "sentiment": "neutral"}
            for i in range(limit)
        ]
