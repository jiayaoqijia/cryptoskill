# Cardano Data Provider Comparison

Detailed comparison of 7 Cardano blockchain data providers for querying chain state, transaction history, and on-chain data.

## Provider Overview

### 1. Blockfrost

| Attribute | Detail |
|---|---|
| **Type** | Hosted |
| **Protocol** | REST API (HTTPS) |
| **Setup complexity** | Low (sign up, get API key) |
| **Cost** | Free tier: 50k req/day. Paid plans from $10/mo. Enterprise available. |
| **Strengths** | Comprehensive API, many SDKs, well-documented, reliable uptime, IPFS support |
| **Weaknesses** | Rate limits on free tier, latency vs local node, vendor dependency |
| **Best for** | Prototyping, frontend dApps, moderate-traffic backends, teams without infra capacity |

Key endpoints: addresses, transactions, blocks, epochs, assets, scripts, accounts, pools, governance.

SDKs: JavaScript/TypeScript, Python, Rust, Go, Java, Kotlin, Swift, Elixir, .NET.

### 2. Ogmios

| Attribute | Detail |
|---|---|
| **Type** | Self-hosted |
| **Protocol** | WebSocket (JSON-RPC) |
| **Setup complexity** | Medium (requires cardano-node) |
| **Cost** | Infrastructure only (node + Ogmios server) |
| **Strengths** | Low latency, real-time chain-tip data, tx submission + evaluation, protocol params |
| **Weaknesses** | No historical queries, no UTxO indexing by address, requires node |
| **Best for** | Tx submission backends, real-time state queries, paired with Kupo |

Provides: local chain sync, local tx submission, local tx evaluation (script budget), local state query (protocol params, epoch info, stake distribution).

Does NOT provide: address-based UTxO lookup, transaction history, asset metadata.

### 3. Kupo

| Attribute | Detail |
|---|---|
| **Type** | Self-hosted |
| **Protocol** | REST API (HTTP) |
| **Setup complexity** | Medium (requires cardano-node or Ogmios) |
| **Cost** | Infrastructure only |
| **Strengths** | Fast UTxO lookups, pattern-based indexing, lightweight, datum/script resolution |
| **Weaknesses** | Only indexes what matches configured patterns, no tx history, no protocol params |
| **Best for** | UTxO queries by address/asset/datum, smart contract state reads, paired with Ogmios |

Patterns: match by address, payment credential, policy ID, asset name, output reference.

Pruning: can run pruned (only unspent UTxOs) or full (with spent history).

### 4. Koios

| Attribute | Detail |
|---|---|
| **Type** | Hosted (community-run, decentralized) |
| **Protocol** | REST API (HTTPS, PostgREST) |
| **Setup complexity** | Low (no signup for basic, API token for higher limits) |
| **Cost** | Free tier generous. Premium tiers available. |
| **Strengths** | No signup needed, comprehensive endpoints, community-maintained, multiple backend instances |
| **Weaknesses** | Community-dependent uptime, occasional inconsistencies between instances |
| **Best for** | Open-source projects, quick queries, developers wanting no vendor lock-in |

Endpoints organized by: network, epoch, block, transactions, address, asset, pool, script, account, governance.

Supports bulk queries via POST with arrays of addresses/txs.

### 5. Cardano GraphQL

| Attribute | Detail |
|---|---|
| **Type** | Self-hosted |
| **Protocol** | GraphQL (over HTTP) |
| **Setup complexity** | High (DB-Sync + PostgreSQL + Hasura + GraphQL server) |
| **Cost** | Infrastructure only (significant: same as DB-Sync plus Hasura) |
| **Strengths** | Flexible queries, relationship traversal, request only needed fields, subscriptions |
| **Weaknesses** | Heavy infrastructure, complex setup, depends on DB-Sync sync state |
| **Best for** | Complex relational queries, custom dashboards, teams already running DB-Sync |

Schema covers: blocks, transactions, UTxOs, tokens, staking, delegations, pool metadata.

### 6. DB-Sync

| Attribute | Detail |
|---|---|
| **Type** | Self-hosted |
| **Protocol** | SQL (PostgreSQL) |
| **Setup complexity** | High (cardano-node + PostgreSQL + DB-Sync, initial sync days) |
| **Cost** | Infrastructure only. Requires 100GB+ disk, 16GB+ RAM recommended. |
| **Strengths** | Full chain data in SQL, maximum query flexibility, standard tooling (any SQL client) |
| **Weaknesses** | Resource-heavy, slow initial sync, schema updates on upgrades, operational burden |
| **Best for** | Analytics, reporting, historical research, data warehousing, complex aggregate queries |

Database schema: 50+ tables covering blocks, txs, UTxOs, scripts, datums, redeemers, multi-assets, staking, governance, pool metadata.

### 7. Oura

| Attribute | Detail |
|---|---|
| **Type** | Self-hosted |
| **Protocol** | Event pipeline (configurable sinks) |
| **Setup complexity** | Medium (requires cardano-node or relay) |
| **Cost** | Infrastructure only |
| **Strengths** | Real-time event streaming, flexible sinks (Kafka, Elastic, webhook, file), filters and mappers |
| **Weaknesses** | Not a query API (push, not pull), no historical backfill without replay, pipeline complexity |
| **Best for** | Real-time notifications, event-driven architectures, feeding external systems, monitoring |

Sinks: stdout, file, Kafka, Elasticsearch, webhook, AWS SQS/S3/Lambda, GCP PubSub, Redis, terminal.

Filters: by address, policy, asset, transaction metadata, block slot range.

## Decision Matrix

| Need | Blockfrost | Ogmios | Kupo | Koios | GraphQL | DB-Sync | Oura | Yaci Store |
|---|---|---|---|---|---|---|---|---|
| UTxO by address | Yes | No | Yes | Yes | Yes | Yes | No | Yes |
| Tx history | Yes | No | No | Yes | Yes | Yes | No | Yes |
| Protocol params | Yes | Yes | No | Yes | Yes | Yes | No | Yes |
| Tx submission | Yes | Yes | No | No | No | No | No | Yes |
| Tx evaluation | No | Yes | No | No | No | No | No | Yes† |
| Datum resolution | Yes | No | Yes | Yes | Yes | Yes | No | Yes |
| Asset metadata | Yes | No | No | Yes | Yes | Yes | No | Yes |
| Real-time events | No | Yes | No | No | Sub | No | Yes | In-proc |
| Historical analytics | Partial | No | No | Partial | Yes | Yes | No | Yes |
| SQL access | No | No | No | No | No | Yes | No | Yes |
| No infra needed | Yes | No | No | Yes | No | No | No | No |
| Free | Limited | Yes* | Yes* | Yes | Yes* | Yes* | Yes* | Yes* |

*Self-hosted: free software but requires infrastructure.
†Requires a configured evaluation backend — Ogmios, or a Scalus-backed local evaluator.

**Yaci Store** is a modular JVM indexer: enable only the stores you need (UTxO,
transaction, assets, governance, ...), each backed by your own Postgres — hence
direct SQL access. It exposes a **Blockfrost-compatible REST API** (`/blocks`,
`/epochs` including `latest/parameters`, `/txs`, `/tx/submit`, `/addresses`,
`/accounts`, `/assets`, `/scripts`, `/metadata`, `/utils/txs/evaluate`), so any
Blockfrost client — including cardano-client-lib's `BFBackendService` — points at
it unchanged.

Its "events" are **Spring application events consumed in-process**: you write
listeners and processors inside your own Spring Boot app to build custom indexers.
That is a different shape from Oura's streaming sinks (Kafka, webhooks, S3) — Yaci
Store is a library you embed, not a pipe you tap. Against Kupo it trades
pattern-matching simplicity for a full relational schema; against DB-Sync it trades
completeness for modularity and a much lighter footprint.

It is the indexer embedded in Yaci DevKit, so a project can develop locally and run
the same component in production. See
`${CLAUDE_SKILL_DIR}/../../docs/sources/yaci-store/` — `stores/`, `plugins/`,
`usage/as-library/`, `blockfrost/endpoints/`.

## Common Pairings

1. **Ogmios + Kupo**: Most popular self-hosted combo. Ogmios for tx submission, evaluation, and protocol params. Kupo for UTxO lookups and datum resolution.

2. **Blockfrost + Ogmios**: Blockfrost for reads, Ogmios for tx submission/evaluation (lower latency).

3. **DB-Sync + Oura**: DB-Sync for historical queries, Oura for real-time event processing.

4. **Koios + Blockfrost**: Koios as primary (free), Blockfrost as fallback (reliability).

## Choosing by Context

### Backend Service
- **Small/medium scale**: Blockfrost or Koios (no infra management)
- **High scale / low latency**: Ogmios + Kupo (self-hosted, co-located with node)
- **Full data access**: DB-Sync (if you need SQL analytics alongside)

### dApp Frontend
- **Fastest path**: Blockfrost SDK (well-documented, many language SDKs)
- **No-signup**: Koios (community endpoints, no API key needed)
- **Custom backend**: Ogmios + Kupo behind your own API layer

### Data Pipeline
- **Real-time streaming**: Oura to Kafka/Elasticsearch
- **Batch analytics**: DB-Sync with scheduled SQL queries
- **Hybrid**: Oura for live events, DB-Sync for historical backfill

### One-off Query
- **Quick check**: Koios (no signup, curl-friendly)
- **With a node running**: cardano-cli query
- **Programmatic**: Blockfrost free tier

## Querying through a TypeScript SDK

The 7 providers above are infrastructure. A TypeScript project usually reaches them through a client library rather than raw HTTP/WebSocket.

**Evolution SDK** wraps Blockfrost, Kupmios, Maestro, and Koios behind one interface — `Client.make(network).withBlockfrost(...)` (or `.withKupmios` / `.withMaestro` / `.withKoios`). The provider is a config choice; query code (`getUtxos`, `getUtxosWithUnit`, `getUtxoByUnit`, `getUtxosByOutRef`, `getDatum`, `getDelegation`, `getProtocolParameters`, `awaitTx`) is identical across all four. A **provider-only client** (no wallet) covers pure read/query and pre-signed submission.

The practical effect: the provider decision is reversible — start on hosted Blockfrost, move to self-hosted Kupmios later, with no change to query code. Docs: `docs/sources/evolution-sdk/providers/` and `querying/`.
