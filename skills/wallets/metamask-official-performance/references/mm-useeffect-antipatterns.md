---
title: useEffect Lifecycle Anti-Patterns (MetaMask)
impact: HIGH
tags: useEffect, setState, cleanup, AbortController, unmount, memory-leaks
---

# Skill: useEffect Lifecycle Anti-Patterns

> **Scope.** The platform-agnostic taxonomy — unstable dependency identity, wrong
> dependencies, derived state via effect, cascading effect chains, missing timer cleanup,
> uncancelled async — is the single source in the **`effect-antipatterns`** knowledge file,
> installed alongside this skill under `knowledge/`. This file is the MetaMask Mobile
> instance of its lifecycle half: the verified instances, the repo's own idioms, and the
> fix recipes.

[mm-hook-dependency-arrays.md](mm-hook-dependency-arrays.md) covers *when* effects re-run (the deps side). This file covers what goes wrong **inside and after** the effect: state derived in effects instead of render, effects chained off each other's setState, async work that outlives the component, and missing cleanup. These patterns cause extra render passes, memory leaks, and the classic "setState on unmounted component" warnings — and they're invisible to selector/re-render sweeps.

## Pattern — derived state via useEffect + setState ("you might not need an effect")

```tsx
// ❌ two render passes per change: render → effect → setState → render again
const [visibleTokens, setVisibleTokens] = useState([]);
useEffect(() => {
  setVisibleTokens(tokens.filter((t) => !t.hidden));
}, [tokens]);

// ✅ derive during render — one pass, no state to drift out of sync
const visibleTokens = useMemo(() => tokens.filter((t) => !t.hidden), [tokens]);
```

If a value is computable from props/state/store, compute it in render (memoize only if it's expensive or feeds a memoized child). State + effect is for *synchronizing with something external*, not for derivation.

## Pattern — cascading effect chains

```tsx
// ❌ effect A sets state → triggers effect B → sets state → triggers effect C…
useEffect(() => { setAccount(deriveAccount(accounts, selected)); }, [accounts, selected]);
useEffect(() => { setBalances(deriveBalances(account)); }, [account]);
useEffect(() => { setFiat(deriveFiat(balances, rate)); }, [balances, rate]);
// 4 render passes for one upstream change, and the intermediate renders show stale combinations
```

**Fix:** collapse the chain into render-time derivation (one `useMemo` per step, or one for the lot). Each link in a setState-chain is a full extra render pass *and* a window where the UI shows an inconsistent intermediate state.

## Pattern — async work that outlives the component

```tsx
// ❌ fetch resolves after unmount (or after the input changed) → setState on dead component / stale data wins
useEffect(() => {
  fetchTokenMetadata(address).then((meta) => setMetadata(meta));
}, [address]);
```

Two equivalent fixes — pick one and use it consistently:

```tsx
// ✅ cancelled flag — cheapest, works for any promise
useEffect(() => {
  let cancelled = false;
  fetchTokenMetadata(address).then((meta) => {
    if (!cancelled) setMetadata(meta);
  });
  return () => { cancelled = true; };
}, [address]);

// ✅ AbortController — also cancels the network request itself (RN fetch supports `signal`)
useEffect(() => {
  const controller = new AbortController();
  fetch(url, { signal: controller.signal })
    .then((r) => r.json())
    .then(setData)
    .catch((e) => { if (e.name !== 'AbortError') setError(e); });
  return () => controller.abort();
}, [url]);
```

The cancelled flag prevents the *setState*; AbortController additionally stops the request from consuming bandwidth/battery. The race-condition variant (stale response overwriting fresh data when `address` changes quickly) is fixed by the same cleanup — the old effect's closure is cancelled before the new one runs.

**Codify, don't copy-paste** (from the extension performance audit): once a repo has three hand-rolled cancelled flags, extract shared hooks — `useIsMounted()`, `useAbortableEffect(fn, deps)` (effect receives a signal), `useEventListener(target, event, handler)` (auto-removes on unmount) — so cleanup is the default, not per-site diligence.

## Pattern — missing cleanup for timers / subscriptions / listeners

```tsx
// ❌ each mount adds another interval/listener; none are removed
useEffect(() => {
  const id = setInterval(refreshGasEstimate, 15000);
  emitter.on('update', onUpdate);
}, []);

// ✅ every subscription returns its teardown
useEffect(() => {
  const id = setInterval(refreshGasEstimate, 15000);
  emitter.on('update', onUpdate);
  return () => { clearInterval(id); emitter.off('update', onUpdate); };
}, []);
```

Leaked intervals keep firing (and keep dispatching) forever; leaked listeners hold the closure — and everything it captured — out of garbage collection. See [js-memory-leaks.md](js-memory-leaks.md) for hunting these in a running app, and [mm-streaming-realtime.md](mm-streaming-realtime.md) for subscription lifecycles tied to visibility.

## Pattern — regular variable where a ref is needed

```tsx
// ❌ reset to false on every render — the guard never works
let hasLoggedImpression = false;
useEffect(() => {
  if (!hasLoggedImpression) { logImpression(); hasLoggedImpression = true; }
});

// ✅ useRef persists across renders without triggering them
const hasLoggedImpression = useRef(false);
```

Any mutable flag/cache/previous-value that must survive re-renders but shouldn't cause them belongs in a ref, not a closure variable (and not state).

## Pattern — large objects captured in effect closures

An effect (or its cleanup) that closes over a large object — full token lists, raw API payloads — pins that object in memory for as long as the subscription lives. Extract the fields you need into locals *before* the closure, or read through a ref, so the big object can be collected.

## How to find

```bash
# setState-from-effect derivation candidates (review hits — some are legitimate syncs)
grep -rn -A3 "useEffect(" app --include="*.tsx" | grep -B1 "set[A-Z]" | grep -v ".test."

# fetch/promises in effects with no signal/cancelled handling nearby
grep -rn -A6 "useEffect(" app --include="*.ts*" | grep -E "fetch\(|\.then\(" | grep -v "signal\|cancelled\|abort" | grep -v ".test."

# intervals/timeouts/listeners inside effects — then eyeball for a `return () =>` teardown
grep -rn "setInterval\|setTimeout\|addEventListener\|\.on(" app --include="*.ts*" | grep -v ".test." | grep -v "clear\|remove\|off("
```

## Verify

- React DevTools highlight-updates: the derive-in-render fix removes the double render pass on the affected component.
- No "setState on unmounted component" / no stale-data flash when rapidly switching the input (account/network) that drives the effect.
- For cleanup fixes: navigate to the screen and back N times → timer/listener count stays flat (see [js-memory-leaks.md](js-memory-leaks.md)).

## Don't over-correct

- Effects that *synchronize with external systems* (subscriptions, navigation, imperative APIs) are the legitimate use — don't mechanically rewrite every effect as `useMemo`.
- An async effect whose component provably never unmounts mid-flight (e.g. root-level, app lifetime) doesn't need a cancelled flag — but say so in review rather than assuming.
- Don't wrap trivial derivations in `useMemo` while de-effecting — plain expressions are fine until profiling or a memoized child says otherwise.

## Related

- [mm-hook-dependency-arrays.md](mm-hook-dependency-arrays.md) — the deps side: JSON.stringify, inline literals, stale closures
- [js-memory-leaks.md](js-memory-leaks.md) — measuring leaks the missing cleanups cause
- [mm-streaming-realtime.md](mm-streaming-realtime.md) — subscription setup/teardown for real-time screens
- [mm-unstable-hook-return.md](mm-unstable-hook-return.md) — unstable hook returns that make effects re-run
