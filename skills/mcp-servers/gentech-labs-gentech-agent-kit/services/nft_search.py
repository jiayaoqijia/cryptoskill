"""
GenTech x402 backend — NFT Search (port 8094)

Searches Solana NFT collections via Magic Eden's public API.
Paid via the x402 gateway (front gate); X-Payment-Proof accepted here.
"""

import os
import time
import httpx
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="GenTech NFT Search", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_start = time.time()


@app.get("/v1/health")
async def health():
    return {"status": "ok", "service": "nft_search", "uptime": int(time.time() - _start)}


@app.get("/v1/nft/search")
async def nft_search(
    request: Request,
    q: str = Query(..., description="Collection name or symbol search"),
    limit: int = Query(10, ge=1, le=25),
):
    proof = request.headers.get("X-Payment-Proof", "")
    if not proof.strip():
        return JSONResponse(
            status_code=402,
            content={"error": "payment_required", "message": "X-Payment-Proof header required."},
        )

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            # Magic Eden v2 doesn't support search param; fetch batches and
            # filter client-side (offset/limit must be multiples of 20)
            resp = await client.get(
                "https://api-mainnet.magiceden.dev/v2/collections",
                params={"offset": 0, "limit": 100},
                headers={"accept": "application/json"},
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        return {"error": "magiceden_unavailable", "message": str(e)}

    q_lower = q.lower().strip()
    results = []
    for c in data if isinstance(data, list) else []:
        symbol = str(c.get("symbol", "") or "")
        name = str(c.get("name", "") or "")
        if q_lower and q_lower not in f"{name} {symbol}".lower():
            continue
        results.append({
            "symbol": symbol,
            "name": name,
            "description": (c.get("description") or "")[:300],
            "image": c.get("image", ""),
            "totalSupply": c.get("totalSupply", c.get("totalItems", 0)),
            "floorPrice": c.get("floorPrice", {}).get("value", 0) if isinstance(c.get("floorPrice"), dict) else c.get("floorPrice", 0),
            "listedCount": c.get("listedCount", 0),
            "volume24h": c.get("volume24h", 0),
        })
        if len(results) >= limit:
            break

    return {"query": q, "count": len(results), "collections": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8094")))
