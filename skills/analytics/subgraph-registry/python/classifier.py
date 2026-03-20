"""
Subgraph Classifier

Rule-based classification engine that analyzes subgraph schemas and metadata
to assign domain, protocol type, canonical entities, schema fingerprints,
and composite reliability scores.

Designed to classify 15K+ subgraphs efficiently using polars DataFrames.
"""

import hashlib
import math
import re
from dataclasses import dataclass, field

# ── Domain Keywords ──────────────────────────────────────────

DOMAIN_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "defi": {
        "schema": [
            "swap", "pool", "liquidity", "vault", "borrow", "lend", "stake",
            "deposit", "withdraw", "collateral", "debt", "interest", "yield",
            "farm", "reward", "fee", "amm", "pair", "reserve", "flash",
            "leverage", "margin", "perpetual", "option", "strike", "premium",
            "bridge", "wrap", "mint", "burn", "token", "erc20",
        ],
        "name": [
            "swap", "dex", "exchange", "lend", "borrow", "vault", "yield",
            "farm", "stake", "bridge", "amm", "pool", "finance", "fi",
            "perp", "option", "derivative",
        ],
    },
    "nfts": {
        "schema": [
            "nft", "erc721", "erc1155", "tokenuri", "collection", "metadata",
            "royalt", "auction", "bid", "listing", "offer", "marketplace",
        ],
        "name": [
            "nft", "collectible", "art", "punk", "ape", "bayc", "opensea",
            "blur", "marketplace", "gallery", "auction",
        ],
    },
    "dao": {
        "schema": [
            "proposal", "vote", "governor", "timelock", "quorum", "delegate",
            "ballot", "execution", "treasury", "multisig",
        ],
        "name": [
            "dao", "govern", "vote", "snapshot", "compound-gov", "nouns",
            "treasury",
        ],
    },
    "gaming": {
        "schema": [
            "player", "game", "character", "item", "quest", "battle",
            "score", "level", "achievement", "inventory", "world",
        ],
        "name": [
            "game", "play", "metaverse", "world", "quest", "battle", "loot",
        ],
    },
    "identity": {
        "schema": [
            "domain", "resolver", "registration", "name", "record", "reverse",
            "registrar", "label", "subdomain",
        ],
        "name": [
            "ens", "name", "identity", "did", "lens", "space-id",
            "unstoppable",
        ],
    },
    "infrastructure": {
        "schema": [
            "indexer", "delegator", "curator", "epoch", "allocation",
            "subgraph", "network", "operator", "oracle", "keeper",
            "registry", "proxy",
        ],
        "name": [
            "graph", "network", "chainlink", "oracle", "keeper", "infra",
            "registry", "proxy",
        ],
    },
    "social": {
        "schema": [
            "profile", "post", "comment", "follow", "publication", "mirror",
            "collect", "reaction", "feed",
        ],
        "name": [
            "lens", "social", "farcaster", "mirror", "forum", "community",
        ],
    },
    "analytics": {
        "schema": [
            "daydata", "hourdata", "snapshot", "metric", "stat", "aggregate",
            "historical",
        ],
        "name": ["analytics", "stats", "metrics", "dashboard", "data"],
    },
}

# ── Protocol Type Rules ──────────────────────────────────────

PROTOCOL_TYPE_RULES = [
    {
        "type": "dex",
        "schema": ["swap", "pair", "pool", "amm", "route", "liquidity"],
        "name": [
            "swap", "dex", "exchange", "amm", "uniswap", "sushi", "curve",
            "balancer", "pancake", "trader-joe", "camelot", "velodrome",
            "aerodrome",
        ],
        "min": 2,
    },
    {
        "type": "lending",
        "schema": ["borrow", "lend", "collateral", "liquidat", "repay", "debt", "interest", "reserve"],
        "name": ["aave", "compound", "lend", "borrow", "maker", "morpho", "spark", "silo"],
        "min": 2,
    },
    {
        "type": "bridge",
        "schema": ["bridge", "relay", "message", "cross-chain", "destination", "source"],
        "name": ["bridge", "hop", "stargate", "across", "wormhole", "layerzero", "synapse"],
        "min": 1,
    },
    {
        "type": "staking",
        "schema": ["stake", "unstake", "validator", "delegation", "slash", "epoch", "withdrawal", "indexer", "delegator", "curator"],
        "name": ["staking", "stake", "lido", "rocket", "eigenlayer", "restake", "graph network"],
        "min": 2,
    },
    {
        "type": "options",
        "schema": ["option", "strike", "premium", "expir", "exercise", "call", "put"],
        "name": ["option", "premia", "dopex", "lyra", "hegic", "opyn"],
        "min": 2,
    },
    {
        "type": "perpetuals",
        "schema": ["perpetual", "perp", "position", "margin", "leverage", "funding", "liquidat"],
        "name": ["perp", "gmx", "gains", "kwenta", "dydx", "perpetual"],
        "min": 2,
    },
    {
        "type": "nft-marketplace",
        "schema": ["listing", "bid", "auction", "offer", "collection", "sale", "royalt"],
        "name": ["opensea", "blur", "rarible", "foundation", "superrare", "marketplace"],
        "min": 2,
    },
    {
        "type": "yield-aggregator",
        "schema": ["vault", "strategy", "harvest", "yield", "apy", "compound"],
        "name": ["yearn", "beefy", "harvest", "yield", "vault", "convex"],
        "min": 2,
    },
    {
        "type": "governance",
        "schema": ["proposal", "vote", "governor", "delegate", "quorum"],
        "name": ["gov", "dao", "vote", "snapshot", "tally"],
        "min": 2,
    },
    {
        "type": "name-service",
        "schema": ["domain", "resolver", "registrar", "registration", "label"],
        "name": ["ens", "name", "domain", "space-id", "unstoppable"],
        "min": 2,
    },
]

# ── Canonical Entity Vocabulary ──────────────────────────────

CANONICAL_ENTITIES = {
    "liquidity_pool": ["pool", "pair", "market", "ammpool", "liquiditypool"],
    "trade": ["swap", "trade", "exchange", "fill", "order"],
    "token": ["token", "asset", "erc20", "currency", "coin"],
    "position": ["position", "stake", "deposit", "userposition", "liquidityprovider"],
    "vault": ["vault", "strategy", "farm"],
    "loan": ["borrow", "loan", "debt", "borrowposition"],
    "collateral": ["collateral", "reserve", "supply"],
    "liquidation": ["liquidation", "liquidationevent", "liquidationcall"],
    "nft_collection": ["collection", "nftcollection", "contract"],
    "nft_item": ["nftitem", "nfttoken", "erc721token", "erc1155token"],
    "nft_sale": ["nftsale", "sale", "listing", "auction", "offer"],
    "proposal": ["proposal", "governanceproposal"],
    "delegate": ["delegate", "delegator", "voter"],
    "domain_name": ["domain", "name", "registration", "resolver"],
    "daily_snapshot": ["daydata", "dailysnapshot", "day"],
    "hourly_snapshot": ["hourdata", "hourlysnapshot", "hour"],
    "transaction": ["transaction", "tx", "event"],
    "account": ["account", "user", "wallet", "owner"],
}


# ── Schema Parsing ───────────────────────────────────────────

ENTITY_RE = re.compile(r"type\s+(\w+)\s+@entity[^{]*\{([^}]*)\}", re.DOTALL)
FIELD_RE = re.compile(r"(\w+)\s*:")


@dataclass
class SchemaEntity:
    name: str
    fields: list[str]
    field_count: int


def parse_schema(schema_text: str | None) -> list[SchemaEntity]:
    if not schema_text:
        return []
    entities = []
    for m in ENTITY_RE.finditer(schema_text):
        name = m.group(1)
        body = m.group(2)
        fields = FIELD_RE.findall(body)
        entities.append(SchemaEntity(name=name, fields=fields, field_count=len(fields)))
    return entities


def schema_fingerprint(entities: list[SchemaEntity]) -> str | None:
    if not entities:
        return None
    sig = "|".join(
        sorted(f"{e.name.lower()}:{e.field_count}" for e in entities)
    )
    return hashlib.md5(sig.encode()).hexdigest()[:12]


# ── Classification ───────────────────────────────────────────

@dataclass
class Classification:
    id: str
    display_name: str | None
    description: str | None
    website: str | None
    code_repository: str | None
    owner: str | None

    # Deployment
    ipfs_hash: str | None
    network: str | None
    powered_by_substreams: bool

    # Classification
    domain: str
    classification_confidence: int
    domain_scores: dict[str, int]
    protocol_type: str
    self_reported_categories: list[str]

    # Schema
    schema_fingerprint: str | None
    entity_count: int
    canonical_entities: list[dict]
    all_entities: list[dict]

    # Signal
    reliability_score: float
    signalled_tokens: str
    staked_tokens: str
    query_fees: str
    query_volume_30d: int

    # Time
    created_at: int
    updated_at: int

    # Auto-generated description
    auto_description: str = ""

    # Family (set after grouping)
    schema_family: dict | None = None


def _score_domain(sg: dict, entities: list[SchemaEntity]) -> tuple[str, int, dict]:
    scores: dict[str, int] = {}
    name_lower = (sg.get("display_name") or "").lower()
    desc_lower = (sg.get("description") or "").lower()
    entity_names = [e.name.lower() for e in entities]
    all_fields = [f.lower() for e in entities for f in e.fields]
    schema_text = " ".join(entity_names + all_fields)

    # Self-reported categories boost
    for cat in sg.get("categories") or []:
        cl = cat.lower()
        if "defi" in cl:
            scores["defi"] = scores.get("defi", 0) + 5
        if "nft" in cl:
            scores["nfts"] = scores.get("nfts", 0) + 5
        if "dao" in cl or "governance" in cl:
            scores["dao"] = scores.get("dao", 0) + 5
        if "gaming" in cl:
            scores["gaming"] = scores.get("gaming", 0) + 5
        if "social" in cl:
            scores["social"] = scores.get("social", 0) + 5
        if "infrastructure" in cl:
            scores["infrastructure"] = scores.get("infrastructure", 0) + 5
        if "marketplace" in cl:
            scores["nfts"] = scores.get("nfts", 0) + 3

    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        for kw in keywords["schema"]:
            if kw in schema_text:
                score += 2
        for kw in keywords["name"]:
            if kw in name_lower:
                score += 3
            if kw in desc_lower:
                score += 1
        if score > 0:
            scores[domain] = scores.get(domain, 0) + score

    sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    top = next(iter(sorted_scores), "unknown")
    conf = sorted_scores.get(top, 0)
    return top, conf, sorted_scores


def _score_protocol_type(sg: dict, entities: list[SchemaEntity]) -> str:
    name_lower = (sg.get("display_name") or "").lower()
    desc_lower = (sg.get("description") or "").lower()
    entity_names = [e.name.lower() for e in entities]
    all_fields = [f.lower() for e in entities for f in e.fields]
    schema_text = " ".join(entity_names + all_fields)

    best_type = "general"
    best_score = 0

    for rule in PROTOCOL_TYPE_RULES:
        score = 0
        for ind in rule["schema"]:
            if ind in schema_text:
                score += 1
        for ind in rule["name"]:
            if ind in name_lower or ind in desc_lower:
                score += 2
        if score >= rule["min"] and score > best_score:
            best_type = rule["type"]
            best_score = score

    return best_type


def _map_canonical(entities: list[SchemaEntity]) -> list[dict]:
    mapped = []
    for entity in entities:
        nl = entity.name.lower()
        best_match = None
        best_score = 0
        for canonical, aliases in CANONICAL_ENTITIES.items():
            for alias in aliases:
                if nl == alias:
                    score = 3
                elif alias in nl or nl in alias:
                    score = 1
                else:
                    continue
                if score > best_score:
                    best_match = canonical
                    best_score = score
        if best_match:
            mapped.append({
                "name": entity.name,
                "canonical_type": best_match,
                "field_count": entity.field_count,
                "key_fields": entity.fields[:10],
            })
    return mapped


def _wei_to_float(wei_str: str) -> float:
    try:
        return int(wei_str) / 1e18
    except (ValueError, TypeError):
        return 0.0


def _reliability_score(sg: dict, query_volume: int = 0) -> float:
    # Curation signal: log10(GRT) / 5 — 100K GRT = 1.0
    signal = math.log10(_wei_to_float(sg.get("signalled_tokens", "0")) + 1) / 5
    # Indexer stake: log10(GRT) / 7 — 10M GRT = 1.0
    stake = math.log10(_wei_to_float(sg.get("staked_tokens", "0")) + 1) / 7
    # Query fees: log10(GRT) / 5 — 100K GRT fees = 1.0
    fees = math.log10(_wei_to_float(sg.get("query_fees", "0")) + 1) / 5
    # 30d query volume from QoS: log10(queries) / 8 — 100M queries = 1.0
    qv = math.log10(query_volume + 1) / 8 if query_volume > 0 else 0.0

    signal = min(1.0, signal)
    stake = min(1.0, stake)
    fees = min(1.0, fees)
    qv = min(1.0, qv)

    penalty = 0.5 if sg.get("denied_at", 0) > 0 else 0.0

    # Weighted: fees 30%, volume 30% (both prove real usage), signal 20%, stake 20%
    raw = (signal * 0.20 + stake * 0.20 + fees * 0.30 + qv * 0.30) - penalty
    return round(max(0.0, min(1.0, raw)), 4)


# ── Auto-Description Generator ──────────────────────────────

NETWORK_NAMES = {
    "mainnet": "Ethereum",
    "arbitrum-one": "Arbitrum",
    "base": "Base",
    "matic": "Polygon",
    "bsc": "BNB Chain",
    "optimism": "Optimism",
    "avalanche": "Avalanche",
    "gnosis": "Gnosis",
    "fantom": "Fantom",
    "celo": "Celo",
    "linea": "Linea",
    "scroll": "Scroll",
    "zksync-era": "zkSync Era",
    "moonbeam": "Moonbeam",
    "blast-mainnet": "Blast",
    "polygon-zkevm": "Polygon zkEVM",
    "sonic": "Sonic",
    "near-mainnet": "NEAR",
    "mode-mainnet": "Mode",
    "sei-mainnet": "Sei",
}

PROTOCOL_TYPE_LABELS = {
    "dex": "decentralized exchange (DEX)",
    "lending": "lending/borrowing protocol",
    "bridge": "cross-chain bridge",
    "staking": "staking protocol",
    "options": "options protocol",
    "perpetuals": "perpetuals/derivatives protocol",
    "nft-marketplace": "NFT marketplace",
    "yield-aggregator": "yield aggregator",
    "governance": "governance protocol",
    "name-service": "name service",
    "general": None,
}

ENTITY_DESCRIPTIONS = {
    "liquidity_pool": "liquidity pools",
    "trade": "trades/swaps",
    "token": "tokens",
    "position": "user positions",
    "vault": "vaults/strategies",
    "loan": "loans/borrows",
    "collateral": "collateral/reserves",
    "liquidation": "liquidations",
    "nft_collection": "NFT collections",
    "nft_item": "NFT items",
    "nft_sale": "NFT sales/listings",
    "proposal": "governance proposals",
    "delegate": "delegates/voters",
    "domain_name": "domain name registrations",
    "daily_snapshot": "daily snapshots",
    "hourly_snapshot": "hourly snapshots",
    "transaction": "transactions",
    "account": "accounts/users",
}


# Canonical types that conflict with certain protocol types — use raw entity names instead
_CONFLICTING_CANONICAL = {
    "staking": {"nft_sale", "nft_item", "nft_collection"},
    "lending": {"nft_sale", "nft_item", "nft_collection"},
    "bridge": {"nft_sale", "nft_item", "nft_collection"},
    "governance": {"nft_sale", "nft_item", "nft_collection"},
}


def _generate_description(
    display_name: str | None,
    network: str | None,
    domain: str,
    protocol_type: str,
    canonical_entities: list[dict],
    all_entities: list[dict],
    entity_count: int,
) -> str:
    """Generate a description from classification data."""
    name = display_name or "Unknown"
    chain = NETWORK_NAMES.get(network, network.title() if network else "an unknown chain")
    ptype_label = PROTOCOL_TYPE_LABELS.get(protocol_type)

    # Get canonical types that conflict with this protocol type
    conflicts = _CONFLICTING_CANONICAL.get(protocol_type, set())

    # Build entity summary (deduplicated canonical types)
    # When canonical type conflicts with protocol_type, use the raw entity name instead
    seen = set()
    entity_types = []
    for ce in canonical_entities:
        ct = ce.get("canonical_type") if isinstance(ce, dict) else ce
        ename = ce.get("name", "") if isinstance(ce, dict) else ""
        if ct and ct in conflicts:
            # Use raw entity name instead of misleading canonical label
            if ename and ename not in seen:
                seen.add(ename)
                entity_types.append(ename)
        elif ct and ct not in seen:
            seen.add(ct)
            label = ENTITY_DESCRIPTIONS.get(ct, ct.replace("_", " "))
            entity_types.append(label)

    # Core entities (skip snapshots and generic ones for the summary)
    core_entities = [e for e in entity_types if e not in (
        "daily snapshots", "hourly snapshots", "transactions", "accounts/users"
    )]
    has_snapshots = any(e in entity_types for e in ("daily snapshots", "hourly snapshots"))

    # Build the description
    parts = []

    # Opening line
    if ptype_label:
        parts.append(f"Indexes {name} {ptype_label} on {chain}.")
    else:
        domain_label = domain.upper() if domain in ("dao", "nfts") else domain.title()
        parts.append(f"Indexes {name} ({domain_label}) on {chain}.")

    # What it tracks
    if core_entities:
        if len(core_entities) <= 4:
            parts.append(f"Tracks {', '.join(core_entities)}.")
        else:
            parts.append(f"Tracks {', '.join(core_entities[:4])}, and {len(core_entities) - 4} more entity types.")

    # Snapshots
    if has_snapshots:
        snapshot_types = []
        if "hourly snapshots" in entity_types:
            snapshot_types.append("hourly")
        if "daily snapshots" in entity_types:
            snapshot_types.append("daily")
        parts.append(f"Includes {' and '.join(snapshot_types)} time-series data.")

    # List notable unclassified entities
    unclassified = [e["name"] for e in all_entities if e.get("type") is None and not e["name"].startswith("_")]

    # When few canonical matches but many unclassified entities, show key schema entities
    if len(core_entities) <= 1 and unclassified:
        notable = unclassified[:6]
        parts.append(f"Key entities: {', '.join(notable)}.")
    elif entity_count > 15 and unclassified:
        if len(unclassified) <= 6:
            parts.append(f"Also includes: {', '.join(unclassified)}.")
        elif entity_count > 25:
            parts.append(f"Rich schema with {entity_count} entity types.")

    return " ".join(parts)


def classify_one(sg: dict, query_volume: int = 0) -> Classification:
    entities = parse_schema(sg.get("schema"))
    domain, confidence, domain_scores = _score_domain(sg, entities)
    protocol_type = _score_protocol_type(sg, entities)
    canonical = _map_canonical(entities)
    fp = schema_fingerprint(entities)
    reliability = _reliability_score(sg, query_volume)

    all_ents = [
        {"name": e.name, "type": next((c["canonical_type"] for c in canonical if c["name"] == e.name), None), "fields": e.field_count}
        for e in entities
    ]

    auto_desc = _generate_description(
        display_name=sg.get("display_name"),
        network=sg.get("network"),
        domain=domain,
        protocol_type=protocol_type,
        canonical_entities=canonical,
        all_entities=all_ents,
        entity_count=len(entities),
    )

    return Classification(
        id=sg["id"],
        display_name=sg.get("display_name"),
        description=sg.get("description"),
        website=sg.get("website"),
        code_repository=sg.get("code_repository"),
        owner=sg.get("owner_name") or sg.get("owner_id"),
        ipfs_hash=sg.get("ipfs_hash"),
        network=sg.get("network"),
        powered_by_substreams=sg.get("powered_by_substreams", False),
        domain=domain,
        classification_confidence=confidence,
        domain_scores=domain_scores,
        protocol_type=protocol_type,
        self_reported_categories=sg.get("categories") or [],
        schema_fingerprint=fp,
        entity_count=len(entities),
        canonical_entities=canonical,
        all_entities=all_ents,
        auto_description=auto_desc,
        reliability_score=reliability,
        signalled_tokens=sg.get("signalled_tokens", "0"),
        staked_tokens=sg.get("staked_tokens", "0"),
        query_fees=sg.get("query_fees", "0"),
        query_volume_30d=query_volume,
        created_at=sg.get("created_at", 0),
        updated_at=sg.get("updated_at", 0),
    )


def classify_all(
    subgraphs: list[dict],
    query_volumes: dict[str, int] | None = None,
) -> list[Classification]:
    """Classify all subgraphs and detect schema families."""
    query_volumes = query_volumes or {}

    classified = []
    for sg in subgraphs:
        ipfs = sg.get("ipfs_hash")
        qv = query_volumes.get(ipfs, 0) if ipfs else 0
        classified.append(classify_one(sg, qv))

    # Group by fingerprint → schema families
    families: dict[str, list[str]] = {}
    for c in classified:
        if c.schema_fingerprint:
            families.setdefault(c.schema_fingerprint, []).append(c.id)

    for c in classified:
        fp = c.schema_fingerprint
        if fp and len(families.get(fp, [])) > 1:
            members = families[fp]
            c.schema_family = {
                "fingerprint": fp,
                "members": len(members),
                "siblings": [m for m in members if m != c.id],
            }

    return classified
