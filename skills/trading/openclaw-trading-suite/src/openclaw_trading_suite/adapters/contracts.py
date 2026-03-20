from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class AdapterType(str, Enum):
    EXECUTION = "execution"
    MARKET_DATA = "market_data"
    NEWS = "news"


@dataclass(frozen=True)
class BaseAdapter(ABC):
    name: str
    adapter_type: AdapterType
    version: str = "v1"


@dataclass(frozen=True)
class ExecutionAdapter(BaseAdapter):
    adapter_type: AdapterType = AdapterType.EXECUTION

    @abstractmethod
    def place_order(self, order: dict[str, Any]) -> dict[str, Any]:
        """Place an order and return normalized execution metadata."""


@dataclass(frozen=True)
class MarketDataAdapter(BaseAdapter):
    adapter_type: AdapterType = AdapterType.MARKET_DATA

    @abstractmethod
    def get_latest_quote(self, symbol: str) -> dict[str, Any]:
        """Return normalized quote data for a symbol."""


@dataclass(frozen=True)
class NewsAdapter(BaseAdapter):
    adapter_type: AdapterType = AdapterType.NEWS

    @abstractmethod
    def get_headlines(self, topic: str, limit: int = 10) -> list[dict[str, Any]]:
        """Return normalized headlines for a topic."""

