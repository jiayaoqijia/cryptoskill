---
name: page-cache-and-direct-io
domain: software-engineering/page-cache-and-direct-io
trigger: "Choosing between the kernel's buffer cache and direct I/O."
anti_trigger: "Not for application caching, and not for database buffer pools."
scope: "The buffer cache, its sharing, and paying to skip it."
status: seedling
---

# Page cache and direct I/O

## Standard

Ordinary file reads and writes pass through the kernel's page cache: reads are served from memory when resident, and writes are recorded in memory and flushed later. The cache is shared across processes, which makes a second reader of the same file nearly free, and it is managed by the kernel, which means the program neither pays for nor controls eviction.

Direct I/O skips the cache: the transfer goes to storage with one fewer copy, which helps workloads that stream data once and gain nothing from residency, and it is a requirement for databases that maintain their own buffer pool and cannot tolerate the kernel's double caching. The cost is real — unaligned or undersized direct transfers are penalized or rejected, and the program inherits the flush and ordering responsibilities the cache was quietly performing. The choice is per-workload, not per-program.

Primary sources: <https://man7.org/linux/man-pages/man2/mmap.2.html> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Record whether each hot file's access pattern is re-read, stream-once, or mixed.
- Use cached I/O for re-read data; the cache is the fastest layer available.
- Reserve direct I/O for stream-once workloads or self-managed buffer pools.
- Record alignment and size constraints when direct I/O is chosen.
- Record durability semantics separately: cache flushing and direct I/O are independent decisions.
- Measure with the cache warm before judging a cached path slow.

## Procedure

1. Classify each hot file by access pattern.
2. Record current cache behaviour with a warm-cache measurement.
3. Choose direct I/O only where the pattern shows no reuse.
4. Verify alignment and transfer-size constraints for direct paths.
5. Re-measure with the same residency conditions.
6. Record the decision and both measurements.

## Anti-patterns

- Choosing direct I/O for a re-read dataset.
- Comparing a cold direct read against a warm cached read.
- Assuming direct I/O implies durability without a flush call.
- Ignoring the alignment requirements and paying silent penalties.
- Blaming the cache for a slowdown that is a re-read of unresident data.

## Done checklist

- [ ] Access patterns classified.
- [ ] Warm-cache baseline taken.
- [ ] Direct I/O chosen only for stream-once data.
- [ ] Alignment constraints recorded.
- [ ] Durability handled separately.
- [ ] Both measurements recorded.

Note also that the cache serves reads and writes with different generosity: a written page can sit in cache dirty, visible to reads but not yet durable, and a program that treats a successful write as a durability guarantee is relying on a flush policy it never stated. Recording durability independently of the caching choice keeps that assumption from hiding inside a throughput decision.

## Sources

- File I/O interfaces: <https://man7.org/linux/man-pages/man2/mmap.2.html>
- System measurement: <https://www.brendangregg.com/linuxperf.html>
- Event-driven I/O context: <https://man7.org/linux/man-pages/man7/epoll.7.html>
