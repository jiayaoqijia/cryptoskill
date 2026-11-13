---
name: ac-low-level-io-and-syscalls
description: "The boundary between a program and the kernel: syscall cost and batching, buffered versus direct I/O, memory-mapped files and when they beat read, epoll and readiness-based event loops, io_uring and submission queues, vectored I/O, blocking versus non-blocking sockets, and the written I/O record. It explains what crossing the kernel boundary costs and how to cross it fewer times; it never recommends a framework and never promises a throughput. Use when asking \"syscall overhead\", \"read vs mmap\", \"direct I/O\", \"epoll\", \"io_uring\", \"zero copy\", \"sendfile\", \"vectored I/O\", \"blocking versus non-blocking\", \"why is reading this file slow\", \"batching syscalls\". Not for application caching (ac-caching-and-invalidation), not for distributed replication (ac-distributed-state-and-replication), not for file format layout (ac-binary-formats)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Low-level I/O and syscalls

## Overview

Every read, write, or socket operation crosses a boundary: the kernel mediates access to files, devices, and the network, and each crossing has a fixed cost independent of the bytes moved. A program that reads a file in one-megabyte chunks pays the same number of crossings as one reading in four-kilobyte chunks, at a fraction of the boundary overhead — and a program that reads byte-by-byte through a buffered wrapper may pay no boundary at all, at the cost of an extra copy.

This skill covers the boundary's mechanics: what a syscall costs, when direct I/O avoids the page cache, what mmap buys and what it gives up, how readiness-driven event loops work, what submission-queue interfaces change, and why vectored and zero-copy interfaces exist. The buffer cache and the syscall boundary are design surfaces; the application-level cache is a different skill.

Primary sources: <https://man7.org/linux/man-pages/man2/mmap.2.html> and <https://man7.org/linux/man-pages/man7/epoll.7.html>.

## When to use

- When a workload is I/O-bound and the crossing count, not the byte count, is the bottleneck.
- When choosing between read, mmap, and direct I/O for a large dataset.
- When an event loop's readiness model matters to correctness or latency.
- When zero-copy or vectored interfaces are under consideration.

## When NOT to use

- For application-level caching and invalidation (use ac-caching-and-invalidation).
- For replication and consistency across machines (use ac-distributed-state-and-replication).
- For the byte-level layout of the data itself (use ac-binary-formats).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/syscall-cost-and-batching.md` | `software-engineering/syscall-cost-and-batching` | The fixed cost of the boundary and amortizing it. |
| `subskills/page-cache-and-direct-io.md` | `software-engineering/page-cache-and-direct-io` | The buffer cache, its sharing, and paying to skip it. |
| `subskills/mmap-versus-read.md` | `software-engineering/mmap-versus-read` | Mapping a file versus reading it, and each one's failure mode. |
| `subskills/readiness-and-event-loops.md` | `software-engineering/readiness-and-event-loops` | epoll, edge versus level triggering, and the thundering herd. |
| `subskills/submission-queues.md` | `software-engineering/submission-queues` | io_uring-style submission and completion for dense I/O. |
| `subskills/vectored-and-zero-copy.md` | `software-engineering/vectored-and-zero-copy` | Scatter-gather and the copies an interface can avoid. |
| `subskills/blocking-and-nonblocking.md` | `software-engineering/blocking-and-nonblocking` | What blocking promises, and what non-blocking requires in exchange. |
| `subskills/io-record.md` | `software-engineering/io-record` | The written record: I/O model choices and their measurements. |

## Status and honest limits

Syscall costs and cache behaviour are kernel- and hardware-specific, and interfaces differ across platforms — what is a submission queue on one system is an async handle on another, with different semantics for cancellation and ordering. The page cache is shared state the program does not control, so measurements of cached I/O are measurements of a warm machine. Nothing here recommends a specific interface, and any I/O-model decision carries its platform and kernel version in the record, because the numbers that justify it do not transfer.
