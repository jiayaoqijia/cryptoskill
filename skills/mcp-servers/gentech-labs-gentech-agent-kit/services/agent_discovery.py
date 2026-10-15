"""
GenTech x402 backend — Agent Discovery (port 8091)

Wraps the 8004scan ERC-8004 registry API. Finds on-chain AI agents.
Paid via the x402 gateway (front gate), so this service only needs to
answer data requests. Accepts X-Payment-Proof for defense-in-depth but
the real verification happens at the gateway.
"""

import os
import time
import httpx
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="GenTech Agent Discovery", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

REGISTRY_API = os.getenv("A2A_DISCOVERY_API_URL", "https://8004scan.io/api/v1/agents")
_start = time.time()


@app.get("/v1/health")
async def health():
    return {"status": "ok", "service": "agent_discovery", "uptime": int(time.time() - _start)}


def _testnet_chain(chain_id) -> bool:
    return str(chain_id) in ("84532", "11155111", "1187947933", "0", "")


@app.get("/v1/agents/search")
async def search_agents(
    request: Request,
    q: str = Query("", description="Search term: name, tag, or service"),
    chain: str = Query("", description="Chain ID filter, e.g. 8453 (Base)"),
    limit: int = Query(10, ge=1, le=50),
):
    """Search the ERC-8004 registry for agents."""
    proof = request.headers.get("X-Payment-Proof", "")
    if not proof.strip():
        return JSONResponse(
            status_code=402,
            content={"error": "payment_required", "message": "X-Payment-Proof header required."},
        )

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(REGISTRY_API, params={"limit": 100})
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        return {"error": "registry_unavailable", "message": str(e)}

    agents = data if isinstance(data, list) else data.get("items", data.get("agents", data.get("data", [])))
    q_lower = q.lower().strip()
    results = []
    for a in agents:
        name = str(a.get("name", "") or "")
        desc = str(a.get("description", "") or "")
        tags = a.get("supported_protocols", []) or a.get("tags", []) or []
        tags_str = " ".join(tags) if isinstance(tags, list) else str(tags)
        chain_id = a.get("chain_id", a.get("chainId", a.get("network", "")))
        is_testnet = a.get("is_testnet", _testnet_chain(chain_id))
        haystack = f"{name} {desc} {tags_str}".lower()

        if q_lower and q_lower not in haystack:
            continue
        if chain and str(chain_id) != chain:
            continue
        if is_testnet or _testnet_chain(chain_id):
            continue

        results.append({
            "id": a.get("agent_id", a.get("id", a.get("agentId", ""))),
            "name": name or "Unnamed Agent",
            "description": desc[:300],
            "chainId": chain_id,
            "owner": a.get("owner_address", a.get("owner", "")),
            "tags": tags,
            "endpoints": a.get("service_endpoints", a.get("endpoints", [])),
            "x402": a.get("x402_supported", a.get("x402", False)),
            "createdAt": a.get("created_at", a.get("createdAt", "")),
            "verified": a.get("is_verified", False),
            "stars": a.get("star_count", 0),
        })
        if len(results) >= limit:
            break

    return {"query": q, "chain": chain, "count": len(results), "agents": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8091")))
