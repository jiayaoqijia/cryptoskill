---
name: amp-analysis
domain: software-engineering/amp-analysis
trigger: "Quantifying a workload's read, write, and space amplification."
anti_trigger: "Not for capacity headroom in general (ac-chaos-and-capacity-testing)."
scope: "Read, write, and space amplification as the design currency of an engine."
status: seedling
---

# Amplification analysis

## Standard

Every storage engine multiplies the work it is asked to do. Read amplification is the number of pages touched to satisfy one logical read; write amplification is the bytes physically written per logical byte inserted; space amplification is the storage held per logical byte live. These three form the currency of engine choice, and every design decision trades one for another: the log adds write amplification to make writes safe, the merge adds read amplification to keep batched writes bounded, the tombstone adds space amplification to defer the reclaim.

Because they trade against each other, no configuration minimizes all three, and an argument about storage tuning is nearly always an argument about which amplification matters for a workload. Writing the three numbers down for a workload converts a preference dispute into arithmetic: a point-lookup-heavy workload cares about read amplification and can tolerate write costs; an append-only workload inverts that preference; a space-constrained system cares about the third.

Primary sources: <https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide> and <https://postgresql.org/docs/current/routine-vacuuming.html>.

## Decision rules

- Define the three measures precisely as page counts, byte ratios, and live ratios.
- Record write amplification for the logical write path including log and merge.
- Record read amplification for the workload's actual key mix including absent keys.
- Record space amplification with a compaction schedule stated.
- Record which amplification binds the workload, with the evidence.
- Record the trade being made when a tuning knob is turned.

## Procedure

1. Define the three units before measuring.
2. Measure or derive write amplification for a workload's insert pattern.
3. Measure read amplification for the workload's key distribution including misses.
4. Measure or derive space amplification after a compaction cycle.
5. Rank the three and record which binds.
6. Write the record with each tuning knob annotated by the amplification it trades.

## Anti-patterns

- Quoting vendor throughput without the amplification it implies.
- Arguing about an engine without stating which amplification binds.
- Measuring read amplification only on present keys.
- Reporting space amplification without a compaction cycle completed.
- Turning a tuning knob without recording what it trades.

## Done checklist

- [ ] Units defined for all three measures.
- [ ] Write amplification measured or derived.
- [ ] Read amplification measured including absent keys.
- [ ] Space amplification measured after a compaction.
- [ ] Binding amplification identified with evidence.
- [ ] Each knob annotated with its trade.

## Sources

- Log-structured merge tree amplification model: <https://en.wikipedia.org/wiki/Log-structured_merge-tree>
- RocksDB tuning guide's write, read, and space discussion: <https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide>
- PostgreSQL vacuum and bloat documentation: <https://postgresql.org/docs/current/routine-vacuuming.html>
