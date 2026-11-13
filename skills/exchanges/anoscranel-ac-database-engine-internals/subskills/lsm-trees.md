---
name: lsm-trees
domain: software-engineering/lsm-trees
trigger: "Reading or designing log-structured merge tree behaviour."
anti_trigger: "Not for analytical columnar layout (ac-analytical-data-modeling)."
scope: "Append-only layers, memtables, the merge that keeps depth bounded."
status: seedling
---

# LSM trees

## Standard

A log-structured merge tree never updates data in place. A write lands in an in-memory memtable, which is immutable once full and flushed to disk as a sorted run; reads check the memtable, then each run from newest to oldest, and a background merge rewrites runs into larger sorted runs so the number of levels stays bounded. Writes are sequential and small; reads pay a price proportional to the number of runs not yet merged.

That trade is the whole design. A workload of appends and keyed lookups pays little for the merge machinery; a workload of overwrites pays it twice, once for the write itself and again for the compaction that eventually reclaims the space the overwritten copies occupy. The decision to use an LSM engine is therefore a decision that the write path's sequential cost dominates the read path's layered cost.

Primary sources: <https://en.wikipedia.org/wiki/Log-structured_merge-tree> and <https://github.com/google/leveldb/blob/main/doc/impl.md>.

## Decision rules

- Record the level structure and the size ratio between levels.
- Record, per read, the worst-case number of runs consulted before a key is found or declared absent.
- Record the memtable's share of memory and the flush frequency that follows.
- Record the overwrite pattern and the space it holds until compaction reclaims it.
- Record whether a bloom filter or a summary bounds the read cost.
- Record the point at which a read's cost becomes a merge-scheduling question rather than a lookup question.

## Procedure

1. Record the level count and per-level size ratio.
2. Insert the workload's write pattern and note the per-level run count.
3. Record the read path's run count for the workload's key distribution.
4. Record memtable memory and its flush frequency.
5. Record compaction's trigger and its effect on read cost after a run.
6. Write the record distinguishing the write cost, the read cost, and the merge cost as three separate lines.

## Anti-patterns

- Comparing LSM write throughput with B-tree write throughput without the accompanying read-path and space costs.
- Treating a read's layered cost as fixed when the merge schedule changes it.
- Overwriting heavily in an LSM without recording the space the pattern holds.
- Sizing the memtable without recording the flush frequency it implies.
- Skipping the absent-key cost, which consults every level.

## Done checklist

- [ ] Level structure and ratios recorded.
- [ ] Read-path run count measured for the key distribution.
- [ ] Memtable size and flush frequency recorded.
- [ ] Overwrite holding-space impact recorded.
- [ ] Bloom or summary bounding recorded.
- [ ] Write, read, and merge costs recorded as separate lines.

A further observation is that the absent-key lookup is the worst case the design cannot hide: a read for a key that never existed consults every level and every summary mechanism before concluding absence, so workloads that generate high rates of negative lookups deserve a named line in the record rather than being averaged into the hit-rate.

## Sources

- Log-structured merge tree structure and cost model: <https://en.wikipedia.org/wiki/Log-structured_merge-tree>
- RocksDB basic architecture documentation: <https://github.com/facebook/rocksdb/wiki>
- LevelDB LSM tree documentation: <https://github.com/google/leveldb/blob/main/doc/impl.md>
