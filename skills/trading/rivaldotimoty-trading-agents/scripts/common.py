"""Shared helpers for the trading-agents skill scripts.

Market detection, benchmark mapping, currency, annualisation factors and
Indonesia Stock Exchange (IDX) price-tick / lot rules.
"""
from __future__ import annotations

import math
import re

# suffix -> (market code, benchmark ticker, currency)
SUFFIX_MARKETS = {
    ".JK": ("idx", "^JKSE", "IDR"),
    ".HK": ("hk", "^HSI", "HKD"),
    ".T": ("jp", "^N225", "JPY"),
    ".L": ("uk", "^FTSE", "GBP"),
    ".NS": ("in", "^NSEI", "INR"),
    ".BO": ("in", "^BSESN", "INR"),
    ".TO": ("ca", "^GSPTSE", "CAD"),
    ".AX": ("au", "^AXJO", "AUD"),
    ".SS": ("cn", "000001.SS", "CNY"),
    ".SZ": ("cn", "399001.SZ", "CNY"),
    ".SI": ("sg", "^STI", "SGD"),
    ".KL": ("my", "^KLSE", "MYR"),
    ".KS": ("kr", "^KS11", "KRW"),
    ".TW": ("tw", "^TWII", "TWD"),
}

CRYPTO_QUOTES = ("-USD", "-USDT", "-USDC", "-IDR", "-EUR", "-BTC", "-ETH")

CRYPTO_ALIASES = {
    "BITCOIN": "BTC-USD", "BTC": "BTC-USD",
    "ETHEREUM": "ETH-USD", "ETH": "ETH-USD",
    "SOLANA": "SOL-USD", "SOL": "SOL-USD",
    "BNB": "BNB-USD", "XRP": "XRP-USD", "DOGE": "DOGE-USD",
    "ADA": "ADA-USD", "CARDANO": "ADA-USD",
}


def detect_market(ticker: str) -> dict:
    """Return market info for a Yahoo-style ticker."""
    t = ticker.upper().strip()
    if t.endswith(CRYPTO_QUOTES):
        bench = None if t.startswith("BTC-") else "BTC-USD"
        quote = t.split("-")[-1]
        return {"market": "crypto", "benchmark": bench,
                "currency": quote if quote not in ("USDT", "USDC") else "USD",
                "periods_per_year": 365}
    if t.startswith("^"):
        return {"market": "index", "benchmark": None, "currency": None,
                "periods_per_year": 252}
    for suffix, (mkt, bench, ccy) in SUFFIX_MARKETS.items():
        if t.endswith(suffix):
            return {"market": mkt, "benchmark": bench, "currency": ccy,
                    "periods_per_year": 252}
    if re.fullmatch(r"[A-Z.\-]{1,6}", t):
        return {"market": "us", "benchmark": "SPY", "currency": "USD",
                "periods_per_year": 252}
    return {"market": "other", "benchmark": None, "currency": None,
            "periods_per_year": 252}


def normalize_ticker(raw: str, market_hint: str | None = None) -> str:
    """Best-effort normalisation: 'bbca' + idx hint -> 'BBCA.JK', 'bitcoin' -> 'BTC-USD'."""
    t = raw.upper().strip().replace(" ", "")
    if t in CRYPTO_ALIASES and (market_hint in (None, "crypto")):
        if market_hint == "crypto" or t in ("BITCOIN", "ETHEREUM", "SOLANA", "CARDANO"):
            return CRYPTO_ALIASES[t]
    if market_hint == "crypto" and "-" not in t:
        return f"{t}-USD"
    if market_hint == "idx" and "." not in t and re.fullmatch(r"[A-Z]{4}", t):
        return f"{t}.JK"
    return t


# ---------------------------------------------------------------- IDX rules
# Fraksi harga (price tick) for IDX equities. Verify against the latest IDX
# regulation if in doubt; these have been stable for years.
IDX_TICKS = [(200, 1), (500, 2), (2000, 5), (5000, 10), (math.inf, 25)]
IDX_LOT = 100  # shares per lot


def idx_tick(price: float) -> int:
    for upper, tick in IDX_TICKS:
        if price < upper:
            return tick
    return 25


def round_to_tick(price: float, market: str, mode: str = "nearest") -> float:
    """Round a price to a valid tick. mode: nearest | down | up."""
    if price is None or not math.isfinite(price):
        return price
    if market != "idx":
        # generic: 2 decimals above 1, more precision below 1
        nd = 2 if abs(price) >= 1 else 6
        return round(price, nd)
    tick = idx_tick(price)
    q = price / tick
    if mode == "down":
        q = math.floor(q)
    elif mode == "up":
        q = math.ceil(q)
    else:
        q = round(q)
    return float(q * tick)


def lot_size(market: str) -> int:
    return IDX_LOT if market == "idx" else 1


def fmt_num(x, nd: int = 2) -> str:
    """Human formatting with thousands separators; None -> 'n/a'."""
    if x is None:
        return "n/a"
    try:
        if isinstance(x, float) and not math.isfinite(x):
            return "n/a"
    except TypeError:
        return str(x)
    ax = abs(x)
    if ax >= 1e12:
        return f"{x/1e12:.2f}T"
    if ax >= 1e9:
        return f"{x/1e9:.2f}B"
    if ax >= 1e6:
        return f"{x/1e6:.2f}M"
    if ax >= 1000:
        return f"{x:,.0f}"
    if ax >= 1:
        return f"{x:,.{nd}f}"
    return f"{x:.6g}"
