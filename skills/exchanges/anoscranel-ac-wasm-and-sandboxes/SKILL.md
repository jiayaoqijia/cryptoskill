---
name: ac-wasm-and-sandboxes
description: "Running untrusted or portable code inside a boundary: WebAssembly's execution model and linear memory, the host boundary and what crosses it, sandbox isolation and capability scoping, embedding and host function design, compiling targets and their trade-offs, side channels and the limits of the boundary, and the written sandbox record. It explains how a sandboxed runtime contains execution and where it leaks; it never recommends a runtime and never declares a sandbox unbreakable. Use when asking \"WebAssembly\", \"WASM\", \"sandbox untrusted code\", \"linear memory\", \"host function\", \"wasm module embedding\", \"guest and host\", \"capability-based sandbox\", \"plugin runtime\", \"sandbox side channel\", \"compile to wasm\", \"wasm performance overhead\". Not for browser execution of trusted application code (ac-frontend-bundling), not for container security (ac-security-standards), not for VM and OS-level isolation."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# WASM and sandboxes

## Overview

Some code must run without being trusted: third-party plugins, user-supplied rules, portable modules shipped across environments. A sandbox runtime gives that code a place to execute with a boundary around it — a linear memory it owns, an instruction set it cannot escape by construction, and a narrow, explicit interface to the host. WebAssembly is the dominant such runtime, and its model is the reference case: memory is a separate region the host can inspect but the guest cannot pointer past, and every host capability arrives through a declared function the host chose to provide.

The craft is the boundary. A sandbox contains what its interface permits and nothing more; each host function is a policy decision about what the guest may reach, and the aggregate surface is the real security posture. This skill covers that machinery: the memory model, the host boundary, capability scoping, embedding decisions, and the honest limits — side channels and resource consumption sit outside the model and must be handled explicitly.

Primary sources: <https://webassembly.github.io/spec/> and <https://llvm.org/docs/>.

## When to use

- When running plugins, user-defined logic, or third-party modules.
- When designing the host interface of an embedded runtime.
- When a portable execution target is under evaluation.
- When auditing what a sandboxed guest can reach.

## When NOT to use

- For browser bundling of your own application's frontend (use ac-frontend-bundling).
- For container and OS-level isolation standards (use ac-security-standards).
- For hypervisor and VM isolation design (not covered; different boundary class).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/linear-memory-model.md` | `software-engineering/linear-memory-model` | One memory, no pointers out, and what the boundary guarantees. |
| `subskills/host-boundary-functions.md` | `software-engineering/host-boundary-functions` | The explicit interface where guest code calls a host that chose to be reachable. |
| `subskills/capability-scoping.md` | `software-engineering/capability-scoping` | Granting capabilities per guest rather than ambient authority. |
| `subskills/embedding-and-orchestration.md` | `software-engineering/embedding-and-orchestration` | Instantiation, lifetimes, and managing many guests in one process. |
| `subskills/compilation-targets.md` | `software-engineering/compilation-targets` | Compiling to the sandbox and the trade-offs each toolchain makes. |
| `subskills/side-channels-and-limits.md` | `software-engineering/side-channels-and-limits` | What the boundary does not cover: timing, resources, and speculative leakage. |
| `subskills/sandbox-record.md` | `software-engineering/sandbox-record` | The written record: surface, capabilities, and the audits behind them. |

## Status and honest limits

A sandbox's guarantee is about the instruction stream, not the environment around it: spec-conforming execution prevents memory escape but says nothing about timing side channels, resource exhaustion, or the correctness of the host functions themselves. Real deployments are broken most often at the host boundary — an over-broad function or a trusting host — and least often at the core runtime. Nothing here declares a configuration safe; a sandbox is a reduction of attack surface, evidence about which must be recorded, not assumed.
