---
title: React Compiler (MetaMask)
impact: HIGH
tags: react-compiler, memoization, babel, app-wide
---

# Skill: React Compiler in MetaMask

React Compiler auto-memoizes components, callbacks, and computed values at build time — removing most of the need for manual `React.memo`/`useMemo`/`useCallback`. It runs **app-wide** in this repo (metamask-mobile#31171 enabled v1.0.0 app-wide), wired through `babel.config.js`.

## Current state (verified)

- `babel-plugin-react-compiler`, `react-compiler-runtime`, and `eslint-plugin-react-compiler` are installed.
- ESLint: `react-compiler/react-compiler: 'warn'` is enabled.
- `babel.config.js`: the `react-compiler` plugin runs **first** and applies to every file, with no path allowlist and no `target` override, so the plugin's own default, `target: '19'`, applies. It's disabled under Jest, to avoid a `jest.mock` hoisting conflict with the compiler's injected `_c` helper:
  ```js
  // scripts/react-compiler.js
  const isTestEnv = process.env.NODE_ENV === 'test';
  const reactCompilerBabelConfig = isTestEnv ? [] : [reactCompilerPlugin];
  ```
  Set `REACT_COMPILER_LOG_FAILURES=true` to attach a logger that appends every `CompileError`/`CompileSkip` event to a git-ignored `react-compiler.log`. Without it, the compiler keeps its quiet default (no logger, no bailout output).
- `react-native-worklets/plugin` must remain **last** in the plugin list. It compiles `'worklet'` directives. `react-native-reanimated/plugin` is reanimated v4's deprecated alias for it.

## Fix a component the compiler skips

The compiler already runs app-wide (see above). There's no allowlist to edit. When a component isn't picking up the compiler's memoization:

1. **Check for Rules-of-React violations first.** The compiler silently skips
   components that break the rules (safe, but you lose the optimization).
   Surface them with the already-installed ESLint plugin:
   ```bash
   yarn eslint <path>   # react-compiler/react-compiler warnings = what the compiler would skip
   ```
   (The standalone `react-compiler-healthcheck` CLI gives a repo-wide count, but
   it isn't installed; the ESLint plugin runs the same Rules-of-React checks.)
2. **Clear Metro's cache** — it caches compiled output aggressively:
   ```bash
   yarn watch:clean
   ```
3. **Verify:** in React DevTools, optimized components show a **`Memo ✨`** badge. You can also confirm `'use no memo'` isn't silently opting a component out.

## What it does / doesn't do

- **Does:** auto-memoize components and hook values that follow the Rules of React; reduce cascading re-renders.
- **Doesn't:** fix bad patterns. It optimizes *correct* code. A broken selector still returns new refs — the compiler can't save you. Fix [mm-selector-memoization.md](mm-selector-memoization.md) first.
- **Class components** are not optimized.

## Interaction with manual memoization

You can gradually drop hand-written `useMemo`/`useCallback`/`React.memo` once the compiler is verified working on a path, but do it deliberately and re-measure. Under Jest, and on any file carrying `'use no memo'`, the compiler doesn't run, so manual memoization still matters there.

**Exception — effect dependencies.** Keep any `useMemo`/`useCallback` whose output is used as a `useEffect` dependency, here or in a consumer: the compiler's memoization is not guaranteed to match the manual strategy, and a mismatch causes over/under-firing of effects or infinite loops — a correctness change, not a perf tweak. Official guidance is to leave existing manual memoization in place and only omit it in *new* code ([reactwg/react-compiler#16](https://github.com/reactwg/react-compiler/discussions/16)).

## What breaks compilation (it will skip the component)

- Mutating props or state during render.
- Side effects during render (e.g. incrementing a module variable).
- Other Rules-of-React violations flagged by the ESLint plugin / healthcheck.

Fix the ESLint `react-compiler` warnings on a path to get it compiling.

## Don't

- Don't assume there's a path list to edit. The compiler applies app-wide, and the only files it skips are under Jest or carrying `'use no memo'`.
- Don't assume the compiler targets React 18. `scripts/react-compiler.js` sets no `target` option, so the plugin's default, `target: '19'`, applies.
- Don't reorder `react-native-worklets/plugin` away from last in the plugin list.

## Related

- [js-react-compiler.md](js-react-compiler.md) — upstream reference on how the compiler transforms code
- [mm-react-compiler-error-triage.md](mm-react-compiler-error-triage.md) — triaging compiler errors (`Todo`/unsupported vs actionable), `panicThreshold` ratcheting, and measuring real coverage
- [mm-selector-memoization.md](mm-selector-memoization.md) — fix data-layer re-renders the compiler can't
