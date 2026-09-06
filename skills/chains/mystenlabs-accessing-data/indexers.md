# Custom Indexers — `sui-indexer-alt`

Source: https://docs.sui.io/guides/operator/indexer-stack-setup

When to build one: the hosted gRPC and GraphQL APIs can't efficiently answer your query shape. Symptoms:
- You need custom aggregations / leaderboards / analytics not supported by GraphQL.
- Filter combinations cause full table scans on the General-Purpose Indexer.
- You need to store app-computed derived state alongside on-chain state.
- You need to retain data beyond the public services' retention policy.

If you can answer your query with `client.core.*` or a GraphQL query, **don't** build an indexer. Operating one is ongoing work: storage infrastructure, checkpoint ingestion, failure handling, backfills, migrations.

## Architecture

From the docs:
> The indexer "consists of multiple pipelines that each read, transform, and write checkpoint data."

Custom indexers can write to **any storage layer** — Postgres is the default and most common choice, but you can target any backend (other databases, message queues, data lakes, etc.) by implementing the framework's `Store` and `Connection` traits.

```
 Sui network                               Your infrastructure
 ┌──────────┐        backfill GCS             ┌──────────────────────┐
 │  Full    │        checkpoint bucket        │  sui-indexer-alt     │
 │  nodes   │◀─────────────────────────────── │  pipelines           │
 │  (gRPC)  │        steady state             │                      │
 └──────────┘        (new checkpoints)        │  events.toml         │
                                              │  obj_versions.toml   │
                                              │  coin_transfers.toml │
                                              └─────────┬────────────┘
                                                        ▼
                                              ┌──────────────────────┐
                                              │  Your storage layer  │
                                              │  (Postgres default)  │
                                              └──────────────────────┘
                                                        ▼
                                              ┌──────────────────────┐
                                              │  Your query layer    │
                                              │  (REST / GraphQL /   │
                                              │  raw SQL)            │
                                              └──────────────────────┘
```

## Ingestion sources

Two operational modes:

| Mode | Source | URL pattern |
|---|---|---|
| **Backfill** (historical catch-up) | GCS checkpoint buckets | `gs://mysten-mainnet-checkpoints-use4` (mainnet), similar for testnet |
| **Steady state** (tip of chain) | Full node gRPC | Same URL as your normal gRPC endpoint |

The indexer automatically switches from GCS to gRPC when it catches up to tip.

## Pipeline model

Each pipeline:
1. Defines a data source (checkpoint stream).
2. Defines a transform (what to extract from each checkpoint — events, object changes, coin transfers, etc.).
3. Defines a target schema (Postgres tables by default, but can be any storage layer).
4. Runs concurrently with other pipelines, each writing to its own tables.

Config example (TOML, from the docs pattern):
```toml
# events.toml
[source]
kind = "remote_store"
url = "gs://mysten-mainnet-checkpoints-use4"

[pipeline.events]
concurrency = { kind = "adaptive", initial = 200, min = 50, max = 2000 }

[database]
url = "postgres://localhost/sui_indexer"
```

Multiple pipelines can run in the same process, each targeting different tables. The General-Purpose Indexer is itself a collection of pipelines; yours can sit alongside it or stand alone.

## Tuning

Concurrency:
```toml
concurrency = { kind = "adaptive", initial = 200, min = 50, max = 2000 }
```

The adaptive strategy ramps up concurrency during backfill (GCS is cheap and parallel-friendly) and scales back for steady state. For simple workloads, a fixed concurrency is fine.

Other knobs:
- Batch size for DB writes.
- Retry and backoff policy on transient failures.
- Checkpoint retention (how far back to keep data).

## When to use which

| Scenario | Solution |
|---|---|
| Balance / owned / simple reads | **gRPC `client.core.*`** — no indexer |
| Frontend dashboard with joins | **GraphQL RPC** — hosted |
| Custom leaderboard / aggregations | **Custom indexer** |
| Cross-table joins with app-specific filters | **Custom indexer** |
| Event processing for a game / market | **Custom indexer** (or GraphQL for read-only) |
| Long-term analytics (90+ days history) | **Custom indexer** (the hosted indexer's retention may be shorter) |

## Running alongside the General-Purpose Indexer

The General-Purpose Indexer is open-source and runnable locally. Teams often:

1. Run the General-Purpose Indexer for general queries.
2. Run additional custom pipelines for app-specific data.
3. Point GraphQL RPC at the combined Postgres.

This gives a hosted-style experience with app-specific extensions, without reinventing GraphQL resolvers.

## Considerations

- **Storage operations.** If using Postgres (the default): indexes, vacuum, backups, upgrades. If using another backend: equivalent operational overhead. It's ongoing either way.
- **Checkpoint store egress.** GCS reads for backfill can be slow and bandwidth-heavy for huge histories. Budget accordingly.
- **Sync lag.** Steady-state lag is typically seconds; during backfill it can be hours or days depending on concurrency and history depth.
- **Schema migrations.** Changing a pipeline's schema often requires a backfill. Plan migrations carefully.
- **Testing.** Run against testnet / a replay node before pointing at mainnet.

## Alternatives before building your own

Try in this order:
1. **gRPC `client.core.*`** — zero ops cost.
2. **GraphQL RPC hosted** — zero ops cost, more flexibility.
3. **Run the General-Purpose Indexer locally** — you own the Postgres but the pipelines are prebuilt.
4. **Custom pipelines via `sui-indexer-alt`** — you write the pipelines.

Skip 4 if 1–3 solve your problem.

## Common mistakes

- **Building a custom indexer for a one-off query.** Ongoing ops cost > query value. Use GraphQL.
- **Assuming the indexer provides transactional guarantees.** It's eventually consistent relative to the chain. For point-in-time accurate reads, reference the checkpoint sequence number.
- **Running backfill without concurrency limits.** GCS egress caps or Postgres write throughput will bottleneck. Use adaptive concurrency.
- **Storing on-chain-only data.** If it's already in a full node's gRPC response, you might not need a custom pipeline — just cache.
- **Not retaining checkpoint sequence numbers alongside derived data.** Without them, you can't reconstruct or replay.
