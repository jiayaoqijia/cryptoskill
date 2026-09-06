---
title: Redux & useSelector Anti-Patterns (MetaMask)
impact: HIGH
tags: redux, useSelector, isEqual, re-renders, real-time, local-state
---

# Skill: Redux & useSelector Anti-Patterns

Redux is MetaMask's committed architecture — this skill is about using it correctly, **not** replacing it. Three patterns cause avoidable re-renders.

## Pattern 1 — `useSelector(selector, isEqual)` as a band-aid

```ts
// ❌ runs a lodash deep comparison on EVERY dispatch to decide whether to re-render
const pendingApprovals = useSelector(selectPendingApprovals, isEqual);
const tokenBalances   = useSelector(selectContractBalances, isEqual);
```

**Why it's wrong:** `isEqual` is a symptom. The component re-renders falsely because the **selector** returns a new reference each call, so someone reached for deep equality at the consumer to suppress it. But now an O(n) deep compare runs on every dispatch, every frame — during high-stakes flows (approval modals, confirmations).

**Verified instances (6 files):** `useMusdConversion.ts`, `PermissionApproval.tsx`, `useApprovalRequest.ts`, `useTokenBalancesController.ts`, `Views/AccountPermissions/AccountPermissions.tsx`, `Views/confirmations/hooks/useApprovalFlow.ts`.

**Fix:** make the selector return a stable reference (see [mm-selector-memoization.md](mm-selector-memoization.md)), then **remove** the `isEqual` argument. If a stable selector genuinely needs structural equality at the consumer, prefer `shallowEqual` from `react-redux` over lodash `isEqual`.

```ts
const pendingApprovals = useSelector(selectPendingApprovals); // selector now memoized
```

## Pattern 2 — Inline `useSelector(state => state.x)` bypassing named selectors

```ts
// ❌ no memoization, no reuse, no types; re-renders on any change to that slice
const browserTabs = useSelector((state: RootState) => state.browser.tabs);
const browserTabs = useSelector((state: any) => state.browser.tabs); // also drops type safety
```

**Verified instances:** `MultichainTransactionListItem.tsx:48`, `useNavigateToCardPage.tsx:42`, `useGoToPortfolioBridge.ts:25` (3 files).

**Why it's wrong:** an inline accessor returning an array/object hands a fresh reference to the consumer whenever that slice changes (and defeats reuse/memoization across the app). For derived data it's worse — `useSelector(s => s.items.filter(...))` allocates every render.

**Fix:** create a named selector in `app/selectors/`:
```ts
// selectors/browser.ts
export const selectBrowserTabs = (state: RootState) => state.browser.tabs;
// component
const browserTabs = useSelector(selectBrowserTabs);
```
For derived data, make it a memoized `createSelector`/`createDeepEqualSelector`.

## Pattern 3 — Transient / real-time data in Redux

```ts
// ❌ dispatching high-frequency data into the global store
socket.on('price', (p) => dispatch(setPrice(p)));            // many/sec → global re-renders
setInterval(() => dispatch(updateProgress(...)), 16);        // animation state in Redux
```

**Why it's wrong:** every dispatch flows through the whole store and every subscribed `useSelector`. Real-time/transient UI state (animation progress, modal open/closed, live prices, loading spinners) does not belong in Redux.

**Fix — keep it local:**
- Component-local UI state → `useState` / `useRef`.
- Animation state → Reanimated `useSharedValue` (UI thread, zero React re-renders) — see [mm-layout-animations.md](mm-layout-animations.md).
- Real-time streams → a local store/ref or direct UI update; write to Redux only when you need to persist (e.g. on app background).

> **Do NOT** introduce Jotai/Zustand/etc. The principle is "transient state ≠ Redux," and the destination is React-local state or shared values — not a new library.

## How to find

```bash
# isEqual band-aids
grep -rn "useSelector(.*isEqual)" app --include="*.ts" --include="*.tsx" | grep -v ".test."

# inline selectors hitting raw state
grep -rn "useSelector((state" app --include="*.tsx" | grep -v ".test." | grep -E "=> *state\.[a-zA-Z]+\.[a-zA-Z]+\)?$"

# dispatch on a timer / socket / listener
grep -rn "dispatch(" app --include="*.ts" --include="*.tsx" | grep -v ".test." \
  | grep -iE "setInterval|setTimeout|\.on\(|addEventListener|socket"
```

## Verify

- After removing `isEqual`: React Native DevTools shows the consumer no longer re-renders on unrelated dispatches.
- After de-Reduxing real-time data: no Redux action fires on each tick/message (check Redux DevTools / logging); FPS holds during the stream.

## Related

- [mm-selector-memoization.md](mm-selector-memoization.md) — the upstream fix for Pattern 1
- [mm-context-performance.md](mm-context-performance.md) — the Context equivalent of over-broad subscriptions
- [js-profile-react.md](js-profile-react.md) — confirm the re-render reduction
