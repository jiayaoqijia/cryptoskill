---
title: Unstable Hook Return Values (MetaMask)
impact: CRITICAL
tags: hooks, memoization, re-renders, usememo, reference-stability, cascade
---

# Skill: Unstable Hook Return Values

This is the **non-Redux twin of [mm-selector-memoization.md](mm-selector-memoization.md)**. A custom hook that builds a fresh array/object/function and returns it **without `useMemo`/`useCallback`** hands a new reference to every consumer on **every render**. That new identity invalidates every downstream `useMemo([hookReturn])`, defeating memoization that already exists below it and cascading re-renders through whole lists.

It's insidious because the downstream code *looks* correct — the children are memoized, the lists use `useMemo` — but the root hook quietly invalidates all of it. And it's **not grep-able** the way a selector is: you find it by reading the hook's return path.

## The pattern

```ts
// ❌ new array every render — no useMemo
function useBalanceChanges() {
  const native = getNativeBalanceChange(...);          // BigNumber math, every render
  const tokens = getTokenBalanceChanges(...);
  return { value: [ ...(native ? [native] : []), ...tokens ] };   // fresh ref every time
}
```

```tsx
// consumer's memo is defeated — input identity changes every render
const outgoing = useMemo(() => value.filter(isOutgoing), [value]);   // re-runs every render
// → <BalanceChangeList> useMemo([balanceChanges]) re-sorts every render
// → every <BalanceChangeRow> (keyed by index, not React.memo) re-renders
```

A single parent re-render cascades through the entire list. This is usually the **dominant** cost on a re-render-heavy screen.

## The fix

Stabilize at the source, then memoize the leaves:

```ts
function useBalanceChanges() {
  const value = useMemo(
    () => [ ...(native ? [native] : []), ...tokens ],
    [native, tokens],            // stable identity when inputs unchanged
  );
  return { value };
}
```
Then `React.memo` the row component and give it a **stable key** (`asset.address`/`tokenId`, not `index`). Memoizing the root without memoizing the rows leaves half the cascade; do both.

## Sibling render-phase smells (same file, same fix mindset)

These travel with unstable returns and compound the cascade — look for them while you're in the hook:

- **Side effects / `setState` during render** — a `for` loop in the render body calling `trackEvent(...)` or `setProcessedAssets([...])`. Effects and state updates belong in `useEffect`, not the render phase; in render they trigger extra render passes. **Fix:** move into `useEffect`.
- **O(n²) reduce-with-spread** — `items.reduce((acc, x) => ({ ...acc, [x.id]: x }), {})` rebuilds the whole accumulator each step *and* runs every render. **Fix:** plain assignment in a `useMemo` (`acc[x.id] = x`).
- **Unmemoized array feeding another hook** — a fresh `.filter().map()` passed into `useDisplayNames(...)`/`useAsyncResult(...)` every render (this is also *why* `JSON.stringify`-in-deps band-aids appear — see [mm-hook-dependency-arrays.md](mm-hook-dependency-arrays.md)).

## How to find (read, don't just grep)

Greps narrow the candidates; the confirmation is reading the return path.

```bash
DIR=app/components/UI/<Feature>
# custom hooks, then read each hook's return: does it build [...]/{...}/=> inline without useMemo/useCallback?
grep -rn "^export function use\|^export const use\|return \[\|return {" --include='*.ts*' "$DIR"
# components mapping over a hook's returned array (cascade surface)
grep -rn "\.map(" --include='*.tsx' "$DIR"
# render-phase setState / side effects
grep -rn "set[A-Z][A-Za-z]*(\|trackEvent(" --include='*.ts*' "$DIR"   # then check it's NOT inside useEffect/useCallback
```

For each hook: **does it return a non-primitive built inline, and is that return wrapped in `useMemo`/`useCallback`?** If not, and a consumer depends on it (in deps or via `.map()`), that's the bug.

## Worked example (SimulationDetails)

The **structure** below is verified in the code; the **runtime magnitude** ("dominant cost") is a hypothesis to confirm with the Profiler before treating as fact.

`useBalanceChanges` (`useBalanceChanges.ts`, ~L307: the `balanceChanges` array, returned as `{ value }`) builds a fresh array (re-running the BigNumber math) every render with **no `useMemo`**. Downstream, `SimulationDetails`' `outgoing`/`incoming` filters (`SimulationDetails.tsx:244-245`) and `<BalanceChangeList>`'s `useMemo([balanceChanges])` invalidate every render → `sortBalanceChanges` re-runs → every `<BalanceChangeRow>` (keyed by `index` at `BalanceChangeList.tsx:51`, not memo'd) re-renders, each rendering `AmountPill`/`AssetPill`(+ its own `useSelector`)/`FiatDisplay`. The memos below are all correct; the root hook's unstable return defeats them. (Structure confirmed by reading; whether this is the *dominant* cost needs a Profiler recording — see Verify.)

## Verify

- `console.count('[perf] hook body ran')` in the hook body and `console.count('[perf] re-sort')` in the consumer's `useMemo` — both firing every render confirms the cascade.
- RN DevTools Profiler ("why did this render?"): rows showing "props changed → `balanceChange`" or "parent rendered" across the whole list.
- After the fix: hook body still runs (hooks run every render) but `value` keeps identity → consumer `useMemo`s stop re-running → row commits drop. Prove it with Reassure (`*.perf-test.tsx`).

## Related

- [mm-selector-memoization.md](mm-selector-memoization.md) — the Redux twin (broken `createSelector`)
- [mm-hook-dependency-arrays.md](mm-hook-dependency-arrays.md) — the `JSON.stringify`-in-deps band-aid that unstable arrays cause
- [mm-audit-playbook.md](mm-audit-playbook.md) — the reference-stability audit checklist (this is the non-grep-able class)
- [js-profile-react.md](js-profile-react.md) — confirm the cascade
