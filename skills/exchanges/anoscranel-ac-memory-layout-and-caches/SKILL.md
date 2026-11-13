---
name: ac-memory-layout-and-caches
description: "How a program's memory behaves on real hardware: cache lines and what sharing one costs, the memory hierarchy's latency ladder, false sharing and padding as a fix, aligned access and unaligned penalties, prefetching and the access pattern that makes it useless, page faults and the major-minor split, NUMA and the locality that decides remote memory costs, and the written layout record. It explains how data placement performs and how to observe it; it never recommends a processor and never promises a speedup. Use when asking \"cache line\", \"false sharing\", \"memory alignment\", \"prefetch\", \"page fault\", \"NUMA\", \"memory latency\", \"cache miss\", \"why is iteration order so much faster\", \"padded structure\", \"locality of reference\". Not for profiling methodology in general (ac-performance), not for page allocation inside a database engine (ac-query-and-index-design), not for OS process memory limits (ac-resource-exhaustion-diagnosis)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Memory layout and caches

## Overview

A program's memory accesses land on a hierarchy, not a flat store: registers, L1 through L3 caches, DRAM, and beyond. Each step down costs an order of magnitude more time, and the hardware accelerates the common case by fetching in cache-line units and predicting access patterns. A program whose data layout cooperates with that machinery can be several times faster than one with identical algorithmic complexity laid out against the grain.

This skill covers the layout decisions that interact with the hierarchy: cache-line sharing and false sharing, alignment, access order and prefetch, and NUMA locality. These are design-level choices — how a struct is ordered, how a matrix is traversed, which thread writes which field — and they are observable directly in profiler counters rather than only in end-to-end timing.

Primary sources: <https://www.akkadia.org/drepper/cpumemory.pdf> and <https://man7.org/linux/man-pages/man2/mmap.2.html>.

## When to use

- When a hot loop is slower than its algorithm predicts, or two equivalent traversals differ.
- When threads share a structure and scaling degrades with thread count.
- When a syscall with eager memory setup is outperformed by a lazy variant.
- When a data-parallel computation degrades on a multi-socket machine.

## When NOT to use

- For profiling methodology and flame graphs (use ac-performance).
- For database page and buffer management (use ac-query-and-index-design).
- For process memory limits and OOM diagnosis (use ac-resource-exhaustion-diagnosis).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/cache-lines-and-coherence.md` | `software-engineering/cache-lines-and-coherence` | The unit of transfer and what sharing a line across cores costs. |
| `subskills/hierarchy-latency.md` | `software-engineering/hierarchy-latency` | The latency ladder and the arithmetic that makes locality decisive. |
| `subskills/false-sharing-and-padding.md` | `software-engineering/false-sharing-and-padding` | Two threads, one cache line, and the padding that separates them. |
| `subskills/alignment-and-unaligned-access.md` | `software-engineering/alignment-and-unaligned-access` | What alignment guarantees, and when reading unaligned is safe or traps. |
| `subskills/prefetch-and-access-order.md` | `software-engineering/prefetch-and-access-order` | Sequential streams, strided access, and the patterns hardware predicts. |
| `subskills/page-faults-and-major-minor.md` | `software-engineering/page-faults-and-major-minor` | The faults that hit storage, the ones that do not, and page residency. |
| `subskills/numa-and-locality.md` | `software-engineering/numa-and-locality` | Remote memory costs, allocation affinity, and migration. |
| `subskills/layout-record.md` | `software-engineering/layout-record` | The written record: layout decisions and the measurements behind them. |

## Status and honest limits

Cache behaviour varies by processor and even by SKU; counters exist for it, but their names and units differ across vendors, and a tuning that helps one chip can hurt another. Latency-aware design also compromises readability — padded structs and split arrays confuse as often as they accelerate, and the honest method is to measure the hot path before restructuring it, not to rearrange layouts speculatively. Where microarchitecture claims matter, primary vendor documentation is the source, and anything here is a starting hypothesis, not a portable law.
