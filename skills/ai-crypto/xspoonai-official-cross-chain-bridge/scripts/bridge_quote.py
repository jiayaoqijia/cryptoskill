#!/usr/bin/env python3
"""
Bridge Quote Script
Gets quotes from multiple bridge protocols
"""

import json
import sys
import urllib.request
import urllib.error
from typing import Dict, List, Optional
from datetime import datetime

# Chain ID mappings
CHAIN_IDS = {
    "ethereum": 1,
    "polygon": 137,
    "arbitrum": 42161,
    "optimism": 10,
    "base": 8453,
    "bsc": 56,
    "avalanche": 43114
}

# Token addresses per chain
TOKEN_ADDRESSES = {
    "ethereum": {
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "ETH": "0x0000000000000000000000000000000000000000",
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    },
    "polygon": {
        "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        "MATIC": "0x0000000000000000000000000000000000000000",
        "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"
    },
    "arbitrum": {
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "ETH": "0x0000000000000000000000000000000000000000",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
    },
    "optimism": {
        "USDC": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
        "USDT": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
        "ETH": "0x0000000000000000000000000000000000000000",
        "WETH": "0x4200000000000000000000000000000000000006"
    },
    "base": {
        "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "ETH": "0x0000000000000000000000000000000000000000",
        "WETH": "0x4200000000000000000000000000000000000006"
    }
}

# Bridge fee estimates (simplified)
BRIDGE_FEES = {
    "stargate": {
        "base_fee_pct": 0.0006,  # 0.06%
        "gas_estimate_usd": 5,
        "time_minutes": 2
    },
    "wormhole": {
        "base_fee_pct": 0.001,
        "gas_estimate_usd": 8,
        "time_minutes": 15
    },
    "across": {
        "base_fee_pct": 0.0015,
        "gas_estimate_usd": 4,
        "time_minutes": 5
    },
    "hop": {
        "base_fee_pct": 0.002,
        "gas_estimate_usd": 6,
        "time_minutes": 10
    },
    "native": {
        "base_fee_pct": 0,
        "gas_estimate_usd": 10,
        "time_minutes": 15
    }
}

# Security ratings
SECURITY_RATINGS = {
    "stargate": {"rating": "HIGH", "score": 85},
    "wormhole": {"rating": "HIGH", "score": 80},
    "across": {"rating": "HIGH", "score": 82},
    "hop": {"rating": "MEDIUM", "score": 75},
    "native": {"rating": "HIGHEST", "score": 95}
}


def get_available_bridges(source: str, dest: str, token: str) -> List[str]:
    """Get list of bridges supporting the route"""
    available = []

    # Stargate supports most EVM chains
    if source in CHAIN_IDS and dest in CHAIN_IDS:
        if token.upper() in ["USDC", "USDT", "ETH", "WETH"]:
            available.append("stargate")

    # Wormhole supports many chains
    if source in CHAIN_IDS and dest in CHAIN_IDS:
        available.append("wormhole")

    # Across supports limited chains
    across_chains = ["ethereum", "polygon", "arbitrum", "optimism", "base"]
    if source in across_chains and dest in across_chains:
        if token.upper() in ["USDC", "ETH", "WETH"]:
            available.append("across")

    # Hop supports L2s
    hop_chains = ["ethereum", "polygon", "arbitrum", "optimism"]
    if source in hop_chains and dest in hop_chains:
        if token.upper() in ["USDC", "USDT", "ETH"]:
            available.append("hop")

    # Native bridges for L2s
    if (source == "ethereum" and dest in ["arbitrum", "optimism", "base", "polygon"]) or \
       (dest == "ethereum" and source in ["arbitrum", "optimism", "base", "polygon"]):
        available.append("native")

    return available


def calculate_quote(bridge: str, amount: float, token: str, source: str, dest: str) -> Dict:
    """Calculate quote for a specific bridge"""
    fees = BRIDGE_FEES.get(bridge, BRIDGE_FEES["stargate"])
    security = SECURITY_RATINGS.get(bridge, {"rating": "UNKNOWN", "score": 50})

    # Calculate fees
    protocol_fee = amount * fees["base_fee_pct"]
    gas_fee = fees["gas_estimate_usd"]

    # Estimate receive amount
    receive_amount = amount - protocol_fee

    # For stablecoins, gas is separate
    # For ETH, might need to account differently
    if token.upper() in ["ETH", "WETH"]:
        # Gas deducted from ETH
        gas_in_eth = gas_fee / 2500  # Rough ETH price
        receive_amount -= gas_in_eth
        total_fee_usd = (protocol_fee + gas_in_eth) * 2500
    else:
        # Stablecoins
        total_fee_usd = protocol_fee + gas_fee

    return {
        "bridge": bridge,
        "source_chain": source,
        "dest_chain": dest,
        "token": token.upper(),
        "amount_in": amount,
        "amount_out": round(receive_amount, 6),
        "fees": {
            "protocol_fee": round(protocol_fee, 6),
            "gas_estimate_usd": round(gas_fee, 2),
            "total_fee_usd": round(total_fee_usd, 2)
        },
        "estimated_time_minutes": fees["time_minutes"],
        "security": security,
        "warnings": get_bridge_warnings(bridge, amount)
    }


def get_bridge_warnings(bridge: str, amount: float) -> List[str]:
    """Get warnings for bridge/amount combination"""
    warnings = []

    if bridge == "wormhole" and amount > 100000:
        warnings.append("Large transfers via Wormhole may require manual claim")

    if bridge == "native" and amount > 10000:
        warnings.append("Native bridge withdrawals may take 7 days for Optimism/Arbitrum")

    if amount > 1000000:
        warnings.append("Consider splitting into smaller transfers for amounts this large")

    return warnings


def get_bridge_quotes(source: str, dest: str, token: str, amount: float) -> Dict:
    """Get quotes from all available bridges"""
    source = source.lower()
    dest = dest.lower()
    token = token.upper()

    # Validate chains
    if source not in CHAIN_IDS:
        raise ValueError(f"Unsupported source chain: {source}")
    if dest not in CHAIN_IDS:
        raise ValueError(f"Unsupported destination chain: {dest}")

    # Get available bridges
    bridges = get_available_bridges(source, dest, token)

    if not bridges:
        raise ValueError(f"No bridges available for {token} from {source} to {dest}")

    # Get quotes from each bridge
    quotes = []
    for bridge in bridges:
        try:
            quote = calculate_quote(bridge, amount, token, source, dest)
            quotes.append(quote)
        except Exception as e:
            continue

    # Sort by receive amount (best first)
    quotes.sort(key=lambda x: x["amount_out"], reverse=True)

    # Determine recommendation
    best_quote = quotes[0] if quotes else None
    fastest = min(quotes, key=lambda x: x["estimated_time_minutes"]) if quotes else None
    safest = max(quotes, key=lambda x: x["security"]["score"]) if quotes else None

    return {
        "success": True,
        "timestamp": datetime.utcnow().isoformat(),
        "request": {
            "source_chain": source,
            "dest_chain": dest,
            "token": token,
            "amount": amount
        },
        "quotes": quotes,
        "recommendations": {
            "best_value": best_quote["bridge"] if best_quote else None,
            "fastest": fastest["bridge"] if fastest else None,
            "safest": safest["bridge"] if safest else None
        },
        "summary": {
            "bridges_available": len(quotes),
            "best_receive_amount": best_quote["amount_out"] if best_quote else 0,
            "fastest_time": fastest["estimated_time_minutes"] if fastest else 0
        }
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        source_chain = input_data.get("source_chain", "ethereum")
        dest_chain = input_data.get("dest_chain", "arbitrum")
        token = input_data.get("token", "USDC")
        amount = float(input_data.get("amount", 1000))

        result = get_bridge_quotes(source_chain, dest_chain, token, amount)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
