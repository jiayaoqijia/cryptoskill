#!/usr/bin/env python3
"""Token comparison script.

Side-by-side comparison of two tokens across price, volume, market cap,
and performance metrics.

Input (JSON via stdin):
    {"token_a": "bitcoin", "token_b": "ethereum", "timeframe": "24h"}

Output (JSON via stdout):
    Comparison data with per-metric winners and investment summary.
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

VALID_TIMEFRAMES = {"24h", "7d", "30d", "90d"}

# Common symbol -> CoinGecko ID mappings
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
    """Resolve a token query to a CoinGecko ID."""
    q = query.strip().lower()
    if q in SYMBOL_MAP:
        return SYMBOL_MAP[q]
    if q.replace("-", "").replace("_", "").isalnum():
        return q
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


def _fetch_token_data(coin_id: str) -> Optional[dict[str, Any]]:
    """Fetch market data for a single token from CoinGecko."""
    url = (
        f"{COINGECKO_BASE}/coins/{coin_id}"
        f"?localization=false&tickers=false&community_data=false&developer_data=false"
    )
    try:
        data = _fetch_json(url)
        if isinstance(data, dict) and "market_data" in data:
            return data
    except Exception:
        pass
    return None


def _extract_metrics(detail: dict[str, Any]) -> dict[str, Any]:
    """Extract comparison metrics from a CoinGecko coin detail response."""
    md = detail.get("market_data", {})

    current_price = md.get("current_price", {}).get("usd")
    market_cap = md.get("market_cap", {}).get("usd")
    volume = md.get("total_volume", {}).get("usd")
    change_24h = md.get("price_change_percentage_24h")
    change_7d = md.get("price_change_percentage_7d")
    change_30d = md.get("price_change_percentage_30d")
    ath = md.get("ath", {}).get("usd")
    ath_change = md.get("ath_change_percentage", {}).get("usd")

    return {
        "name": detail.get("name", "Unknown"),
        "symbol": (detail.get("symbol") or "").upper(),
        "coingecko_id": detail.get("id", ""),
        "current_price": _format_price(current_price),
        "market_cap": market_cap,
        "volume_24h": volume,
        "price_change_24h_pct": round(change_24h, 2) if change_24h is not None else None,
        "price_change_7d_pct": round(change_7d, 2) if change_7d is not None else None,
        "price_change_30d_pct": round(change_30d, 2) if change_30d is not None else None,
        "ath": _format_price(ath),
        "ath_distance_pct": round(ath_change, 2) if ath_change is not None else None,
        "circulating_supply": md.get("circulating_supply"),
        "total_supply": md.get("total_supply"),
        "max_supply": md.get("max_supply"),
        "market_cap_rank": md.get("market_cap_rank"),
    }


def _determine_winner(
    val_a: Optional[float],
    val_b: Optional[float],
    sym_a: str,
    sym_b: str,
    higher_is_better: bool = True,
) -> str:
    """Determine which token wins a metric comparison."""
    if val_a is None and val_b is None:
        return "N/A"
    if val_a is None:
        return sym_b
    if val_b is None:
        return sym_a
    if val_a == val_b:
        return "Tie"
    if higher_is_better:
        return sym_a if val_a > val_b else sym_b
    return sym_a if val_a < val_b else sym_b


def _build_comparison(
    metrics_a: dict[str, Any],
    metrics_b: dict[str, Any],
    timeframe: str,
) -> dict[str, Any]:
    """Build the comparison section with per-metric winners."""
    sym_a = metrics_a["symbol"]
    sym_b = metrics_b["symbol"]

    # Performance key based on timeframe
    perf_key = {
        "24h": "price_change_24h_pct",
        "7d": "price_change_7d_pct",
        "30d": "price_change_30d_pct",
        "90d": "price_change_30d_pct",  # Fall back to 30d for 90d
    }.get(timeframe, "price_change_24h_pct")

    comparison = {
        "market_cap_winner": _determine_winner(
            metrics_a.get("market_cap"), metrics_b.get("market_cap"), sym_a, sym_b
        ),
        "volume_winner": _determine_winner(
            metrics_a.get("volume_24h"), metrics_b.get("volume_24h"), sym_a, sym_b
        ),
        "24h_performance_winner": _determine_winner(
            metrics_a.get("price_change_24h_pct"), metrics_b.get("price_change_24h_pct"), sym_a, sym_b
        ),
        "7d_performance_winner": _determine_winner(
            metrics_a.get("price_change_7d_pct"), metrics_b.get("price_change_7d_pct"), sym_a, sym_b
        ),
        "30d_performance_winner": _determine_winner(
            metrics_a.get("price_change_30d_pct"), metrics_b.get("price_change_30d_pct"), sym_a, sym_b
        ),
        "closer_to_ath": _determine_winner(
            metrics_a.get("ath_distance_pct"),
            metrics_b.get("ath_distance_pct"),
            sym_a,
            sym_b,
            higher_is_better=True,  # Less negative = closer to ATH = "higher"
        ),
    }
    return comparison


def _build_summary(
    metrics_a: dict[str, Any],
    metrics_b: dict[str, Any],
    comparison: dict[str, Any],
    timeframe: str,
) -> str:
    """Generate a human-readable comparison summary."""
    sym_a = metrics_a["symbol"]
    sym_b = metrics_b["symbol"]
    name_a = metrics_a["name"]
    name_b = metrics_b["name"]

    wins_a = sum(1 for v in comparison.values() if v == sym_a)
    wins_b = sum(1 for v in comparison.values() if v == sym_b)

    parts: list[str] = []

    if wins_a > wins_b:
        parts.append(f"{name_a} leads in {wins_a} out of {len(comparison)} metrics.")
    elif wins_b > wins_a:
        parts.append(f"{name_b} leads in {wins_b} out of {len(comparison)} metrics.")
    else:
        parts.append(f"{name_a} and {name_b} are evenly matched across metrics.")

    # ATH distance insight
    ath_a = metrics_a.get("ath_distance_pct")
    ath_b = metrics_b.get("ath_distance_pct")
    if ath_a is not None and ath_b is not None:
        closer = sym_a if ath_a > ath_b else sym_b
        closer_dist = max(ath_a, ath_b)
        further_dist = min(ath_a, ath_b)
        parts.append(
            f"{closer} is closer to its ATH ({closer_dist:+.1f}%) compared to "
            f"the other ({further_dist:+.1f}%), suggesting stronger recovery."
        )

    # Performance comparison for the requested timeframe
    perf_key = {
        "24h": "price_change_24h_pct",
        "7d": "price_change_7d_pct",
        "30d": "price_change_30d_pct",
    }.get(timeframe, "price_change_24h_pct")

    perf_a = metrics_a.get(perf_key)
    perf_b = metrics_b.get(perf_key)
    if perf_a is not None and perf_b is not None:
        if perf_a > perf_b:
            parts.append(f"Over {timeframe}, {sym_a} ({perf_a:+.2f}%) outperforms {sym_b} ({perf_b:+.2f}%).")
        elif perf_b > perf_a:
            parts.append(f"Over {timeframe}, {sym_b} ({perf_b:+.2f}%) outperforms {sym_a} ({perf_a:+.2f}%).")

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------


def compare_tokens(token_a: str, token_b: str, timeframe: str = "24h") -> dict[str, Any]:
    """Compare two tokens side by side."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    coin_id_a = _resolve_token(token_a)
    coin_id_b = _resolve_token(token_b)

    if coin_id_a == coin_id_b:
        return {
            "status": "error",
            "error": {
                "code": "INVALID_INPUT",
                "message": f"Both tokens resolve to the same ID '{coin_id_a}'. Please provide two different tokens.",
            },
            "timestamp": now,
        }

    # Fetch both tokens (sequential to respect rate limits)
    detail_a = _fetch_token_data(coin_id_a)
    detail_b = _fetch_token_data(coin_id_b)

    if detail_a is None:
        return {
            "status": "error",
            "error": {
                "code": "INVALID_TOKEN",
                "message": f"Token '{token_a}' (resolved to '{coin_id_a}') not found on CoinGecko.",
            },
            "timestamp": now,
        }

    if detail_b is None:
        return {
            "status": "error",
            "error": {
                "code": "INVALID_TOKEN",
                "message": f"Token '{token_b}' (resolved to '{coin_id_b}') not found on CoinGecko.",
            },
            "timestamp": now,
        }

    metrics_a = _extract_metrics(detail_a)
    metrics_b = _extract_metrics(detail_b)

    comparison = _build_comparison(metrics_a, metrics_b, timeframe)
    summary = _build_summary(metrics_a, metrics_b, comparison, timeframe)

    return {
        "status": "success",
        "data": {
            "token_a": metrics_a,
            "token_b": metrics_b,
            "comparison": comparison,
            "summary": summary,
            "timeframe": timeframe,
            "timestamp": now,
        },
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

    # Validate required params
    token_a = params.get("token_a")
    token_b = params.get("token_b")

    if not token_a or not isinstance(token_a, str) or not token_a.strip():
        json.dump(
            {
                "status": "error",
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "Missing required parameter 'token_a'. Provide a token name, symbol, or CoinGecko ID.",
                },
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            sys.stdout,
            indent=2,
        )
        return

    if not token_b or not isinstance(token_b, str) or not token_b.strip():
        json.dump(
            {
                "status": "error",
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "Missing required parameter 'token_b'. Provide a token name, symbol, or CoinGecko ID.",
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
                    "message": f"Invalid timeframe '{timeframe}'. Must be one of: {', '.join(sorted(VALID_TIMEFRAMES))}",
                },
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            sys.stdout,
            indent=2,
        )
        return

    result = compare_tokens(
        token_a=token_a.strip(),
        token_b=token_b.strip(),
        timeframe=timeframe,
    )
    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
