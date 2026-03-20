"""
Subgraph Registry MCP Server

Exposes the classified subgraph registry as MCP tools that agents can call
to discover and select the right subgraph before querying The Graph.

Tools:
  - search_subgraphs: Filter by domain, network, protocol type, entity, keyword
  - recommend_subgraph: Natural language goal -> best subgraphs
  - get_subgraph_detail: Full classification detail for a specific subgraph
  - list_registry_stats: Available domains, networks, protocol types
"""

import json
import sqlite3
import sys
import urllib.request
import tempfile
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DB_PATH = DATA_DIR / "registry.db"

# GitHub raw URL for the pre-built registry
GITHUB_DB_URL = "https://github.com/PaulieB14/subgraph-registry/raw/main/python/data/registry.db"


def ensure_db():
    """Download the registry DB from GitHub if not present locally."""
    if DB_PATH.exists():
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Registry not found locally. Downloading from GitHub...", file=sys.stderr)

    try:
        urllib.request.urlretrieve(GITHUB_DB_URL, str(DB_PATH))
        size_mb = DB_PATH.stat().st_size / 1024 / 1024
        print(f"Downloaded registry.db ({size_mb:.1f} MB)", file=sys.stderr)
    except Exception as e:
        print(f"Failed to download registry: {e}", file=sys.stderr)
        print(f"Run `python registry.py` to build it locally.", file=sys.stderr)
        sys.exit(1)


def get_db():
    ensure_db()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row):
    return {k: row[k] for k in row.keys()}


# ── Tool Implementations ─────────────────────────────────────

def search_subgraphs(
    query: str = "",
    domain: str = "",
    network: str = "",
    protocol_type: str = "",
    entity: str = "",
    min_reliability: float = 0.0,
    limit: int = 20,
) -> str:
    """Search and filter classified subgraphs."""
    conn = get_db()
    conditions = []
    params = []

    if domain:
        conditions.append("domain = ?")
        params.append(domain)
    if network:
        conditions.append("network = ?")
        params.append(network)
    if protocol_type:
        conditions.append("protocol_type = ?")
        params.append(protocol_type)
    if entity:
        conditions.append("canonical_entities LIKE ?")
        params.append(f'%"{entity}"%')
    if min_reliability > 0:
        conditions.append("reliability_score >= ?")
        params.append(min_reliability)
    if query:
        # Split into words and match any word (OR) across name/description/auto_description
        words = [w for w in query.strip().split() if len(w) > 2]
        if words:
            word_conds = []
            for w in words[:5]:
                word_conds.append("(display_name LIKE ? OR description LIKE ? OR auto_description LIKE ?)")
                params.extend([f"%{w}%", f"%{w}%", f"%{w}%"])
            conditions.append(f"({' OR '.join(word_conds)})")
        else:
            conditions.append("(display_name LIKE ? OR description LIKE ? OR auto_description LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # Over-fetch to allow dedup by IPFS hash (same deployment, different subgraph IDs)
    fetch_limit = limit * 3
    sql = f"""
        SELECT id, display_name, description, auto_description, domain, protocol_type, network,
               reliability_score, ipfs_hash, entity_count, canonical_entities,
               powered_by_substreams
        FROM subgraphs
        {where}
        ORDER BY reliability_score DESC
        LIMIT ?
    """
    params.append(fetch_limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    # Dedup by IPFS hash — keep highest reliability per deployment
    results = []
    seen_ipfs = set()
    for r in rows:
        ipfs = r["ipfs_hash"]
        if ipfs and ipfs in seen_ipfs:
            continue
        if ipfs:
            seen_ipfs.add(ipfs)
        results.append({
            "id": r["id"],
            "display_name": r["display_name"],
            "description": (r["description"] or r["auto_description"] or "")[:300],
            "domain": r["domain"],
            "protocol_type": r["protocol_type"],
            "network": r["network"],
            "reliability_score": r["reliability_score"],
            "ipfs_hash": r["ipfs_hash"],
            "entity_count": r["entity_count"],
            "canonical_entities": json.loads(r["canonical_entities"]),
            "powered_by_substreams": bool(r["powered_by_substreams"]),
            "query_url": f"https://gateway.thegraph.com/api/[api-key]/subgraphs/id/{r['id']}",
        })
        if len(results) >= limit:
            break

    return json.dumps({
        "total": len(results),
        "subgraphs": results,
        "query_instructions": "To query a subgraph: POST a GraphQL query to the query_url (replace [api-key] with your Graph API key from https://thegraph.com/studio/apikeys/). First fetch the schema with get_subgraph_detail to see available entities and fields.",
    }, indent=2)


def recommend_subgraph(goal: str, chain: str = "") -> str:
    """Given a natural-language goal, find the best matching subgraphs."""
    goal_lower = goal.lower()

    # Infer domain
    domain_map = {
        "defi": ["defi", "swap", "trade", "lend", "borrow", "yield", "stake", "liquidity", "pool", "token"],
        "nfts": ["nft", "collectible", "art", "marketplace"],
        "dao": ["governance", "vote", "proposal", "dao"],
        "identity": ["ens", "domain", "name", "identity"],
        "infrastructure": ["indexer", "graph", "oracle"],
        "social": ["social", "profile", "post", "lens"],
        "gaming": ["game", "player", "quest"],
    }
    type_map = {
        "dex": ["dex", "swap", "trade", "exchange", "amm", "uniswap", "sushi"],
        "lending": ["lend", "borrow", "loan", "collateral", "aave", "compound"],
        "bridge": ["bridge", "cross-chain"],
        "staking": ["stake", "validator", "delegation"],
        "options": ["option", "call", "put", "strike"],
        "perpetuals": ["perp", "perpetual", "leverage", "margin"],
        "governance": ["governance", "vote", "proposal"],
        "name-service": ["ens", "name service", "domain name"],
        "nft-marketplace": ["nft market", "opensea", "blur"],
    }

    domains = [d for d, kws in domain_map.items() if any(k in goal_lower for k in kws)]
    ptypes = [t for t, kws in type_map.items() if any(k in goal_lower for k in kws)]

    conn = get_db()
    conditions = []
    params = []

    if chain:
        conditions.append("network = ?")
        params.append(chain)
    if domains:
        conditions.append(f"domain IN ({','.join('?' * len(domains))})")
        params.extend(domains)
    if ptypes:
        conditions.append(f"protocol_type IN ({','.join('?' * len(ptypes))})")
        params.extend(ptypes)

    # Fallback to text search if no hints matched
    if not domains and not ptypes:
        words = [w for w in goal_lower.split() if len(w) > 2]
        if words:
            text_conds = []
            for w in words[:5]:
                text_conds.append("(display_name LIKE ? OR description LIKE ?)")
                params.extend([f"%{w}%", f"%{w}%"])
            conditions.append(f"({' OR '.join(text_conds)})")

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = f"""
        SELECT id, display_name, description, auto_description, domain, protocol_type, network,
               reliability_score, ipfs_hash, canonical_entities
        FROM subgraphs
        {where}
        ORDER BY reliability_score DESC
        LIMIT 15
    """

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    # Dedup by IPFS hash
    recommendations = []
    seen_ipfs = set()
    for r in rows:
        ipfs = r["ipfs_hash"]
        if ipfs and ipfs in seen_ipfs:
            continue
        if ipfs:
            seen_ipfs.add(ipfs)
        recommendations.append({
            "id": r["id"],
            "display_name": r["display_name"],
            "description": (r["description"] or r["auto_description"] or "")[:300],
            "domain": r["domain"],
            "protocol_type": r["protocol_type"],
            "network": r["network"],
            "reliability_score": r["reliability_score"],
            "ipfs_hash": r["ipfs_hash"],
            "canonical_entities": json.loads(r["canonical_entities"]),
            "query_url": f"https://gateway.thegraph.com/api/[api-key]/subgraphs/id/{r['id']}",
        })
        if len(recommendations) >= 5:
            break

    return json.dumps({
        "goal": goal,
        "chain_filter": chain or None,
        "inferred_domain": domains or None,
        "inferred_protocol_type": ptypes or None,
        "total_matches": len(recommendations),
        "recommendations": recommendations,
    }, indent=2)


def get_subgraph_detail(subgraph_id: str) -> str:
    """Get full classification detail for a specific subgraph by ID or IPFS hash."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM subgraphs WHERE id = ? OR ipfs_hash = ?",
        (subgraph_id, subgraph_id),
    ).fetchone()
    conn.close()

    if not row:
        return json.dumps({"error": f"Subgraph '{subgraph_id}' not found"})

    d = row_to_dict(row)
    d["canonical_entities"] = json.loads(d["canonical_entities"])
    d["categories"] = json.loads(d["categories"])
    return json.dumps(d, indent=2)


def list_registry_stats() -> str:
    """Get registry overview: available domains, networks, protocol types, and counts."""
    conn = get_db()

    domains = conn.execute(
        "SELECT domain, COUNT(*) as count FROM subgraphs GROUP BY domain ORDER BY count DESC"
    ).fetchall()
    networks = conn.execute(
        "SELECT network, COUNT(*) as count FROM subgraphs WHERE network IS NOT NULL GROUP BY network ORDER BY count DESC"
    ).fetchall()
    ptypes = conn.execute(
        "SELECT protocol_type, COUNT(*) as count FROM subgraphs GROUP BY protocol_type ORDER BY count DESC"
    ).fetchall()
    total = conn.execute("SELECT COUNT(*) FROM subgraphs").fetchone()[0]

    conn.close()

    return json.dumps({
        "total_subgraphs": total,
        "domains": {r["domain"]: r["count"] for r in domains},
        "networks": {r["network"]: r["count"] for r in networks},
        "protocol_types": {r["protocol_type"]: r["count"] for r in ptypes},
    }, indent=2)


# ── MCP Protocol (JSON-RPC over stdio) ───────────────────────

TOOLS = [
    {
        "name": "search_subgraphs",
        "description": "Search and filter the classified subgraph registry. Filter by domain (defi, nfts, dao, gaming, identity, infrastructure, social, analytics), network (mainnet, arbitrum-one, base, matic, bsc, optimism, avalanche), protocol_type (dex, lending, bridge, staking, options, perpetuals, nft-marketplace, yield-aggregator, governance, name-service), canonical entity type (liquidity_pool, trade, token, position, vault, loan, collateral, liquidation, nft_collection, nft_item, nft_sale, proposal, delegate, domain_name, account, transaction, daily_snapshot, hourly_snapshot), or free-text keyword. Returns subgraphs ranked by reliability score.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Free-text search across names and descriptions"},
                "domain": {"type": "string", "description": "Filter by domain: defi, nfts, dao, gaming, identity, infrastructure, social, analytics"},
                "network": {"type": "string", "description": "Filter by chain: mainnet, arbitrum-one, base, matic, bsc, optimism, avalanche, etc."},
                "protocol_type": {"type": "string", "description": "Filter by protocol type: dex, lending, bridge, staking, options, perpetuals, etc."},
                "entity": {"type": "string", "description": "Filter by canonical entity: liquidity_pool, trade, token, position, vault, loan, etc."},
                "min_reliability": {"type": "number", "description": "Minimum reliability score (0-1). Higher = more signal/stake/fees."},
                "limit": {"type": "integer", "description": "Max results to return (default: 20)", "default": 20},
            },
        },
    },
    {
        "name": "recommend_subgraph",
        "description": "Given a natural-language goal like 'find DEX trades on Arbitrum' or 'get lending liquidation data', returns the best matching subgraphs with reliability scores and query instructions. Automatically infers domain and protocol type from the goal.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "goal": {"type": "string", "description": "What you want to do, e.g. 'query Uniswap pool data on Base'"},
                "chain": {"type": "string", "description": "Optional chain filter: mainnet, arbitrum-one, base, matic, etc."},
            },
            "required": ["goal"],
        },
    },
    {
        "name": "get_subgraph_detail",
        "description": "Get full classification detail for a specific subgraph by its subgraph ID or IPFS hash. Returns domain, protocol type, canonical entities, reliability score, signal data, and metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subgraph_id": {"type": "string", "description": "Subgraph ID or IPFS hash (Qm...)"},
            },
            "required": ["subgraph_id"],
        },
    },
    {
        "name": "list_registry_stats",
        "description": "Get an overview of the subgraph registry: total count, available domains, networks, and protocol types with counts. Use this to understand what data is available before searching.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]

TOOL_HANDLERS = {
    "search_subgraphs": lambda args: search_subgraphs(**args),
    "recommend_subgraph": lambda args: recommend_subgraph(**args),
    "get_subgraph_detail": lambda args: get_subgraph_detail(**args),
    "list_registry_stats": lambda args: list_registry_stats(),
}


def handle_request(request: dict) -> dict:
    method = request.get("method", "")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "subgraph-registry",
                    "version": "0.1.0",
                },
            },
        }

    if method == "notifications/initialized":
        return None  # No response for notifications

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        }

    if method == "tools/call":
        tool_name = request["params"]["name"]
        tool_args = request["params"].get("arguments", {})

        handler = TOOL_HANDLERS.get(tool_name)
        if not handler:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }

        try:
            result_text = handler(tool_args)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": result_text}],
                },
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"error": str(e)})}],
                    "isError": True,
                },
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main():
    """Run MCP server over stdio (JSON-RPC)."""
    print("Subgraph Registry MCP server starting...", file=sys.stderr)

    # Download from GitHub if not local
    ensure_db()

    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM subgraphs").fetchone()[0]
    conn.close()
    print(f"Loaded registry: {count} subgraphs from {DB_PATH}", file=sys.stderr)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue

        response = handle_request(request)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
