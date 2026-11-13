---
name: chunking-and-compaction
domain: software-engineering/chunking-and-compaction
trigger: "Understanding how the engine stores samples over time and what that costs."
anti_trigger: "Not for query construction, and not for application memory management."
scope: "Head chunks, compression, block compaction, and the cost curve."
status: seedling
---

# Chunking and compaction

## Standard

Time-series samples are written into a head chunk — an in-memory window that accumulates recent samples per series — and sealed when full. The sealed chunks are compressed, and over time blocks are compacted: neighbouring windows merged, small files coalesced, and the index rewritten so that old data is stored in fewer, larger structures. The design insight behind every production engine is that recent writes go to a small hot set and old reads come from cold compacted blocks, so the two halves of the lifecycle get different treatments.

The cost curve follows. Head memory is proportional to active series times chunk size — which is why cardinality dominates memory. Compression works because timestamps move predictably and values change slowly, so delta encoding and bit-packing shrink typical streams by an order of magnitude, and the Gorilla result made these designs practical at fleet scale. Compaction is not free: it is background work that spikes disk IO, and a cardinality surge converts a smooth compaction schedule into a foreground problem.

Primary sources: <https://en.wikipedia.org/wiki/Time_series_database> and <https://prometheus.io/docs/prometheus/latest/storage/>.

## Decision rules

- Expect head memory — active series times chunk size — as the dominant memory budget line, and size it from the schema, not from hope.
- Benefit from compression by designing samples that change slowly: sparse bursts and high-entropy values compress worse.
- Sweep points: the compaction schedule is a tuning variable that trades write latency against background IO, and a surge in series count re-balances that trade.
- Size disk from the compacted steady state, measured in the record, then check retention estimates against it.
- Treat a chart of compaction duration over weeks as an engine-health metric, and investigate a sustained rise the same as a latency rise.
- Model the cost of a schema change, not only its functional benefit, because storage memory and compaction spikes are schema consequences.

## Procedure

1. Record the chunk size and the memory per active series the engine documents.
2. Project head memory at the schema's expected active-series count and compare with the node's memory budget.
3. Measure the compression ratio after a typical week, not a synthetic suite: real streams determine the disk math.
4. Record the compaction schedule, and instrument compaction latency and IO as engine health.
5. On any schema or fleet change, re-project head memory and disk from the recorded ratios.
6. Record the cost curve — head memory, compression ratio, compaction times — with measurement dates.

## Anti-patterns

- Sizing the node from sample volume, then being surprised when memory tracks the series count instead.
- Reading the compression ratio from a marketing number rather than the actual fleet.
- A sustained compaction slowdown dismissed as background noise until ingest stalls behind it.
- Estimating disk at synthesize-the-load conditions, then producing unpredictable data at production.
- Adding labels without re-projecting head memory because the change is only code review discussable.

## Done checklist

- [ ] Head memory budgeted from active series and chunk size.
- [ ] Compression ratio measured on real data.
- [ ] Compaction latency and IO instrumented as engine health.
- [ ] Disk sized from measured steady state.
- [ ] Compaction schedule recorded as a tuning variable.
- [ ] Cost curve in the record with dates.

## Sources

- Time-series database systems, Gorilla among them: <https://en.wikipedia.org/wiki/Time_series_database>
- Storage lifecycle overview: <https://prometheus.io/docs/prometheus/latest/storage/>
- Capacity-planning overview: <https://prometheus.io/docs/introduction/overview/>
