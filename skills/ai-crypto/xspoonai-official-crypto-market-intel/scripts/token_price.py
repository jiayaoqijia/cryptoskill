#!/usr/bin/env python3
"""Token price analysis script.

Provides detailed price data for a specific token including historical context,
simple moving averages, and trend direction.

Input (JSON via stdin):
    {"token": "bitcoin", "timeframe": "7d"}

Output (JSON via stdout):
    Comprehensive price data with trend analysis.
"""

import json
import sys
import urllib.request
import urllib.error
import time
from datetime import datetime, timezone
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COINGECKO_BASE = "https://api.coingecko.com/api/v3"

VALID_TIMEFRAMES = {"24h": 1, "7d": 7, "30d": 30, "90d": 90}

# Common symbol -> CoinGecko ID mappings for convenience
SYMBOL_MAP: dict[str, str] = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "ada": "cardano",
    "avax": "avalanche-2",
    "dot": "polkadot",
    "matic": "matic-network",
    "pol": "polygon-ecosystem-token",
    "link": "chainlink",
    "uni": "uniswap",
    "aave": "aave",
    "doge": "dogecoin",
    "shib": "shiba-inu",
    "arb": "arbitrum",
    "op": "optimism",
    "atom": "cosmos",
    "near": "near",
    "apt": "aptos",
    "sui": "sui",
    "ton": "toncoin",
    "mkr": "maker",
    "crv": "curve-dao-token",
    "comp": "compound-governance-token",
    "snx": "synthetix-network-token",
    "xrp": "ripple",
    "bnb": "binancecoin",
    "trx": "tron",
    "ftm": "fantom",
    "pepe": "pepe",
    "bonk": "bonk",
    "floki": "floki",
    "wif": "dogwifcoin",
    "imx": "immutable-x",
    "sand": "the-sandbox",
    "mana": "decentraland",
    "axs": "axie-infinity",
    "gala": "gala",
}

MAX_RETRIES = 3
RETRY_DELAYS = [2, 4, 8]
REQUEST_TIMEOUT = 15

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def _fetch_json(url: str) -> Any:
    """Fetch JSON from *url* with retry logic for rate limiting."""
    headers = {
        "Accept": "application/json",
        "User-Agent": "SpoonOS-MarketIntel/1.0",
    }
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAYS[attempt])
                continue
            raise
        except urllib.error.URLError:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAYS[attempt])
                continue
            raise
    return None


# ---------------------------------------------------------------------------
# Token resolution
# ---------------------------------------------------------------------------


def _resolve_token(query: str) -> str:
    """Resolve a token query to a CoinGecko ID.

    Accepts:
      - CoinGecko ID directly (e.g., "bitcoin")
      - Common symbol (e.g., "BTC")
      - Name with spaces (e.g., "Shiba Inu")
    """
    q = query.strip().lower()

    # Check symbol map first
    if q in SYMBOL_MAP:
        return SYMBOL_MAP[q]

    # If it looks like a CoinGecko slug already, return as-is
    if q.replace("-", "").replace("_", "").isalnum():
        return q

    # Convert name to slug format
    return q.replace(" ", "-")


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------


def _format_price(price: Optional[float]) -> Optional[float]:
    """Format price to appropriate decimal places."""
    if price is None:
        return None
    if price >= 1:
        return round(price, 2)
    if price >= 0.01:
        return round(price, 4)
    return round(price, 8)


def _calc_sma(prices: list[float], window: int) -> Optional[float]:
    """Calculate Simple Moving Average over the last *window* data points."""
    if not prices or len(prices) < window:
        return None
    subset = prices[-window:]
    return round(sum(subset) / len(subset), 2)


def _determine_trend(
    current_price: float,
    sma_7: Optional[float],
    sma_30: Optional[float],
    change_7d: Optional[float],
) -> tuple[str, str]:
    """Determine trend direction and reasoning."""
    signals: list[str] = []
    bullish = 0
    bearish = 0

    if sma_7 is not None:
        if current_price > sma_7:
            bullish += 1
            signals.append("Price above 7-day SMA")
        else:
            bearish += 1
            signals.append("Price below 7-day SMA")

    if sma_30 is not None:
        if current_price > sma_30:
            bullish += 1
            signals.append("Price above 30-day SMA")
        else:
            bearish += 1
            signals.append("Price below 30-day SMA")

    if change_7d is not None:
        if change_7d > 3:
            bullish += 1
            signals.append(f"Positive 7d momentum ({change_7d:+.1f}%)")
        elif change_7d < -3:
            bearish += 1
            signals.append(f"Negative 7d momentum ({change_7d:+.1f}%)")
        else:
            signals.append(f"Flat 7d momentum ({change_7d:+.1f}%)")

    if bullish > bearish:
        trend = "bullish"
    elif bearish > bullish:
        trend = "bearish"
    else:
        trend = "neutral"

    reason = ". ".join(signals) if signals else "Insufficient data for trend analysis"
    return trend, reason


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------


def get_token_price(token: str, timeframe: str = "24h") -> dict[str, Any]:
    """Fetch detailed price data for a token."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    coin_id = _resolve_token(token)
    days = VALID_TIMEFRAMES.get(timeframe, 1)

    # Fetch coin detail
    detail_url = (
        f"{COINGECKO_BASE}/coins/{coin_id}"
        f"?localization=false&tickers=false&community_data=false&developer_data=false"
    )
    try:
        detail = _fetch_json(detail_url)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {
                "status": "error",
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": f"Token '{token}' not found on CoinGecko. Try using the full name or CoinGecko ID.",
                },
                "timestamp": now,
            }
        return {
            "status": "error",
            "error": {
                "code": "API_ERROR",
                "message": f"CoinGecko API error (HTTP {exc.code}): {exc.reason}",
            },
            "timestamp": now,
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": {
                "code": "NETWORK_ERROR",
                "message": f"Network error fetching token data: {exc}",
            },
            "timestamp": now,
        }

    if not isinstance(detail, dict) or "market_data" not in detail:
        return {
            "status": "error",
            "error": {
                "code": "API_ERROR",
                "message": "Unexpected response format from CoinGecko.",
            },
            "timestamp": now,
        }

    md = detail["market_data"]

    # Fetch historical price data for SMA calculation
    chart_url = (
        f"{COINGECKO_BASE}/coins/{coin_id}/market_chart"
        f"?vs_currency=usd&days=30"
    )
    prices_list: list[float] = []
    history_summary: Optional[dict[str, Any]] = None

    try:
        chart_data = _fetch_json(chart_url)
        raw_prices = chart_data.get("prices", [])
        prices_list = [p[1] for p in raw_prices if isinstance(p, list) and len(p) == 2]

        if prices_list:
            # Build history summary for the requested timeframe
            tf_prices = prices_list[-days * 24:] if days <= 30 else prices_list
            if tf_prices:
                history_summary = {
                    "timeframe": timeframe,
                    "high": _format_price(max(tf_prices)),
                    "low": _format_price(min(tf_prices)),
                    "avg": _format_price(sum(tf_prices) / len(tf_prices)),
                    "volatility_pct": round(
                        ((max(tf_prices) - min(tf_prices)) / (sum(tf_prices) / len(tf_prices))) * 100, 2
                    ) if tf_prices else None,
                    "data_points": len(tf_prices),
                }
    except Exception:
        pass  # Historical data is supplementary

    current_price = md.get("current_price", {}).get("usd")
    change_7d = md.get("price_change_percentage_7d")
    change_30d = md.get("price_change_percentage_30d")

    # Calculate SMAs from hourly prices (30-day chart gives hourly data)
    sma_7 = _calc_sma(prices_list, 7 * 24) if prices_list else None
    sma_30 = _calc_sma(prices_list, len(prices_list)) if prices_list else None

    # Determine trend
    trend = "neutral"
    trend_reason = "Insufficient data"
    if current_price is not None:
        trend, trend_reason = _determine_trend(current_price, sma_7, sma_30, change_7d)

    # ATH info
    ath = md.get("ath", {}).get("usd")
    ath_date_raw = md.get("ath_date", {}).get("usd", "")
    ath_date = ath_date_raw[:10] if ath_date_raw else None
    ath_distance = md.get("ath_change_percentage", {}).get("usd")

    # ATL info
    atl = md.get("atl", {}).get("usd")
    atl_date_raw = md.get("atl_date", {}).get("usd", "")
    atl_date = atl_date_raw[:10] if atl_date_raw else None

    result = {
        "status": "success",
        "data": {
            "name": detail.get("name", "Unknown"),
            "symbol": (detail.get("symbol") or "").upper(),
            "coingecko_id": detail.get("id", coin_id),
            "current_price": _format_price(current_price),
            "market_cap": md.get("market_cap", {}).get("usd"),
            "market_cap_rank": md.get("market_cap_rank"),
            "total_volume_24h": md.get("total_volume", {}).get("usd"),
            "circulating_supply": md.get("circulating_supply"),
            "total_supply": md.get("total_supply"),
            "max_supply": md.get("max_supply"),
            "ath": _format_price(ath),
            "ath_date": ath_date,
            "ath_distance_pct": round(ath_distance, 2) if ath_distance else None,
            "atl": _format_price(atl),
            "atl_date": atl_date,
            "price_change_24h_pct": round(md.get("price_change_percentage_24h") or 0, 2),
            "price_change_7d_pct": round(change_7d, 2) if change_7d else None,
            "price_change_30d_pct": round(change_30d, 2) if change_30d else None,
            "sma_7": _format_price(sma_7),
            "sma_30": _format_price(sma_30),
            "trend": trend,
            "trend_reason": trend_reason,
            "price_history_summary": history_summary,
            "timestamp": now,
        },
    }
    return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Read JSON input from stdin, execute, write JSON output to stdout."""
    try:
        raw = sys.stdin.read().strip()
        params: dict[str, Any] = json.loads(raw) if raw else {}
    except json.JSONDecodeError as exc:
        json.dump(
            {
                "status": "error",
                "error": {
                    "code": "INVALID_INPUT",
                    "message": f"Malformed JSON input: {exc}",
                },
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            sys.stdout,
            indent=2,
        )
        return

    # Validate required token param
    token = params.get("token")
    if not token or not isinstance(token, str) or not token.strip():
        json.dump(
            {
                "status": "error",
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "Missing required parameter 'token'. Provide a token name, symbol, or CoinGecko ID.",
                },
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            sys.stdout,
            indent=2,
        )
        return

    # Validate timeframe
    timeframe = str(params.get("timeframe", "24h")).lower()
    if timeframe not in VALID_TIMEFRAMES:
        json.dump(
            {
                "status": "error",
                "error": {
                    "code": "INVALID_TIMEFRAME",
                    "message": f"Invalid timeframe '{timeframe}'. Must be one of: {', '.join(VALID_TIMEFRAMES.keys())}",
                },
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            sys.stdout,
            indent=2,
        )
        return

    result = get_token_price(token=token.strip(), timeframe=timeframe)
    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
