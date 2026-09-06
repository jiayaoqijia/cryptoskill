#!/usr/bin/env python3
"""
Wallet Balance Script
Fetches comprehensive wallet balance including ETH and tokens
"""

import json
import sys
import os
import urllib.request
import urllib.error
from typing import Optional, List, Dict

# Chain configurations
CHAIN_CONFIG = {
    "ethereum": {
        "api_url": "https://api.etherscan.io/api",
        "api_key_env": "ETHERSCAN_API_KEY",
        "native_symbol": "ETH",
        "chain_id": 1
    },
    "polygon": {
        "api_url": "https://api.polygonscan.com/api",
        "api_key_env": "POLYGONSCAN_API_KEY",
        "native_symbol": "POL",  # Renamed from MATIC on Sept 4, 2024
        "chain_id": 137
    },
    "arbitrum": {
        "api_url": "https://api.arbiscan.io/api",
        "api_key_env": "ARBISCAN_API_KEY",
        "native_symbol": "ETH",
        "chain_id": 42161
    },
    "optimism": {
        "api_url": "https://api-optimistic.etherscan.io/api",
        "api_key_env": "OPTIMISM_API_KEY",
        "native_symbol": "ETH",
        "chain_id": 10
    },
    "base": {
        "api_url": "https://api.basescan.org/api",
        "api_key_env": "BASESCAN_API_KEY",
        "native_symbol": "ETH",
        "chain_id": 8453
    }
}

# Known token addresses for major tokens
KNOWN_TOKENS = {
    "ethereum": {
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "DAI": "0x6B175474E89094C44Da98b954EeacdeCB5BE3830",
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "UNI": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        "LINK": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
        "AAVE": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
    },
    "polygon": {
        "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        "WMATIC": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"
    },
    "arbitrum": {
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "ARB": "0x912CE59144191C1204E64559FE8253a0e49E6548"
    }
}


def fetch_api(base_url: str, params: dict, api_key: Optional[str] = None) -> dict:
    """Fetch data from Etherscan-like API"""
    if api_key:
        params["apikey"] = api_key

    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{base_url}?{query}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "WalletBalance/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to fetch data: {e}")


def get_eth_balance(address: str, chain: str) -> dict:
    """Get native token balance"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    api_key = os.getenv(config["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")

    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest"
    }

    data = fetch_api(config["api_url"], params, api_key)

    if data.get("status") == "1":
        balance_wei = int(data.get("result", 0))
        balance = balance_wei / 1e18
        return {
            "balance_wei": str(balance_wei),
            "balance": balance,
            "symbol": config["native_symbol"]
        }

    return {"balance": 0, "symbol": config["native_symbol"], "balance_wei": "0"}


def get_token_balances(address: str, chain: str) -> List[Dict]:
    """Get ERC20 token balances"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    api_key = os.getenv(config["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")

    params = {
        "module": "account",
        "action": "tokentx",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "page": 1,
        "offset": 100
    }

    data = fetch_api(config["api_url"], params, api_key)

    # Track unique tokens and get their current balances
    token_addresses = set()
    token_info = {}

    if data.get("status") == "1":
        for tx in data.get("result", []):
            token_addr = tx.get("contractAddress", "").lower()
            if token_addr and token_addr not in token_info:
                token_info[token_addr] = {
                    "address": token_addr,
                    "symbol": tx.get("tokenSymbol", "UNKNOWN"),
                    "name": tx.get("tokenName", "Unknown Token"),
                    "decimals": int(tx.get("tokenDecimal", 18))
                }
                token_addresses.add(token_addr)

    # Get balances for discovered tokens
    token_balances = []
    for token_addr, info in list(token_info.items())[:20]:  # Limit to 20 tokens
        try:
            balance = get_token_balance(address, token_addr, chain, info["decimals"])
            if balance > 0:
                token_balances.append({
                    "address": info["address"],
                    "symbol": info["symbol"],
                    "name": info["name"],
                    "balance": balance,
                    "decimals": info["decimals"]
                })
        except:
            continue

    # Sort by balance (assuming similar value, this is a rough sort)
    token_balances.sort(key=lambda x: x["balance"], reverse=True)

    return token_balances


def get_token_balance(wallet: str, token: str, chain: str, decimals: int = 18) -> float:
    """Get specific token balance"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    api_key = os.getenv(config["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")

    params = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": token,
        "address": wallet,
        "tag": "latest"
    }

    data = fetch_api(config["api_url"], params, api_key)

    if data.get("status") == "1":
        balance_raw = int(data.get("result", 0))
        return balance_raw / (10 ** decimals)

    return 0


def get_nft_count(address: str, chain: str) -> int:
    """Get count of NFTs held"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    api_key = os.getenv(config["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")

    # Get ERC721 transfers
    params = {
        "module": "account",
        "action": "tokennfttx",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc"
    }

    data = fetch_api(config["api_url"], params, api_key)

    # Count unique NFTs currently held
    nft_holdings = {}

    if data.get("status") == "1":
        for tx in data.get("result", []):
            contract = tx.get("contractAddress", "").lower()
            token_id = tx.get("tokenID", "")
            key = f"{contract}_{token_id}"

            if tx.get("to", "").lower() == address.lower():
                nft_holdings[key] = True
            elif tx.get("from", "").lower() == address.lower():
                nft_holdings.pop(key, None)

    return len(nft_holdings)


def get_wallet_balance(address: str, chain: str, include_tokens: bool = True) -> dict:
    """Get comprehensive wallet balance"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    # Validate address
    if not address.startswith("0x") or len(address) != 42:
        raise ValueError(f"Invalid address format: {address}")

    # Get native balance
    native_balance = get_eth_balance(address, chain)

    # Get token balances
    token_balances = []
    if include_tokens:
        token_balances = get_token_balances(address, chain)

    # Get NFT count
    nft_count = get_nft_count(address, chain)

    # Calculate totals (simplified without price feed)
    total_tokens = len(token_balances)

    return {
        "success": True,
        "chain": chain,
        "address": address,
        "native_balance": {
            "symbol": native_balance["symbol"],
            "balance": round(native_balance["balance"], 6),
            "balance_wei": native_balance["balance_wei"]
        },
        "token_holdings": {
            "count": total_tokens,
            "tokens": token_balances[:10]  # Top 10 tokens
        },
        "nft_holdings": {
            "count": nft_count
        },
        "summary": {
            "has_native_balance": native_balance["balance"] > 0,
            "has_tokens": total_tokens > 0,
            "has_nfts": nft_count > 0,
            "activity_status": "ACTIVE" if (native_balance["balance"] > 0 or total_tokens > 0) else "EMPTY"
        }
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        address = input_data.get("address")
        chain = input_data.get("chain", "ethereum")
        include_tokens = input_data.get("include_tokens", True)

        if not address:
            print(json.dumps({"error": "Missing required parameter: address"}))
            sys.exit(1)

        result = get_wallet_balance(address, chain, include_tokens)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
