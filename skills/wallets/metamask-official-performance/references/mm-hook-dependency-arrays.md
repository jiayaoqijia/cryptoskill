---
title: Hook Dependency Arrays (MetaMask)
impact: HIGH
tags: useEffect, useMemo, useCallback, dependencies, JSON.stringify
---

# Skill: Hook Dependency Arrays

Dependency arrays decide when `useEffect`/`useMemo`/`useCallback` re-run. The most common MetaMask problem is **`JSON.stringify` inside a dependency array** — it runs a synchronous serialization on every render just to compute the dependency key, which is both expensive and a sign the upstream reference is unstable.

## Pattern — `JSON.stringify` in deps

```ts
// ❌ serializes (possibly large) data on EVERY render to build the dep key
const decimals = useAsyncResultOrThrow(
  () => fetchAllErc20Decimals(addresses, clientId),
  [JSON.stringify(addresses)],
);
useEffect(() => { /* ... */ }, [JSON.stringify(params)]);
```

**Why it's wrong:** the whole point of a dep array is a cheap identity check. `JSON.stringify(addresses)` on an array of token addresses runs every render — and in `useBalanceChanges` it runs **3×** per render. For a power user reviewing a complex transaction, that's on every dispatch during the approval flow.

**Verified instances:** `useBalanceChanges.ts` (3×: lines ~262/267/276), `useSimulationMetrics.ts:113`, `usePolling.ts:42`.

**Fix — stabilize the reference upstream, then depend on it directly:**
```ts
// Make the array reference stable based on what actually changes its contents
const addresses = useMemo(
  () => deriveErc20Addresses(account, chainId),
  [account, chainId],
);
// now depend on the stable ref — no per-render stringify
const decimals = useAsyncResultOrThrow(
  () => fetchAllErc20Decimals(addresses, clientId),
  [addresses, clientId],
);
```
If you truly only have an unstable array and can't stabilize it, a stable primitive key is still cheaper computed once: `const key = useMemo(() => addresses.join(','), [addresses])` — but prefer fixing the source.

## Pattern — object/array literal created inline in deps

```ts
// ❌ new object every render → effect runs every render (or infinite loop)
useEffect(() => { ... }, [{ id: user.id }]);
useMemo(() => compute(opts), [{ a, b }]);
```
**Fix:** depend on the primitives (`[user.id]`) or a memoized object.

## Pattern — `useMemo`/`useCallback` with wrong deps

```ts
// ❌ empty deps but reads state → stale closure
const onPress = useCallback(() => doThing(count), []);   // count frozen at first render
// ❌ empty deps but "uses" values → should be a module constant
const config = useMemo(() => ({ a: 1, b: 2 }), []);      // just hoist it out
```
**Fix:** include the values you read; or if there are genuinely none, move the constant outside the component.

> **Note:** the repo's ESLint config does **not** enable `react-hooks/exhaustive-deps`, so missing-dep bugs are **not** caught automatically — review deps by hand.

## How to find

```bash
# JSON.stringify used as / inside a dependency
grep -rn "\[JSON.stringify\|, JSON.stringify" app --include="*.ts" --include="*.tsx" \
  | grep -v ".test." | grep -vi "ChartAssets\|ChartTemplate"

# inline object/array literal in a dep array (heuristic)
grep -rn "}, \[{ \|}, \[\[" app --include="*.ts" --include="*.tsx" | grep -v ".test."
```
For each hit, ask: *does this dependency change identity every render?* If yes, stabilize it.

## Verify

- React Native DevTools "why did this render?" should stop citing the effect/memo's dependency.
- Add a `console.count` (temporarily) in the effect — it should fire only when the real input changes, not every render.

## Don't over-correct

- Don't add `useMemo`/`useCallback` everywhere — only where profiling shows wasted work or a referenced child is memoized. Cheap computations don't need memoizing (the React Compiler also handles many cases on opted-in paths).
- A `JSON.stringify` in a **non-hot** path (rare effect, small object) is acceptable; prioritize hot render paths.

## Related

- [js-react-compiler.md](js-react-compiler.md) / [mm-react-compiler.md](mm-react-compiler.md) — automatic memoization on opted-in paths
- [js-concurrent-react.md](js-concurrent-react.md) — defer expensive derived work
