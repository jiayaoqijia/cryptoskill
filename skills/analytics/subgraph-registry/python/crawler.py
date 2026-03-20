"""
Subgraph Registry Crawler

Queries the Graph Network Arbitrum subgraph to pull metadata, schemas,
signal data, and deployment info for all 15K+ active subgraphs.

Handles:
- Pagination past The Graph's 5000 skip limit via ID-based cursoring
- Incremental sync via createdAt/updatedAt timestamps
- Batched schema fetching with rate limiting
- Streaming JSON output to handle large datasets
"""

import asyncio
import json
import time
from pathlib import Path
from datetime import datetime, timezone

import os

import httpx

# Load .env file if present
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip())

GRAPH_NETWORK_SUBGRAPH_ID = "DZz4kDTdmzWLWsV373w2bSmoar3umKKH9y82SUKr5qmp"

# Support API key via env var or .env
GATEWAY_API_KEY = os.environ.get("GATEWAY_API_KEY", "")
if GATEWAY_API_KEY:
    GATEWAY_URL = f"https://gateway.thegraph.com/api/{GATEWAY_API_KEY}/subgraphs/id/{GRAPH_NETWORK_SUBGRAPH_ID}"
else:
    GATEWAY_URL = f"https://gateway.thegraph.com/api/subgraphs/id/{GRAPH_NETWORK_SUBGRAPH_ID}"

PAGE_SIZE = 1000
SCHEMA_BATCH_SIZE = 10
DATA_DIR = Path(__file__).parent / "data"

# ── GraphQL Queries ──────────────────────────────────────────

SUBGRAPHS_QUERY = """
query CrawlSubgraphs($first: Int!, $lastId: String!, $minUpdatedAt: Int!) {
  subgraphs(
    first: $first
    orderBy: id
    orderDirection: asc
    where: { active: true, id_gt: $lastId, updatedAt_gte: $minUpdatedAt }
  ) {
    id
    createdAt
    updatedAt
    currentSignalledTokens
    signalledTokens
    unsignalledTokens
    nameSignalAmount
    metadata {
      displayName
      description
      categories
      codeRepository
      website
    }
    owner {
      id
      defaultName { name }
    }
    currentVersion {
      version
      subgraphDeployment {
        ipfsHash
        signalledTokens
        stakedTokens
        queryFeesAmount
        indexingRewardAmount
        curatorFeeRewards
        activeSubgraphCount
        deniedAt
        manifest {
          network
          poweredBySubstreams
          schemaIpfsHash
          startBlock
        }
      }
    }
  }
}
"""

SCHEMAS_QUERY = """
query FetchSchemas($ids: [String!]!) {
  subgraphDeploymentManifests(where: { id_in: $ids }) {
    id
    network
    schema { id schema }
  }
}
"""

NETWORK_STATS_QUERY = """
{
  graphNetwork(id: "1") {
    subgraphCount
    activeSubgraphCount
    totalQueryFees
    totalIndexingRewards
  }
}
"""


async def query_subgraph(client: httpx.AsyncClient, query: str, variables: dict | None = None) -> dict:
    """Execute a GraphQL query against the Graph Network subgraph."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    for attempt in range(3):
        try:
            resp = await client.post(GATEWAY_URL, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            if "errors" in data:
                raise Exception(f"GraphQL errors: {data['errors']}")
            return data["data"]
        except (httpx.HTTPStatusError, httpx.ReadTimeout) as e:
            if attempt < 2:
                wait = 2 ** attempt
                print(f"  Retry {attempt+1} after {wait}s: {e}")
                await asyncio.sleep(wait)
            else:
                raise


async def crawl_all_subgraphs(client: httpx.AsyncClient, min_updated_at: int = 0) -> list[dict]:
    """
    Crawl all active subgraphs using ID-based cursor pagination.
    This avoids The Graph's 5000 skip limit.
    """
    all_subgraphs = []
    last_id = ""
    page = 0

    print(f"Crawling subgraphs (updated after {datetime.fromtimestamp(min_updated_at, tz=timezone.utc).isoformat() if min_updated_at else 'epoch'})...")

    while True:
        data = await query_subgraph(client, SUBGRAPHS_QUERY, {
            "first": PAGE_SIZE,
            "lastId": last_id,
            "minUpdatedAt": min_updated_at,
        })

        batch = data["subgraphs"]
        all_subgraphs.extend(batch)
        page += 1

        print(f"  Page {page}: +{len(batch)} (total: {len(all_subgraphs)})")

        if len(batch) < PAGE_SIZE:
            break

        last_id = batch[-1]["id"]
        await asyncio.sleep(0.2)  # gentle rate limit

    return all_subgraphs


async def fetch_schemas(client: httpx.AsyncClient, ipfs_hashes: list[str]) -> dict[str, str]:
    """Fetch schema text for deployments, batched to avoid query size limits."""
    schemas = {}
    total = len(ipfs_hashes)

    for i in range(0, total, SCHEMA_BATCH_SIZE):
        batch = ipfs_hashes[i:i + SCHEMA_BATCH_SIZE]
        try:
            data = await query_subgraph(client, SCHEMAS_QUERY, {"ids": batch})
            for manifest in data.get("subgraphDeploymentManifests", []):
                if manifest.get("schema") and manifest["schema"].get("schema"):
                    schemas[manifest["id"]] = manifest["schema"]["schema"]
        except Exception as e:
            print(f"  Schema batch error at {i}: {e}")

        done = min(i + SCHEMA_BATCH_SIZE, total)
        if done % 100 == 0 or done == total:
            print(f"  Schemas fetched: {len(schemas)}/{total}")

        await asyncio.sleep(0.1)

    return schemas


def flatten_subgraph(sg: dict, schemas: dict[str, str]) -> dict:
    """Flatten a raw subgraph response into a clean record."""
    meta = sg.get("metadata") or {}
    deployment = (sg.get("currentVersion") or {}).get("subgraphDeployment") or {}
    manifest = deployment.get("manifest") or {}
    ipfs_hash = deployment.get("ipfsHash")
    owner = sg.get("owner") or {}

    return {
        "id": sg["id"],
        "display_name": meta.get("displayName"),
        "description": meta.get("description"),
        "categories": meta.get("categories") or [],
        "code_repository": meta.get("codeRepository"),
        "website": meta.get("website"),
        "owner_id": owner.get("id"),
        "owner_name": (owner.get("defaultName") or {}).get("name"),
        "created_at": sg.get("createdAt", 0),
        "updated_at": sg.get("updatedAt", 0),
        "current_signalled_tokens": sg.get("currentSignalledTokens", "0"),
        # Deployment
        "ipfs_hash": ipfs_hash,
        "network": manifest.get("network"),
        "powered_by_substreams": manifest.get("poweredBySubstreams", False),
        "start_block": manifest.get("startBlock"),
        "signalled_tokens": deployment.get("signalledTokens", "0"),
        "staked_tokens": deployment.get("stakedTokens", "0"),
        "query_fees": deployment.get("queryFeesAmount", "0"),
        "indexing_rewards": deployment.get("indexingRewardAmount", "0"),
        "curator_fees": deployment.get("curatorFeeRewards", "0"),
        "active_subgraph_count": deployment.get("activeSubgraphCount", 0),
        "denied_at": deployment.get("deniedAt", 0),
        # Schema (can be None)
        "schema": schemas.get(ipfs_hash) if ipfs_hash else None,
    }


QOS_SUBGRAPH_ID = "Dtr9rETvwokot4BSXaD5tECanXfqfJKcvHuaaEgPDD2D"
QOS_EPOCH_START = 1608163200  # Day 0 of QoS day numbering (2020-12-17)

QOS_DAY_QUERY = """
query($dayStart: BigInt!, $nextDay: BigInt!, $lastId: String!) {
  queryDailyDataPoints(
    first: 1000
    orderBy: id
    orderDirection: asc
    where: { dayStart_gte: $dayStart, dayStart_lt: $nextDay, id_gt: $lastId }
  ) {
    id
    subgraphDeployment { id }
    query_count
  }
}
"""


async def _fetch_qos_day(client: httpx.AsyncClient, qos_url: str, day_start: int) -> dict[str, int]:
    """Fetch all query volumes for a single UTC day."""
    next_day = day_start + 86400
    volumes: dict[str, int] = {}
    last_id = ""

    for _ in range(10):  # Max pages per day
        for attempt in range(3):
            try:
                resp = await client.post(
                    qos_url,
                    json={
                        "query": QOS_DAY_QUERY,
                        "variables": {
                            "dayStart": str(day_start),
                            "nextDay": str(next_day),
                            "lastId": last_id,
                        },
                    },
                    timeout=60,
                )
                resp_json = resp.json()
                if "errors" in resp_json:
                    if attempt < 2:
                        await asyncio.sleep(3)
                        continue
                    return volumes  # Return what we have
                points = resp_json.get("data", {}).get("queryDailyDataPoints", [])
                break
            except Exception:
                if attempt < 2:
                    await asyncio.sleep(3)
                    continue
                return volumes
        else:
            break

        if not points:
            break

        for p in points:
            dep = p.get("subgraphDeployment")
            if dep and dep.get("id"):
                qc = int(float(p.get("query_count", "0")))
                volumes[dep["id"]] = volumes.get(dep["id"], 0) + qc

        last_id = points[-1]["id"]
        if len(points) < 1000:
            break

    return volumes


async def fetch_qos_volumes(client: httpx.AsyncClient, deployment_hashes: list[str]) -> dict[str, int]:
    """Fetch 30-day query volumes from the QoS subgraph, one day at a time."""
    if GATEWAY_API_KEY:
        qos_url = f"https://gateway.thegraph.com/api/{GATEWAY_API_KEY}/subgraphs/id/{QOS_SUBGRAPH_ID}"
    else:
        qos_url = f"https://gateway.thegraph.com/api/subgraphs/id/{QOS_SUBGRAPH_ID}"

    # Start from yesterday (today resets at midnight UTC)
    now = int(time.time())
    today_start = now - (now % 86400)

    volumes: dict[str, int] = {}
    days_fetched = 0

    for days_ago in range(1, 31):
        day_start = today_start - (days_ago * 86400)
        day_volumes = await _fetch_qos_day(client, qos_url, day_start)

        for ipfs, qc in day_volumes.items():
            volumes[ipfs] = volumes.get(ipfs, 0) + qc

        days_fetched += 1
        if days_ago % 10 == 0:
            print(f"  ... {days_ago} days fetched, {len(volumes)} deployments so far")

    print(f"  Fetched {days_fetched} days of QoS data, {len(volumes)} deployments with volume")
    return volumes


async def full_crawl(
    min_updated_at: int = 0,
    fetch_schemas_flag: bool = True,
    max_subgraphs: int | None = None,
) -> dict:
    """Full crawl pipeline."""
    start = time.time()

    async with httpx.AsyncClient(http2=True) as client:
        # Network stats
        print("\n=== Graph Network Stats ===")
        stats_data = await query_subgraph(client, NETWORK_STATS_QUERY)
        stats = stats_data["graphNetwork"]
        print(f"  Total subgraphs: {stats['subgraphCount']}")
        print(f"  Active subgraphs: {stats['activeSubgraphCount']}")

        # Crawl
        print("\n=== Crawling Subgraphs ===")
        raw_subgraphs = await crawl_all_subgraphs(client, min_updated_at)

        if max_subgraphs and len(raw_subgraphs) > max_subgraphs:
            # Sort by signal descending, take top N
            raw_subgraphs.sort(
                key=lambda s: int(s.get("currentSignalledTokens") or "0"),
                reverse=True,
            )
            raw_subgraphs = raw_subgraphs[:max_subgraphs]
            print(f"  Limited to top {max_subgraphs} by signal")

        # Deduplicate deployments
        seen_hashes = set()
        unique_hashes = []
        for sg in raw_subgraphs:
            dep = (sg.get("currentVersion") or {}).get("subgraphDeployment") or {}
            h = dep.get("ipfsHash")
            if h and h not in seen_hashes:
                seen_hashes.add(h)
                unique_hashes.append(h)
        print(f"  Unique deployments: {len(unique_hashes)} (from {len(raw_subgraphs)} subgraphs)")

        # Fetch schemas
        schemas = {}
        if fetch_schemas_flag:
            print("\n=== Fetching Schemas ===")
            schemas = await fetch_schemas(client, unique_hashes)
            print(f"  Total schemas: {len(schemas)}")

        # Fetch 30d query volumes from QoS subgraph
        print("\n=== Fetching Query Volumes (QoS) ===")
        query_volumes = await fetch_qos_volumes(client, unique_hashes)
        print(f"  Deployments with volume data: {len(query_volumes)}")
        if query_volumes:
            top = sorted(query_volumes.items(), key=lambda x: x[1], reverse=True)[:5]
            for h, v in top:
                print(f"    {h[:16]}... = {v:,.0f} queries/30d")

    # Flatten
    subgraphs = [flatten_subgraph(sg, schemas) for sg in raw_subgraphs]

    # Attach query volumes
    for sg in subgraphs:
        ipfs = sg.get("ipfs_hash")
        if ipfs and ipfs in query_volumes:
            sg["query_volume_30d"] = query_volumes[ipfs]

    elapsed = time.time() - start
    with_schema = sum(1 for s in subgraphs if s["schema"])
    with_desc = sum(1 for s in subgraphs if s["description"])
    with_cats = sum(1 for s in subgraphs if s["categories"])
    with_vol = sum(1 for s in subgraphs if s.get("query_volume_30d", 0) > 0)

    print(f"\n=== Crawl Complete ({elapsed:.1f}s) ===")
    print(f"  Subgraphs: {len(subgraphs)}")
    print(f"  With schemas: {with_schema}")
    print(f"  With descriptions: {with_desc}")
    print(f"  With categories: {with_cats}")
    print(f"  With 30d query volume: {with_vol}")

    return {
        "crawled_at": datetime.now(timezone.utc).isoformat(),
        "sync_timestamp": int(time.time()),
        "network_stats": stats,
        "subgraphs": subgraphs,
    }


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Crawl Graph Network subgraphs")
    parser.add_argument("--max", type=int, default=None, help="Max subgraphs to crawl (None = all)")
    parser.add_argument("--no-schemas", action="store_true", help="Skip schema fetching")
    parser.add_argument("--since", type=int, default=0, help="Only fetch subgraphs updated after this unix timestamp")
    parser.add_argument("--output", type=str, default=str(DATA_DIR / "crawl-raw.json"))
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = await full_crawl(
        min_updated_at=args.since,
        fetch_schemas_flag=not args.no_schemas,
        max_subgraphs=args.max,
    )

    # Write with schemas stripped for summary
    output = Path(args.output)
    output.write_text(json.dumps(data, indent=2, default=str))
    print(f"\nWritten to {output} ({output.stat().st_size / 1024 / 1024:.1f} MB)")

    # Write a lite version without schema text
    lite_path = output.with_name("crawl-summary.json")
    lite = {
        **data,
        "subgraphs": [
            {k: v for k, v in sg.items() if k != "schema"}
            | {"entity_count": len(__import__('re').findall(r'type \w+ @entity', sg["schema"] or ""))}
            for sg in data["subgraphs"]
        ],
    }
    lite_path.write_text(json.dumps(lite, indent=2, default=str))
    print(f"Written to {lite_path} ({lite_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    asyncio.run(main())
