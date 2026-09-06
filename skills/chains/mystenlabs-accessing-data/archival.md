# Archival Store

Source: https://docs.sui.io/concepts/data-access/archival-store

Generally available. The Archival Store provides long-term historical access to data pruned from full nodes.

## What it is

From the docs:
> The Archival Store provides "long-term storage and access to historical network data that might no longer be available on full nodes because of pruning."
> Full nodes "enforce limited retention for scalability and performance," which is why this archival infrastructure exists — to preserve data after nodes discard it.

It retains:
- Old transactions.
- Old checkpoints.
- Old object versions (point-in-time state).

## Why pruning exists

Full nodes serve real-time queries. Retaining the entire history on every node would balloon storage and degrade query performance. Pruning lets full nodes stay fast by offloading older data to the archival backbone.

## Access model

How the Archival Store is accessed depends on the API:

**GraphQL RPC** routes supported historical point lookups (transactions, objects, checkpoints) to archival transparently when the operator has configured archival backing. For most apps using a properly configured GraphQL stack, the Archival Store is invisible — you query the same GraphQL endpoint you always use, and the service fetches from archival as needed. Note: this routing is operator-configured — if the GraphQL operator has not set up archival backing, retention is limited to the Postgres database's retention policy.

**gRPC** does **not** implicitly fall back to the Archival Store. Full-node gRPC serves only data within its retention window. For historical data beyond full-node retention, gRPC clients must query an Archival Service endpoint directly. The Archival Service endpoint exposes the same standard `LedgerService` gRPC API as full nodes — clients use the same request types and methods, just pointed at a different URL.

## When it matters

- **Compliance / audit** — proving on-chain activity from months or years ago.
- **Dispute resolution** — "what did this object look like at checkpoint X?".
- **Long-range analytics** — backfilling a custom indexer from deep history.
- **Historical explorers** — letting users browse old transactions beyond the live full node retention.

## Example: historical object version

GraphQL RPC is the easiest way to request a specific past version:

```graphql
query { object(address: "0x...", version: 42) { ... } }
```

If version 42 has been pruned from the full node, GraphQL RPC pulls it from the archival backbone. No client-side logic needed.

## For custom indexer backfills

When seeding a custom `sui-indexer-alt` pipeline from history, point the backfill source at the checkpoint GCS bucket (e.g., `gs://mysten-mainnet-checkpoints-use4`) rather than the archival service — the buckets are the canonical historical source for checkpoint ingestion. The Archival Store is the **query-side** counterpart to this; the backfill side of a custom indexer reads checkpoints directly.

## Common mistakes

- **Assuming full nodes have the whole history.** They don't. Past the pruning horizon, you see "not found" unless archival is available. GraphQL routes to archival transparently (when operator-configured). For gRPC, you must query an Archival Service endpoint directly.
- **Assuming gRPC transparently routes to archival.** It does not. Full-node gRPC only serves data within its retention window. For historical gRPC reads, clients need a separate Archival Service endpoint.
- **Confusing "Archival Store" with "checkpoint store."** Checkpoint store (GCS buckets) is the canonical checkpoint archive for backfill ingestion. Archival Store is the query-side service that serves pruned reads. Related but distinct.
