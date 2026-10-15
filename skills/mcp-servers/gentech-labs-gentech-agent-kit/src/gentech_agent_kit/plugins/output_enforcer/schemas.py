"""
Output Enforcer — Shared Schemas

Pydantic models for common Agent Kit tool output shapes.
Each schema corresponds to one tool's return structure.

Use with the @validated_output decorator:
    @mcp.tool()
    @validated_output(schemas.QuoteResponse)
    def get_quote(symbol: str) -> str:
        ...
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


# ── Generic helpers ──────────────────────────────────────────────────────────

def _check_is_number(v: Any) -> Any:
    """Coerce string-encoded numbers. Pydantic strict mode rejects them."""
    if isinstance(v, str):
        try:
            return float(v)
        except (ValueError, TypeError):
            return v
    return v


# ── Quote Tool ───────────────────────────────────────────────────────────────
# Output shape:
#   { "symbol": "BTC", "timestamp": "...", "BTC": { "price": ..., ... } }
# The key that matches symbol is dynamic.

class QuoteData(BaseModel):
    """Per-token quote data (nested under a dynamic symbol key)."""
    price: Optional[float] = None
    v24h_change_pct: Optional[float] = Field(None, alias="24h_change_pct")
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None

    # Accept any extra fields (e.g. other coin data in batch queries)
    model_config = {"extra": "ignore"}

    @field_validator("price", "market_cap", "volume_24h", mode="before")
    @classmethod
    def _coerce_numbers(cls, v):
        return _check_is_number(v)


class QuoteResponse(BaseModel):
    """Expected shape of get_quote() output."""
    symbol: str
    timestamp: Optional[str] = None

    # The rest is per-symbol data; validate it loosely
    model_config = {"extra": "allow"}

    def get_quote_data(self, sym: str | None = None) -> QuoteData | None:
        """Extract QuoteData for a specific symbol."""
        key = sym or self.symbol
        raw = getattr(self, key, None)
        if raw and isinstance(raw, dict):
            return QuoteData(**raw)
        return None


# ── Listings Tool ────────────────────────────────────────────────────────────

class TokenListing(BaseModel):
    """A single token in the listings output."""
    rank: Optional[int] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    v24h_change_pct: Optional[float] = Field(None, alias="24h_change_pct")
    market_cap: Optional[float] = None

    model_config = {"extra": "ignore", "populate_by_name": True}

    @field_validator("price", "market_cap", mode="before")
    @classmethod
    def _coerce_numbers(cls, v):
        return _check_is_number(v)


class ListingsResponse(BaseModel):
    """Expected shape of get_listings() output."""
    count: int
    tokens: list[TokenListing]


# ── Search Tool ──────────────────────────────────────────────────────────────

class TokenInfo(BaseModel):
    """Token metadata from search_token()."""
    name: Optional[str] = None
    symbol: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    date_added: Optional[str] = None
    platform: Optional[dict[str, Any] | str] = None
    tags: list[str] = []

    model_config = {"extra": "ignore"}


class SearchResponse(BaseModel):
    """Expected shape of search_token() output."""
    data: dict[str, TokenInfo]


# ── Trending Tool ────────────────────────────────────────────────────────────

class TrendingItem(BaseModel):
    """A single trending token."""
    symbol: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    change_24h_pct: Optional[float] = None

    model_config = {"extra": "ignore"}

    @field_validator("price", mode="before")
    @classmethod
    def _coerce_numbers(cls, v):
        return _check_is_number(v)


class TrendingResponse(BaseModel):
    """Expected shape of get_trending() output."""
    kind: str
    count: int
    results: list[TrendingItem]

    @field_validator("count", mode="before")
    @classmethod
    def _coerce_count(cls, v):
        return int(v) if isinstance(v, str) else v


# ── DEX Pairs Tool ───────────────────────────────────────────────────────────

class DexPair(BaseModel):
    """A single DEX trading pair."""
    exchange: Optional[str] = None
    pair: Optional[str] = None
    price: Optional[float] = None
    volume_24h_usd: Optional[float] = None
    liquidity_usd: Optional[float] = None
    price_change_24h_pct: Optional[float] = None

    model_config = {"extra": "ignore"}

    @field_validator("price", "volume_24h_usd", "liquidity_usd", mode="before")
    @classmethod
    def _coerce_numbers(cls, v):
        return _check_is_number(v)


class DexPairsResponse(BaseModel):
    """Expected shape of get_dex_pairs() output."""
    symbol: str
    count: int
    pairs: list[DexPair]


# ── Kit Info Tool ────────────────────────────────────────────────────────────

class KitInfoResponse(BaseModel):
    """Expected shape of kit_info() output."""
    name: str
    version: str
    description: Optional[str] = None
    tools: list[str]
    plugins: int
    plugins_list: list[str]
    updates: Optional[str] = None
    docs: Optional[str] = None


# ── Error Response ───────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    """A generic error response from any tool."""
    error: str


# ── Enum for discovery ───────────────────────────────────────────────────────

__all__ = [
    "QuoteResponse",
    "ListingsResponse",
    "SearchResponse",
    "TrendingResponse",
    "DexPairsResponse",
    "KitInfoResponse",
    "ErrorResponse",
    "QuoteData",
    "TokenListing",
    "TokenInfo",
    "TrendingItem",
    "DexPair",
]
