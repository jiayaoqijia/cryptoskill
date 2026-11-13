---
name: ac-compilers-and-abis
description: "What a compiler and an ABI actually decide: compilation phases and where diagnostics come from, the distinction between language semantics and target behaviour, undefined behaviour and what it licenses the optimizer to do, the ABI as a binding contract for layout and calls, name mangling and symbol resolution, linking static versus dynamic and symbol visibility, and the written toolchain record. It explains how translation and linkage constrain code; it never recommends a compiler and never promises a binary outcome. Use when asking \"undefined behavior\", \"ABI compatibility\", \"name mangling\", \"static versus dynamic linking\", \"symbol visibility\", \"linker errors\", \"compilation phases\", \"calling convention\", \"why does this work in debug but not release\", \"why is this struct size different\". Not for build-system wiring and caching (ac-monorepo-and-build-systems), not for language runtime and concurrency (ac-async-and-concurrency), not for binary format design on disk (ac-binary-formats)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Compilers and ABIs

## Overview

Between source and a running program sit two contracts most engineers meet only when they break. The first is the compiler: translation proceeds in phases, and where an error surfaces determines which one fired — a diagnostic at parse time, at semantic analysis, or a misbehaviour at runtime that no diagnostic caught. The second is the ABI: the binary-level agreement on how types are laid out, how functions receive arguments, and how symbols are named, shared across separately compiled code.

The practical consequences surface as puzzles that seem like compiler bugs. A program that works in debug and breaks in release, or a struct whose size differs between modules, is usually meeting an ABI interpretation difference or an undefined behaviour the optimizer exploited. This skill explains the machinery behind those outcomes and how to read them as evidence about the contracts.

Primary sources: <https://en.cppreference.com/w/c/language.html> and <https://llvm.org/docs/>.

## When to use

- When the same source behaves differently across build modes or modules.
- When linking separately compiled code and symbols or layouts disagree.
- When diagnosing whether an unexpected runtime outcome traces to undefined behaviour.
- When making a shared library's surface stable across versions.

## When NOT to use

- For build wiring, caching, and target graphs (use ac-monorepo-and-build-systems).
- For language concurrency and async runtimes (use ac-async-and-concurrency).
- For on-disk or on-wire byte layout (use ac-binary-formats).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/compilation-phases.md` | `software-engineering/compilation-phases` | From preprocessing to linking, and which phase produces which diagnostic. |
| `subskills/semantics-versus-target.md` | `software-engineering/semantics-versus-target` | What the language guarantees versus what the target makes fast or slow. |
| `subskills/undefined-behaviour.md` | `software-engineering/undefined-behaviour` | What UB licenses the optimizer to do, and how to detect reliance on it. |
| `subskills/abi-as-contract.md` | `software-engineering/abi-as-contract` | Layout, calling convention, and symbol naming as a binding agreement. |
| `subskills/name-mangling-and-symbols.md` | `software-engineering/name-mangling-and-symbols` | How overloaded names become symbols, and how resolution finds them. |
| `subskills/linking-models.md` | `software-engineering/linking-models` | Static and dynamic linkage, visibility, and what breaks at load time. |
| `subskills/toolchain-record.md` | `software-engineering/toolchain-record` | The written record: toolchain versions, flags, and ABI decisions. |

## Status and honest limits

Compiler behaviour and optimization decisions are implementation-specific and change between versions; this skill explains the categories, not any one compiler's current behaviour. The UB space is the largest honest limit — a list of examples cannot bound what optimizers may assume, and the only sound discipline is to treat any UB diagnosis as a licence the code granted, to be removed rather than reasoned around. Nothing here recommends a toolchain, and every toolchain-sensitive claim is only meaningful with the version attached.
