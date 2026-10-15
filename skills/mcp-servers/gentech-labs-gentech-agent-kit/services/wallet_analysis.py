"""
GenTech x402 backend — Wallet Analysis (port 8093)

Portfolio analysis for a Solana wallet: token balances via Solana RPC,
priced via DexScreener. Multi-chain friendly (EVM via public RPC later).
Paid via the x402 gateway (front gate); X-Payment-Proof accepted here.
"""

import os
import time
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="GenTech Wallet Analysis", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SOLANA_RPC = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
_start = time.time()


@app.get("/v1/health")
async def health():
    return {"status": "ok", "service": "wallet_analysis", "uptime": int(time.time() - _start)}


async def _rpc(method: str, params: list):
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(SOLANA_RPC, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
        resp.raise_for_status()
        return resp.json().get("result")


async def _price_usd(mint: str) -> float:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"https://api.dexscreener.com/latest/dex/tokens/{mint}")
            pairs = resp.json().get("pairs", []) or []
            for p in pairs:
                if p.get("priceUsd"):
                    return float(p["priceUsd"])
    except Exception:
        pass
    return 0.0


@app.get("/v1/wallet/portfolio/{address}")
async def wallet_portfolio(address: str, request: Request):
    proof = request.headers.get("X-Payment-Proof", "")
    if not proof.strip():
        return JSONResponse(
            status_code=402,
            content={"error": "payment_required", "message": "X-Payment-Proof header required."},
        )

    try:
        accounts = await _rpc("getTokenAccountsByOwner", [
            address,
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
            {"encoding": "jsonParsed"},
        ])
        lamports = await _rpc("getBalance", [address])
    except Exception as e:
        return {"error": "rpc_unavailable", "message": str(e)}

    sol_balance = (lamports or {}).get("value", 0) / 1e9 if lamports else 0.0
    tokens = []
    total_usd = 0.0
    if accounts:
        for item in accounts.get("value", [])[:40]:
            try:
                info = item["account"]["data"]["parsed"]["info"]
                mint = info["mint"]
                amount = float(info["tokenAmount"]["uiAmount"] or 0)
                if amount <= 0:
                    continue
                price = await _price_usd(mint)
                usd = amount * price
                total_usd += usd
                tokens.append({
                    "mint": mint,
                    "symbol": info.get("tokenAmount", {}).get("decimals", 0),
                    "amount": round(amount, 6),
                    "priceUsd": price,
                    "valueUsd": round(usd, 2),
                })
            except Exception:
                continue

    tokens.sort(key=lambda x: x["valueUsd"], reverse=True)
    return {
        "address": address,
        "chain": "solana",
        "solBalance": round(sol_balance, 6),
        "solValueUsd": round(sol_balance * (await _price_usd("So11111111111111111111111111111111111111112")), 2),
        "tokenCount": len(tokens),
        "totalValueUsd": round(total_usd, 2),
        "tokens": tokens[:20],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8093")))
