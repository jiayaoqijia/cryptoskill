#!/usr/bin/env python3
"""
Portfolio Tracker Script
Tracks portfolio value across multiple chains
"""

import json
import sys
import os
import urllib.request
import urllib.error
from typing import Optional, List, Dict
from datetime import datetime

# Chain configurations
CHAIN_CONFIG = {
    "ethereum": {
        "api_url": "https://api.etherscan.io/api",
        "api_key_env": "ETHERSCAN_API_KEY",
        "native_symbol": "ETH",
        "coingecko_id": "ethereum"
    },
    "polygon": {
        "api_url": "https://api.polygonscan.com/api",
        "api_key_env": "POLYGONSCAN_API_KEY",
        "native_symbol": "POL",  # Renamed from MATIC on Sept 4, 2024
        "coingecko_id": "matic-network"
    },
    "arbitrum": {
        "api_url": "https://api.arbiscan.io/api",
        "api_key_env": "ARBISCAN_API_KEY",
        "native_symbol": "ETH",
        "coingecko_id": "ethereum"
    },
    "optimism": {
        "api_url": "https://api-optimistic.etherscan.io/api",
        "api_key_env": "OPTIMISM_API_KEY",
        "native_symbol": "ETH",
        "coingecko_id": "ethereum"
    },
    "base": {
        "api_url": "https://api.basescan.org/api",
        "api_key_env": "BASESCAN_API_KEY",
        "native_symbol": "ETH",
        "coingecko_id": "ethereum"
    }
}


def fetch_json(url: str, headers: dict = None) -> dict:
    """Fetch JSON from URL"""
    default_headers = {"User-Agent": "PortfolioTracker/1.0"}
    if headers:
        default_headers.update(headers)

    try:
        req = urllib.request.Request(url, headers=default_headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to fetch data: {e}")


def fetch_api(base_url: str, params: dict, api_key: Optional[str] = None) -> dict:
    """Fetch data from Etherscan-like API"""
    if api_key:
        params["apikey"] = api_key

    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{base_url}?{query}"

    return fetch_json(url)


def get_eth_price() -> Dict[str, float]:
    """Get current prices for major tokens"""
    try:
        # Use CoinGecko API for prices
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum,matic-network,bitcoin&vs_currencies=usd"
        data = fetch_json(url)

        return {
            "ETH": data.get("ethereum", {}).get("usd", 0),
            "POL": data.get("matic-network", {}).get("usd", 0),  # POL (formerly MATIC)
            "BTC": data.get("bitcoin", {}).get("usd", 0)
        }
    except:
        # Fallback prices if API fails
        return {"ETH": 2500, "POL": 0.8, "BTC": 45000}


def get_native_balance(address: str, chain: str) -> float:
    """Get native token balance for a chain"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        return 0

    api_key = os.getenv(config["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")

    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest"
    }

    try:
        data = fetch_api(config["api_url"], params, api_key)
        if data.get("status") == "1":
            return int(data.get("result", 0)) / 1e18
    except:
        pass

    return 0


def get_stablecoin_balances(address: str, chain: str) -> Dict[str, float]:
    """Get stablecoin balances"""
    stablecoins = {
        "ethereum": {
            "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "DAI": "0x6B175474E89094C44Da98b954EeacdeCB5BE3830"
        },
        "polygon": {
            "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"
        },
        "arbitrum": {
            "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
            "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
        }
    }

    chain_stables = stablecoins.get(chain, {})
    balances = {}

    config = CHAIN_CONFIG.get(chain)
    if not config:
        return balances

    api_key = os.getenv(config["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")

    for symbol, contract in chain_stables.items():
        try:
            params = {
                "module": "account",
                "action": "tokenbalance",
                "contractaddress": contract,
                "address": address,
                "tag": "latest"
            }

            data = fetch_api(config["api_url"], params, api_key)

            if data.get("status") == "1":
                decimals = 6 if symbol in ["USDC", "USDT"] else 18
                balance = int(data.get("result", 0)) / (10 ** decimals)
                if balance > 0:
                    balances[symbol] = balance
        except:
            continue

    return balances


def track_portfolio(address: str, chains: List[str]) -> dict:
    """Track portfolio across multiple chains"""
    if not address.startswith("0x") or len(address) != 42:
        raise ValueError(f"Invalid address format: {address}")

    # Get current prices
    prices = get_eth_price()

    # Track balances per chain
    chain_balances = {}
    total_usd = 0
    total_native = 0
    total_stables = 0

    for chain in chains:
        config = CHAIN_CONFIG.get(chain)
        if not config:
            continue

        # Get native balance
        native_balance = get_native_balance(address, chain)
        native_symbol = config["native_symbol"]
        native_price = prices.get(native_symbol, 0)
        native_usd = native_balance * native_price

        # Get stablecoin balances
        stables = get_stablecoin_balances(address, chain)
        stables_total = sum(stables.values())

        chain_balances[chain] = {
            "native": {
                "symbol": native_symbol,
                "balance": round(native_balance, 6),
                "usd_value": round(native_usd, 2)
            },
            "stablecoins": {
                symbol: round(balance, 2)
                for symbol, balance in stables.items()
            },
            "stablecoins_total": round(stables_total, 2),
            "total_usd": round(native_usd + stables_total, 2)
        }

        total_usd += native_usd + stables_total
        total_native += native_usd
        total_stables += stables_total

    # Calculate allocations
    native_pct = (total_native / total_usd * 100) if total_usd > 0 else 0
    stable_pct = (total_stables / total_usd * 100) if total_usd > 0 else 0

    # Determine risk profile
    if stable_pct > 70:
        risk_profile = "CONSERVATIVE"
    elif stable_pct > 40:
        risk_profile = "MODERATE"
    else:
        risk_profile = "AGGRESSIVE"

    return {
        "success": True,
        "address": address,
        "timestamp": datetime.utcnow().isoformat(),
        "chains_tracked": chains,
        "chain_breakdown": chain_balances,
        "portfolio_summary": {
            "total_usd": round(total_usd, 2),
            "native_tokens_usd": round(total_native, 2),
            "stablecoins_usd": round(total_stables, 2)
        },
        "allocation": {
            "native_tokens_pct": round(native_pct, 1),
            "stablecoins_pct": round(stable_pct, 1)
        },
        "analysis": {
            "risk_profile": risk_profile,
            "diversification": "GOOD" if len(chains) >= 3 else "MODERATE" if len(chains) >= 2 else "CONCENTRATED",
            "top_chain": max(chain_balances.keys(), key=lambda c: chain_balances[c]["total_usd"]) if chain_balances else None
        },
        "prices_used": prices
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        address = input_data.get("address")
        chains = input_data.get("chains", ["ethereum"])

        if not address:
            print(json.dumps({"error": "Missing required parameter: address"}))
            sys.exit(1)

        result = track_portfolio(address, chains)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
