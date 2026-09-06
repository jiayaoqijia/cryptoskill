#!/usr/bin/env python3
"""
Neo N3 Balance Script
Queries NEO and GAS balances using Neo RPC API
"""

import json
import sys
import urllib.request
import urllib.error
from typing import Optional, Dict

# Network configurations
NETWORK_CONFIG = {
    "mainnet": {
        "rpc_url": "https://mainnet1.neo.coz.io:443",
        "network_id": 860833102
    },
    "testnet": {
        "rpc_url": "https://testnet1.neo.coz.io:443",
        "network_id": 894710606
    }
}

# Native contract script hashes
NEO_TOKEN = "0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5"
GAS_TOKEN = "0xd2a4cff31913016155e38e474a2c06d08be276cf"


def rpc_call(url: str, method: str, params: list) -> dict:
    """Make a JSON-RPC call to Neo node"""
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"RPC call failed: {e}")


def address_to_scripthash(address: str) -> str:
    """Convert Neo address to script hash (simplified)"""
    # Note: In production, use proper base58 decoding
    # This is a placeholder that returns the address for RPC params
    return address


def get_nep17_balances(address: str, network: str) -> Dict:
    """Get all NEP-17 token balances for an address"""
    config = NETWORK_CONFIG.get(network)
    if not config:
        raise ValueError(f"Unknown network: {network}")

    result = rpc_call(
        config["rpc_url"],
        "getnep17balances",
        [address]
    )

    if "error" in result:
        raise ValueError(result["error"].get("message", "RPC error"))

    return result.get("result", {})


def get_unclaimed_gas(address: str, network: str) -> float:
    """Get unclaimed GAS for an address"""
    config = NETWORK_CONFIG.get(network)
    if not config:
        raise ValueError(f"Unknown network: {network}")

    result = rpc_call(
        config["rpc_url"],
        "getunclaimedgas",
        [address]
    )

    if "error" in result:
        return 0

    unclaimed = result.get("result", {}).get("unclaimed", "0")
    return int(unclaimed) / 1e8


def get_block_count(network: str) -> int:
    """Get current block count"""
    config = NETWORK_CONFIG.get(network)
    if not config:
        raise ValueError(f"Unknown network: {network}")

    result = rpc_call(
        config["rpc_url"],
        "getblockcount",
        []
    )

    return result.get("result", 0)


def format_balance(amount: str, decimals: int) -> float:
    """Format balance with proper decimals"""
    try:
        return int(amount) / (10 ** decimals)
    except (ValueError, TypeError):
        return 0


def get_balance(address: str, network: str = "mainnet") -> dict:
    """Get comprehensive balance for a Neo address"""
    # Validate address format (Neo addresses start with 'N')
    if not address.startswith("N") or len(address) != 34:
        raise ValueError(f"Invalid Neo address format: {address}")

    # Get NEP-17 balances
    balances_data = get_nep17_balances(address, network)

    # Parse balances
    neo_balance = 0
    gas_balance = 0
    other_tokens = []

    for balance in balances_data.get("balance", []):
        asset_hash = balance.get("assethash", "").lower()
        amount = balance.get("amount", "0")
        last_updated = balance.get("lastupdatedblock", 0)

        if asset_hash == NEO_TOKEN.lower():
            neo_balance = format_balance(amount, 0)  # NEO has 0 decimals
        elif asset_hash == GAS_TOKEN.lower():
            gas_balance = format_balance(amount, 8)  # GAS has 8 decimals
        else:
            other_tokens.append({
                "asset_hash": asset_hash,
                "amount": amount,
                "last_updated_block": last_updated
            })

    # Get unclaimed GAS
    unclaimed_gas = get_unclaimed_gas(address, network)

    # Get current block height
    block_height = get_block_count(network)

    return {
        "success": True,
        "network": network,
        "address": address,
        "block_height": block_height,
        "balances": {
            "NEO": {
                "amount": neo_balance,
                "decimals": 0,
                "contract": NEO_TOKEN
            },
            "GAS": {
                "amount": round(gas_balance, 8),
                "decimals": 8,
                "contract": GAS_TOKEN
            }
        },
        "unclaimed_gas": round(unclaimed_gas, 8),
        "other_tokens": other_tokens[:10],  # Limit to top 10
        "rpc_endpoint": NETWORK_CONFIG[network]["rpc_url"]
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        address = input_data.get("address")
        network = input_data.get("network", "mainnet")

        if not address:
            print(json.dumps({"error": "Missing required parameter: address"}))
            sys.exit(1)

        result = get_balance(address, network)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
