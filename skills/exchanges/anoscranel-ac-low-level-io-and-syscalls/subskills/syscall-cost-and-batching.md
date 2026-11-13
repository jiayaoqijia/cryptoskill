---
name: syscall-cost-and-batching
domain: software-engineering/syscall-cost-and-batching
trigger: "Amortizing the fixed cost of crossing the kernel boundary."
anti_trigger: "Not for network protocol design, and not for scheduler latency."
scope: "The fixed cost of the boundary and amortizing it."
status: seedling
---

# Syscall cost and batching

## Standard

A syscall is a controlled transition: the program traps into the kernel, the kernel validates arguments and performs the work, and control returns with results. The transition itself has a fixed cost — privilege switch, entry and exit paths, potential cache and TLB disturbance — independent of how many bytes are moved. Small frequent syscalls therefore spend more time on the boundary than on the work, and the same total bytes moved in fewer, larger calls can be many times cheaper.

The design rule that follows is batching at the boundary: accumulate writes and flush in groups, read in buffer-sized units rather than token-sized ones, and use interfaces that combine operations when the platform offers them. The count is measurable directly — a profiler shows syscalls as a category, and the ratio of boundary time to work time is the number that justifies or dismisses a batching change.

Primary sources: <https://man7.org/linux/man-pages/man2/mmap.2.html> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Measure syscall counts for the hot path, not only the byte counts.
- Record the boundary-to-work time ratio for the dominant calls.
- Buffer small writes and flush on size or time, whichever bound is hit first.
- Read in units that amortize the boundary across many elements.
- Prefer interfaces that batch at the kernel's own queue when density justifies them.
- Record the flush policy of every buffer added, since buffering changes failure semantics.

## Procedure

1. Count syscalls and bytes on the hot path.
2. Compute bytes per call and boundary time per call.
3. Identify calls below the amortization threshold.
4. Batch or buffer them with an explicit flush policy.
5. Re-measure counts and end-to-end time.
6. Record both the counts and the flush policy.

## Anti-patterns

- Writing one small record at a time to a file.
- Adding buffering without recording its flush policy.
- Batching when the data is latency-sensitive and the flush delay dominates.
- Counting bytes as a proxy for boundary crossings.
- Assuming syscall cost from an old benchmark on different hardware.

## Done checklist

- [ ] Syscall counts measured.
- [ ] Boundary-to-work ratio computed.
- [ ] Sub-threshold calls identified.
- [ ] Buffering added with a flush policy.
- [ ] Counts re-measured.
- [ ] Flush policies recorded.

Batching also has a durability face: a group of writes flushed as one unit commits or fails together, which changes what a partial failure means mid-batch, and the record should state whether the flush boundary is a transaction boundary or merely an efficiency one.

## Sources

- Syscall interfaces and semantics: <https://man7.org/linux/man-pages/man2/mmap.2.html>
- System profiling: <https://www.brendangregg.com/linuxperf.html>
- Readiness interfaces: <https://man7.org/linux/man-pages/man7/epoll.7.html>
