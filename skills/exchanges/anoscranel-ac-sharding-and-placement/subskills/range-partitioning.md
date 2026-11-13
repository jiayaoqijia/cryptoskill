---
name: range-partitioning
domain: software-engineering/range-partitioning
trigger: "Reading ordered key-space splits and their hotspot risk."
anti_trigger: "Not for hash placement, and not for analytical pruning inside a single engine."
scope: "Ordered splits that serve range scans and concentrate hotspot risk."
status: seedling
---

# Range partitioning

## Standard

Range partitioning splits an ordered key space into contiguous chunks: everything between two split points lives together. Records near each other in key order co-locate, so range scans touch few partitions, and prefix queries can be routed exactly. The price sits where the order is densest: partition boundaries follow the traffic's mass, and a key range that receives disproportionate writes becomes a hotspot that the scheme cannot spread by construction.

Time-ordered data is the canonical case. Timestamps give a natural order and an ever-arriving write frontier, so the newest partition absorbs all inserts while the old ones rest — which is a feature for retention and a hotspot for writes, and systems commonly salt the write frontier or pre-split future ranges to compensate.

Primary sources: <https://en.wikipedia.org/wiki/Shard_(database_architecture)> and <https://dataintensive.net/>.

## Decision rules

- Record the split points, who chooses them, and whether they adjust automatically.
- Record the access pattern each range serves: point, prefix, range, or sequence.
- Record where the write frontier falls and whether it concentrates.
- Record the pre-splitting or salting policy for frontier hotspots.
- Record how a new range is created and how its position is announced.
- Record how partition sizes are kept within bounds as data grows.

## Procedure

1. Write the key order and where splits sit.
2. Identify who moves split points and under what signal.
3. Map the traffic onto the ranges and locate the write frontier.
4. Test the frontier's write concentration on the busiest range.
5. Record salting or pre-split mitigation if the frontier is hot.
6. Write the range design with the hotspot analysis stated.

## Anti-patterns

- Choosing range partitioning for load evenness when that is its weakness.
- Letting the newest timestamp range take all writes without mitigation.
- Splitting manually once and never revisiting as data grows.
- Moving split points without a routing update path.
- Assuming old ranges stay cold; exports and backfills wake them.

## Done checklist

- [ ] Split points and ownership recorded.
- [ ] Served access patterns recorded.
- [ ] Write frontier located.
- [ ] Hotspot concentration measured.
- [ ] Mitigation policy recorded.
- [ ] Range growth management stated.

Range partitioning is also the placement read most often invalidated by growth: split points chosen for a dataset double the size are wrong, and the record should state the size at which the current boundaries were chosen so the next reader knows when they were last true.

## Sources

- Range sharding reference: <https://en.wikipedia.org/wiki/Shard_(database_architecture)>
- Partitioning discussion: <https://dataintensive.net/>
- Distributed patterns overview: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
