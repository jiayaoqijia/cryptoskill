#!/usr/bin/env python3
"""
Bridge Comparison Script
Compare cross-chain bridge protocols side by side using real-time
data from the DeFiLlama Bridges API.

Supports comparing specific bridges by name, retrieving top N bridges
by volume, and filtering bridges by chain support.

Author: Nihal Nihalani
Version: 1.0.0
"""

import json
import sys
import time
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

BRIDGES_API = "https://bridges.llama.fi/bridges?includeChains=true"

USER_AGENT = "BridgeAnalyzer/1.0"

# Chain name normalization mapping
CHAIN_ALIASES: Dict[str, str] = {
    "ethereum": "Ethereum",
    "eth": "Ethereum",
    "mainnet": "Ethereum",
    "arbitrum": "Arbitrum",
    "arb": "Arbitrum",
    "optimism": "Optimism",
    "op": "Optimism",
    "polygon": "Polygon",
    "matic": "Polygon",
    "bsc": "BSC",
    "bnb": "BSC",
    "binance": "BSC",
    "base": "Base",
    "avalanche": "Avalanche",
    "avax": "Avalanche",
    "solana": "Solana",
    "sol": "Solana",
    "fantom": "Fantom",
    "ftm": "Fantom",
    "gnosis": "Gnosis",
    "xdai": "Gnosis",
    "linea": "Linea",
    "zksync": "zkSync Era",
    "zksync era": "zkSync Era",
    "scroll": "Scroll",
    "mantle": "Mantle",
    "metis": "Metis",
    "celo": "Celo",
    "moonbeam": "Moonbeam",
    "kava": "Kava",
    "aurora": "Aurora",
    "harmony": "Harmony",
    "cronos": "Cronos",
}


def _fetch_json(url: str, max_retries: int = 3, timeout: int = 20) -> Dict[str, Any]:
    """Fetch JSON from URL with retry logic and 429 handling.

    Args:
        url: The URL to fetch.
        max_retries: Maximum number of retry attempts.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response as a dictionary.

    Raises:
        SystemExit: On unrecoverable fetch errors.
    """
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                time.sleep(wait)
                continue
            _error_exit(f"HTTP error {e.code} fetching {url}")
        except urllib.error.URLError as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            _error_exit(f"URL error: {e.reason}")
        except Exception as e:
            _error_exit(f"Unexpected error: {str(e)}")
    _error_exit("Max retries exceeded")


def _error_exit(message: str) -> None:
    """Print error JSON and exit."""
    output = {
        "success": False,
        "error": message,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    print(json.dumps(output, indent=2))
    sys.exit(1)


def _normalize_chain(chain: str) -> str:
    """Normalize a chain name to DeFiLlama format.

    Args:
        chain: User-provided chain name.

    Returns:
        Normalized chain name matching DeFiLlama conventions.
    """
    lower = chain.strip().lower()
    if lower in CHAIN_ALIASES:
        return CHAIN_ALIASES[lower]
    # Title case fallback for unknown chains
    return chain.strip().title()


def _match_bridge_name(bridge_data: Dict[str, Any], search_name: str) -> bool:
    """Check if a bridge matches the search name (case-insensitive, partial).

    Args:
        bridge_data: Bridge data from DeFiLlama API.
        search_name: User-provided bridge name to search for.

    Returns:
        True if the bridge matches the search name.
    """
    search_lower = search_name.strip().lower()
    name = bridge_data.get("name", "").lower()
    display_name = bridge_data.get("displayName", "").lower()
    return (
        search_lower in name
        or search_lower in display_name
        or name in search_lower
        or display_name in search_lower
    )


def _format_bridge(bridge: Dict[str, Any], rank: int) -> Dict[str, Any]:
    """Format a bridge entry for output.

    Args:
        bridge: Raw bridge data from DeFiLlama.
        rank: Volume rank among all bridges.

    Returns:
        Formatted bridge data dictionary.
    """
    chains = bridge.get("chains", [])
    volume_24h = bridge.get("volumePrevDay", 0) or 0
    volume_1h = bridge.get("lastHourlyVolume", 0) or 0
    current_day = bridge.get("currentDayVolume", 0) or 0

    return {
        "name": bridge.get("name", "Unknown"),
        "display_name": bridge.get("displayName", bridge.get("name", "Unknown")),
        "id": bridge.get("id"),
        "volume_24h": round(float(volume_24h), 2),
        "volume_current_day": round(float(current_day), 2),
        "volume_1h": round(float(volume_1h), 2),
        "chains_count": len(chains),
        "chains": sorted(chains),
        "volume_rank": rank,
    }


def _rank_bridges(bridges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Assign volume rank to each bridge.

    Args:
        bridges: List of bridge data from DeFiLlama.

    Returns:
        The same list sorted by 24h volume descending.
    """
    return sorted(
        bridges,
        key=lambda b: float(b.get("volumePrevDay", 0) or 0),
        reverse=True,
    )


def compare_specific(
    all_bridges: List[Dict[str, Any]],
    names: List[str],
    sort_by: str = "volume",
) -> Dict[str, Any]:
    """Compare specific bridges by name.

    Args:
        all_bridges: All bridge data from API.
        names: List of bridge names to compare.
        sort_by: Sort key -- 'volume' or 'chains_count'.

    Returns:
        Comparison result dictionary.
    """
    ranked = _rank_bridges(all_bridges)
    rank_map: Dict[int, int] = {}
    for idx, b in enumerate(ranked):
        rank_map[b.get("id", idx)] = idx + 1

    matched = []
    not_found = []

    for name in names:
        found = False
        for bridge in all_bridges:
            if _match_bridge_name(bridge, name):
                rank = rank_map.get(bridge.get("id"), 0)
                matched.append(_format_bridge(bridge, rank))
                found = True
                break
        if not found:
            not_found.append(name)

    if sort_by == "chains_count":
        matched.sort(key=lambda b: b["chains_count"], reverse=True)
    else:
        matched.sort(key=lambda b: b["volume_24h"], reverse=True)

    result: Dict[str, Any] = {
        "bridges": matched,
        "total_matched": len(matched),
        "query_type": "specific",
        "sort_by": sort_by,
    }
    if not_found:
        result["not_found"] = not_found

    return result


def compare_top(
    all_bridges: List[Dict[str, Any]],
    top_n: int = 10,
    sort_by: str = "volume",
) -> Dict[str, Any]:
    """Get top N bridges by volume or chain count.

    Args:
        all_bridges: All bridge data from API.
        top_n: Number of top bridges to return.
        sort_by: Sort key -- 'volume' or 'chains_count'.

    Returns:
        Top N comparison result dictionary.
    """
    if sort_by == "chains_count":
        sorted_bridges = sorted(
            all_bridges,
            key=lambda b: len(b.get("chains", [])),
            reverse=True,
        )
    else:
        sorted_bridges = _rank_bridges(all_bridges)

    # Build rank map by volume regardless of sort
    volume_ranked = _rank_bridges(all_bridges)
    rank_map: Dict[int, int] = {}
    for idx, b in enumerate(volume_ranked):
        rank_map[b.get("id", idx)] = idx + 1

    top_n = min(top_n, len(sorted_bridges))
    bridges = []
    for bridge in sorted_bridges[:top_n]:
        rank = rank_map.get(bridge.get("id"), 0)
        bridges.append(_format_bridge(bridge, rank))

    return {
        "bridges": bridges,
        "total_matched": len(bridges),
        "total_available": len(all_bridges),
        "query_type": "top",
        "sort_by": sort_by,
    }


def compare_by_chain(
    all_bridges: List[Dict[str, Any]],
    chain: str,
    sort_by: str = "volume",
) -> Dict[str, Any]:
    """Get bridges supporting a specific chain.

    Args:
        all_bridges: All bridge data from API.
        chain: Chain name to filter by.
        sort_by: Sort key -- 'volume' or 'chains_count'.

    Returns:
        Chain-filtered comparison result dictionary.
    """
    normalized = _normalize_chain(chain)

    # Build rank map
    volume_ranked = _rank_bridges(all_bridges)
    rank_map: Dict[int, int] = {}
    for idx, b in enumerate(volume_ranked):
        rank_map[b.get("id", idx)] = idx + 1

    matched = []
    for bridge in all_bridges:
        chains = bridge.get("chains", [])
        # Case-insensitive chain matching
        chain_names_lower = [c.lower() for c in chains]
        if normalized.lower() in chain_names_lower:
            rank = rank_map.get(bridge.get("id"), 0)
            matched.append(_format_bridge(bridge, rank))

    if sort_by == "chains_count":
        matched.sort(key=lambda b: b["chains_count"], reverse=True)
    else:
        matched.sort(key=lambda b: b["volume_24h"], reverse=True)

    return {
        "bridges": matched,
        "total_matched": len(matched),
        "query_type": "chain_filter",
        "chain": normalized,
        "sort_by": sort_by,
    }


def validate_input(data: Dict[str, Any]) -> Optional[str]:
    """Validate input parameters.

    Args:
        data: Parsed input JSON.

    Returns:
        Error message string, or None if valid.
    """
    has_bridges = "bridges" in data
    has_top = "top" in data
    has_chain = "chain" in data

    if not has_bridges and not has_top and not has_chain:
        return (
            "Missing required parameter. Provide one of: "
            "'bridges' (list of names), 'top' (number), or 'chain' (chain name)."
        )

    if has_bridges:
        if not isinstance(data["bridges"], list) or len(data["bridges"]) == 0:
            return "'bridges' must be a non-empty list of bridge names."
        if len(data["bridges"]) > 20:
            return "'bridges' list cannot exceed 20 entries."

    if has_top:
        try:
            top = int(data["top"])
            if top < 1 or top > 50:
                return "'top' must be between 1 and 50."
        except (ValueError, TypeError):
            return "'top' must be a valid integer."

    if has_chain:
        if not isinstance(data["chain"], str) or len(data["chain"].strip()) == 0:
            return "'chain' must be a non-empty string."

    if "sort_by" in data:
        if data["sort_by"] not in ("volume", "chains_count"):
            return "'sort_by' must be 'volume' or 'chains_count'."

    return None


def main() -> None:
    """Main entry point. Reads JSON from stdin and outputs comparison results."""
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            _error_exit("No input provided. Send JSON via stdin.")
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        _error_exit(f"Invalid JSON input: {str(e)}")
        return

    error = validate_input(data)
    if error:
        _error_exit(error)
        return

    sort_by = data.get("sort_by", "volume")

    # Fetch bridge data from DeFiLlama
    api_data = _fetch_json(BRIDGES_API)
    all_bridges = api_data.get("bridges", [])

    if not all_bridges:
        _error_exit("No bridge data returned from DeFiLlama API.")
        return

    # Route to appropriate comparison function
    if "bridges" in data:
        result = compare_specific(all_bridges, data["bridges"], sort_by)
    elif "chain" in data:
        result = compare_by_chain(all_bridges, data["chain"], sort_by)
    else:
        top_n = int(data.get("top", 10))
        result = compare_top(all_bridges, top_n, sort_by)

    result["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    output = {
        "success": True,
        "data": result,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
