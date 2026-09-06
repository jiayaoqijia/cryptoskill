---
name: accessing-data
description: >
  How to read data from the Sui network. Use when choosing or implementing
  a data access strategy — queries for on-chain state, indexing pipelines,
  historical lookups, event subscriptions, cross-chain reads, or off-chain
  blob storage. Covers the two live Sui APIs (gRPC and GraphQL RPC),
  the Archival Store, the General-Purpose Indexer,
  the `sui-indexer-alt` custom indexing framework, and Walrus for off-chain
  blobs.
---

# Accessing Data on Sui

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

"How do I read data from Sui?" is the most frequently mis-answered question in agent-written Sui code. The defaults have changed. This skill fixes it.

**Key fact: JSON-RPC is deprecated.** Sui Foundation mainnet full nodes will disable JSON-RPC the week of July 27, 2026, with full code decommission by mid-October 2026. New code must use gRPC or GraphQL RPC. `SuiJsonRpcClient` still exists as a deprecated migration surface but should not be used for new projects.

The four canonical data surfaces are:

1. **gRPC** (generally available) — low-latency, real-time, code-gen-friendly. Served by full nodes. Supports streaming/subscriptions. The default for transaction submission, live reads, and ingestion pipelines.
2. **GraphQL RPC** (generally available) — flexible relational queries over the General-Purpose Indexer's Postgres + full node + Archival Store. Supports reads, transaction submission, and dry-run. Best for frontends, dashboards, wallets, and any client that benefits from composable queries.
3. **Archival Store** (generally available) — long-term historical storage of transactions, checkpoints, and object states beyond full-node pruning. GraphQL RPC can route supported historical lookups to the Archival Store transparently when the operator has configured archival backing. For gRPC, clients must query an Archival Service endpoint directly for historical data beyond full-node retention. Archival routing is operator-configured: if the operator hasn't set up archival backing, retention is limited to what the primary store holds.
4. **Custom indexer (`sui-indexer-alt`)** — build your own data pipeline keyed on exactly the on-chain data your app needs. Writes to any storage layer (Postgres by default, but any backend works). Ingests checkpoints from GCS (backfill) + full node gRPC (steady state).

Off-chain blob data (images, audio, models, large JSON) belongs on **Walrus**, not on-chain. Sui stores blob metadata; the blobs themselves sit on Walrus storage nodes.

All patterns in this skill are derived from:
- https://docs.sui.io/concepts/data-access/data-serving (overview & deprecation notice)
- https://docs.sui.io/concepts/data-access/graphql-rpc (GraphQL)
- https://docs.sui.io/concepts/data-access/archival-store (archival)
- https://docs.sui.io/guides/operator/indexer-stack-setup (general-purpose indexer)
- https://docs.wal.app (Walrus)

If unsure about an API, fetch from the relevant page before answering. Do not guess from Ethereum/Solana analogs — Sui's data surfaces are distinct.

---

## Reference files

### grpc — gRPC API
**Path:** `grpc.md`
**Load when:** writing backend services, indexers, exchanges, market makers, real-time clients, or any high-throughput read path. Also when subscribing to effects streams or doing dry runs / transaction simulation.
**Covers:** service surface (`ledger_service`, `transaction_execution_service`, `move_package_service`, `name_service`, `subscription_service`), endpoint URLs per network, the TypeScript (`SuiGrpcClient`) and Rust (`sui-rpc` crate) clients, streaming vs request-response, code-gen for arbitrary languages.

### graphql — GraphQL RPC
**Path:** `graphql.md`
**Load when:** the app needs flexible, composable queries — e.g., a frontend that joins object data with owner metadata and event history in a single request, transaction submission or dry-run via GraphQL, or historical queries with filters.
**Covers:** GraphQL endpoint URLs, relationship to the General-Purpose Indexer + Archival Store, `SuiGraphQLClient` usage, typical query shapes, pagination patterns, rate limits, transaction execution and simulation via GraphQL, execution-attached read-after-write consistency.

### indexers — Custom indexing (`sui-indexer-alt`)
**Path:** `indexers.md`
**Load when:** a user asks "how do I track X event across history?", "how do I build an explorer / leaderboard / analytics pipeline?", or when a GraphQL or gRPC query is too slow / not filterable the way they need.
**Covers:** the checkpoint-streaming pipeline model, backfill (GCS buckets like `gs://mysten-mainnet-checkpoints-use4`) vs steady-state (full node gRPC), writing a pipeline config (`events.toml`, `obj_versions.toml` patterns), concurrency tuning, and when to run the General-Purpose Indexer vs a custom one.

### archival — Archival Store
**Path:** `archival.md`
**Load when:** the data you need has been pruned from full nodes — old transactions, old object versions, old checkpoints. GraphQL RPC can route supported historical lookups to archival transparently when operator-configured; for gRPC, clients need a separate Archival Service endpoint.
**Covers:** what the Archival Store retains, why pruning exists, how GraphQL RPC routes to archival transparently (operator-configured) and how gRPC clients need a separate Archival Service endpoint, use cases (compliance, dispute resolution, long-range analytics).

### walrus — Off-chain blob storage
**Path:** `walrus.md`
**Load when:** the user wants to store a file (image, audio, model, document, large JSON, video) "on Sui" or is trying to put megabytes of data into a Move object. Route them to Walrus.
**Covers:** why you don't put blobs on-chain (250 KB per-object cap, storage-fund economics), the Walrus model (erasure-coded blobs stored off-chain with on-chain availability certificates), blob lifecycle, and the `@mysten/walrus` client extension.

### use-cases — Use case → method mapping
**Path:** `use-cases.md`
**Load when:** the user describes what they want to *do* and you need to pick the right surface. This is the first file to load for an unfamiliar data access request.
**Covers:** table of common use cases (balance lookup, owned-object list, event subscription, historical point-in-time read, analytics dashboard, cross-table joins, blob storage) mapped to the right API with rationale.

## Routing guide

| Task | Load |
|------|------|
| "How do I read X from Sui?" (first-pass question) | use-cases |
| Writing a backend/indexer read path | grpc + indexers |
| Writing a frontend data query | graphql (+ frontend-apps skill for hook patterns) |
| Building a custom analytics / explorer pipeline | indexers |
| Looking up data older than full-node retention | archival + graphql |
| Storing / retrieving a large file | walrus |
| Migrating from JSON-RPC | use-cases + grpc + graphql |
| Designing a new app from scratch | use-cases (then grpc or graphql based on client type) |
| Full code review of a data-heavy app | **all reference files** |

## Skill Content

### Key concepts

- **JSON-RPC is deprecated.** Sui Foundation mainnet full nodes will disable it the week of **July 27, 2026**; full code decommission by **mid-October 2026**. New code must use gRPC or GraphQL RPC. `SuiJsonRpcClient` still exists in the SDK as a deprecated migration stopgap.
- **gRPC is the performance default (GA).** Typed protobuf, streaming, low latency, polyglot client code gen (TS, Rust, Go, Python, etc.). Served directly by full nodes. Best for backends, indexers, and apps built in typed systems languages.
- **GraphQL RPC is the flexibility default (GA).** Reads from the General-Purpose Indexer's Postgres + full node + Archival Store. Also supports transaction submission and dry-run. One request can span multiple entity types. Best for frontends, tools, and apps built in dynamic languages.
- **Archival routing is operator-configured.** GraphQL RPC can route supported historical point lookups to the Archival Store transparently when the operator has configured archival backing. gRPC does not implicitly fall back to archival — gRPC clients must query an Archival Service endpoint directly for historical data beyond full-node retention. If archival is not configured, retention is limited to what the primary store holds.
- **Custom indexers exist because no hosted API fits every query shape.** If you need filtered sorts over millions of rows with app-specific indexes, run your own `sui-indexer-alt` pipeline. Custom indexers can write to any storage layer by implementing the framework's `Store` and `Connection` traits — Postgres is the default, not a requirement.
- **On-chain storage is not general-purpose blob storage.** Max Move object size is 250 KB. Storage is paid once (storage fund redistributes returns to validators). Big files go to Walrus.
- **The storage fund does not "hold your data."** It's an economic mechanism: a fraction of each write fee goes in; validators earn yield that pays for ongoing storage. It affects pricing, not where you store.

### Rules

1. **No JSON-RPC for new code.** JSON-RPC is deprecated; Sui Foundation mainnet full nodes will disable it the week of July 27, 2026. If a tutorial says `new SuiClient({ url: getFullnodeUrl(...) })`, replace with `new SuiGrpcClient({ network, baseUrl })`. If existing code uses `SuiJsonRpcClient`, migrate it to `SuiGrpcClient` or `SuiGraphQLClient`. Offer `SuiJsonRpcClient` only as a short-term migration stopgap — it still exists in the SDK but is deprecated.
2. **State GA status when recommending APIs.** gRPC, GraphQL RPC, and the Archival Store are all **generally available**. When recommending any of these — especially when answering archival or history questions — explicitly state they are generally available. Do not call them beta or experimental.
3. **Choose your initial API based on what you're building.** Front-ends, tools, and apps in dynamic languages → start with **GraphQL RPC** (superset of gRPC functionality, composable queries, transparent archival routing when operator-configured). Backends, indexers, and apps in typed systems languages → start with **gRPC** (performance, streaming, code-gen). Only switch if you hit a limitation. **Current temporary caveats** (will be resolved in the coming months): only gRPC supports subscriptions; only GraphQL supports filtered pagination over historical transactions and events.
4. **Archival routing differs by API.** GraphQL RPC routes supported historical point lookups to the Archival Store transparently when the operator has configured archival backing. gRPC does not implicitly fall back to archival — gRPC clients must query an Archival Service endpoint directly for historical data beyond full-node retention. If archival is not configured, retention is limited to what the primary store holds.
5. **Build a custom indexer only when hosted APIs don't fit.** Operating an indexer is ongoing work — Postgres, checkpoint ingestion, failure handling. Evaluate GraphQL RPC first.
6. **Put large files on Walrus.** Never advise embedding images/audio/video in Move objects or in transaction inputs. If the user is trying to, route them to the `walrus` reference file.
7. **Map use case → method correctly.** See `use-cases.md`:
   - Live balance / owned-object / coin list → **gRPC `client.core.*`**.
   - Flexible multi-entity query for a frontend → **GraphQL RPC**.
   - Historical transaction > N days old → **GraphQL RPC** (routes through archival transparently when operator-configured) or **gRPC via a separate Archival Service endpoint**.
   - Custom leaderboard / analytics across all events → **custom indexer**.
   - Transaction subscription / real-time effects feed → **gRPC streaming**.
   - Large files → **Walrus**.
8. **Read-after-write consistency varies by API.** For **GraphQL RPC**, queries nested under `executeTransaction` or `simulateTransaction` are evaluated in a special scope just after the executed/simulated transaction, without waiting for indexing. This provides consistent read-after-write for fields that don't require indexed history (e.g., effects, gas, object changes). Prefer selecting these fields in the same GraphQL request rather than making a separate indexed follow-up query. For **gRPC**, call `client.waitForTransaction({ digest })` before the follow-up read. In both cases, cross-node reads after a write are not guaranteed immediately visible.
9. **Cite docs when unsure.** All sources listed above.

### Common mistakes

- **Using `client.getObject` / `client.getOwnedObjects` / `client.getCoins`** — these are v1 method names from the deprecated JSON-RPC surface. v2 is `client.core.getObject` / `client.core.listOwnedObjects` / `client.core.listCoins` on any of the v2 clients.
- **Recommending "the Sui API" without specifying which.** "The Sui API" conflates different interfaces with different use cases. Always name gRPC or GraphQL.
- **Telling users to "use the indexer"** for a simple query that gRPC covers in one method. Only reach for a custom indexer when you've outgrown the hosted APIs.
- **Storing images or large JSON "on Sui."** Sui's 250 KB object size limit and pricing model make this wrong. Use Walrus.
- **Assuming gRPC and GraphQL return the same shape.** gRPC is protobuf; GraphQL is typed GraphQL. Response shapes differ; field names differ; pagination differs.
- **Polling for events.** Use gRPC streaming / subscriptions instead. Polling is high-cost and high-latency.
- **Reading from an RPC node and writing to a different one expecting read-after-write consistency.** Fullnodes are eventually consistent across the network. For GraphQL, prefer selecting fields in the same `executeTransaction` mutation (execution-attached scope gives consistent results without indexing). For gRPC, read from the same node you wrote to, or `waitForTransaction` before cross-node reads.
- **Conflating "storage fund" with "storage service."** The storage fund is a tokenomics mechanism. It is not an API you call.
- **Assuming gRPC transparently routes to archival.** Only GraphQL RPC transparently routes supported historical lookups to the Archival Store (when operator-configured). For gRPC, clients must query an Archival Service endpoint directly for historical data beyond full-node retention.
- **Assuming archival routing is automatic.** It's operator-configured. If the operator hasn't set up archival backing, retention is limited to what the primary store holds (e.g., the Postgres database's retention policy for GraphQL).
