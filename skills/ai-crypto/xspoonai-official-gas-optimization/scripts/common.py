#!/usr/bin/env python3
"""
Shared config and helpers for gas-optimization scripts.
"""

import json
import os
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

CHAIN_CONFIG: Dict[str, Dict[str, Any]] = {
    "ethereum": {
        "chain_id": 1,
        "rpc_url": "https://eth.llamarpc.com",
        "api_url": "https://api.etherscan.io/api",
        "api_key_env": "ETHERSCAN_API_KEY",
        "native_symbol": "ETH",
        "block_time": 12,
    },
    "polygon": {
        "chain_id": 137,
        "rpc_url": "https://polygon-rpc.com",
        "api_url": "https://api.polygonscan.com/api",
        "api_key_env": "POLYGONSCAN_API_KEY",
        "native_symbol": "POL",
        "block_time": 2,
    },
    "arbitrum": {
        "chain_id": 42161,
        "rpc_url": "https://arb1.arbitrum.io/rpc",
        "api_url": "https://api.arbiscan.io/api",
        "api_key_env": "ARBISCAN_API_KEY",
        "native_symbol": "ETH",
        "block_time": 0.25,
    },
    "optimism": {
        "chain_id": 10,
        "rpc_url": "https://mainnet.optimism.io",
        "api_url": "https://api-optimistic.etherscan.io/api",
        "api_key_env": "OPTIMISM_API_KEY",
        "native_symbol": "ETH",
        "block_time": 2,
    },
    "base": {
        "chain_id": 8453,
        "rpc_url": "https://mainnet.base.org",
        "api_url": "https://api.basescan.org/api",
        "api_key_env": "BASESCAN_API_KEY",
        "native_symbol": "ETH",
        "block_time": 2,
    },
}

RPC_ENV_MAP = {
    "ethereum": "ETHEREUM_RPC",
    "polygon": "POLYGON_RPC",
    "arbitrum": "ARBITRUM_RPC",
    "optimism": "OPTIMISM_RPC",
    "base": "BASE_RPC",
}

GAS_LIMITS = {
    "eth_transfer": 21000,
    "erc20_transfer": 65000,
    "erc20_approve": 46000,
    "nft_transfer": 85000,
    "nft_mint": 200000,
    "uniswap_swap": 150000,
    "uniswap_add_liquidity": 250000,
    "aave_deposit": 200000,
    "aave_borrow": 300000,
    "contract_deploy": 500000,
}

# Multicall-style batching: one base + multicall logic; save (n-1)*21k vs separate txs
MULTICALL_OVERHEAD_BASE = 26000  # 21k base + ~5k multicall wrapper
BASE_GAS_PER_TX = 21000


def get_rpc_url(chain: str) -> str:
    env_key = RPC_ENV_MAP.get(chain)
    if env_key and os.getenv(env_key):
        return os.getenv(env_key, "")
    return CHAIN_CONFIG[chain]["rpc_url"]


def rpc_post(rpc_url: str, method: str, params: List[Any]) -> Any:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        rpc_url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "GasOptimization/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            out = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"RPC request failed: {e}") from e
    if "error" in out:
        msg = out["error"].get("message", "RPC error")
        raise RuntimeError(f"RPC error: {msg}")
    return out.get("result")


def fetch_api(base_url: str, params: dict, api_key: Optional[str] = None) -> dict:
    if api_key:
        params["apikey"] = api_key
    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{base_url}?{query}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GasOptimization/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"API request failed: {e}") from e


def get_eth_price() -> float:
    api_key = os.getenv("ETHERSCAN_API_KEY")
    params = {"module": "stats", "action": "ethprice"}
    try:
        data = fetch_api("https://api.etherscan.io/api", params, api_key)
        if data.get("status") == "1":
            return float(data["result"].get("ethusd", 0))
    except Exception:
        pass
    return 0.0
