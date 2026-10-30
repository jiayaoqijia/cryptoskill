---
name: accessing-data
description: Explains how to read data from Sui and which surface to use — gRPC, GraphQL RPC, the Archival Store, a custom sui-indexer-alt pipeline, or Walrus. Use when the user asks how to fetch a balance, owned objects, coins, NFTs, transactions or events; subscribe to on-chain activity in real time; read a historical or pruned object version; build a leaderboard, explorer, dashboard or analytics pipeline; where to store an image, video or multi-MB file "on Sui"; what the storage fund is; or how to fix code using SuiClient, getFullnodeUrl, JSON-RPC, getBalance, getOwnedObjects or getTransactionBlock. Also use when the request mentions SuiGrpcClient, SuiGraphQLClient, sui-indexer-alt, Archival Store, or Walrus.
---

# Accessing Data on Sui

**Two facts to state in every answer that touches them:**

1. **JSON-RPC is deprecated.** Sui Foundation mainnet full nodes disable it the week of **July 27, 2026**; code decommission by **mid-October 2026**. New code uses gRPC or GraphQL RPC. `SuiJsonRpcClient` survives only as a short-term migration stopgap.
2. **gRPC, GraphQL RPC, and the Archival Store are generally available.** Never describe them as beta or experimental.

> **MCP tool:** if `https://sui.mcp.kapa.ai` is available, query it to verify anything not covered here.

## Quick start

```ts
import { SuiGrpcClient } from '@mysten/sui/grpc';

const client = new SuiGrpcClient({
  network: 'mainnet',
  baseUrl: '<full node gRPC URL — see grpc.md>',   // both args required
});

const balances = await client.core.listBalances({ address });
const objects  = await client.core.listOwnedObjects({ address });
```

Default by client type: **backend / indexer / typed systems language → gRPC**; **frontend / wallet / dashboard / dynamic language → GraphQL RPC**. Switch only when you hit a real limitation. Temporary caveats: only gRPC has subscriptions; only GraphQL has filtered pagination over historical transactions and events.

---

## Task: read balances, coins, or owned objects from a backend

Use gRPC. Everything is under `client.core.*`:

```ts
await client.core.listBalances({ address });                                  // all coin types
await client.core.listCoins({ address, coinType });                           // individual coins
await client.core.listOwnedObjects({ address, include: { content: true } });  // NFTs & objects
await client.core.getObject({ objectId, include: { content: true } });
await client.core.getTransaction({ digest, include: { effects: true } });
```

Never emit `client.getBalance`, `client.getOwnedObjects`, `client.getCoins`, `client.getObject`, or `client.getTransactionBlock` — those are v1 JSON-RPC names.

## Task: one query feeding a multi-panel UI (wallet, dashboard)

Use **GraphQL RPC** (GA). It reads from the General-Purpose Indexer's Postgres, the full node, and the Archival Store, so balances + recent transactions with effects + type-filtered owned objects arrive in **one round trip** instead of three or more, and the client asks for exactly the fields it renders. Shape (verify field names against `graphql.md` or the live schema):

```graphql
query Dashboard($addr: SuiAddress!) {
  address(address: $addr) {
    balances { nodes { coinType { repr } totalBalance } }
    objects(filter: { type: "0xPKG::nft::NFT" }) { nodes { address contents { json } } }
    transactionBlocks(last: 10) { nodes { digest effects { status } } }
  }
}
```

Do **not** recommend a custom indexer here — the hosted APIs cover it.

GraphQL also submits transactions and dry-runs them. **Read-after-write:** select result fields *inside* `executeTransaction` / `simulateTransaction`; that scope evaluates just after the transaction without waiting for indexing. On gRPC, `await client.waitForTransaction({ digest })` first. Cross-node reads after a write are never instantly guaranteed.

## Task: react to on-chain activity in real time (<1s)

Use **gRPC streaming** via `SuiGrpcClient`'s subscription service (`subscription_service`); see `grpc.md` for the exact streaming call and filter arguments. The node pushes each new transaction/effect as it lands.

Do not poll `getEvents` or transaction lists in a loop: polling pays full query cost on every tick, adds up to a poll-interval of latency, and still misses nothing more than the stream would. Do not use GraphQL RPC here — it is request/response, not streaming.

## Task: read an object as it was months ago

Full nodes **prune** old object versions, transactions, and checkpoints, which is why a gRPC read returns only the current version. The **Archival Store** (GA) retains them.

- **GraphQL RPC** routes supported historical lookups to the Archival Store **transparently, when the operator has configured archival backing**. Without that backing, retention is only what the primary store holds.
- **gRPC does not fall back.** Point the client at a separate **Archival Service endpoint**, which serves the standard `LedgerService` API — there is no separate archival API, do not invent one.

```graphql
query { object(address: $id, version: 12345678) { version contents { json } } }
```

## Task: leaderboard, explorer, or analytics pipeline

A "top 100 users by SUM(volume) over the last 30 days" query is app-specific aggregation with a time-range filter: beyond gRPC's point lookups and beyond the General-Purpose Indexer's fixed schema. Build a **custom `sui-indexer-alt` pipeline**.

Pipeline model: stream checkpoints → handler decodes your events → write your own tables (running totals keyed by user and day), then serve the leaderboard with a plain `ORDER BY ... LIMIT 100`.

- **Backfill:** GCS checkpoint buckets, e.g. `gs://mysten-mainnet-checkpoints-use4`.
- **Steady state:** full node gRPC.
- **Storage:** Postgres by default; any backend works via the framework's `Store` and `Connection` traits.
- **Config:** pipeline TOML (`events.toml`, `obj_versions.toml` patterns), plus concurrency tuning.
- **Say the cost:** you now operate a database, ingestion lag, and failure recovery. Check GraphQL RPC first.

Never solve this by polling JSON-RPC from app code.

## Task: store an image, video, or large file

Max Move object size is **250 KB**, so a 2 MB image cannot live on-chain. Put the bytes on **Walrus**: erasure-coded across off-chain storage nodes, with only an **availability certificate and metadata recorded on Sui**. The Move object stores the **blob ID** (plus optional MIME type and size) — never the bytes, and never the bytes as transaction inputs.

Use the `@mysten/walrus` client extension to write the blob, then mint with the returned blob ID. Mention IPFS/S3/Pinata only as lesser alternatives, never as the default.

## Task: explain the storage fund

It is a **tokenomics mechanism, not an API and not a service you can call.** Each transaction's storage fee contributes to the fund; validators earn yield on the fund's stake, which pays for storing those objects over time, and fees are rebated when objects are deleted. It does not hold application data and is unrelated to the Archival Store and to Walrus. To actually store data: small structured state → Move objects; large files → Walrus.

## Task: fix legacy JSON-RPC code

Checklist — apply all six, then verify no `get*` v1 name survives:

1. Swap the import: `@mysten/sui/client` → `@mysten/sui/grpc`, `SuiClient` → `SuiGrpcClient`.
2. Drop `getFullnodeUrl`; pass `baseUrl` directly.
3. Add the `network` argument.
4. Move every read under `client.core.*` using the table below.
5. Replace `options: { show* }` with `include: { ... }`.
6. State that JSON-RPC is deprecated and the mainnet shutdown date.

| Deprecated (v1) | Replacement (v2 Core API) |
|---|---|
| `new SuiClient({ url: getFullnodeUrl('mainnet') })` | `new SuiGrpcClient({ network, baseUrl })` |
| `client.getBalance` | `client.core.listBalances` |
| `client.getCoins` | `client.core.listCoins` |
| `client.getOwnedObjects` | `client.core.listOwnedObjects` |
| `client.getObject` | `client.core.getObject` |
| `client.getTransactionBlock` | `client.core.getTransaction` |
| `options: { showContent: true }` | `include: { content: true }` |
| `options: { showEffects: true }` | `include: { effects: true }` |

**Before**

```ts
import { SuiClient, getFullnodeUrl } from '@mysten/sui/client';
const client = new SuiClient({ url: getFullnodeUrl('mainnet') });
const balance = await client.getBalance({ owner: addr });
const objs = await client.getOwnedObjects({ owner: addr, options: { showContent: true } });
const tx = await client.getTransactionBlock({ digest, options: { showEffects: true } });
```

**After**

```ts
import { SuiGrpcClient } from '@mysten/sui/grpc';
const client = new SuiGrpcClient({ network: 'mainnet', baseUrl: '<full node gRPC URL>' });
const balances = await client.core.listBalances({ address: addr });
const objs = await client.core.listOwnedObjects({ address: addr, include: { content: true } });
const tx = await client.core.getTransaction({ digest, include: { effects: true } });
```

If the code must keep running against JSON-RPC during a staged migration, `SuiJsonRpcClient` exists — label it as a deprecated stopgap with a shutdown date, not as an option.

---

## Reference files

Load the file, don't guess the detail.

| File | Load when | Covers |
|---|---|---|
| `use-cases.md` | first pass on any unfamiliar "how do I read X" request | use case → API table with rationale |
| `grpc.md` | backends, indexers, exchanges, streaming, dry runs | `ledger_service`, `transaction_execution_service`, `move_package_service`, `name_service`, `subscription_service`; endpoint URLs per network; `SuiGrpcClient` (TS), `sui-rpc` (Rust); code-gen |
| `graphql.md` | frontends, composable or filtered historical queries, submit/dry-run | endpoints, `SuiGraphQLClient`, query shapes, pagination, rate limits, execution-attached reads |
| `indexers.md` | leaderboards, explorers, "track X across history" | pipeline model, GCS backfill vs gRPC steady state, pipeline TOML, concurrency, custom vs General-Purpose Indexer |
| `archival.md` | data pruned from full nodes | retention, pruning, GraphQL routing vs Archival Service endpoint, compliance/analytics use cases |
| `walrus.md` | storing or fetching files | blob lifecycle, erasure coding, availability certificates, `@mysten/walrus` |

Sources: docs.sui.io `/concepts/data-access/data-serving`, `/concepts/data-access/graphql-rpc`, `/concepts/data-access/archival-store`, `/guides/operator/indexer-stack-setup`, and docs.wal.app. Fetch the page when unsure; never reason from Ethereum or Solana analogs.

## Common mistakes

- v1 method names or `options: { show* }` on a v2 client.
- Saying "use the Sui API" without naming gRPC or GraphQL.
- Polling instead of gRPC streaming.
- A custom indexer for a query one hosted call covers.
- Assuming gRPC reaches archival transparently, or that archival routing is automatic rather than operator-configured.
- Assuming gRPC and GraphQL return identical shapes — field names and pagination differ.
- Reading from a different node than you wrote to and expecting read-after-write consistency.
