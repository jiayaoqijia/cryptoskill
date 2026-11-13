---
name: ac-gpu-and-parallel-compute
description: "Programming parallel hardware productively: warps executing in lockstep and divergence as serialisation, the device memory hierarchy, coalesced access as the dominant lever, occupancy as a scheduling property, kernel launch overhead and fusion, host-to-device transfer as the hidden cost, mixed precision, and the written accelerator record. It explains how parallel throughput hardware behaves and how to reason about its limits; it never recommends a vendor and never promises a speedup. Use when asking \"GPU programming\", \"CUDA\", \"warp divergence\", \"shared memory bank conflict\", \"memory coalescing\", \"occupancy\", \"kernel launch overhead\", \"mixed precision\", \"parallel reduction\", \"why is my GPU kernel slow\". Not for CPU cache hierarchy and locality (ac-memory-layout-and-caches), not for compiler codegen and ABI (ac-compilers-and-abis), not for latency profiling of serial code (ac-performance)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# GPU and parallel compute

## Overview

A GPU is not a fast CPU. It is a throughput machine that trades per-thread latency for massive parallelism, and it rewards programs that are written for its execution model and punishes programs that are not. The punishment is silent: code compiles, runs, and produces correct answers at a tenth of the achievable rate, because the hardware is spending its time waiting — on uncoalesced memory, on divergent branches, on transfers between host and device that no profile of the kernel itself will show.

This skill covers the reasoning needed to write for such hardware: the execution model where warps advance in lockstep and divergence serialises, the memory hierarchy whose slowest level sits behind the fastest, coalescing as the first and largest lever, occupancy as a scheduling property that trades against per-thread resources, launch overhead and fusion, host–device transfer as a cost the profiler must be told to display, and reduced numeric formats that change both speed and results. It is about the reasoning, not about a vendor's API surface.

Primary sources: <https://docs.nvidia.com/cuda/> and <https://www.khronos.org/registry/OpenCL/>.

## When to use

- When writing or reviewing kernels for GPU or other throughput processors.
- When a kernel runs correctly but far below the device's expected throughput.
- When choosing between doing work on host or device.
- When reduced numeric precision is proposed for speed.

## When NOT to use

- For CPU cache lines and single-thread locality (use ac-memory-layout-and-caches).
- For compiler codegen, ABI, and linking (use ac-compilers-and-abis).
- For serial-code latency profiling methodology (use ac-performance).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/execution-model.md` | `software-engineering/execution-model` | Warps in lockstep, divergence as serialisation, and latency hiding. |
| `subskills/memory-hierarchy.md` | `software-engineering/gpu-memory-hierarchy` | Global, shared, and register memory, and what each costs. |
| `subskills/coalescing-and-banks.md` | `software-engineering/coalescing-and-banks` | Contiguous access patterns as the first lever, and bank conflicts. |
| `subskills/occupancy-and-resources.md` | `software-engineering/occupancy-and-resources` | Resident warps as scheduling slack, traded against per-thread state. |
| `subskills/launch-and-fusion.md` | `software-engineering/launch-and-fusion` | Launch overhead, fusion, streams, and the host–device transfer tax. |
| `subskills/numeric-formats.md` | `software-engineering/numeric-formats` | Half and mixed precision, tensor units, and result-changing formats. |
| `subskills/parallel-algorithms.md` | `software-engineering/parallel-algorithms` | Reductions, scans, tiling, and patterns that map to the hardware. |
| `subskills/accelerator-record.md` | `software-engineering/accelerator-record` | The written record: device, numbers, and the transfer ledger. |

## Status and honest limits

Numbers in accelerators move by two orders of magnitude across architectures — a doubling of shared memory per block can invert an occupancy decision made on the previous generation. Every floor and ceiling in this skill is therefore written as a ratio or a measurement to take, never as a constant to remember. Nothing here recommends one vendor's hardware over another's, and the skill deliberately stops at the reasoning layer: API specifics live in vendor documentation, and a kernel that follows every rule here can still be defeated by an access pattern unique to the problem.
