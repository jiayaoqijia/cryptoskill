---
name: perf-hooks-effects
description: >
  Extension UI hooks and effects: when not to use `useEffect`, dependency arrays, why
  `JSON.stringify` deps are never the fix, cascading effects, `AbortController` cleanup. Use
  when an effect loops or fires every render, deps are stringified to force equality, or state
  lands after unmount. Rendering goes to `perf-rendering`.
base: true
---
