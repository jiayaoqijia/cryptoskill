#!/usr/bin/env python3
"""
Solana Balance Script
Fetches SOL and SPL token balances for a wallet
"""

import json
import sys
import os
import urllib.request
import urllib.error
from typing import Dict, List, Optional

# Default RPC endpoints
DEFAULT_RPC = "https://api.mainnet-beta.solana.com"

# Known token mints
KNOWN_TOKENS = {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": {"symbol": "USDC", "decimals": 6},
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": {"symbol": "USDT", "decimals": 6},
    "So11111111111111111111111111111111111111112": {"symbol": "wSOL", "decimals": 9},
    "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN": {"symbol": "JUP", "decimals": 6},
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": {"symbol": "BONK", "decimals": 5},
    "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So": {"symbol": "mSOL", "decimals": 9},
    "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn": {"symbol": "JitoSOL", "decimals": 9},
    "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs": {"symbol": "ETH", "decimals": 8},
    "7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj": {"symbol": "stSOL", "decimals": 9}
}

# Token program IDs
TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
TOKEN_2022_PROGRAM_ID = "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"


def rpc_request(method: str, params: list, rpc_url: str = None) -> dict:
    """Make JSON-RPC request to Solana"""
    url = rpc_url or os.getenv("SOLANA_RPC_URL", DEFAULT_RPC)

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "SolanaBalance/1.0"
            }
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"RPC request failed: {e}")


def get_sol_balance(address: str) -> Dict:
    """Get SOL balance for an address"""
    result = rpc_request("getBalance", [address])

    if "error" in result:
        raise ValueError(f"RPC error: {result['error']}")

    lamports = result.get("result", {}).get("value", 0)
    sol = lamports / 1e9

    return {
        "lamports": lamports,
        "sol": sol
    }


def get_token_accounts(address: str) -> List[Dict]:
    """Get all SPL token accounts for an address"""
    # Get Token Program accounts
    params = [
        address,
        {"programId": TOKEN_PROGRAM_ID},
        {"encoding": "jsonParsed"}
    ]

    result = rpc_request("getTokenAccountsByOwner", params)

    if "error" in result:
        return []

    accounts = result.get("result", {}).get("value", [])
    token_balances = []

    for account in accounts:
        try:
            parsed = account.get("account", {}).get("data", {}).get("parsed", {})
            info = parsed.get("info", {})
            token_amount = info.get("tokenAmount", {})

            mint = info.get("mint", "")
            amount = int(token_amount.get("amount", 0))
            decimals = token_amount.get("decimals", 0)
            ui_amount = token_amount.get("uiAmount", 0)

            if amount > 0:
                token_info = KNOWN_TOKENS.get(mint, {"symbol": "UNKNOWN", "decimals": decimals})
                token_balances.append({
                    "mint": mint,
                    "symbol": token_info["symbol"],
                    "balance": ui_amount,
                    "raw_amount": str(amount),
                    "decimals": decimals,
                    "token_account": account.get("pubkey")
                })
        except Exception:
            continue

    # Sort by symbol (known tokens first)
    token_balances.sort(key=lambda x: (x["symbol"] == "UNKNOWN", x["symbol"]))

    return token_balances


def get_stake_accounts(address: str) -> Dict:
    """Get stake accounts for an address using getProgramAccounts with stake program"""
    # Stake Program ID
    STAKE_PROGRAM_ID = "Stake11111111111111111111111111111111111111"

    # Note: getProgramAccounts with memcmp filter for stake authority
    # This is a simplified approach - stake accounts have complex structure
    params = [
        STAKE_PROGRAM_ID,
        {
            "encoding": "jsonParsed",
            "filters": [
                {"memcmp": {"offset": 12, "bytes": address}}  # Staker authority offset
            ]
        }
    ]

    result = rpc_request("getProgramAccounts", params)

    # Handle response
    if "error" in result or not result.get("result"):
        return {"count": 0, "total_staked": 0, "accounts": [], "note": "No stake accounts found or RPC error"}

    accounts = result.get("result", [])

    return {
        "count": len(accounts),
        "note": "Use Solana Explorer or CLI for detailed stake account info"
    }


def get_wallet_balance(address: str) -> Dict:
    """Get comprehensive wallet balance"""
    # Validate address format (basic check)
    if len(address) < 32 or len(address) > 44:
        raise ValueError(f"Invalid Solana address format: {address}")

    # Get SOL balance
    sol_balance = get_sol_balance(address)

    # Get SPL token balances
    token_balances = get_token_accounts(address)

    # Filter for significant balances
    significant_tokens = [t for t in token_balances if t["balance"] > 0.001]

    # Categorize tokens
    stablecoins = [t for t in significant_tokens if t["symbol"] in ["USDC", "USDT"]]
    liquid_staking = [t for t in significant_tokens if t["symbol"] in ["mSOL", "JitoSOL", "stSOL", "bSOL"]]
    other_tokens = [t for t in significant_tokens if t not in stablecoins and t not in liquid_staking]

    return {
        "success": True,
        "address": address,
        "network": "mainnet-beta",
        "sol_balance": {
            "sol": round(sol_balance["sol"], 9),
            "lamports": sol_balance["lamports"],
            "rent_exempt_minimum": 0.00203928  # Approximate minimum for rent exemption
        },
        "token_holdings": {
            "total_tokens": len(significant_tokens),
            "stablecoins": stablecoins,
            "liquid_staking": liquid_staking,
            "other_tokens": other_tokens[:10]  # Limit display
        },
        "summary": {
            "has_sol": sol_balance["sol"] > 0,
            "has_tokens": len(significant_tokens) > 0,
            "estimated_staked_sol": sum(t["balance"] for t in liquid_staking),
            "activity_status": "ACTIVE" if sol_balance["sol"] > 0 or len(significant_tokens) > 0 else "EMPTY"
        }
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        address = input_data.get("address")

        if not address:
            print(json.dumps({"error": "Missing required parameter: address"}))
            sys.exit(1)

        result = get_wallet_balance(address)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
