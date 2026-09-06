#!/usr/bin/env python3
"""
Uniswap V3 Quote Script
Fetches swap quotes from Uniswap V3 Quoter contract
"""

import json
import sys
import os
from typing import Optional

try:
    from web3 import Web3
    from web3.middleware import geth_poa_middleware
except ImportError:
    print(json.dumps({"error": "web3 package not installed. Run: pip install web3"}))
    sys.exit(1)

# Uniswap V3 Quoter V2 ABI (minimal)
QUOTER_V2_ABI = [
    {
        "inputs": [
            {
                "components": [
                    {"name": "tokenIn", "type": "address"},
                    {"name": "tokenOut", "type": "address"},
                    {"name": "amountIn", "type": "uint256"},
                    {"name": "fee", "type": "uint24"},
                    {"name": "sqrtPriceLimitX96", "type": "uint160"}
                ],
                "name": "params",
                "type": "tuple"
            }
        ],
        "name": "quoteExactInputSingle",
        "outputs": [
            {"name": "amountOut", "type": "uint256"},
            {"name": "sqrtPriceX96After", "type": "uint160"},
            {"name": "initializedTicksCrossed", "type": "uint32"},
            {"name": "gasEstimate", "type": "uint256"}
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# ERC20 ABI (minimal)
ERC20_ABI = [
    {"inputs": [], "name": "decimals", "outputs": [{"type": "uint8"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "symbol", "outputs": [{"type": "string"}], "stateMutability": "view", "type": "function"}
]

# Chain configurations
# RPC URLs sourced from Chainlist.org (https://chainlist.org)
CHAIN_CONFIG = {
    "ethereum": {
        "rpc": os.getenv("RPC_URL", "https://eth.llamarpc.com"),
        "quoter": "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
        "chain_id": 1
    },
    "polygon": {
        "rpc": os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com"),
        "quoter": "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
        "chain_id": 137
    },
    "arbitrum": {
        "rpc": os.getenv("ARBITRUM_RPC_URL", "https://arb1.arbitrum.io/rpc"),
        "quoter": "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
        "chain_id": 42161
    },
    "optimism": {
        "rpc": os.getenv("OPTIMISM_RPC_URL", "https://mainnet.optimism.io"),
        "quoter": "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
        "chain_id": 10
    },
    "base": {
        "rpc": os.getenv("BASE_RPC_URL", "https://mainnet.base.org"),
        "quoter": "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a",
        "chain_id": 8453
    }
}

# Common token addresses
COMMON_TOKENS = {
    "ethereum": {
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "DAI": "0x6B175474E89094C44Da98b954EeacdeCB5BE3830",
        "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    },
    "polygon": {
        "WMATIC": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"
    }
}

FEE_TIERS = [100, 500, 3000, 10000]  # 0.01%, 0.05%, 0.3%, 1%


def resolve_token(token: str, chain: str) -> str:
    """Resolve token symbol to address"""
    if token.startswith("0x") and len(token) == 42:
        return Web3.to_checksum_address(token)

    chain_tokens = COMMON_TOKENS.get(chain, {})
    upper_token = token.upper()
    if upper_token in chain_tokens:
        return chain_tokens[upper_token]

    raise ValueError(f"Unknown token: {token}")


def get_quote(token_in: str, token_out: str, amount_in: int, chain: str) -> dict:
    """Get best quote across all fee tiers"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    w3 = Web3(Web3.HTTPProvider(config["rpc"]))

    # Add PoA middleware for certain chains
    if chain in ["polygon", "bsc"]:
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    if not w3.is_connected():
        raise ConnectionError(f"Failed to connect to {chain} RPC")

    quoter = w3.eth.contract(
        address=Web3.to_checksum_address(config["quoter"]),
        abi=QUOTER_V2_ABI
    )

    # Get token info
    token_in_contract = w3.eth.contract(address=token_in, abi=ERC20_ABI)
    token_out_contract = w3.eth.contract(address=token_out, abi=ERC20_ABI)

    try:
        token_in_decimals = token_in_contract.functions.decimals().call()
        token_in_symbol = token_in_contract.functions.symbol().call()
    except:
        token_in_decimals = 18
        token_in_symbol = "TOKEN_IN"

    try:
        token_out_decimals = token_out_contract.functions.decimals().call()
        token_out_symbol = token_out_contract.functions.symbol().call()
    except:
        token_out_decimals = 18
        token_out_symbol = "TOKEN_OUT"

    best_quote = None
    best_amount = 0

    for fee in FEE_TIERS:
        try:
            result = quoter.functions.quoteExactInputSingle({
                "tokenIn": token_in,
                "tokenOut": token_out,
                "amountIn": amount_in,
                "fee": fee,
                "sqrtPriceLimitX96": 0
            }).call()

            amount_out = result[0]
            gas_estimate = result[3]

            if amount_out > best_amount:
                best_amount = amount_out
                best_quote = {
                    "fee_tier": fee,
                    "amount_out": amount_out,
                    "gas_estimate": gas_estimate
                }
        except Exception:
            continue

    if not best_quote:
        raise ValueError("No valid quote found across any fee tier")

    # Calculate price impact (simplified)
    amount_in_decimal = amount_in / (10 ** token_in_decimals)
    amount_out_decimal = best_quote["amount_out"] / (10 ** token_out_decimals)

    return {
        "success": True,
        "chain": chain,
        "token_in": {
            "address": token_in,
            "symbol": token_in_symbol,
            "amount": str(amount_in),
            "amount_decimal": amount_in_decimal
        },
        "token_out": {
            "address": token_out,
            "symbol": token_out_symbol,
            "amount": str(best_quote["amount_out"]),
            "amount_decimal": amount_out_decimal
        },
        "fee_tier": best_quote["fee_tier"] / 10000,  # Convert to percentage
        "gas_estimate": best_quote["gas_estimate"],
        "exchange_rate": amount_out_decimal / amount_in_decimal if amount_in_decimal > 0 else 0
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        token_in = input_data.get("token_in")
        token_out = input_data.get("token_out")
        amount = input_data.get("amount")
        chain = input_data.get("chain", "ethereum")

        if not all([token_in, token_out, amount]):
            print(json.dumps({"error": "Missing required parameters: token_in, token_out, amount"}))
            sys.exit(1)

        # Resolve token addresses
        token_in_addr = resolve_token(token_in, chain)
        token_out_addr = resolve_token(token_out, chain)

        # Get quote
        result = get_quote(token_in_addr, token_out_addr, int(amount), chain)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
