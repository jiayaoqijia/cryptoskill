#!/usr/bin/env python3
"""
Transaction Builder Script
Builds and encodes Ethereum transactions
"""

import json
import sys
import os
import urllib.request
import urllib.error
from typing import Optional

# Chain configurations
# Note: Polygon MATIC was renamed to POL on September 4, 2024
# Note: Etherscan API V1 deprecated Aug 2025, but still works for now
# RPC URLs sourced from Chainlist.org (https://chainlist.org)
CHAIN_CONFIG = {
    "ethereum": {
        "chain_id": 1,
        "rpc_url": "https://eth.llamarpc.com",
        "api_url": "https://api.etherscan.io/api",
        "api_key_env": "ETHERSCAN_API_KEY",
        "native_symbol": "ETH"
    },
    "polygon": {
        "chain_id": 137,
        "rpc_url": "https://polygon-rpc.com",
        "api_url": "https://api.polygonscan.com/api",
        "api_key_env": "POLYGONSCAN_API_KEY",
        "native_symbol": "POL"  # Renamed from MATIC on Sept 4, 2024
    },
    "arbitrum": {
        "chain_id": 42161,
        "rpc_url": "https://arb1.arbitrum.io/rpc",
        "api_url": "https://api.arbiscan.io/api",
        "api_key_env": "ARBISCAN_API_KEY",
        "native_symbol": "ETH"
    },
    "optimism": {
        "chain_id": 10,
        "rpc_url": "https://mainnet.optimism.io",
        "api_url": "https://api-optimistic.etherscan.io/api",
        "api_key_env": "OPTIMISM_API_KEY",
        "native_symbol": "ETH"
    },
    "base": {
        "chain_id": 8453,
        "rpc_url": "https://base.llamarpc.com",
        "api_url": "https://api.basescan.org/api",
        "api_key_env": "BASESCAN_API_KEY",
        "native_symbol": "ETH"
    },
    "bsc": {
        "chain_id": 56,
        "rpc_url": "https://bsc-dataseed.bnbchain.org",
        "api_url": "https://api.bscscan.com/api",
        "api_key_env": "BSCSCAN_API_KEY",
        "native_symbol": "BNB"
    },
    "zksync": {
        "chain_id": 324,
        "rpc_url": "https://mainnet.era.zksync.io",
        "api_url": "https://block-explorer-api.mainnet.zksync.io/api",
        "api_key_env": "ZKSYNC_API_KEY",
        "native_symbol": "ETH"
    },
    "linea": {
        "chain_id": 59144,
        "rpc_url": "https://rpc.linea.build",
        "api_url": "https://api.lineascan.build/api",
        "api_key_env": "LINEASCAN_API_KEY",
        "native_symbol": "ETH"
    },
    "neox": {
        "chain_id": 47763,
        "rpc_url": "https://mainnet-1.rpc.banelabs.org",
        "api_url": "https://xexplorer.neo.org/api",
        "api_key_env": "NEOX_API_KEY",
        "native_symbol": "GAS"
    }
}

# ERC20 function signatures
ERC20_TRANSFER_SIG = "0xa9059cbb"  # transfer(address,uint256)
ERC20_APPROVE_SIG = "0x095ea7b3"  # approve(address,uint256)


def fetch_api(base_url: str, params: dict, api_key: Optional[str] = None) -> dict:
    """Fetch data from Etherscan-like API"""
    if api_key:
        params["apikey"] = api_key

    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{base_url}?{query}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TxBuilder/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to fetch data: {e}")


def get_nonce(address: str, chain: str) -> int:
    """Get current nonce for address"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    api_key = os.getenv(config["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")

    params = {
        "module": "proxy",
        "action": "eth_getTransactionCount",
        "address": address,
        "tag": "pending"
    }

    data = fetch_api(config["api_url"], params, api_key)

    if data.get("result"):
        return int(data["result"], 16)

    return 0


def get_gas_price(chain: str) -> dict:
    """Get current gas prices"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    api_key = os.getenv(config["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")

    params = {
        "module": "gastracker",
        "action": "gasoracle"
    }

    data = fetch_api(config["api_url"], params, api_key)

    if data.get("status") == "1":
        result = data.get("result", {})
        return {
            "low": int(float(result.get("SafeGasPrice", 20))),
            "medium": int(float(result.get("ProposeGasPrice", 25))),
            "fast": int(float(result.get("FastGasPrice", 30)))
        }

    # Fallback
    return {"low": 20, "medium": 25, "fast": 30}


def get_balance(address: str, chain: str) -> float:
    """Get native balance"""
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
        return int(data.get("result", 0)) / 1e18

    return 0


def encode_address(address: str) -> str:
    """Encode address to 32 bytes"""
    return address.lower().replace("0x", "").zfill(64)


def encode_uint256(value: int) -> str:
    """Encode uint256 to 32 bytes"""
    return hex(value)[2:].zfill(64)


def eth_to_wei(eth_amount: float) -> int:
    """Convert ETH to wei"""
    return int(eth_amount * 1e18)


def build_eth_transfer(from_addr: str, to_addr: str, amount: float, chain: str, priority: str = "medium") -> dict:
    """Build ETH transfer transaction"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    # Validate addresses
    if not from_addr.startswith("0x") or len(from_addr) != 42:
        raise ValueError(f"Invalid from address: {from_addr}")
    if not to_addr.startswith("0x") or len(to_addr) != 42:
        raise ValueError(f"Invalid to address: {to_addr}")

    # Get nonce
    nonce = get_nonce(from_addr, chain)

    # Get gas price
    gas_prices = get_gas_price(chain)
    gas_price_gwei = gas_prices.get(priority, gas_prices["medium"])

    # Check balance
    balance = get_balance(from_addr, chain)
    if balance < amount:
        raise ValueError(f"Insufficient balance: {balance} {config['native_symbol']} < {amount}")

    # Gas limit for ETH transfer
    gas_limit = 21000

    # Calculate max fee
    gas_cost_eth = (gas_limit * gas_price_gwei) / 1e9
    total_cost = amount + gas_cost_eth

    if balance < total_cost:
        raise ValueError(f"Insufficient balance for amount + gas: {balance} < {total_cost}")

    # Build transaction
    value_wei = eth_to_wei(amount)

    tx = {
        "from": from_addr,
        "to": to_addr,
        "value": hex(value_wei),
        "gas": hex(gas_limit),
        "maxFeePerGas": hex(int(gas_price_gwei * 1.5 * 1e9)),
        "maxPriorityFeePerGas": hex(int(gas_price_gwei * 1e9)),
        "nonce": hex(nonce),
        "chainId": config["chain_id"],
        "type": "0x2"  # EIP-1559
    }

    return {
        "success": True,
        "action": "eth_transfer",
        "chain": chain,
        "transaction": tx,
        "human_readable": {
            "from": from_addr,
            "to": to_addr,
            "amount": f"{amount} {config['native_symbol']}",
            "gas_limit": gas_limit,
            "gas_price": f"{gas_price_gwei} gwei",
            "estimated_fee": f"{gas_cost_eth:.6f} {config['native_symbol']}",
            "total_cost": f"{total_cost:.6f} {config['native_symbol']}",
            "nonce": nonce
        },
        "warnings": []
    }


def build_token_transfer(from_addr: str, to_addr: str, token_addr: str, amount: float, decimals: int, chain: str, priority: str = "medium") -> dict:
    """Build ERC20 token transfer transaction"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    # Validate addresses
    for addr, name in [(from_addr, "from"), (to_addr, "to"), (token_addr, "token")]:
        if not addr.startswith("0x") or len(addr) != 42:
            raise ValueError(f"Invalid {name} address: {addr}")

    # Get nonce
    nonce = get_nonce(from_addr, chain)

    # Get gas price
    gas_prices = get_gas_price(chain)
    gas_price_gwei = gas_prices.get(priority, gas_prices["medium"])

    # Gas limit for token transfer
    gas_limit = 65000

    # Convert amount to token units
    amount_raw = int(amount * (10 ** decimals))

    # Encode transfer function call
    # transfer(address to, uint256 amount)
    data = ERC20_TRANSFER_SIG + encode_address(to_addr) + encode_uint256(amount_raw)

    # Calculate gas cost
    gas_cost_eth = (gas_limit * gas_price_gwei) / 1e9

    # Check ETH balance for gas
    eth_balance = get_balance(from_addr, chain)
    if eth_balance < gas_cost_eth:
        raise ValueError(f"Insufficient ETH for gas: {eth_balance} < {gas_cost_eth}")

    # Build transaction
    tx = {
        "from": from_addr,
        "to": token_addr,
        "value": "0x0",
        "data": data,
        "gas": hex(gas_limit),
        "maxFeePerGas": hex(int(gas_price_gwei * 1.5 * 1e9)),
        "maxPriorityFeePerGas": hex(int(gas_price_gwei * 1e9)),
        "nonce": hex(nonce),
        "chainId": config["chain_id"],
        "type": "0x2"
    }

    return {
        "success": True,
        "action": "token_transfer",
        "chain": chain,
        "transaction": tx,
        "human_readable": {
            "from": from_addr,
            "to": to_addr,
            "token_contract": token_addr,
            "amount": f"{amount} tokens",
            "gas_limit": gas_limit,
            "gas_price": f"{gas_price_gwei} gwei",
            "estimated_fee": f"{gas_cost_eth:.6f} {config['native_symbol']}",
            "nonce": nonce
        },
        "warnings": ["Ensure you have sufficient token balance before signing"]
    }


def build_approve(from_addr: str, spender: str, token_addr: str, amount: float, decimals: int, chain: str, priority: str = "medium") -> dict:
    """Build ERC20 approval transaction"""
    config = CHAIN_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    # Validate addresses
    for addr, name in [(from_addr, "from"), (spender, "spender"), (token_addr, "token")]:
        if not addr.startswith("0x") or len(addr) != 42:
            raise ValueError(f"Invalid {name} address: {addr}")

    # Get nonce
    nonce = get_nonce(from_addr, chain)

    # Get gas price
    gas_prices = get_gas_price(chain)
    gas_price_gwei = gas_prices.get(priority, gas_prices["medium"])

    # Gas limit for approval
    gas_limit = 46000

    # Convert amount to token units
    amount_raw = int(amount * (10 ** decimals))

    # Encode approve function call
    # approve(address spender, uint256 amount)
    data = ERC20_APPROVE_SIG + encode_address(spender) + encode_uint256(amount_raw)

    # Calculate gas cost
    gas_cost_eth = (gas_limit * gas_price_gwei) / 1e9

    # Build transaction
    tx = {
        "from": from_addr,
        "to": token_addr,
        "value": "0x0",
        "data": data,
        "gas": hex(gas_limit),
        "maxFeePerGas": hex(int(gas_price_gwei * 1.5 * 1e9)),
        "maxPriorityFeePerGas": hex(int(gas_price_gwei * 1e9)),
        "nonce": hex(nonce),
        "chainId": config["chain_id"],
        "type": "0x2"
    }

    warnings = []
    if amount_raw == 2**256 - 1:
        warnings.append("WARNING: Unlimited approval. Consider using exact amounts instead.")

    return {
        "success": True,
        "action": "token_approve",
        "chain": chain,
        "transaction": tx,
        "human_readable": {
            "from": from_addr,
            "spender": spender,
            "token_contract": token_addr,
            "approval_amount": f"{amount} tokens" if amount_raw < 2**256 - 1 else "UNLIMITED",
            "gas_limit": gas_limit,
            "gas_price": f"{gas_price_gwei} gwei",
            "estimated_fee": f"{gas_cost_eth:.6f} {config['native_symbol']}",
            "nonce": nonce
        },
        "warnings": warnings
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        action = input_data.get("action", "transfer_eth")
        from_addr = input_data.get("from")
        to_addr = input_data.get("to")
        amount = float(input_data.get("amount", 0))
        chain = input_data.get("chain", "ethereum")
        priority = input_data.get("priority", "medium")

        if not from_addr:
            print(json.dumps({"error": "Missing required parameter: from"}))
            sys.exit(1)

        if action == "transfer_eth":
            if not to_addr:
                print(json.dumps({"error": "Missing required parameter: to"}))
                sys.exit(1)
            result = build_eth_transfer(from_addr, to_addr, amount, chain, priority)

        elif action == "transfer_token":
            token_addr = input_data.get("token")
            decimals = int(input_data.get("decimals", 18))
            if not to_addr or not token_addr:
                print(json.dumps({"error": "Missing required parameters: to, token"}))
                sys.exit(1)
            result = build_token_transfer(from_addr, to_addr, token_addr, amount, decimals, chain, priority)

        elif action == "approve":
            spender = input_data.get("spender")
            token_addr = input_data.get("token")
            decimals = int(input_data.get("decimals", 18))
            if not spender or not token_addr:
                print(json.dumps({"error": "Missing required parameters: spender, token"}))
                sys.exit(1)
            result = build_approve(from_addr, spender, token_addr, amount, decimals, chain, priority)

        else:
            print(json.dumps({"error": f"Unknown action: {action}"}))
            sys.exit(1)

        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
