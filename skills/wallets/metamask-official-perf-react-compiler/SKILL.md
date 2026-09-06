---
name: perf-react-compiler
description: >
  React Compiler in the Extension UI: what it optimizes, where it bails out, and when manual
  memoization is still needed. Use when deciding whether `useMemo`, `useCallback` or
  `React.memo` are still required, reviewing reflexive memoization, or working out why a
  component isn't optimized. Dependency arrays go to `perf-hooks-effects`.
base: true
---
