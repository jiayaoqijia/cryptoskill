"""
Registry Builder

End-to-end pipeline:
1. Crawls the Graph Network subgraph
2. Classifies all subgraphs
3. Builds indices and summary stats
4. Outputs the agent-friendly JSON registry
5. Optionally writes to SQLite for fast lookups
"""

import asyncio
import json
import sqlite3
import time
from dataclasses import asdict
from pathlib import Path

from crawler import full_crawl
from classifier import classify_all, Classification

DATA_DIR = Path(__file__).parent / "data"
REGISTRY_FILE = DATA_DIR / "registry.json"
SYNC_STATE_FILE = DATA_DIR / "sync-state.json"
SQLITE_FILE = DATA_DIR / "registry.db"


def load_sync_state() -> dict:
    try:
        return json.loads(SYNC_STATE_FILE.read_text())
    except FileNotFoundError:
        return {"last_sync_timestamp": 0, "total_classified": 0}


def save_sync_state(state: dict):
    SYNC_STATE_FILE.write_text(json.dumps(state, indent=2))


def build_summary(classified: list[Classification]) -> dict:
    by_domain: dict[str, int] = {}
    by_network: dict[str, int] = {}
    by_protocol_type: dict[str, int] = {}
    families: dict[str, dict] = {}

    for sg in classified:
        by_domain[sg.domain] = by_domain.get(sg.domain, 0) + 1
        if sg.network:
            by_network[sg.network] = by_network.get(sg.network, 0) + 1
        by_protocol_type[sg.protocol_type] = by_protocol_type.get(sg.protocol_type, 0) + 1

        if sg.schema_family:
            fp = sg.schema_family["fingerprint"]
            if fp not in families:
                families[fp] = {
                    "fingerprint": fp,
                    "member_count": sg.schema_family["members"],
                    "representative_name": sg.display_name,
                    "domain": sg.domain,
                    "protocol_type": sg.protocol_type,
                }

    return {
        "total_subgraphs": len(classified),
        "by_domain": dict(sorted(by_domain.items(), key=lambda x: x[1], reverse=True)),
        "by_network": dict(sorted(by_network.items(), key=lambda x: x[1], reverse=True)),
        "by_protocol_type": dict(sorted(by_protocol_type.items(), key=lambda x: x[1], reverse=True)),
        "schema_family_count": len(families),
        "top_schema_families": sorted(families.values(), key=lambda x: x["member_count"], reverse=True)[:20],
    }


def build_indices(classified: list[Classification]) -> dict:
    by_domain: dict[str, list] = {}
    by_network: dict[str, list] = {}
    by_entity: dict[str, list] = {}

    for sg in classified:
        entry = {
            "id": sg.id,
            "name": sg.display_name,
            "network": sg.network,
            "protocol_type": sg.protocol_type,
            "reliability_score": sg.reliability_score,
            "ipfs_hash": sg.ipfs_hash,
        }

        by_domain.setdefault(sg.domain, []).append(entry)

        if sg.network:
            by_network.setdefault(sg.network, []).append({**entry, "domain": sg.domain})

        for ce in sg.canonical_entities:
            by_entity.setdefault(ce["canonical_type"], []).append({
                **entry,
                "entity_name": ce["name"],
                "domain": sg.domain,
            })

    # Sort all lists by reliability
    for lst in by_domain.values():
        lst.sort(key=lambda x: x["reliability_score"], reverse=True)
    for lst in by_network.values():
        lst.sort(key=lambda x: x["reliability_score"], reverse=True)
    for lst in by_entity.values():
        lst.sort(key=lambda x: x["reliability_score"], reverse=True)

    return {"by_domain": by_domain, "by_network": by_network, "by_entity": by_entity}


def write_sqlite(classified: list[Classification], db_path: Path = SQLITE_FILE):
    """Write registry to SQLite for fast agent lookups."""
    db_path.unlink(missing_ok=True)
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()

    c.execute("""
        CREATE TABLE subgraphs (
            id TEXT PRIMARY KEY,
            display_name TEXT,
            description TEXT,
            auto_description TEXT,
            website TEXT,
            code_repository TEXT,
            owner TEXT,
            ipfs_hash TEXT,
            network TEXT,
            powered_by_substreams BOOLEAN,
            domain TEXT,
            classification_confidence INTEGER,
            protocol_type TEXT,
            schema_fingerprint TEXT,
            entity_count INTEGER,
            reliability_score REAL,
            signalled_tokens TEXT,
            staked_tokens TEXT,
            query_fees TEXT,
            query_volume_30d INTEGER,
            created_at INTEGER,
            updated_at INTEGER,
            categories TEXT,
            canonical_entities TEXT,
            all_entities TEXT
        )
    """)

    c.execute("CREATE INDEX idx_domain ON subgraphs(domain)")
    c.execute("CREATE INDEX idx_network ON subgraphs(network)")
    c.execute("CREATE INDEX idx_protocol_type ON subgraphs(protocol_type)")
    c.execute("CREATE INDEX idx_reliability ON subgraphs(reliability_score DESC)")
    c.execute("CREATE INDEX idx_fingerprint ON subgraphs(schema_fingerprint)")

    for sg in classified:
        c.execute("""
            INSERT INTO subgraphs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            sg.id, sg.display_name, sg.description, sg.auto_description,
            sg.website, sg.code_repository, sg.owner, sg.ipfs_hash, sg.network,
            sg.powered_by_substreams, sg.domain, sg.classification_confidence,
            sg.protocol_type, sg.schema_fingerprint, sg.entity_count,
            sg.reliability_score, sg.signalled_tokens, sg.staked_tokens,
            sg.query_fees, sg.query_volume_30d, sg.created_at, sg.updated_at,
            json.dumps(sg.self_reported_categories),
            json.dumps([ce["canonical_type"] for ce in sg.canonical_entities]),
            json.dumps(sg.all_entities),
        ))

    conn.commit()
    conn.close()
    print(f"  SQLite written to {db_path} ({db_path.stat().st_size / 1024:.0f} KB)")


async def build_registry(
    max_subgraphs: int | None = None,
    incremental: bool = False,
    write_db: bool = True,
):
    print("╔══════════════════════════════════════════════╗")
    print("║   Subgraph Registry Builder (Python)        ║")
    print("╚══════════════════════════════════════════════╝\n")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    sync_state = load_sync_state()
    min_updated = sync_state["last_sync_timestamp"] if incremental else 0

    if incremental and min_updated > 0:
        from datetime import datetime, timezone
        print(f"Incremental: fetching updates since {datetime.fromtimestamp(min_updated, tz=timezone.utc).isoformat()}\n")

    # 1. Crawl
    raw_data = await full_crawl(
        min_updated_at=min_updated,
        fetch_schemas_flag=True,
        max_subgraphs=max_subgraphs,
    )

    # 2. Classify
    print("\n=== Classifying ===")
    t0 = time.time()
    # Build query volume map from crawler data
    query_volumes = {}
    for sg in raw_data["subgraphs"]:
        ipfs = sg.get("ipfs_hash")
        vol = sg.get("query_volume_30d", 0)
        if ipfs and vol > 0:
            query_volumes[ipfs] = query_volumes.get(ipfs, 0) + vol
    if query_volumes:
        print(f"  Query volumes available for {len(query_volumes)} deployments")

    classified = classify_all(raw_data["subgraphs"], query_volumes)
    print(f"  Classified {len(classified)} subgraphs in {time.time()-t0:.1f}s")

    # 2b. Deduplicate — keep highest-reliability entry per IPFS hash
    before_count = len(classified)
    seen_ipfs: dict[str, int] = {}
    deduped = []
    for sg in classified:
        ipfs = sg.ipfs_hash
        if not ipfs:
            deduped.append(sg)
            continue
        if ipfs in seen_ipfs:
            existing_idx = seen_ipfs[ipfs]
            if sg.reliability_score > deduped[existing_idx].reliability_score:
                deduped[existing_idx] = sg
        else:
            seen_ipfs[ipfs] = len(deduped)
            deduped.append(sg)
    classified = deduped
    removed = before_count - len(classified)
    if removed > 0:
        print(f"  Deduplicated: removed {removed} duplicate deployments ({before_count} → {len(classified)})")

    # 3. Build summary + indices
    print("\n=== Building Indices ===")
    summary = build_summary(classified)
    indices = build_indices(classified)

    print(f"  Domains: {', '.join(summary['by_domain'].keys())}")
    print(f"  Networks: {', '.join(list(summary['by_network'].keys())[:10])}")
    print(f"  Protocol types: {', '.join(summary['by_protocol_type'].keys())}")
    print(f"  Schema families: {summary['schema_family_count']}")
    print(f"  Entity types indexed: {', '.join(indices['by_entity'].keys())}")

    # 4. Assemble registry
    registry = {
        "version": "0.1.0",
        "generated_at": raw_data["crawled_at"],
        "sync_timestamp": raw_data["sync_timestamp"],
        "network_stats": raw_data["network_stats"],
        "summary": summary,
        "indices": indices,
        "subgraphs": [asdict(c) for c in classified],
    }

    # 5. Write outputs
    REGISTRY_FILE.write_text(json.dumps(registry, indent=2, default=str))
    size_mb = REGISTRY_FILE.stat().st_size / 1024 / 1024
    print(f"\n  Registry: {REGISTRY_FILE} ({size_mb:.1f} MB)")

    if write_db:
        write_sqlite(classified)

    # Update sync state
    save_sync_state({
        "last_sync_timestamp": raw_data["sync_timestamp"],
        "total_classified": len(classified),
        "last_run_at": raw_data["crawled_at"],
    })

    # Print report
    print("\n╔══════════════════════════════════════════════╗")
    print("║   Registry Summary                          ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  Total classified: {len(classified):<24}║")
    print("║                                             ║")
    print("║  By Domain:                                 ║")
    for domain, count in summary["by_domain"].items():
        print(f"║    {domain:<22} {count:>5}            ║")
    print("║                                             ║")
    print("║  Top Networks:                              ║")
    for net, count in list(summary["by_network"].items())[:8]:
        print(f"║    {net:<22} {count:>5}            ║")
    print("║                                             ║")
    print("║  Top Protocol Types:                        ║")
    for pt, count in list(summary["by_protocol_type"].items())[:8]:
        print(f"║    {pt:<22} {count:>5}            ║")
    print("╚══════════════════════════════════════════════╝")

    return registry


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=None, help="Max subgraphs")
    parser.add_argument("--incremental", action="store_true")
    parser.add_argument("--no-db", action="store_true", help="Skip SQLite output")
    args = parser.parse_args()

    asyncio.run(build_registry(
        max_subgraphs=args.max,
        incremental=args.incremental,
        write_db=not args.no_db,
    ))
