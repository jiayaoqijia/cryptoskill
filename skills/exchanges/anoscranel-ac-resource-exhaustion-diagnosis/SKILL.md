---
name: ac-resource-exhaustion-diagnosis
description: "Diagnosing the failure class where a resource runs out: file descriptors and port exhaustion, connection and cursor leaks, thread pool saturation, memory pressure and the out-of-memory kill, and the gradual-degradation curves that precede each. It explains how to tell which resource is exhausted from the symptoms it produces; it never recommends a product and never treats a restart as a fix. Use when asking \"too many open files\", \"address already in use\", \"connection pool exhausted\", \"thread pool saturated\", \"OOM killed\", \"memory leak in production\", \"out of file descriptors\", \"cannot allocate\". Not for the scientific method of finding the underlying bug (ac-debugging), not for capacity planning headroom (ac-chaos-and-capacity-testing), not for resilience budgets that bound the failure (ac-resilience-budgets)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Resource exhaustion diagnosis

## Overview

A large share of production failures are the same event wearing different masks: a finite pool somewhere ran out. File descriptors, ephemeral ports, database connections, worker threads, heap — each has a limit, each produces a characteristic complaint when exhausted, and each leaves a curve of gradual degradation before the hard failure that most teams never look at.

This skill is the differential diagnosis of exhaustion: reading the symptom to identify which resource ran out, then finding whether it is a leak (usage rises and never falls), saturation (usage is legitimately at the limit), or a limit set below the workload's real need. The boundary with capacity testing is time: that skill plans headroom in advance; this one starts when the pager has already fired.

Primary sources: <https://www.kernel.org/doc/html/latest/admin-guide/sysctl/> and <https://learn.microsoft.com/en-us/azure/well-architected/>.

## When to use

- "Too many open files", "address already in use", "cannot allocate", "OOM killed".
- A pool error: connections, cursors, threads, or requests queued and timing out.
- Latency degrading over days and clearing on restart — the leak signature.
- Setting limits for a deployment from evidence rather than habit.

## When NOT to use

- For finding the defect that causes a leak once identified (use ac-debugging).
- For headroom planning before saturation (use ac-chaos-and-capacity-testing).
- For bounding the blast radius once exhausted (use ac-resilience-budgets).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/fds-and-ports.md` | `software-engineering/fds-and-ports` | File descriptors, ephemeral ports, the TIME_WAIT pile, and their hard errors. |
| `subskills/connection-and-cursor-leaks.md` | `software-engineering/connection-and-cursor-leaks` | Pools that never return: leaked connections, cursors, sessions, and handles. |
| `subskills/thread-pool-saturation.md` | `software-engineering/thread-pool-saturation` | When all threads are busy, what queued requests experience, and what blocks them. |
| `subskills/memory-pressure-and-oom.md` | `software-engineering/memory-pressure-and-oom` | Heap curves, the kernel's kill decision, and reading the OOM record. |
| `subskills/leak-versus-limit.md` | `software-engineering/leak-versus-limit` | The three causes of exhaustion and the evidence that separates them. |
| `subskills/limits-from-evidence.md` | `software-engineering/limits-from-evidence` | Setting ulimits, pool sizes, and quotas from measured need, not defaults. |
| `subskills/exhaustion-record.md` | `software-engineering/exhaustion-record` | The written record: resource, curve, verdict, and the limit change made. |

## Status and honest limits

Exhaustion symptoms mislead: a "connection pool exhausted" error is often caused by something slow elsewhere holding connections longer than the pool can absorb, so the error names the victim, not the cause. Every diagnosis here is a hypothesis until the curve is read over time — a snapshot at the moment of failure cannot distinguish a leak from a legitimate peak. Nothing recommends a product, and a restart that clears the symptom has not diagnosed anything; it has reset the clock.
