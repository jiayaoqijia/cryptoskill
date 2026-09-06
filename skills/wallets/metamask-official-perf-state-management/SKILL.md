---
name: perf-state-management
description: >
  Extension Redux state and selectors: reducer purity, keeping non-serializable values out of
  the store, normalization, Immer, batching, identity output selectors. Use when components
  re-render on unrelated state changes, a selector returns a fresh identity every call, or
  state is mutated in a reducer. Memoization goes to `perf-rendering`.
base: true
---
