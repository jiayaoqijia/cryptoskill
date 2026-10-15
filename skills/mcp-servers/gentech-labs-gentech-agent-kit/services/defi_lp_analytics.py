"""
GenTech x402 backend — DeFi LP Analytics (port 8092)

Wraps DexScreener to score LP positions for a token address.
Paid via the x402 gateway (front gate); X-Payment-Proof accepted here
for defense-in-depth. Efficiency scoring mirrors our LFJ rebalancing engine.
"""

import os
import time
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="GenTech DeFi LP Analytics", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_start = time.time()


@app.get("/v1/health")
async def health():
    return {"status": "ok", "service": "defi_lp_analytics", "uptime": int(time.time() - _start)}


def _score_efficiency(pair: dict) -> dict:
    """Score an LP position's efficiency — mirrors LFJ rebalancing engine."""
    try:
        fee = float(pair.get("fee", {}).get("volume", 0) or 0)
        liquidity = float(pair.get("liquidity", {}).get("usd", 0) or 0)
        txns = pair.get("txns", {}).get("h24", {})
        buys = int(txns.get("buys", 0) or 0)
        sells = int(txns.get("sells", 0) or 0)
        total = buys + sells
        buy_ratio = (buys / total) if total else 0.5
    except (TypeError, ValueError):
        fee, liquidity, buy_ratio = 0.0, 0.0, 0.5

    # Fee-to-liquidity ratio: higher = more efficient capital
    fee_eff = min(fee / liquidity, 1.0) if liquidity > 0 else 0.0
    # Buy pressure: balanced-ish with slight buy tilt is healthy
    balance = 1.0 - abs(buy_ratio - 0.55) * 2
    balance = max(0.0, min(1.0, balance))

    score = round(100 * (0.6 * fee_eff + 0.4 * balance))
    return {
        "efficiency_score": score,
        "fee_to_liquidity": round(fee_eff, 6),
        "buy_ratio_24h": round(buy_ratio, 4),
        "signal": "rebalance" if score < 40 else ("hold" if score < 70 else "optimize"),
    }


@app.get("/v1/defi/lp/{address}")
async def lp_analytics(address: str, request: Request):
    proof = request.headers.get("X-Payment-Proof", "")
    if not proof.strip():
        return JSONResponse(
            status_code=402,
            content={"error": "payment_required", "message": "X-Payment-Proof header required."},
        )

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(f"https://api.dexscreener.com/latest/dex/tokens/{address}")
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        return {"error": "dexscreener_unavailable", "message": str(e)}

    pairs = data.get("pairs", []) or []
    scored = []
    for p in pairs[:10]:
        scored.append({
            "dex": p.get("dexId", ""),
            "pair": p.get("baseToken", {}).get("symbol", "") + "/" + p.get("quoteToken", {}).get("symbol", ""),
            "priceUsd": p.get("priceUsd", ""),
            "liquidityUsd": p.get("liquidity", {}).get("usd", 0),
            "volume24hUsd": p.get("volume", {}).get("h24", 0),
            "fee24hUsd": p.get("fee", {}).get("h24", 0),
            **{k: v for k, v in _score_efficiency(p).items()},
        })

    scored.sort(key=lambda x: x.get("efficiency_score", 0), reverse=True)
    return {
        "address": address,
        "chain": data.get("chainId", ""),
        "pairs_analyzed": len(scored),
        "best_pool": scored[0] if scored else None,
        "pools": scored,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8092")))
