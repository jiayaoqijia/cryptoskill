#!/usr/bin/env python3
"""
Blob Quote – EIP-4844 blob gas cost on Ethereum (Cancun+). eth_blobBaseFee.
stdin JSON → stdout JSON.
"""

import json
import sys
from typing import Any, Dict

from common import CHAIN_CONFIG, get_eth_price, get_rpc_url, rpc_post


def wei_to_gwei(wei: int) -> float:
    return wei / 1e9


# EIP-4844: 1 blob ~= 128 KB; blob gas per blob = 131072
BLOB_GAS_PER_BLOB = 131072


def blob_quote(chain: str, blob_count: int = 1) -> Dict[str, Any]:
    if chain != "ethereum":
        return {
            "success": True,
            "chain": chain,
            "blob_supported": False,
            "message": "EIP-4844 blob gas is only relevant on Ethereum mainnet (Cancun+).",
        }
    rpc_url = get_rpc_url(chain)
    try:
        raw = rpc_post(rpc_url, "eth_blobBaseFee", [])
    except Exception as e:
        return {
            "success": False,
            "chain": chain,
            "error": str(e),
            "message": "eth_blobBaseFee may not be supported (pre-Cancun or RPC without blob support).",
        }
    blob_base_wei = int(raw, 16) if isinstance(raw, str) else int(raw)
    blob_base_gwei = wei_to_gwei(blob_base_wei)
    gas_per_blob = BLOB_GAS_PER_BLOB * blob_base_wei
    cost_per_blob_eth = gas_per_blob / 1e18
    eth_price = get_eth_price()
    cost_per_blob_usd = cost_per_blob_eth * eth_price if eth_price > 0 else None

    total_gas = blob_count * BLOB_GAS_PER_BLOB
    total_cost_eth = (total_gas * blob_base_wei) / 1e18
    total_cost_usd = total_cost_eth * eth_price if eth_price > 0 else None

    return {
        "success": True,
        "chain": chain,
        "blob_supported": True,
        "blob_base_fee_gwei": round(blob_base_gwei, 4),
        "blob_gas_per_blob": BLOB_GAS_PER_BLOB,
        "cost_per_blob_eth": round(cost_per_blob_eth, 8),
        "cost_per_blob_usd": round(cost_per_blob_usd, 4) if cost_per_blob_usd is not None else None,
        "eth_price_usd": eth_price or None,
        "requested_blob_count": blob_count,
        "total_blob_gas": total_gas,
        "total_blob_cost_eth": round(total_cost_eth, 8),
        "total_blob_cost_usd": round(total_cost_usd, 4) if total_cost_usd is not None else None,
        "note": "Blobs are used for L2 batch data, etc. Include blob tx params when building EIP-4844 txs.",
    }


def main() -> None:
    try:
        inp = json.loads(sys.stdin.read())
        chain = inp.get("chain", "ethereum")
        blob_count = int(inp.get("blob_count", 1))
        blob_count = max(1, min(6, blob_count))
        result = blob_quote(chain, blob_count)
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
