#!/usr/bin/env python3
"""Trending tokens discovery script.

Discovers trending tokens by combining trading volume rankings with price
momentum signals from CoinGecko's free API.

Input (JSON via stdin):
    {"category": "all", "limit": 20}

Output (JSON via stdout):
    Ranked list of trending tokens with momentum scores.
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

VALID_CATEGORIES = {"all", "defi", "layer1", "layer2", "meme", "gaming"}

CATEGORY_TOKENS: dict[str, set[str]] = {
    "defi": {
        "aave", "uniswap", "maker", "curve-dao-token", "compound-governance-token",
        "synthetix-network-token", "sushi", "yearn-finance", "pancakeswap-token",
        "lido-dao", "rocket-pool", "frax-share", "convex-finance", "1inch",
        "dydx-chain", "the-graph", "chainlink", "ondo-finance",
    },
    "layer1": {
        "bitcoin", "ethereum", "solana", "cardano", "avalanche-2", "polkadot",
        "cosmos", "near", "aptos", "sui", "toncoin", "internet-computer",
        "algorand", "hedera-hashgraph", "fantom", "tezos", "flow",
    },
    "layer2": {
        "matic-network", "arbitrum", "optimism", "metis-token", "manta-network",
        "starknet", "immutable-x", "mantle", "zksync", "scroll", "base",
        "polygon-ecosystem-token",
    },
    "meme": {
        "dogecoin", "shiba-inu", "pepe", "bonk", "floki", "dogwifcoin",
        "brett", "memecoin", "book-of-meme", "cat-in-a-dogs-world",
    },
    "gaming": {
        "axie-infinity", "the-sandbox", "decentraland", "immutable-x",
        "gala", "enjincoin", "illuvium", "vulcan-forged", "merit-circle",
        "beam-2", "pixels", "portal-2", "ronin",
    },
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


def _calc_momentum_score(
    price_change_24h: Optional[float],
    price_change_7d: Optional[float],
    volume: Optional[float],
    market_cap: Optional[float],
) -> tuple[float, str]:
    """Calculate a 0-10 momentum score and label.

    Factors:
      - 24h price change (40% weight)
      - 7d price change (30% weight)
      - Volume/Market-cap ratio (30% weight)
    """
    score = 5.0  # neutral baseline

    # Price momentum (24h) -- clamped to [-50, 50]
    if price_change_24h is not None:
        clamped = max(-50, min(50, price_change_24h))
        score += (clamped / 50) * 2.0  # contributes +/- 2 points

    # Price momentum (7d) -- clamped to [-100, 100]
    if price_change_7d is not None:
        clamped = max(-100, min(100, price_change_7d))
        score += (clamped / 100) * 1.5  # contributes +/- 1.5 points

    # Volume/MC ratio -- higher ratio = more trading interest
    if volume and market_cap and market_cap > 0:
        ratio = volume / market_cap
        # Typical healthy ratio is 0.05-0.15; above 0.3 is very high
        vol_score = min(ratio / 0.3, 1.0) * 1.5
        score += vol_score

    score = max(0.0, min(10.0, round(score, 1)))

    if score >= 8:
        label = "Strong Bullish"
    elif score >= 6.5:
        label = "Bullish"
    elif score >= 4.5:
        label = "Neutral"
    elif score >= 3:
        label = "Bearish"
    else:
        label = "Strong Bearish"

    return score, label


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------


def get_trending_tokens(category: str = "all", limit: int = 20) -> dict[str, Any]:
    """Fetch and rank trending tokens."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Fetch top tokens by volume
    per_page = min(max(limit, 20), 250)
    url = (
        f"{COINGECKO_BASE}/coins/markets?vs_currency=usd"
        f"&order=volume_desc&per_page={per_page}&page=1"
        f"&sparkline=false&price_change_percentage=24h,7d"
    )

    try:
        raw_tokens = _fetch_json(url)
    except Exception as exc:
        return {
            "status": "error",
            "error": {
                "code": "API_ERROR",
                "message": f"Failed to fetch market data: {exc}",
            },
            "timestamp": now,
        }

    if not isinstance(raw_tokens, list):
        return {
            "status": "error",
            "error": {
                "code": "API_ERROR",
                "message": "Unexpected response format from CoinGecko.",
            },
            "timestamp": now,
        }

    # Also fetch CoinGecko trending (social signals)
    trending_ids: set[str] = set()
    try:
        trending_data = _fetch_json(f"{COINGECKO_BASE}/search/trending")
        for coin_wrapper in trending_data.get("coins", []):
            item = coin_wrapper.get("item", {})
            cid = item.get("id")
            if cid:
                trending_ids.add(cid)
    except Exception:
        pass  # Non-critical: trending social data is supplementary

    # Filter by category
    category_filter = CATEGORY_TOKENS.get(category)

    tokens = []
    for t in raw_tokens:
        cid = t.get("id", "")
        if category_filter and cid not in category_filter:
            continue

        price_change_24h = t.get("price_change_percentage_24h")
        price_change_7d = t.get("price_change_percentage_7d_in_currency")
        volume = t.get("total_volume")
        mcap = t.get("market_cap")

        momentum, label = _calc_momentum_score(price_change_24h, price_change_7d, volume, mcap)

        # Boost score slightly if token is also in CoinGecko trending
        if cid in trending_ids:
            momentum = min(10.0, round(momentum + 0.5, 1))

        tokens.append({
            "name": t.get("name", "Unknown"),
            "symbol": (t.get("symbol") or "").upper(),
            "coingecko_id": cid,
            "current_price": _format_price(t.get("current_price")),
            "price_change_24h_pct": round(price_change_24h, 2) if price_change_24h else None,
            "volume_24h": volume,
            "market_cap": mcap,
            "momentum_score": momentum,
            "momentum_label": label,
            "is_trending_social": cid in trending_ids,
        })

    # Sort by momentum score descending, then volume descending
    tokens.sort(key=lambda x: (x["momentum_score"], x["volume_24h"] or 0), reverse=True)

    # Apply limit and add rank
    tokens = tokens[:limit]
    for i, tok in enumerate(tokens, 1):
        tok["rank"] = i

    return {
        "status": "success",
        "data": {
            "trending": tokens,
            "category": category,
            "count": len(tokens),
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

    # Validate category
    category = str(params.get("category", "all")).lower()
    if category not in VALID_CATEGORIES:
        json.dump(
            {
                "status": "error",
                "error": {
                    "code": "INVALID_CATEGORY",
                    "message": f"Invalid category '{category}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}",
                },
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            sys.stdout,
            indent=2,
        )
        return

    # Validate limit
    limit = params.get("limit", 20)
    try:
        limit = int(limit)
        limit = max(1, min(100, limit))
    except (ValueError, TypeError):
        limit = 20

    result = get_trending_tokens(category=category, limit=limit)
    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
