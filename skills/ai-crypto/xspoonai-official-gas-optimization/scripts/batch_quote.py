#!/usr/bin/env python3
"""
Batch Quote – Compare batch (multicall-style) vs separate transaction gas and savings.
stdin JSON → stdout JSON.
"""

import json
import os
import sys
from typing import Any, Dict, List, Union

from common import (
    BASE_GAS_PER_TX,
    CHAIN_CONFIG,
    GAS_LIMITS,
    MULTICALL_OVERHEAD_BASE,
    fetch_api,
    get_eth_price,
    get_rpc_url,
    rpc_post,
)


def wei_to_gwei(wei: int) -> float:
    return wei / 1e9


def gwei_to_wei(gwei: float) -> int:
    return int(gwei * 1e9)


def get_gas_price_gwei(chain: str) -> float:
    cfg = CHAIN_CONFIG[chain]
    api_key = os.getenv(cfg["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")
    params = {"module": "gastracker", "action": "gasoracle"}
    data = fetch_api(cfg["api_url"], params, api_key)
    if data.get("status") == "1":
        r = data.get("result", {})
        return float(r.get("ProposeGasPrice", r.get("SafeGasPrice", 25)))
    # Fallback eth_gasPrice
    rpc_url = get_rpc_url(chain)
    r = rpc_post(rpc_url, "eth_gasPrice", [])
    return wei_to_gwei(int(r, 16))


def resolve_operations(ops: List[Union[str, int]]) -> List[int]:
    out: List[int] = []
    for x in ops:
        if isinstance(x, int):
            out.append(max(21000, x))
        elif isinstance(x, str) and x in GAS_LIMITS:
            out.append(GAS_LIMITS[x])
        else:
            out.append(GAS_LIMITS.get("erc20_transfer", 65000))
    return out


def batch_quote(chain: str, operations: List[Union[str, int]]) -> Dict[str, Any]:
    if chain not in CHAIN_CONFIG:
        raise ValueError(f"Unsupported chain: {chain}")
    gas_limits = resolve_operations(operations)
    separate_total = sum(gas_limits)
    n = len(gas_limits)
    if n <= 1:
        batched = separate_total
    else:
        # One base + multicall wrapper; save (n-1)*21k vs separate txs
        batched = MULTICALL_OVERHEAD_BASE + sum(gas_limits) - (n - 1) * BASE_GAS_PER_TX
    gas_price = get_gas_price_gwei(chain)
    eth_price = get_eth_price() if chain in ("ethereum", "arbitrum", "optimism", "base") else 0
    symbol = CHAIN_CONFIG[chain]["native_symbol"]

    def cost_gwei(gas: int) -> float:
        return gas * gas_price

    cost_sep_gwei = cost_gwei(separate_total)
    cost_batch_gwei = cost_gwei(batched)
    savings_gwei = max(0, cost_sep_gwei - cost_batch_gwei)
    cost_sep_eth = (separate_total * gwei_to_wei(gas_price)) / 1e18
    cost_batch_eth = (batched * gwei_to_wei(gas_price)) / 1e18
    savings_eth = max(0, cost_sep_eth - cost_batch_eth)
    savings_usd = savings_eth * eth_price if eth_price > 0 else None

    return {
        "success": True,
        "chain": chain,
        "native_symbol": symbol,
        "operations": operations,
        "gas_limits": gas_limits,
        "gas_price_gwei": round(gas_price, 2),
        "eth_price_usd": eth_price or None,
        "separate": {
            "total_gas": separate_total,
            "cost_eth": round(cost_sep_eth, 6),
            "cost_usd": round(cost_sep_eth * eth_price, 2) if eth_price > 0 else None,
        },
        "batched": {
            "total_gas": batched,
            "cost_eth": round(cost_batch_eth, 6),
            "cost_usd": round(cost_batch_eth * eth_price, 2) if eth_price > 0 else None,
        },
        "savings": {
            "gas_saved": max(0, separate_total - batched),
            "cost_eth_saved": round(savings_eth, 6),
            "cost_usd_saved": round(savings_usd, 2) if savings_usd is not None else None,
        },
        "recommendation": (
            "Batch transactions (e.g. multicall) to save gas when making multiple calls."
            if n > 1
            else "Single operation; batching not applicable."
        ),
    }


def main() -> None:
    try:
        inp = json.loads(sys.stdin.read())
        chain = inp.get("chain", "ethereum")
        ops = inp.get("operations", ["erc20_transfer", "erc20_transfer", "uniswap_swap"])
        result = batch_quote(chain, ops)
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
