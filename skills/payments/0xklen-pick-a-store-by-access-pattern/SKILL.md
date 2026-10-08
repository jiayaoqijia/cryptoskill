---
name: pick-a-store-by-access-pattern
description: Use when choosing a datastore for a new workload. Derives the engine from measured access pattern, consistency and query shape rather than team familiarity.
---

# Pick a Store by Access Pattern

The store follows the workload. Name the read/write ratio, query shape, consistency and durability needs as numbers first; the shortlist then falls out mechanically instead of by habit.

## Procedure

1. Quantify the workload: keys read/s, writes/s, mean and p99 value size, read:write ratio, and the p99 latency budget.
2. Classify the query shape. Point lookup by key → KV store; ordered range/prefix scan → LSM or B-tree; ad-hoc predicates across columns → relational; full-text → search engine; large immutable blobs → object store.
3. Write down the consistency floor: linearizable reads, read-your-writes, or is a stale read acceptable for a bounded window?
4. Write down the durability floor: may a write be lost on single-node failure, or must it survive loss of a whole zone?
5. Shortlist two engines and load-test both at 2x the projected peak, not on paper.
6. Drive traffic with a realistic mix: `wrk -t4 -c64 -d60s --latency`, `pgbench -c32 -j4 -T60 -S`, `redis-benchmark -n 200000 -c50 -t set,get`.
7. Re-run the test with a working set that exceeds RAM so you measure the disk path, not the page cache.
8. Re-check the two rejected candidates for one weakness each (operational complexity, backup story, team familiarity) before committing.
9. Record the chosen engine, the measured p99, and the working-set size in an ADR; re-test when any input changes by more than 2x.

## Pitfalls

- Choosing Postgres for a 500k-QPS counter because it is familiar; the row lock becomes the bottleneck before the query planner is.
- Benchmarking on a dataset that fits entirely in page cache, then discovering the real disk throughput is 1/50th of the measurement.
- Assuming an "eventually consistent" store gives read-your-writes after a write; usually it does not without a session token.
- Picking an LSM store for read-heavy point lookups and inheriting background compaction that steals the IO budget.
- Treating object storage as a POSIX filesystem: no atomic rename, no cheap listing, per-object request costs.
- Ignoring the durability tier — a cache with no replication is not a system of record, however fast it is.
- Letting the query shape drive toward a search engine when the data is small and static; a flat file plus `grep` is sometimes correct.

## Verification

    pgbench -c32 -j4 -T60 -S -P 10 | tail -n3   # tps and latency under sustained read load

The chosen engine holds p99 under the stated budget at 2x projected peak with a working set exceeding RAM, and the ADR names the numbers that justified it.

Report: "Chose <engine> on a measured <n> QPS / <s> p99 at <size> working set; ADR at docs/adr/NNN-store.md records the losing candidate and why."
