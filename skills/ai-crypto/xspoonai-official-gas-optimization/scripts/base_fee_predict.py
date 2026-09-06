#!/usr/bin/env python3
"""
Base Fee Predict – Base fee history, simple prediction, and when-to-send advice.
Uses eth_feeHistory. stdin JSON → stdout JSON.
"""

import json
import sys
from typing import Any, Dict, List

from common import CHAIN_CONFIG, get_rpc_url, rpc_post


def wei_to_gwei(wei: int) -> float:
    return wei / 1e9


def base_fee_predict(chain: str, blocks: int = 20) -> Dict[str, Any]:
    if chain not in CHAIN_CONFIG:
        raise ValueError(f"Unsupported chain: {chain}")
    rpc_url = get_rpc_url(chain)
    # eth_feeHistory: blockCount, newestBlock, rewardPercentiles (optional)
    raw = rpc_post(
        rpc_url,
        "eth_feeHistory",
        [hex(blocks), "latest", [25.0, 50.0, 75.0]],
    )
    if not raw:
        raise RuntimeError("Empty eth_feeHistory response")

    base_fees: List[float] = []
    for b in raw.get("baseFeePerGas", []):
        base_fees.append(wei_to_gwei(int(b, 16)))
    reward = raw.get("reward") or []

    avg = sum(base_fees) / len(base_fees) if base_fees else 0
    min_bf = min(base_fees) if base_fees else 0
    max_bf = max(base_fees) if base_fees else 0
    last = base_fees[-1] if base_fees else 0

    # Simple "next block" prediction: use recent average (last 5) or overall avg
    recent = base_fees[-5:] if len(base_fees) >= 5 else base_fees
    next_pred = sum(recent) / len(recent) if recent else avg

    # When-to-send heuristic (Ethereum-focused; L2s usually cheap)
    level = "LOW"
    when_hint = "Weekends and 02:00–06:00 UTC often have lower base fee. Current level is low."
    if chain == "ethereum":
        if avg > 40:
            level = "HIGH"
            when_hint = "Base fee is elevated. Prefer waiting for off-peak hours (weekends, early UTC) if not urgent."
        elif avg > 15:
            level = "MEDIUM"
            when_hint = "Moderate base fee. Good for non-urgent txs. Slightly lower often 02:00–06:00 UTC."

    out: Dict[str, Any] = {
        "success": True,
        "chain": chain,
        "blocks_analyzed": len(base_fees),
        "base_fee_gwei": {
            "min": round(min_bf, 2),
            "max": round(max_bf, 2),
            "avg": round(avg, 2),
            "last": round(last, 2),
            "next_block_prediction": round(next_pred, 2),
        },
        "base_fee_level": level,
        "when_to_send": when_hint,
    }
    if reward and len(reward) == len(base_fees):
        # Use 50th percentile tip as reference
        tips = [wei_to_gwei(int(r[1], 16)) for r in reward if r and len(r) > 1]
        if tips:
            out["priority_fee_50pct_gwei"] = round(sum(tips) / len(tips), 2)
    return out


def main() -> None:
    try:
        inp = json.loads(sys.stdin.read())
        chain = inp.get("chain", "ethereum")
        blocks = int(inp.get("blocks", 20))
        blocks = max(5, min(200, blocks))
        result = base_fee_predict(chain, blocks)
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
