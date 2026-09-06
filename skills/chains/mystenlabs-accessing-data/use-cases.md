# Use Case → Method Mapping

First file to load when a user describes what they want to do. Pick the right data surface before writing code.

**All three primary Sui data APIs — gRPC, GraphQL RPC, and the Archival Store — are generally available.** Do not describe them as beta or experimental.

## Decision tree

1. Do you need to **store / retrieve a large file** (image, audio, video, document, arbitrary blob)? → **Walrus** (`walrus.md`). Stop.
2. Is this a **real-time / streaming subscription** (new transactions, new events, effects feed)? → **gRPC** (`grpc.md`).
3. Is this a **single entity read** (one object, one balance, one transaction, one coin list)? → **gRPC** (`grpc.md`). Use `client.core.*` from any SDK.
4. Does the query **join across entities** or filter historical data in a way a single gRPC method doesn't cover (e.g., "all NFTs owned by X minted after date Y with field Z > N")? → **GraphQL RPC** (`graphql.md`).
5. Is this **app-specific analytics** that neither gRPC nor GraphQL covers efficiently (leaderboards, custom aggregations, complex filters over millions of rows)? → **Custom indexer** (`indexers.md`).
6. Is the data **older than full-node retention** and you're hitting "not found"? → Use **GraphQL RPC**, which routes to the Archival Store transparently when the operator has configured archival backing. For **gRPC**, you need a separate Archival Service endpoint for historical data beyond full-node retention. See `archival.md`.
7. None of the above? Choose based on what you're building: **frontends, tools, dynamic languages → GraphQL RPC**; **backends, indexers, typed systems languages → gRPC**.

## Common use cases

| Use case | Primary surface | Rationale |
|---|---|---|
| Show a user's SUI balance | gRPC (`client.core.listBalances`) | Single-entity read; built-in indexing |
| Show a user's owned NFTs | gRPC (`client.core.listOwnedObjects({ owner, filter: { StructType } })`) | Paginated, type-indexed |
| Show details of a specific object | gRPC (`client.core.getObject`) | Point lookup |
| Show recent transactions by an address | gRPC (list transactions) OR GraphQL | gRPC for simple, GraphQL if joining with object changes |
| Wallet transaction history across time | GraphQL | Needs time-range filter + relational join to effects |
| NFT marketplace listings page | GraphQL | Filter + sort across types, pagination, join with prices |
| Leaderboard / custom analytics | Custom indexer | App-specific schema, custom indexes |
| Live feed of new mints of type T | gRPC streaming / subscription | Push, not pull |
| "When did this object last change?" | GraphQL OR custom indexer | Historical versioning is the indexer's job |
| Proof-of-ownership at a past epoch | GraphQL (routes to archival when operator-configured) | Pruned from live full node |
| Bridge / cross-chain state sync | gRPC streaming | Needs low-latency push |
| Storing a 10 MB image referenced by an NFT | Walrus (store) + Sui (reference) | 250 KB object cap |
| Storing application JSON state > 250 KB | Walrus | Object size cap |
| Storing small structured data (< few KB) in an object | Sui (on-chain) | Fine within object size |
| Sending a transaction and then reading the result | gRPC + `waitForTransaction` then read | Eventually-consistent indexer |
| Dashboard with 20 panels of varying data | GraphQL | One request > many round-trips |

## Anti-patterns

| Don't | Do |
|---|---|
| `client.getCoins(...)` (v1 method, removed) | `client.core.listCoins(...)` (v2 Core API) on `SuiGrpcClient` |
| Polling `getOwnedObjects` every second for changes | gRPC subscription / streaming |
| Building a custom indexer for a one-off query | Use GraphQL RPC first; indexer is ongoing ops |
| Storing file bytes in a Move object | Walrus; reference the blob ID on-chain |
| Hitting a different full node for the read than the write | Same node, or `waitForTransaction` first |
| Trusting an unofficial public gRPC endpoint for production | Run a full node or use a reputable RPC provider |
| Inferring block finality from the wallet's returned digest | `client.waitForTransaction({ digest })` |

## GraphQL vs gRPC — choosing by dimension

| Dimension | Prefer GraphQL RPC | Prefer gRPC API |
|---|---|---|
| Client type | Frontends, dashboards, developer tools, scripts, dynamic languages | Backends, indexers, exchanges, low-latency services, typed systems languages |
| Query patterns | Flexible, nested, filtered, or historical queries combining transactions, objects, events, balances in one request | Point lookups, transaction execution, simulation, workflows modeled around protobuf messages |
| Historical access | Can use configured Archival Service for supported historical point lookups; supports filtered pagination over historical txs and events | Does not implicitly fall back to archival; clients need a separate Archival Service endpoint for historical data beyond full-node retention |
| Streaming | No subscription support yet | gRPC subscriptions for live checkpoint/event streaming |
| Consistency | Execution-attached and simulation-attached queries provide read-after-write for fields that don't require indexed history | Use `waitForTransaction` or read from the same node you wrote to |

A good default: **GraphQL for frontends, tools, and flexible query workloads**; **gRPC for backend systems, indexers, streaming, and performance-sensitive typed clients**. You can use both in one application when different components have different requirements.

## "Which SDK" vs "which API"

They're independent axes:

- **API** = gRPC / GraphQL / custom indexer / Walrus.
- **SDK / language** = TypeScript, Rust, Python, etc.

Each official SDK exposes gRPC and GraphQL clients. Pick the API for your use case first, then pick the SDK for your language.

| API | TS | Rust |
|---|---|---|
| gRPC | `SuiGrpcClient` (`@mysten/sui/grpc`) | `sui-rpc` crate |
| GraphQL | `SuiGraphQLClient` (`@mysten/sui/graphql`) | `sui-graphql` crate |
| Custom indexer | `@mysten/sui/graphql` + your own storage | `sui-indexer-alt` + your own storage (Postgres default) |
| Walrus | `@mysten/walrus` extension | TBD / community |

For mappings across SDKs per operation, see the `sui-sdks` skill (`mapping.md`).

## Migrating from JSON-RPC

JSON-RPC is deprecated. Sui Foundation mainnet full nodes will disable it the week of July 27, 2026, with full code decommission by mid-October 2026. If you're staring at a codebase calling `client.getObject` / `getOwnedObjects` / `getCoins` / `getBalance` / etc.:

1. Replace the client: `SuiClient` → `SuiGrpcClient` (imports from `@mysten/sui/grpc` instead of `@mysten/sui/client`).
2. Rename methods: all data access moves under `client.core.*` and is renamed (see `sui-sdks` / `typescript.md` for the full table).
3. Replace `options: { show*: true }` with `include: { ... }`.
4. Replace result shape checks (`result.effects?.status?.status`) with `$kind` discriminant.

Full mapping lives in the `sui-sdks` skill's `typescript.md` file (v1 → v2 table). For a method-by-method migration cookbook, see https://docs.sui.io/develop/accessing-data/grpc/grpc-migration-cookbook.
