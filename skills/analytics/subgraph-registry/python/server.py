"""
Subgraph Registry API Server

FastAPI-based REST API for agent-friendly subgraph discovery.

Endpoints:
  GET /summary              - Registry overview
  GET /domains              - Domain breakdown
  GET /networks             - Network breakdown
  GET /families             - Schema family groups (fork/clone detection)
  GET /subgraphs            - Filter & search subgraphs
  GET /subgraphs/{id}       - Full detail for one subgraph
  GET /search?q=            - Free-text search
  GET /recommend            - Agent-optimized: "find the best subgraph for X"
"""

import json
import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DATA_DIR = Path(__file__).parent / "data"
REGISTRY_FILE = DATA_DIR / "registry.json"
SQLITE_FILE = DATA_DIR / "registry.db"

app = FastAPI(
    title="Subgraph Registry",
    description="Agent-friendly semantic classification of all subgraphs on The Graph Network",
    version="0.1.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Load registry on startup
registry = None


@app.on_event("startup")
def load_registry():
    global registry
    if not REGISTRY_FILE.exists():
        raise RuntimeError("Registry not found. Run `python registry.py` first.")
    registry = json.loads(REGISTRY_FILE.read_text())
    print(f"Loaded registry: {len(registry['subgraphs'])} subgraphs")


def _db():
    """Get SQLite connection for fast queries."""
    if SQLITE_FILE.exists():
        conn = sqlite3.connect(str(SQLITE_FILE))
        conn.row_factory = sqlite3.Row
        return conn
    return None


# ── Endpoints ────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "name": "Subgraph Registry API",
        "version": registry["version"],
        "total_subgraphs": registry["summary"]["total_subgraphs"],
        "generated_at": registry["generated_at"],
        "endpoints": [
            "GET /summary",
            "GET /domains",
            "GET /networks",
            "GET /families",
            "GET /subgraphs?domain=&network=&protocol_type=&entity=&q=&min_reliability=&limit=&offset=",
            "GET /subgraphs/{id}",
            "GET /search?q=",
            "GET /recommend?goal=&chain=",
        ],
    }


@app.get("/summary")
def summary():
    return {
        "version": registry["version"],
        "generated_at": registry["generated_at"],
        "network_stats": registry["network_stats"],
        "summary": registry["summary"],
    }


@app.get("/domains")
def domains():
    return registry["summary"]["by_domain"]


@app.get("/networks")
def networks():
    return registry["summary"]["by_network"]


@app.get("/families")
def families():
    return registry["summary"]["top_schema_families"]


@app.get("/subgraphs")
def list_subgraphs(
    domain: Optional[str] = None,
    network: Optional[str] = None,
    protocol_type: Optional[str] = None,
    entity: Optional[str] = None,
    q: Optional[str] = None,
    min_reliability: float = 0.0,
    substreams: Optional[bool] = None,
    limit: int = Query(50, le=500),
    offset: int = 0,
):
    results = registry["subgraphs"]

    if domain:
        results = [s for s in results if s["domain"] == domain]
    if network:
        results = [s for s in results if s.get("network") == network]
    if protocol_type:
        results = [s for s in results if s["protocol_type"] == protocol_type]
    if entity:
        results = [s for s in results if any(
            ce.get("canonical_type") == entity for ce in s.get("canonical_entities", [])
        )]
    if min_reliability > 0:
        results = [s for s in results if s["reliability_score"] >= min_reliability]
    if substreams is not None:
        results = [s for s in results if s.get("powered_by_substreams") == substreams]
    if q:
        ql = q.lower()
        results = [s for s in results if
                   ql in (s.get("display_name") or "").lower() or
                   ql in (s.get("description") or "").lower()]

    results.sort(key=lambda s: s["reliability_score"], reverse=True)

    return {
        "total": len(results),
        "limit": limit,
        "offset": offset,
        "subgraphs": [
            {
                "id": s["id"],
                "display_name": s.get("display_name"),
                "description": s.get("description"),
                "domain": s["domain"],
                "protocol_type": s["protocol_type"],
                "network": s.get("network"),
                "reliability_score": s["reliability_score"],
                "ipfs_hash": s.get("ipfs_hash"),
                "entity_count": s.get("entity_count", 0),
                "canonical_entities": [ce["canonical_type"] for ce in s.get("canonical_entities", [])],
                "powered_by_substreams": s.get("powered_by_substreams", False),
            }
            for s in results[offset:offset + limit]
        ],
    }


@app.get("/subgraphs/{subgraph_id}")
def get_subgraph(subgraph_id: str):
    sg = next(
        (s for s in registry["subgraphs"]
         if s["id"] == subgraph_id or s.get("ipfs_hash") == subgraph_id),
        None,
    )
    if not sg:
        raise HTTPException(404, "Subgraph not found")
    return sg


@app.get("/search")
def search(q: str = Query(..., min_length=1), limit: int = Query(20, le=100)):
    ql = q.lower()
    results = [
        s for s in registry["subgraphs"]
        if ql in (s.get("display_name") or "").lower()
        or ql in (s.get("description") or "").lower()
        or ql in (s.get("protocol_type") or "")
        or ql in (s.get("domain") or "")
    ]
    results.sort(key=lambda s: s["reliability_score"], reverse=True)

    return {
        "query": q,
        "total": len(results),
        "results": [
            {
                "id": s["id"],
                "display_name": s.get("display_name"),
                "domain": s["domain"],
                "protocol_type": s["protocol_type"],
                "network": s.get("network"),
                "reliability_score": s["reliability_score"],
                "ipfs_hash": s.get("ipfs_hash"),
            }
            for s in results[:limit]
        ],
    }


@app.get("/recommend")
def recommend(
    goal: str = Query(..., description="What the agent wants to do, e.g. 'query DEX trades on Arbitrum'"),
    chain: Optional[str] = None,
    limit: int = Query(5, le=20),
):
    """
    Agent-optimized endpoint. Accepts a natural-language goal and returns
    the best matching subgraphs with usage instructions.
    """
    goal_lower = goal.lower()

    # Extract domain/type hints from goal
    domain_hints = []
    type_hints = []

    domain_map = {
        "defi": ["defi", "swap", "trade", "lend", "borrow", "yield", "stake", "liquidity", "pool"],
        "nfts": ["nft", "collectible", "art", "marketplace"],
        "dao": ["governance", "vote", "proposal", "dao"],
        "identity": ["ens", "domain", "name", "identity"],
        "infrastructure": ["indexer", "graph", "oracle", "infrastructure"],
        "social": ["social", "profile", "post", "lens"],
    }
    type_map = {
        "dex": ["dex", "swap", "trade", "exchange", "amm"],
        "lending": ["lend", "borrow", "loan", "collateral"],
        "bridge": ["bridge", "cross-chain"],
        "staking": ["stake", "validator"],
        "options": ["option", "call", "put", "strike"],
        "perpetuals": ["perp", "perpetual", "leverage", "margin"],
        "governance": ["governance", "vote", "proposal"],
        "name-service": ["ens", "name service", "domain"],
    }

    for domain, keywords in domain_map.items():
        if any(kw in goal_lower for kw in keywords):
            domain_hints.append(domain)

    for ptype, keywords in type_map.items():
        if any(kw in goal_lower for kw in keywords):
            type_hints.append(ptype)

    # Filter
    results = registry["subgraphs"]
    if chain:
        results = [s for s in results if s.get("network") == chain]
    if domain_hints:
        results = [s for s in results if s["domain"] in domain_hints]
    if type_hints:
        results = [s for s in results if s["protocol_type"] in type_hints]

    # If no matches from hints, fall back to text search
    if not results and not domain_hints and not type_hints:
        results = [
            s for s in registry["subgraphs"]
            if any(word in (s.get("display_name") or "").lower() for word in goal_lower.split())
            or any(word in (s.get("description") or "").lower() for word in goal_lower.split())
        ]

    results.sort(key=lambda s: s["reliability_score"], reverse=True)

    return {
        "goal": goal,
        "chain_filter": chain,
        "inferred_domain": domain_hints or None,
        "inferred_protocol_type": type_hints or None,
        "total_matches": len(results),
        "recommendations": [
            {
                "id": s["id"],
                "display_name": s.get("display_name"),
                "description": s.get("description"),
                "domain": s["domain"],
                "protocol_type": s["protocol_type"],
                "network": s.get("network"),
                "reliability_score": s["reliability_score"],
                "ipfs_hash": s.get("ipfs_hash"),
                "canonical_entities": [ce["canonical_type"] for ce in s.get("canonical_entities", [])],
                "query_hint": f"Use subgraph ID '{s['id']}' or IPFS hash '{s.get('ipfs_hash')}' to query via The Graph Gateway",
            }
            for s in results[:limit]
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=3847, reload=True)
