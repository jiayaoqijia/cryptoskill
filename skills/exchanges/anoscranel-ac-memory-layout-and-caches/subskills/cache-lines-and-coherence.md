---
name: cache-lines-and-coherence
domain: software-engineering/cache-lines-and-coherence
trigger: "Understanding the cache line as the unit of transfer and coherence."
anti_trigger: "Not for database page caching, and not for CDN caching."
scope: "The unit of transfer and what sharing a line across cores costs."
status: seedling
---

# Cache lines and coherence

## Standard

The cache does not fetch individual bytes; it fetches cache lines, typically sixty-four bytes, and every subsequent access to that line is nearly free. The practical consequence is that a struct's fields ride together: touching one byte brings its neighbours, so two fields in the same line are effectively one unit of transfer and one unit of coherence.

Coherence is the expensive half. When two cores each hold a line writable and both write it, the line ping-pongs between their caches — each write invalidates the other core's copy, and the memory traffic comes from the coherence protocol rather than from either program's request. A counter incremented by many threads on the same line can become a coherence storm at a scale where a single-threaded counter is free, and the fix is not faster code but separate lines.

Primary sources: <https://www.akkadia.org/drepper/cpumemory.pdf> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Record the line size of the target hardware, and never assume it across vendors.
- Map which structure fields share a line, especially the ones written by different threads.
- Record the coherence traffic observed, not only the miss count.
- Prefer splitting a hot counter or flag onto its own line over reducing its size.
- Record any padding added and the width it fills, so a later reader can remove it knowingly.
- Verify the fix with the same counter that showed the problem, not only end-to-end timing.

## Procedure

1. Identify the structures on the hot path and their field addresses.
2. Compute which fields share a cache line at the observed line size.
3. Measure coherence traffic on the suspected line.
4. Separate contended fields onto their own lines with padding.
5. Re-measure coherence traffic and end-to-end time.
6. Record the layout change and both measurements in the layout record.

## Anti-patterns

- Treating a byte-sized flag as free because it is small.
- Padding every structure by default, paying size for no contention.
- Reading the miss counter without the coherence counter.
- Assuming the line size from a previous machine.
- Keeping the padding without recording why it exists.

## Done checklist

- [ ] Line size recorded for the target hardware.
- [ ] Field-to-line mapping done for hot structures.
- [ ] Coherence traffic measured before and after.
- [ ] Contended fields separated.
- [ ] Padding width recorded.
- [ ] Layout change and measurements in the record.

## Sources

- Memory hierarchy reference: <https://www.akkadia.org/drepper/cpumemory.pdf>
- Linux performance tooling: <https://www.brendangregg.com/linuxperf.html>
- Manual pages for memory syscalls: <https://man7.org/linux/man-pages/man2/mmap.2.html>
