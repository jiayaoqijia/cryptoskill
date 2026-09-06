#!/usr/bin/env python3
"""
Optimization Report – All-in-one gas optimization report: current gas, base fee prediction,
when-to-send, batch hint, and recommendations.
stdin JSON → stdout JSON.
"""

import json
import os
import sys
from typing import Any, Dict

from common import (
    CHAIN_CONFIG,
    GAS_LIMITS,
    fetch_api,
    get_eth_price,
    get_rpc_url,
    rpc_post,
)


def wei_to_gwei(wei: int) -> float:
    return wei / 1e9


def get_gas_oracle(chain: str) -> Dict[str, Any]:
    cfg = CHAIN_CONFIG[chain]
    api_key = os.getenv(cfg["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")
    params = {"module": "gastracker", "action": "gasoracle"}
    data = fetch_api(cfg["api_url"], params, api_key)
    if data.get("status") != "1":
        return {}
    r = data.get("result", {})
    base = r.get("suggestBaseFee") or r.get("SuggestBaseFee")
    return {
        "low": float(r.get("SafeGasPrice", 20)),
        "standard": float(r.get("ProposeGasPrice", 25)),
        "fast": float(r.get("FastGasPrice", 30)),
        "base_fee_gwei": float(base) if base else None,
    }


def fee_history_summary(chain: str, blocks: int = 15) -> Dict[str, Any]:
    try:
        rpc_url = get_rpc_url(chain)
        raw = rpc_post(rpc_url, "eth_feeHistory", [hex(blocks), "latest", [50.0]])
    except Exception:
        return {}
    base_fees = raw.get("baseFeePerGas") or []
    if not base_fees:
        return {}
    gwei = [wei_to_gwei(int(b, 16)) for b in base_fees]
    return {
        "avg_gwei": round(sum(gwei) / len(gwei), 2),
        "min_gwei": round(min(gwei), 2),
        "max_gwei": round(max(gwei), 2),
        "last_gwei": round(gwei[-1], 2),
    }


def optimization_report(chain: str, priority: str = "medium") -> Dict[str, Any]:
    if chain not in CHAIN_CONFIG:
        raise ValueError(f"Unsupported chain: {chain}")
    cfg = CHAIN_CONFIG[chain]
    symbol = cfg["native_symbol"]
    oracle = get_gas_oracle(chain)
    fee_hist = fee_history_summary(chain, 15)
    eth_price = get_eth_price() if chain in ("ethereum", "arbitrum", "optimism", "base") else 0

    low = oracle.get("low", 20)
    std = oracle.get("standard", 25)
    fast = oracle.get("fast", 30)
    base = oracle.get("base_fee_gwei")
    if base is None:
        base = fee_hist.get("last_gwei") or std * 0.7

    prio_map = {"low": low, "standard": std, "medium": std, "fast": fast}
    selected = prio_map.get(priority, std)

    ops = {
        "eth_transfer": GAS_LIMITS["eth_transfer"],
        "erc20_transfer": GAS_LIMITS["erc20_transfer"],
        "uniswap_swap": GAS_LIMITS["uniswap_swap"],
    }
    operation_costs = {}
    for name, gas in ops.items():
        cost_eth = (gas * selected * 1e9) / 1e18
        operation_costs[name] = {
            "gas": gas,
            "cost_eth": round(cost_eth, 6),
            "cost_usd": round(cost_eth * eth_price, 2) if eth_price > 0 else None,
        }

    when_to_send = "Weekends and 02:00–06:00 UTC often have lower gas. Use base_fee_predict for details."
    how_cheaper = [
        "Batch multiple operations (multicall) to save on base fee and overhead.",
        "Use EIP-1559 (maxFeePerGas / maxPriorityFeePerGas) and avoid overbidding.",
        "Use estimate_optimize for contract calls; avoid hardcoded gas limits.",
    ]
    if chain == "ethereum":
        when_to_send = (
            "Base fee varies. Use base_fee_predict for trend. Off-peak (weekends, early UTC) often cheaper."
        )
        how_cheaper.append(
            "For large data (e.g. L2 batches), consider EIP-4844 blobs; use blob_quote."
        )

    return {
        "success": True,
        "chain": chain,
        "native_symbol": symbol,
        "eth_price_usd": eth_price or None,
        "gas_prices_gwei": {
            "low": round(low, 2),
            "standard": round(std, 2),
            "fast": round(fast, 2),
            "base_fee": round(base, 2),
        },
        "selected_priority": priority,
        "selected_gas_price_gwei": round(selected, 2),
        "base_fee_history": fee_hist if fee_hist else None,
        "operation_costs": operation_costs,
        "when_to_send": when_to_send,
        "how_to_send_cheaper": how_cheaper,
        "related_tools": [
            "base_fee_predict – base fee trend and when-to-send",
            "batch_quote – batch vs separate gas",
            "estimate_optimize – per-tx estimate and EIP-1559",
            "blob_quote – EIP-4844 blob cost (Ethereum)",
        ],
    }


def main() -> None:
    try:
        inp = json.loads(sys.stdin.read())
        chain = inp.get("chain", "ethereum")
        priority = inp.get("priority", "medium")
        result = optimization_report(chain, priority)
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
