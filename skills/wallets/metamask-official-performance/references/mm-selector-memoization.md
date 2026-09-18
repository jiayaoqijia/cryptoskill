---
title: Selector Memoization (MetaMask)
impact: CRITICAL
tags: reselect, createSelector, memoization, re-renders, redux, cascade
---

# Skill: Selector Memoization

Broken or absent memoization in widely-used selectors is the single highest-impact performance problem in MetaMask Mobile. One broken root selector returns a new reference on **every** Redux dispatch, which makes every dependent selector and `useSelector` consumer believe the data "changed" — cascading into dozens of unnecessary component re-renders. The cost scales **superlinearly** with user data (a power user with 30 accounts / 1000+ transactions feels it on every interaction).

## The tools this codebase already has

- `createSelector` from `reselect` — reference-equality on inputs.
- **`createDeepEqualSelector`** from `app/selectors/util.ts` — `createSelectorCreator(lruMemoize, deepEqual)`. Recomputes only when inputs are **deeply** equal-or-not. Use this when an input selector returns a fresh object/array on every dispatch (very common with controller state slices).

## The patterns, and what they look like here

The pattern taxonomy itself lives in the **`selector-antipatterns`** knowledge file,
installed alongside this skill under `knowledge/`. It is the single source — read it for the
full definition, the worked before/after of each, and the selector-creator decision tree.
This section maps each pattern onto *this* codebase.

| Pattern | How it shows up in Mobile | Fix here |
|---|---|---|
| **Identity / passthrough result** | `createSelector(selectControllerState, (s) => s.things)`, where `selectControllerState` returns the whole controller: that reference changes whenever any field in the controller updates, even when `.things` did not, so the selector recomputes and returns a new ref on every update to that controller | `createDeepEqualSelector`, or narrow the input to the smallest stable slice |
| **New collection in the result function** | `Object.values(...).sort(...)`, `new Set(...flatMap(...))`, `items.filter(...)`, `state.swapsTransactions ?? {}` | `createDeepEqualSelector`, a stable module-level constant for the empty case, or a `resultEqualityCheck` |
| **Mutation in the result function** | `createSelector([getItems], (items) => { items.sort(cmp); return items; })` | copy first — `[...items].sort(cmp)` |
| **Over-broad input** | `state => state`, or a whole controller slice, as an input selector | narrow the input |
| **Unnecessary deep equality** | reaching for `createDeepEqualSelector` on an already-stable slice | plain `createSelector`; see *Don't over-correct* below |

The two that dominate the verified instances below are the first two.

## Verified MetaMask instances

| Selector | File:line | Pattern | Cascade |
|---|---|---|---|
| `selectSwapsTransactions` | `transactionController.ts:294` | `?? {}` new object | quick win, zero risk |
| `selectOrderedInternalAccountsByLastSelected` | `accountsController.ts:139` | plain `createSelector` + `Object.values().sort()` | → `selectLastSelectedEvmAccount`, `selectLastSelectedSolanaAccount` → Bridge `useSortedSourceNetworks`, `Carousel`, `AssetDetails` (×2) |
| `selectInternalEvmAccounts` | `accountsController.ts:83` | plain `createSelector` + `.filter()` | confirmation flows (`AddressFrom`, `AddressList`) |
| `selectRequiredTransactionIds` | `transactionController.ts:98` | plain `createSelector` → `new Set()` | → `selectRequiredTransactions` → `selectRequiredTransactionHashes` |
| `selectRelatedChainIdsByTransactionId` | `transactionController.ts:120` | plain `createSelector` builds two `new Map()` every dispatch | activity/tx views |

## Fix recipes (with verification)

```ts
// selectSwapsTransactions — stable empty constant
const EMPTY_SWAPS: Record<string, unknown> = {};
export const selectSwapsTransactions = createSelector(
  selectTransactionControllerState,
  (state) => state.swapsTransactions ?? EMPTY_SWAPS,
);

// selectOrderedInternalAccountsByLastSelected — deep-equal so unchanged data reuses the ref
export const selectOrderedInternalAccountsByLastSelected = createDeepEqualSelector(
  selectInternalAccountsById,                  // narrower, structural input
  (accounts) => Object.values(accounts).sort(byLastSelectedDesc),
);

// selectInternalEvmAccounts — deep-equal
export const selectInternalEvmAccounts = createDeepEqualSelector(
  selectInternalAccounts,
  (accounts) => accounts.filter((a) => isEvmAccountType(a.type)),
);

// selectRequiredTransactionIds — deep-equal on the already-deep-equalized tx list
export const selectRequiredTransactionIds = createDeepEqualSelector(
  selectTransactions,
  (txs) => new Set(txs.flatMap((tx) => tx.requiredTransactionIds ?? [])),
);
```

**Verify each fix:**
1. `yarn test:unit <selectorFile>` — no regressions.
2. Add/run a Reassure `*.perf-test.tsx` on a top consumer (e.g. an account-list component) → render count drops.
3. React Native DevTools Profiler: reproduce the interaction (account switch) → the cascade of yellow re-renders shrinks.
4. Confirm the selector returns the **same reference** across two dispatches when the underlying data is unchanged.

## How to find more

```bash
# every createSelector — then eyeball the result function
grep -rn "createSelector(" app/selectors --include="*.ts" | grep -v createDeepEqualSelector

# result functions that allocate (high-signal)
grep -rn "=> .*\.\(map\|filter\|sort\|reverse\)\|new Set\|new Map\|Object\.\(values\|keys\|entries\)\|?? {}\|?? \[\]" app/selectors --include="*.ts"

# mutation smell inside selectors
grep -rn "\.sort(\|\.reverse(\|\.push(\|\.splice(" app/selectors --include="*.ts"
```
Escalate severity by one level if the selector is imported in **10+ files**.

## Don't over-correct

- A selector returning a **primitive** (number/string/bool) is fine even if it filters internally — the consumer memoizes on the primitive. (e.g. notification `.filter().length` is wasteful allocation, not a re-render bug — Low.)
- `createDeepEqualSelector` is not free: deep-comparing a huge slice every dispatch can itself be costly. Prefer narrowing the input over deep-equalizing a giant object.

## Related

- [mm-redux-antipatterns.md](mm-redux-antipatterns.md) — `useSelector(x, isEqual)` is the *symptom* of a broken selector; fix the selector, then remove the `isEqual`.
- [mm-selector-cascade.md](mm-selector-cascade.md) — graph-level view: blast radius of one broken root, and sweeping out downstream band-aids after the fix.
- [mm-state-normalization.md](mm-state-normalization.md) — state/selector *shape*: O(1) lookups, parameterized-selector cache thrashing, view-selector consolidation.
- [js-profile-react.md](js-profile-react.md) — prove the re-render reduction.
