---
name: page-faults-and-major-minor
domain: software-engineering/page-faults-and-major-minor
trigger: "Distinguishing page-fault classes and their costs."
anti_trigger: "Not for database buffer management, and not for memory leaks."
scope: "The faults that hit storage, the ones that do not, and page residency."
status: seedling
---

# Page faults and major-minor

## Standard

A page fault is the processor asking the kernel to make a virtual page present. A minor fault is served from memory: the kernel maps an existing page or lazily allocates a zero page. A major fault requires I/O — reading from a file or a swap device — and costs as much as a disk access. The split between minor and major is, in a single counter pair, the difference between an application that starts slowly because it is doing work and one that starts slowly because it is paging.

The design decisions that follow are about residency and laziness. A memory-mapped file reads on demand by default, so the first traversal of a large region is major-fault bound, while a file pre-read into memory pays at read time and pages in ahead of use. Neither is free; the difference is when the cost arrives and whether it lands inside a latency-sensitive window. Huge pages reduce the number of faults and TLB misses, and are worth recording as a distinct design layer.

Primary sources: <https://man7.org/linux/man-pages/man2/mmap.2.html> and <https://www.brendangregg.com/linuxperf.html>.

## Decision rules

- Record minor and major fault counts separately for the startup window and steady state.
- Track which memory regions are lazy (fault on demand) and which are eagerly resident.
- Record whether anonymous memory is locked or swappable, since swap turns minor faults major under pressure.
- For large mmap'd datasets, record the sequential-fault penalty of the first traversal.
- Record huge-page (transparent or explicit) usage as a distinct policy.
- Treat a rising major-fault rate in steady state as a residency problem, not a startup one.

## Procedure

1. Measure minor and major faults for the process's startup and steady state.
2. Classify large memory regions as lazy or eager.
3. Identify which regions map to files and which are anonymous.
4. Check the swappiness of pages on latency-sensitive paths.
5. Decide the huge-page policy and record it.
6. Re-measure after any residency change.

## Anti-patterns

- Reading total fault counts without the major-minor split.
- Judging startup cost without checking whether it is major-fault bound.
- Letting a latency-sensitive path fault on a mapped file.
- Ignoring swap as the cause when steady-state major faults rise.
- Enabling huge pages without recording the policy.

## Done checklist

- [ ] Minor and major faults measured, startup and steady state.
- [ ] Regions classified lazy or eager.
- [ ] File-backed identified.
- [ ] Sensitive paths swap-checked.
- [ ] Huge-page policy recorded.
- [ ] Post-change measurements taken.

## Sources

- mmap and page behaviour: <https://man7.org/linux/man-pages/man2/mmap.2.html>
- Faults and system tools: <https://www.brendangregg.com/linuxperf.html>
- Kernel memory documentation: <https://docs.kernel.org/bpf/>
