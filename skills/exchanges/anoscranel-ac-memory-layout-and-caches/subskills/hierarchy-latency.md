---
name: hierarchy-latency
domain: software-engineering/hierarchy-latency
trigger: "Working out how the memory latency ladder changes design."
anti_trigger: "Not for network latency budgets, and not for disk I/O tuning."
scope: "The latency ladder and the arithmetic that makes locality decisive."
status: seedling
---

# Hierarchy latency

## Standard

Each level of the memory hierarchy costs roughly an order of magnitude more than the one above it: a register access is sub-nanosecond, an L1 hit a few cycles, a DRAM access hundreds. The exact figures change by generation, but the ratios are stable enough that a design built around locality wins even when its algorithmic complexity is identical to the naive version.

The arithmetic that follows is about trip counts. A loop touching memory sequentially performs many fewer DRAM trips per element than a pointer-chasing loop that walks the same array in random order, and it avoids MMU pagewalks by touching fewer lines.

Secondary effects compound the primary ones: instruction fetch misses and branch predictor cold-starts mean the first iterations of a cold loop can be an order of magnitude slower than steady state, so short loops never reach their billed throughput.

Primary sources: <https://www.akkadia.org/drepper/cpumemory.pdf> and <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>.

## Decision rules

- Record the approximate latency ladder for the target class of hardware, with its source and date.
- State, for any hot path, the number of cache lines touched per element and the number of DRAM trips.
- Distinguish the cold-start penalty of a loop from its steady-state cost when the loop is short.
- Prefer fewer distinct trips over fewer bytes transferred: the line, not the byte, is the moving unit.
- Record any assumption that a level is effectively infinite, as with L2 in a tight loop.
- Estimate before restructuring, and keep the estimate beside the measurement.

## Procedure

1. Write the latency ladder for the hardware, with a source.
2. Traverse the hot path's data access pattern by line, not by element.
3. Estimate DRAM trips and cache-line touches for the current layout.
4. Identify whether the pattern is sequential, strided, or random.
5. Restructure only after estimating the win, then measure.
6. Record the estimate and the measurement side by side.

## Anti-patterns

- Optimizing structure size while ignoring trip count.
- Counting bytes rather than lines.
- Treating latency figures from a different generation as portable.
- Ignoring cold-start costs in short-loop measurements.
- Restructuring without an estimate first.

## Done checklist

- [ ] Ladder recorded with source and date.
- [ ] Lines touched and DRAM trips estimated.
- [ ] Pattern classified (sequential, strided, random).
- [ ] Estimate written before the change.
- [ ] Measurement taken after.
- [ ] Both recorded side by side.

## Sources

- Architecture reference: <https://www.akkadia.org/drepper/cpumemory.pdf>
- Vendor optimization manual (403 to curl, live via reader; primary doc): <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>
- Optimization resources: <https://agner.org/optimize/>
