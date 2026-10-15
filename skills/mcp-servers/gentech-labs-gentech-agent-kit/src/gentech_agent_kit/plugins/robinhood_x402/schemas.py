"""
Robinhood Chain x402 Plugin — Schemas

Pydantic models for Robinhood Chain data tool outputs.
Compatible with the Output Enforcer plugin for schema validation.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


# ── Network Info ─────────────────────────────────────────────────────────────

class RobinhoodNetworkInfo(BaseModel):
    """Robinhood Chain network and facilitator status."""
    plugin: str
    version: str
    chain_id: int
    chain_name: str
    native_token: str
    settlement_token: str
    settlement_asset: str
    facilitator: str
    status: str
    block_number: Optional[int] = None


# ── Stock Price ──────────────────────────────────────────────────────────────

class StockPrice(BaseModel):
    """A single tokenized stock price on Robinhood Chain."""
    symbol: str
    name: Optional[str] = None
    price_usd: Optional[float] = None
    change_24h_pct: Optional[float] = None
    contract: Optional[str] = None
    source: Optional[str] = None
    updated_at: Optional[str] = None


class StockQuoteResponse(BaseModel):
    """Expected shape of rh_get_stock() output."""
    symbol: str
    price: StockPrice | None = None
    model_config = {"extra": "ignore"}


# ── Stock List ───────────────────────────────────────────────────────────────

class StockListItem(BaseModel):
    """A tokenized stock available on Robinhood Chain."""
    symbol: str
    name: str
    contract: str
    category: str = "stock"


class StockListResponse(BaseModel):
    """Expected shape of rh_list_stocks() output."""
    count: int
    stocks: list[StockListItem]
    chain: str = "Robinhood Chain"


# ── x402 Payment ─────────────────────────────────────────────────────────────

class PaymentStatus(BaseModel):
    """Status of an x402 payment verification."""
    status: str
    session_token: Optional[str] = None
    expires_in: Optional[str] = None
    network: Optional[str] = None


class PaymentError(BaseModel):
    """Payment verification error."""
    status: str = "failed"
    error: str
    network: Optional[str] = None


# ── Crypto Quote (via CMC) ───────────────────────────────────────────────────

class CryptoQuoteItem(BaseModel):
    """A single crypto quote result."""
    price: Optional[float] = None
    change_24h_pct: Optional[float] = Field(None, alias="24h_change_pct")
    market_cap: Optional[float] = None
    volume_24h: Optional[float] = None


class CryptoQuoteResponse(BaseModel):
    """Expected shape of rh_crypto_quote() output."""
    symbol: str
    network: str = "robinhood"
    data: dict[str, CryptoQuoteItem] | None = None
    model_config = {"extra": "allow"}


# ── Enum for discovery ───────────────────────────────────────────────────────

__all__ = [
    "RobinhoodNetworkInfo",
    "StockPrice",
    "StockQuoteResponse",
    "StockListItem",
    "StockListResponse",
    "PaymentStatus",
    "PaymentError",
    "CryptoQuoteItem",
    "CryptoQuoteResponse",
]
