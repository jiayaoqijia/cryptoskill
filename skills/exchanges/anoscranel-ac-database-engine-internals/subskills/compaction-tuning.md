---
name: compaction-tuning
domain: software-engineering/compaction-tuning
trigger: "Deciding when merges run and what they cost."
anti_trigger: "Not for general background-job scheduling (ac-scheduled-jobs)."
scope: "When merges run, what they cost, and whose latency they borrow."
status: seedling
---

# Compaction tuning

## Standard

Compaction rewrites sorted runs into larger sorted runs, and its cost is proportional to the data it rewrites. The scheduler decides when that cost is paid, and the choice is between steady low-level merging, which keeps the read path short at a constant write-amplification cost, and size-tiered or level-triggered merging, which batches the work into larger, less frequent surges with the same or greater total cost but higher peak impact.

The tuning question is rarely whether to compact but whose latency funds it. Every merge consumes I/O and CPU that a foreground read or write would otherwise use, so a compaction schedule is a scheduling decision about latency allocation: steady work taxes every operation a little, and spiky work taxes some operations a lot. Recording that allocation, rather than the total, is what makes a compaction setting interpretable.

Primary sources: <https://github.com/facebook/rocksdb/wiki/Compaction> and <https://en.wikipedia.org/wiki/Log-structured_merge-tree>.

## Decision rules

- Record the trigger policy and the total write cost it implies.
- Record the peak impact of a compaction burst on concurrent reads and writes.
- Record the steady-state interference for a chosen rate limit.
- Record the backlog behaviour when writes outpace compaction.
- Record the read-path length the policy maintains, not only the schedule.
- Record the falls-behind threshold and the action it triggers.

## Procedure

1. Record the compaction policy and its trigger conditions.
2. Record total rewrite cost per byte written under the policy.
3. Measure peak foreground impact for a full compaction burst.
4. Apply a rate limit and measure steady-state interference.
5. Record the read-path length the policy maintains.
6. Write the record with the latency allocation stated — who pays and when.

## Anti-patterns

- Tuning only the total cost and ignoring the allocation.
- Running compaction unthrottled and attributing the latency spike to the workload.
- Permitting an unbounded backlog and treating read latency as unrelated.
- Choosing a policy by total cost alone when the peak impact is the binding constraint.
- Not recording the falls-behind threshold and recovery plan.

## Done checklist

- [ ] Trigger policy recorded.
- [ ] Total rewrite cost recorded.
- [ ] Peak foreground impact measured.
- [ ] Steady-state interference measured.
- [ ] Read-path length recorded.
- [ ] Backlog threshold and action recorded.

One further check is backlog growth rate under sustained overload: if write input exceeds the policy's long-run compact rate, the read path lengthens without bound regardless of throttling, and the correct fix is a policy change rather than a throttle change. Recording the input rate and the policy's sustainable rate separates a transient backlog from a structural one.

## Sources

- RocksDB universal and level compaction documentation: <https://github.com/facebook/rocksdb/wiki/Compaction>
- RocksDB tuning guide rate-limiting of background compaction: <https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide>
- Log-structured merge tree structure and merge cost: <https://en.wikipedia.org/wiki/Log-structured_merge-tree>
