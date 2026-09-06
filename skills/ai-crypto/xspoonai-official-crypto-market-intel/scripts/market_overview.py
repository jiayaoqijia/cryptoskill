#!/usr/bin/env python3
"""Market overview script.

Provides a comprehensive crypto market snapshot combining data from CoinGecko,
Fear & Greed Index, and DeFiLlama.

Input (JSON via stdin):
    {} or {"include_defi": true}

Output (JSON via stdout):
    Full market snapshot with sentiment analysis.
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
FEAR_GREED_URL = "https://api.alternative.me/fng/?limit=1"
DEFILLAMA_PROTOCOLS_URL = "https://api.llama.fi/protocols"

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
# Data fetchers
# ---------------------------------------------------------------------------


def _fetch_global_data() -> Optional[dict[str, Any]]:
    """Fetch global crypto market data from CoinGecko."""
    try:
        data = _fetch_json(f"{COINGECKO_BASE}/global")
        return data.get("data") if isinstance(data, dict) else None
    except Exception:
        return None


def _fetch_fear_greed() -> Optional[dict[str, Any]]:
    """Fetch current Fear & Greed Index."""
    try:
        data = _fetch_json(FEAR_GREED_URL)
        if isinstance(data, dict) and data.get("data"):
            entry = data["data"][0]
            return {
                "value": int(entry.get("value", 0)),
                "label": entry.get("value_classification", "Unknown"),
                "timestamp": entry.get("timestamp", ""),
            }
    except Exception:
        pass
    return None


def _fetch_top_movers() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Fetch top gainers and losers from CoinGecko markets."""
    gainers: list[dict[str, Any]] = []
    losers: list[dict[str, Any]] = []
    try:
        # Fetch top 250 by market cap for a broad view
        url = (
            f"{COINGECKO_BASE}/coins/markets?vs_currency=usd"
            f"&order=market_cap_desc&per_page=250&page=1&sparkline=false"
        )
        tokens = _fetch_json(url)
        if not isinstance(tokens, list):
            return gainers, losers

        # Sort by 24h change
        valid = [
            t for t in tokens
            if t.get("price_change_percentage_24h") is not None
        ]
        valid.sort(key=lambda x: x["price_change_percentage_24h"], reverse=True)

        for t in valid[:5]:
            gainers.append({
                "name": t.get("name", "Unknown"),
                "symbol": (t.get("symbol") or "").upper(),
                "change_24h_pct": round(t["price_change_percentage_24h"], 2),
                "current_price": t.get("current_price"),
            })

        for t in valid[-5:]:
            losers.append({
                "name": t.get("name", "Unknown"),
                "symbol": (t.get("symbol") or "").upper(),
                "change_24h_pct": round(t["price_change_percentage_24h"], 2),
                "current_price": t.get("current_price"),
            })
        losers.sort(key=lambda x: x["change_24h_pct"])

    except Exception:
        pass
    return gainers, losers


def _fetch_defi_data() -> Optional[dict[str, Any]]:
    """Fetch DeFi TVL data from DeFiLlama."""
    try:
        protocols = _fetch_json(DEFILLAMA_PROTOCOLS_URL)
        if not isinstance(protocols, list):
            return None

        total_tvl = sum(p.get("tvl", 0) for p in protocols if isinstance(p.get("tvl"), (int, float)))

        # Sort by TVL for top protocols
        protocols.sort(key=lambda x: x.get("tvl", 0), reverse=True)
        top_protocols = []
        for p in protocols[:10]:
            change_1d = p.get("change_1d")
            top_protocols.append({
                "name": p.get("name", "Unknown"),
                "tvl": round(p.get("tvl", 0)),
                "change_24h_pct": round(change_1d, 2) if isinstance(change_1d, (int, float)) else None,
                "category": p.get("category", "Unknown"),
                "chain": p.get("chain", "Multi-chain") if isinstance(p.get("chain"), str) else "Multi-chain",
            })

        return {
            "total_tvl": round(total_tvl),
            "protocol_count": len(protocols),
            "top_protocols": top_protocols,
        }
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Sentiment analysis
# ---------------------------------------------------------------------------


def _generate_sentiment(
    global_data: Optional[dict[str, Any]],
    fear_greed: Optional[dict[str, Any]],
) -> str:
    """Generate a market sentiment summary from available data."""
    parts: list[str] = []

    if fear_greed:
        val = fear_greed["value"]
        label = fear_greed["label"]
        if val >= 75:
            parts.append(f"The market is in an Extreme Greed phase ({val}/100), indicating strong bullish sentiment but potential overheating.")
        elif val >= 55:
            parts.append(f"The market is in a {label} phase ({val}/100), reflecting moderate optimism.")
        elif val >= 45:
            parts.append(f"The market sentiment is neutral ({val}/100), with no strong directional bias.")
        elif val >= 25:
            parts.append(f"The market is in a {label} phase ({val}/100), indicating caution among investors.")
        else:
            parts.append(f"The market is in Extreme Fear ({val}/100), which historically has been a contrarian buying signal.")

    if global_data:
        btc_dom = global_data.get("market_cap_percentage", {}).get("btc", 0)
        mc_change = global_data.get("market_cap_change_percentage_24h_usd", 0)

        if btc_dom > 55:
            parts.append(f"BTC dominance at {btc_dom:.1f}% suggests a risk-off environment within crypto, with capital concentrating in Bitcoin.")
        elif btc_dom < 40:
            parts.append(f"BTC dominance at {btc_dom:.1f}% indicates an altcoin-favorable environment.")
        else:
            parts.append(f"BTC dominance at {btc_dom:.1f}% shows a balanced market.")

        if mc_change > 3:
            parts.append(f"Total market cap is up {mc_change:.1f}% in 24h, showing strong buying pressure.")
        elif mc_change < -3:
            parts.append(f"Total market cap is down {mc_change:.1f}% in 24h, indicating selling pressure.")

    if not parts:
        return "Insufficient data to generate sentiment analysis."

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------


def get_market_overview(include_defi: bool = True) -> dict[str, Any]:
    """Build a comprehensive market overview."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Fetch all data sources
    global_data = _fetch_global_data()
    fear_greed = _fetch_fear_greed()
    gainers, losers = _fetch_top_movers()

    if global_data is None:
        return {
            "status": "error",
            "error": {
                "code": "API_ERROR",
                "message": "Failed to fetch global market data from CoinGecko.",
            },
            "timestamp": now,
        }

    result_data: dict[str, Any] = {
        "total_market_cap": round(global_data.get("total_market_cap", {}).get("usd", 0)),
        "total_market_cap_change_24h_pct": round(
            global_data.get("market_cap_change_percentage_24h_usd", 0), 2
        ),
        "total_volume_24h": round(global_data.get("total_volume", {}).get("usd", 0)),
        "btc_dominance": round(global_data.get("market_cap_percentage", {}).get("btc", 0), 2),
        "eth_dominance": round(global_data.get("market_cap_percentage", {}).get("eth", 0), 2),
        "active_cryptocurrencies": global_data.get("active_cryptocurrencies", 0),
        "fear_greed": fear_greed if fear_greed else {"value": None, "label": "Unavailable", "timestamp": ""},
        "top_gainers": gainers,
        "top_losers": losers,
    }

    # Optionally include DeFi data
    if include_defi:
        defi_data = _fetch_defi_data()
        result_data["defi"] = defi_data if defi_data else {
            "total_tvl": None,
            "protocol_count": None,
            "top_protocols": [],
            "note": "DeFi data temporarily unavailable",
        }

    result_data["market_sentiment"] = _generate_sentiment(global_data, fear_greed)
    result_data["timestamp"] = now

    return {
        "status": "success",
        "data": result_data,
    }


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

    include_defi = bool(params.get("include_defi", True))
    result = get_market_overview(include_defi=include_defi)
    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
