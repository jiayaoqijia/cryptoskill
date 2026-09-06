#!/usr/bin/env python3
"""
DeFi TVL Script
Fetches TVL and APY data from DeFi Llama API
"""

import json
import sys
import urllib.request
import urllib.error

DEFILLAMA_API = "https://api.llama.fi"


def fetch_json(url: str) -> dict:
    """Fetch JSON from URL"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DeFi-Skill/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to fetch data: {e}")


def get_protocol_tvl(protocol: str) -> dict:
    """Get TVL data for a specific protocol"""
    url = f"{DEFILLAMA_API}/protocol/{protocol}"
    data = fetch_json(url)

    if not data:
        raise ValueError(f"Protocol not found: {protocol}")

    return {
        "success": True,
        "protocol": data.get("name", protocol),
        "symbol": data.get("symbol", "N/A"),
        "category": data.get("category", "N/A"),
        "chains": data.get("chains", []),
        "tvl": {
            "current_usd": round(data.get("tvl", 0), 2),
            "change_1d": round(data.get("change_1d", 0), 2),
            "change_7d": round(data.get("change_7d", 0), 2),
            "change_1m": round(data.get("change_1m", 0), 2)
        },
        "chain_tvls": {
            chain: round(tvl, 2)
            for chain, tvl in data.get("chainTvls", {}).items()
            if isinstance(tvl, (int, float))
        },
        "url": data.get("url", "N/A"),
        "description": data.get("description", "N/A")[:500] if data.get("description") else "N/A"
    }


def get_top_protocols(limit: int = 10) -> dict:
    """Get top protocols by TVL"""
    url = f"{DEFILLAMA_API}/protocols"
    data = fetch_json(url)

    if not data:
        raise ValueError("Failed to fetch protocols")

    # Sort by TVL and get top protocols
    sorted_protocols = sorted(data, key=lambda x: x.get("tvl", 0), reverse=True)[:limit]

    return {
        "success": True,
        "total_protocols": len(data),
        "top_protocols": [
            {
                "rank": i + 1,
                "name": p.get("name", "Unknown"),
                "symbol": p.get("symbol", "N/A"),
                "category": p.get("category", "N/A"),
                "tvl_usd": round(p.get("tvl", 0), 2),
                "change_1d": round(p.get("change_1d", 0), 2) if p.get("change_1d") else 0,
                "chains": p.get("chains", [])[:5]  # Limit chains shown
            }
            for i, p in enumerate(sorted_protocols)
        ]
    }


def get_yields(protocol: str = None) -> dict:
    """Get yield/APY data"""
    url = f"{DEFILLAMA_API}/pools"
    data = fetch_json(url)

    if not data or "data" not in data:
        raise ValueError("Failed to fetch yield data")

    pools = data["data"]

    # Filter by protocol if specified
    if protocol:
        pools = [p for p in pools if p.get("project", "").lower() == protocol.lower()]

    # Sort by APY and get top pools
    sorted_pools = sorted(pools, key=lambda x: x.get("apy", 0) or 0, reverse=True)[:20]

    return {
        "success": True,
        "filter": protocol or "all",
        "total_pools": len(pools),
        "top_pools": [
            {
                "pool": p.get("symbol", "Unknown"),
                "project": p.get("project", "Unknown"),
                "chain": p.get("chain", "Unknown"),
                "tvl_usd": round(p.get("tvlUsd", 0), 2),
                "apy": round(p.get("apy", 0), 2) if p.get("apy") else 0,
                "apy_base": round(p.get("apyBase", 0), 2) if p.get("apyBase") else 0,
                "apy_reward": round(p.get("apyReward", 0), 2) if p.get("apyReward") else 0,
                "il_risk": p.get("ilRisk", "Unknown"),
                "stablecoin": p.get("stablecoin", False)
            }
            for p in sorted_pools
        ]
    }


def get_chain_tvl(chain: str) -> dict:
    """Get TVL for a specific chain"""
    url = f"{DEFILLAMA_API}/v2/chains"
    data = fetch_json(url)

    if not data:
        raise ValueError("Failed to fetch chain data")

    chain_data = next((c for c in data if c.get("name", "").lower() == chain.lower()), None)

    if not chain_data:
        # List available chains
        available = [c.get("name") for c in data[:20]]
        raise ValueError(f"Chain not found: {chain}. Available: {', '.join(available)}")

    return {
        "success": True,
        "chain": chain_data.get("name", chain),
        "tvl_usd": round(chain_data.get("tvl", 0), 2),
        "token_symbol": chain_data.get("tokenSymbol", "N/A"),
        "gecko_id": chain_data.get("gecko_id", "N/A")
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        query_type = input_data.get("type", "protocol")
        protocol = input_data.get("protocol")
        chain = input_data.get("chain")
        limit = input_data.get("limit", 10)

        if query_type == "protocol" and protocol:
            result = get_protocol_tvl(protocol)
        elif query_type == "top" or not protocol:
            result = get_top_protocols(limit)
        elif query_type == "yields":
            result = get_yields(protocol)
        elif query_type == "chain" and chain:
            result = get_chain_tvl(chain)
        else:
            result = get_top_protocols(limit)

        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
