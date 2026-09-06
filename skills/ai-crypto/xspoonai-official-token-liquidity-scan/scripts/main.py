#!/usr/bin/env python3
"""Analyze token liquidity across DEX pools with real API data"""
import json
import argparse
import sys
import urllib.request
import urllib.error
import ssl
from datetime import datetime
from collections import defaultdict


def format_success(data):
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error, details=None):
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


# Major DEX tokens and their addresses
KNOWN_TOKENS = {
    "ethereum": {
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "UNI": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    },
    "polygon": {
        "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        "DAI": "0x8f3Cf7ad23Cd3CaDbD9735AFF958023D60d8c662",
        "WMATIC": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
    }
}


def fetch_uniswap_pools(token_address, network="ethereum", limit=50):
    """Fetch pool data from Uniswap v3 subgraph."""
    subgraph_urls = {
        "ethereum": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
        "polygon": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3-polygon",
    }
    
    url = subgraph_urls.get(network, "")
    if not url:
        return []
    
    # GraphQL query to fetch pools containing this token
    query = """
    query {
        pools(first: %d, where: {tokens_contains: ["%s"]}, orderBy: liquidity, orderDirection: desc) {
            id
            symbol
            address: id
            liquidity
            sqrtPrice
            token0 {
                id
                symbol
                decimals
            }
            token1 {
                id
                symbol
                decimals
            }
            volumeUSD
        }
    }
    """ % (limit, token_address.lower())
    
    request_body = json.dumps({"query": query})
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(
            url,
            data=request_body.encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        response = urllib.request.urlopen(req, context=ssl_context, timeout=10)
        result = json.loads(response.read())
        
        if "data" not in result or "pools" not in result["data"]:
            return []
        
        pools = result["data"]["pools"]
        
        # Format pool data
        formatted_pools = []
        for pool in pools:
            try:
                liquidity = float(pool.get("liquidity", 0))
                volume_usd = float(pool.get("volumeUSD", 0))
                
                # Filter out dust pools
                if liquidity < 10000:  # < $10K
                    continue
                
                formatted_pools.append({
                    "address": pool.get("id", "unknown"),
                    "token0": pool.get("token0", {}).get("symbol", "UNKNOWN"),
                    "token1": pool.get("token1", {}).get("symbol", "UNKNOWN"),
                    "liquidity_usd": round(liquidity, 2),
                    "volume_24h_usd": round(volume_usd, 2),
                    "source": "uniswap_v3_subgraph"
                })
            except (ValueError, TypeError, KeyError):
                continue
        
        return formatted_pools
    
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError):
        return []


def analyze_liquidity_api(params):
    """Analyze token liquidity with real or custom data."""
    network = params.get("network", "ethereum")
    use_api = params.get("use_api", True)
    min_liquidity = params.get("min_liquidity_usd", 100000)
    
    # Token can be symbol or address
    token_input = params.get("token", "USDC")
    
    # Resolve token address
    known_tokens = KNOWN_TOKENS.get(network, {})
    token_addr = known_tokens.get(token_input, token_input)  # Use as-is if not a symbol
    
    if use_api and token_addr.startswith("0x"):
        # Fetch real pool data from Uniswap
        pools = fetch_uniswap_pools(token_addr, network)
        source = "uniswap_api"
    else:
        # Use provided pool data
        pools = params.get("pools", [])
        source = "parameters"
    
    # Filter by minimum liquidity
    filtered = [p for p in pools if p.get("liquidity_usd", 0) >= min_liquidity]
    
    if not filtered:
        total_liquidity = 0
        total_volume = 0
        avg_liq = 0
        score = "low"
    else:
        total_liquidity = sum(p.get("liquidity_usd", 0) for p in filtered)
        total_volume = sum(p.get("volume_24h_usd", 0) for p in filtered)
        avg_liq = total_liquidity / len(filtered)
        
        # Liquidity score based on total
        if total_liquidity > 50000000:
            score = "excellent"
        elif total_liquidity > 10000000:
            score = "very_high"
        elif total_liquidity > 5000000:
            score = "high"
        elif total_liquidity > 1000000:
            score = "medium"
        else:
            score = "low"
    
    # Calculate efficiency metrics
    volume_to_liquidity_ratio = (total_volume / total_liquidity * 100) if total_liquidity > 0 else 0
    
    # Top pools by liquidity
    top_pools = sorted(filtered, key=lambda x: x.get("liquidity_usd", 0), reverse=True)[:10]
    
    result = {
        "status": "success",
        "source": source,
        "network": network,
        "token": token_input,
        "pools_analyzed": len(filtered),
        "min_liquidity_usd": min_liquidity,
        "total_liquidity_usd": round(total_liquidity, 2),
        "total_volume_24h_usd": round(total_volume, 2),
        "avg_liquidity_per_pool": round(avg_liq, 2),
        "volume_to_liquidity_ratio_pct": round(volume_to_liquidity_ratio, 2),
        "liquidity_health_score": score,
        "top_pools": top_pools,
        "summary": {
            "highly_liquid": len([p for p in filtered if p.get("liquidity_usd", 0) > 5000000]),
            "moderately_liquid": len([p for p in filtered if 1000000 <= p.get("liquidity_usd", 0) <= 5000000]),
            "lowly_liquid": len([p for p in filtered if min_liquidity <= p.get("liquidity_usd", 0) < 1000000]),
        },
        "analysis_timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Analyze token liquidity across DEX pools')
    parser.add_argument('--params', type=str, required=True, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        params = json.loads(args.params)
        result = analyze_liquidity_api(params)
        print(format_success(result))
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except ValueError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
