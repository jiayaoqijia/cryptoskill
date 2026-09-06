#!/usr/bin/env python3
"""
Estimate Optimize – eth_estimateGas for a tx, then suggest gas limit and EIP-1559 fees.
stdin JSON → stdout JSON.
"""

import json
import os
import sys
from typing import Any, Dict, Optional

from common import (
    CHAIN_CONFIG,
    fetch_api,
    get_eth_price,
    get_rpc_url,
    rpc_post,
)


def wei_to_gwei(wei: int) -> float:
    return wei / 1e9


def gwei_to_wei(gwei: float) -> int:
    return int(gwei * 1e9)


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


def estimate_optimize(
    chain: str,
    to: str,
    data: str,
    value: Optional[str] = None,
    from_addr: Optional[str] = None,
    buffer_pct: float = 1.15,
) -> Dict[str, Any]:
    if chain not in CHAIN_CONFIG:
        raise ValueError(f"Unsupported chain: {chain}")
    rpc_url = get_rpc_url(chain)
    cfg = CHAIN_CONFIG[chain]
    symbol = cfg["native_symbol"]

    tx: Dict[str, Any] = {"to": to, "data": data or "0x"}
    if value is not None and value != "0" and value != "":
        v = value
        if not (v.startswith("0x")):
            v = hex(int(v))
        tx["value"] = v
    if from_addr:
        tx["from"] = from_addr

    raw = rpc_post(rpc_url, "eth_estimateGas", [tx])
    estimated_hex = raw
    estimated = int(estimated_hex, 16) if isinstance(raw, str) else int(raw)
    suggested_limit = int(estimated * buffer_pct)

    oracle = get_gas_oracle(chain)
    base_gwei = oracle.get("base_fee_gwei")
    std_gwei = oracle.get("standard", 25.0)
    if base_gwei is None:
        base_gwei = std_gwei * 0.7

    # EIP-1559: maxFeePerGas >= baseFee + maxPriorityFeePerGas
    priority_gwei = max(1.0, (std_gwei - base_gwei) * 0.5)
    max_fee_gwei = base_gwei * 1.5 + priority_gwei

    eth_price = get_eth_price() if chain in ("ethereum", "arbitrum", "optimism", "base") else 0
    cost_wei = suggested_limit * gwei_to_wei(max_fee_gwei)
    cost_eth = cost_wei / 1e18
    cost_usd = cost_eth * eth_price if eth_price > 0 else None

    return {
        "success": True,
        "chain": chain,
        "native_symbol": symbol,
        "estimated_gas": estimated,
        "suggested_gas_limit": suggested_limit,
        "buffer_pct": buffer_pct,
        "eip1559": {
            "base_fee_gwei": round(base_gwei, 2),
            "max_priority_fee_gwei": round(priority_gwei, 2),
            "max_fee_per_gas_gwei": round(max_fee_gwei, 2),
        },
        "cost_eth": round(cost_eth, 6),
        "cost_usd": round(cost_usd, 2) if cost_usd is not None else None,
        "eth_price_usd": eth_price or None,
        "recommendation": "Use suggested_gas_limit and EIP-1559 fields when building the tx.",
    }


def main() -> None:
    try:
        inp = json.loads(sys.stdin.read())
        chain = inp.get("chain", "ethereum")
        to = inp.get("to", "")
        data = inp.get("data", "0x")
        value = inp.get("value")
        from_addr = inp.get("from")
        buffer_pct = float(inp.get("buffer_pct", 1.15))
        if buffer_pct < 1.0:
            buffer_pct = 1.0
        if not to or not data:
            print(json.dumps({"error": "Missing 'to' or 'data' for estimate"}))
            sys.exit(1)
        result = estimate_optimize(chain, to, data, value, from_addr, buffer_pct)
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
