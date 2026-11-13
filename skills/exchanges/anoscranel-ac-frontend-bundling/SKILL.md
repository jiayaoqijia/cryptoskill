---
name: ac-frontend-bundling
description: "How front-end code becomes something a browser can load: module resolution and the import graph, code splitting and entry points, tree shaking and dead code, bundle budgets and route-level loading, source maps in production, asset graphs and cache-busting, and the written bundle record. It explains what the build produces and how to keep it small; it never recommends a bundler and never promises a load time. Use when asking \"bundle size\", \"code splitting\", \"tree shaking\", \"lazy load\", \"dynamic import\", \"source map\", \"module resolution\", \"entry point\", \"chunk\", \"why is my bundle so big\", \"import cycle\". Not for Core Web Vitals targets and field data (ac-performance), not for monorepo dependency graphs and remote caches (ac-monorepo-and-build-systems), not for general build hermeticity (ac-monorepo-and-build-systems)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Front-end bundling

## Overview

A bundler takes a graph of imports and produces files a browser can fetch. Between those two ends sit the decisions that decide whether the application loads quickly or slowly: which modules resolve to which files, which code is included by default and which is fetched on demand, which exports are dropped as unused, and how the output is split into cacheable pieces. None of these is a runtime concern; all of them are build-output concerns, and they are where most load-time problems are created.

This skill covers the build output layer: module resolution and the import graph it produces, entry points and splitting, tree shaking and the side effects that defeat it, bundle budgets enforced in CI, source maps and what they cost and leak, and asset handling with cache-busting hashes. The runtime measurement of what users experienced belongs to the performance skill.

Primary source: <https://web.dev/learn>.

## When to use

- When bundle size or load behaviour needs diagnosis and the build output is the suspect.
- When adding code splitting or lazy loading to an application.
- When tree shaking is not removing code that appears unused.
- When setting bundle budgets or wiring source maps for production errors.

## When NOT to use

- For Core Web Vitals measurement and targets (use ac-performance).
- For repo-wide build graphs and remote caching (use ac-monorepo-and-build-systems).
- For runtime profiling of rendering cost (use ac-performance).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/module-resolution.md` | `software-engineering/module-resolution` | How an import becomes a file, and the graph it implies. |
| `subskills/entry-points-and-splitting.md` | `software-engineering/entry-points-and-splitting` | Entry points, chunks, and what loads when. |
| `subskills/tree-shaking-and-side-effects.md` | `software-engineering/tree-shaking-and-side-effects` | Dead-code removal and the patterns that defeat it. |
| `subskills/bundle-budgets.md` | `software-engineering/bundle-budgets` | Size budgets enforced in CI and what they should measure. |
| `subskills/source-maps.md` | `software-engineering/source-maps` | Debuggable production output without leaking source. |
| `subskills/asset-graphs-and-hashing.md` | `software-engineering/asset-graphs-and-hashing` | Referencing assets so caches can be trusted. |
| `subskills/bundle-record.md` | `software-engineering/bundle-record` | The written record of output shape and its budgets. |

## Status and honest limits

Bundlers differ in defaults and in the exact resolution algorithm, and the ecosystem moves faster than any summary; the concepts here are stable across tools, but the flag that implements one is not. Nothing here recommends a bundler, and a bundle that measures small can still load slowly when the entry point is reached on a slow first request — the build output is one input among several, and the field data remains the judge.
