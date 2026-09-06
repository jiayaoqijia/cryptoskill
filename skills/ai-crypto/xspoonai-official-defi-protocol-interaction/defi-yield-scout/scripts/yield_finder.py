#!/usr/bin/env python3
"""
DeFi Yield Finder - Discover and rank top yield opportunities across DeFi protocols.

Queries the DeFiLlama pools API to find, filter, and rank yield farming opportunities
across 20+ protocols and 10+ chains. Supports filtering by chain, protocol, minimum TVL,
stablecoin-only, and sorting by APY or TVL.

Input (JSON via stdin):
{
    "chain": "ethereum",        # optional: filter by chain (default: "all")
    "protocol": "aave",         # optional: filter by protocol
    "min_tvl": 1000000,         # optional: minimum TVL in USD (default: 1000000)
    "stablecoin_only": false,   # optional: only stablecoin pools (default: false)
    "sort_by": "apy",           # optional: "apy" or "tvl" (default: "apy")
    "limit": 20                 # optional: max results (default: 20)
}

Output (JSON via stdout):
{
    "success": true,
    "results": [...],
    "total_pools_scanned": 8542,
    "results_count": 20
}

API: https://yields.llama.fi/pools (free, no API key)
"""

import json
import sys
import urllib.request
import urllib.error
import time
from typing import Any, Dict, List, Optional, Tuple


# DeFiLlama pools endpoint
DEFILLAMA_POOLS_URL = "https://yields.llama.fi/pools"

# Chain name normalization map
CHAIN_ALIASES: Dict[str, str] = {
    "ethereum": "Ethereum",
    "eth": "Ethereum",
    "bsc": "BSC",
    "binance": "BSC",
    "polygon": "Polygon",
    "matic": "Polygon",
    "arbitrum": "Arbitrum",
    "arb": "Arbitrum",
    "base": "Base",
    "optimism": "Optimism",
    "op": "Optimism",
    "avalanche": "Avalanche",
    "avax": "Avalanche",
    "solana": "Solana",
    "sol": "Solana",
    "fantom": "Fantom",
    "ftm": "Fantom",
    "gnosis": "Gnosis",
    "xdai": "Gnosis",
    "celo": "Celo",
    "moonbeam": "Moonbeam",
    "moonriver": "Moonriver",
    "harmony": "Harmony",
    "aurora": "Aurora",
    "cronos": "Cronos",
    "metis": "Metis",
    "linea": "Linea",
    "scroll": "Scroll",
    "zksync": "zkSync Era",
    "zksync era": "zkSync Era",
    "polygon zkevm": "Polygon zkEVM",
    "mantle": "Mantle",
    "blast": "Blast",
    "manta": "Manta",
    "mode": "Mode",
}

# Maximum retry attempts for API calls
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2.0


def _fetch_json(url: str, timeout: int = 25) -> Tuple[Optional[Dict], Optional[str]]:
    """Fetch JSON from a URL with retry logic and 429 handling.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        Tuple of (data_dict, error_string). One will be None.
    """
    headers = {
        "User-Agent": "DeFiYieldScout/1.0",
        "Accept": "application/json",
    }

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)
                return data, None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = RETRY_DELAY_BASE * (2 ** attempt)
                time.sleep(wait_time)
                continue
            return None, f"HTTP {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            return None, f"URL error: {str(e.reason)}"
        except json.JSONDecodeError as e:
            return None, f"JSON decode error: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"

    return None, "Max retries exceeded (rate limited)"


def _normalize_chain(chain: str) -> Optional[str]:
    """Normalize chain name to DeFiLlama format.

    Args:
        chain: User-provided chain name.

    Returns:
        Normalized chain name or None if 'all'.
    """
    if not chain or chain.lower() in ("all", "any", "*"):
        return None
    return CHAIN_ALIASES.get(chain.lower(), chain.title())


def _format_tvl(tvl: float) -> str:
    """Format TVL as human-readable string.

    Args:
        tvl: TVL in USD.

    Returns:
        Formatted string like "$1.23B" or "$45.6M".
    """
    if tvl >= 1_000_000_000:
        return f"${tvl / 1_000_000_000:.2f}B"
    elif tvl >= 1_000_000:
        return f"${tvl / 1_000_000:.2f}M"
    elif tvl >= 1_000:
        return f"${tvl / 1_000:.2f}K"
    else:
        return f"${tvl:.2f}"


def _assess_tvl_trend(pool: Dict) -> str:
    """Assess TVL trend from pool data.

    DeFiLlama provides tvlPct1D, tvlPct7D, tvlPct30D for TVL changes.

    Args:
        pool: Pool data from DeFiLlama.

    Returns:
        Trend string: "growing", "shrinking", or "stable".
    """
    pct_7d = pool.get("tvlPct7D")
    pct_30d = pool.get("tvlPct30D")

    if pct_7d is not None and pct_30d is not None:
        if pct_7d > 5 and pct_30d > 10:
            return "growing"
        elif pct_7d < -5 and pct_30d < -10:
            return "shrinking"
        elif pct_7d > 2 or pct_30d > 5:
            return "growing"
        elif pct_7d < -2 or pct_30d < -5:
            return "shrinking"
    elif pct_7d is not None:
        if pct_7d > 5:
            return "growing"
        elif pct_7d < -5:
            return "shrinking"

    return "stable"


def _assess_il_risk(pool: Dict) -> str:
    """Assess impermanent loss risk for a pool.

    Args:
        pool: Pool data from DeFiLlama.

    Returns:
        IL risk level: "none", "low", "moderate", or "high".
    """
    il_risk = pool.get("ilRisk")
    if il_risk == "no":
        return "none"

    stablecoin = pool.get("stablecoin", False)
    if stablecoin:
        return "none"

    symbol = pool.get("symbol", "").upper()

    # Single-asset pools (lending, staking)
    if "-" not in symbol and "/" not in symbol:
        return "none"

    # Stablecoin pairs
    stables = {"USDC", "USDT", "DAI", "BUSD", "FRAX", "LUSD", "TUSD", "GUSD", "USDP", "SUSD", "CUSD"}
    tokens = [t.strip() for t in symbol.replace("/", "-").split("-")]
    stable_count = sum(1 for t in tokens if t in stables)

    if stable_count == len(tokens):
        return "low"  # Stablecoin-stablecoin pair, minimal IL
    elif stable_count >= 1:
        return "moderate"  # One stable, one volatile
    else:
        return "high"  # All volatile assets


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float.

    Args:
        value: Value to convert.
        default: Default if conversion fails.

    Returns:
        Float value.
    """
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _validate_input(params: Dict) -> Tuple[Dict, Optional[str]]:
    """Validate and normalize input parameters.

    Args:
        params: Raw input parameters.

    Returns:
        Tuple of (normalized_params, error_string).
    """
    normalized = {}

    # Chain
    chain_raw = params.get("chain", "all")
    if not isinstance(chain_raw, str):
        return {}, "Parameter 'chain' must be a string"
    normalized["chain"] = _normalize_chain(chain_raw)

    # Protocol
    protocol = params.get("protocol")
    if protocol is not None:
        if not isinstance(protocol, str):
            return {}, "Parameter 'protocol' must be a string"
        normalized["protocol"] = protocol.lower().strip()
    else:
        normalized["protocol"] = None

    # Min TVL
    min_tvl = params.get("min_tvl", 1_000_000)
    try:
        normalized["min_tvl"] = float(min_tvl)
    except (TypeError, ValueError):
        return {}, "Parameter 'min_tvl' must be a number"
    if normalized["min_tvl"] < 0:
        return {}, "Parameter 'min_tvl' must be non-negative"

    # Stablecoin only
    normalized["stablecoin_only"] = bool(params.get("stablecoin_only", False))

    # Sort by
    sort_by = params.get("sort_by", "apy")
    if sort_by not in ("apy", "tvl"):
        return {}, "Parameter 'sort_by' must be 'apy' or 'tvl'"
    normalized["sort_by"] = sort_by

    # Limit
    limit = params.get("limit", 20)
    try:
        normalized["limit"] = int(limit)
    except (TypeError, ValueError):
        return {}, "Parameter 'limit' must be an integer"
    if normalized["limit"] < 1:
        return {}, "Parameter 'limit' must be at least 1"
    if normalized["limit"] > 100:
        normalized["limit"] = 100

    return normalized, None


def _filter_pools(pools: List[Dict], params: Dict) -> List[Dict]:
    """Filter pools based on user criteria.

    Args:
        pools: Raw pool data from DeFiLlama.
        params: Normalized filter parameters.

    Returns:
        Filtered list of pool dicts.
    """
    filtered = []

    chain_filter = params["chain"]
    protocol_filter = params["protocol"]
    min_tvl = params["min_tvl"]
    stablecoin_only = params["stablecoin_only"]

    for pool in pools:
        # Skip pools with no APY data
        apy = _safe_float(pool.get("apy"))
        if apy <= 0:
            continue

        # TVL filter
        tvl = _safe_float(pool.get("tvlUsd"))
        if tvl < min_tvl:
            continue

        # Chain filter
        if chain_filter:
            pool_chain = pool.get("chain", "")
            if pool_chain.lower() != chain_filter.lower():
                continue

        # Protocol filter
        if protocol_filter:
            pool_project = pool.get("project", "").lower()
            if protocol_filter not in pool_project:
                continue

        # Stablecoin filter
        if stablecoin_only:
            if not pool.get("stablecoin", False):
                continue

        # Skip pools with unreasonably high APY (>10000% is likely a data error)
        if apy > 10000:
            continue

        filtered.append(pool)

    return filtered


def _format_pool(pool: Dict, rank: int) -> Dict:
    """Format a pool into the output structure.

    Args:
        pool: Raw pool data from DeFiLlama.
        rank: Rank position.

    Returns:
        Formatted pool dict.
    """
    apy_total = _safe_float(pool.get("apy"))
    apy_base = _safe_float(pool.get("apyBase"))
    apy_reward = _safe_float(pool.get("apyReward"))
    tvl = _safe_float(pool.get("tvlUsd"))

    # If base + reward don't sum to total, attribute to base
    if apy_base == 0 and apy_reward == 0 and apy_total > 0:
        apy_base = apy_total

    return {
        "rank": rank,
        "pool": pool.get("symbol", "Unknown"),
        "pool_id": pool.get("pool", ""),
        "chain": pool.get("chain", "Unknown"),
        "protocol": pool.get("project", "Unknown"),
        "apy_total": round(apy_total, 2),
        "apy_base": round(apy_base, 2),
        "apy_reward": round(apy_reward, 2),
        "tvl_usd": round(tvl, 2),
        "tvl_display": _format_tvl(tvl),
        "stablecoin": pool.get("stablecoin", False),
        "il_risk": _assess_il_risk(pool),
        "tvl_trend": _assess_tvl_trend(pool),
        "exposure": pool.get("exposure", "single"),
        "pool_meta": pool.get("poolMeta"),
    }


def find_yields(params: Dict) -> Dict:
    """Main function to find and rank yield opportunities.

    Args:
        params: Validated input parameters.

    Returns:
        Result dict with success status and yield data.
    """
    # Fetch pool data from DeFiLlama
    data, error = _fetch_json(DEFILLAMA_POOLS_URL)
    if error:
        return {
            "success": False,
            "error": f"Failed to fetch DeFiLlama data: {error}",
            "suggestion": "DeFiLlama API may be temporarily unavailable. Try again in a moment.",
        }

    pools = data.get("data", [])
    if not pools:
        return {
            "success": False,
            "error": "No pool data returned from DeFiLlama",
        }

    total_scanned = len(pools)

    # Filter pools
    filtered = _filter_pools(pools, params)

    if not filtered:
        return {
            "success": True,
            "query": {
                "chain": params["chain"] or "all",
                "protocol": params["protocol"] or "any",
                "min_tvl": params["min_tvl"],
                "stablecoin_only": params["stablecoin_only"],
            },
            "total_pools_scanned": total_scanned,
            "results_count": 0,
            "results": [],
            "message": "No pools found matching your criteria. Try lowering min_tvl or broadening filters.",
        }

    # Sort pools
    sort_key = params["sort_by"]
    if sort_key == "apy":
        filtered.sort(key=lambda p: _safe_float(p.get("apy")), reverse=True)
    else:
        filtered.sort(key=lambda p: _safe_float(p.get("tvlUsd")), reverse=True)

    # Apply limit
    limited = filtered[: params["limit"]]

    # Format results
    results = [_format_pool(pool, i + 1) for i, pool in enumerate(limited)]

    # Compute summary statistics
    apys = [r["apy_total"] for r in results]
    tvls = [r["tvl_usd"] for r in results]

    summary = {
        "avg_apy": round(sum(apys) / len(apys), 2) if apys else 0,
        "max_apy": round(max(apys), 2) if apys else 0,
        "min_apy": round(min(apys), 2) if apys else 0,
        "total_tvl": round(sum(tvls), 2),
        "total_tvl_display": _format_tvl(sum(tvls)),
        "chains_represented": len(set(r["chain"] for r in results)),
        "protocols_represented": len(set(r["protocol"] for r in results)),
    }

    return {
        "success": True,
        "query": {
            "chain": params["chain"] or "all",
            "protocol": params["protocol"] or "any",
            "min_tvl": params["min_tvl"],
            "stablecoin_only": params["stablecoin_only"],
            "sort_by": params["sort_by"],
        },
        "total_pools_scanned": total_scanned,
        "results_count": len(results),
        "results": results,
        "summary": summary,
        "metadata": {
            "data_source": "DeFiLlama",
            "api_endpoint": DEFILLAMA_POOLS_URL,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
    }


def main() -> None:
    """Entry point: read JSON from stdin, process, write JSON to stdout."""
    try:
        raw_input = sys.stdin.read().strip()
        if not raw_input:
            params = {}
        else:
            params = json.loads(raw_input)
    except json.JSONDecodeError as e:
        result = {
            "success": False,
            "error": f"Invalid JSON input: {str(e)}",
            "usage": {
                "description": "Find top DeFi yield opportunities",
                "example_input": {
                    "chain": "ethereum",
                    "protocol": "aave",
                    "min_tvl": 1000000,
                    "stablecoin_only": False,
                    "sort_by": "apy",
                    "limit": 20,
                },
            },
        }
        print(json.dumps(result, indent=2))
        return

    if not isinstance(params, dict):
        result = {
            "success": False,
            "error": "Input must be a JSON object",
        }
        print(json.dumps(result, indent=2))
        return

    # Validate input
    validated, error = _validate_input(params)
    if error:
        result = {
            "success": False,
            "error": f"Input validation failed: {error}",
        }
        print(json.dumps(result, indent=2))
        return

    # Find yields
    result = find_yields(validated)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
