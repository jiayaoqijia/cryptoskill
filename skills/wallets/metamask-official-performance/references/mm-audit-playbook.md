---
title: Audit & Review Playbook (MetaMask)
impact: HIGH
tags: audit, code-review, grep, severity, checklist
---

# Skill: Audit & Review Playbook

For reviewing a PR/diff or auditing a file, component, or feature. Output: findings with `file:line`, severity, and a link to the fix guide.

## Mode

- **Targeted** (single file / component / small diff): read the files and report concrete findings with `file:line`.
- **Broad** (whole feature / repo): run the grep sweeps below and triage hits; don't read everything.

Always: **measure before asserting impact** where feasible, and respect the guardrails at the bottom (don't over-flag).

## Severity rubric

- **Critical** — cascading re-renders / broken memoization in a widely-used selector; unbounded list with no virtualization; startup-path cost.
- **High** — local but frequent re-renders; JS-thread layout animation; `isEqual` band-aids; lodash main-package imports; missing list perf props on growing data.
- **Medium** — latent risk, less-traveled path; inline `useSelector(state=>state.x)`.
- **Low** — allocation waste with no re-render impact (e.g. `.filter().length`), style nits.

Escalate one level if a selector/component is used in 10+ files.

## Grep sweeps

> **Scope to the suspect dir when auditing one feature** — set `DIR=app/components/UI/<Feature>` and replace `app` with `$DIR` below. Each row leads with a **detection recipe** (how to find the pattern anywhere); the global `file:line` instances are an appendix at the bottom and go stale — don't rely on them when auditing a specific feature.

### Eager / redundant work on mount → [mm-eager-work-on-mount.md](mm-eager-work-on-mount.md)
The #1 "opening a screen is slow" cause, and the one a re-render/selector sweep misses. Run this FIRST for any open/navigation-TTI complaint.
```bash
grep -rn "PagerView\|Carousel\|TabView\|ScrollView horizontal" app --include="*.tsx" | grep -v ".test."   # mounts all children?
grep -rn "use[A-Z][A-Za-z]*\(Data\|Query\|Fetch\|Market\|Prices\)" app --include="*.tsx" | grep -v ".test."  # fetch hook per tab/item?
grep -rn "enabled" app --include="*.ts*" | grep -v ".test."   # an enabled/isActive gate that exists but isn't passed at the call site
```
Read the call sites: is a data hook running for tabs/pages/items that aren't visible? An `enabled` prop that the hook accepts but the call site omits is the bug.

### Selectors → [mm-selector-memoization.md](mm-selector-memoization.md)
```bash
grep -rn "createSelector(" app/selectors --include="*.ts" | grep -v createDeepEqualSelector
grep -rn "=> .*\.\(map\|filter\|sort\|reverse\)\|new Set\|new Map\|Object\.\(values\|keys\|entries\)\|?? {}\|?? \[\]" app/selectors --include="*.ts"
grep -rn "\.sort(\|\.reverse(\|\.push(\|\.splice(" app/selectors --include="*.ts"   # mutation
```
Check each result function for: identity/passthrough, new collection without deep-equal, mutation, `state=>state` input.

### Redux / useSelector → [mm-redux-antipatterns.md](mm-redux-antipatterns.md)
```bash
grep -rn "useSelector(.*isEqual)" app --include="*.tsx" --include="*.ts" | grep -v ".test."
grep -rn "useSelector((state" app --include="*.tsx" | grep -v ".test."   # inline accessors
grep -rn "dispatch(" app --include="*.ts" --include="*.tsx" | grep -v ".test." | grep -iE "setInterval|setTimeout|\.on\(|addEventListener|socket"
```

### Context → [mm-context-performance.md](mm-context-performance.md)
```bash
grep -rn "Provider value={{" app --include="*.tsx" | grep -v ".test."
```

### Hooks → [mm-hook-dependency-arrays.md](mm-hook-dependency-arrays.md)
```bash
grep -rn "\[JSON.stringify\|, JSON.stringify" app --include="*.ts" --include="*.tsx" | grep -v ".test."
```
(`exhaustive-deps` is NOT linted in this repo — check effect deps by hand.)

### Animations → [mm-layout-animations.md](mm-layout-animations.md)
```bash
grep -rn "useNativeDriver: false" app --include="*.tsx" --include="*.ts" | grep -v ".test."
```
Flag the ones animating `width`/`height`/`flex`/`top`/`left`.

### Lists → [js-lists-flatlist-flashlist.md](js-lists-flatlist-flashlist.md)
```bash
grep -rn "<ScrollView" app --include="*.tsx" | grep -v ".test."    # then check for .map() of growable data
grep -rn "<FlatList" app --include="*.tsx" | grep -v ".test."      # check perf props on growable lists
```
FlashList v2: do **not** flag missing `estimatedItemSize`.

### Bundle → [bundle-barrel-exports.md](bundle-barrel-exports.md) / [bundle-library-size.md](bundle-library-size.md)
```bash
grep -rln "export \* from\|export {.*} from" app --include="*.ts" --include="*.tsx" | grep -E "index\.(ts|tsx)$"  # barrels
grep -rn "from 'lodash'" app --include="*.ts" --include="*.tsx" | grep -v ".test.\|lodash/"                        # main-package lodash
```

### Memory → [js-memory-leaks.md](js-memory-leaks.md)
```bash
grep -rn "addEventListener\|setInterval\|\.subscribe(\|AppState.addEventListener" app --include="*.ts" --include="*.tsx" | grep -v ".test."
```
For each, confirm a matching cleanup (`return () => …`, `.remove()`, `clearInterval`, `unsubscribe`). Known gap: `app/core/SDKConnectV2/services/connection-registry.ts:487`.

## Reference-stability audit (NOT grep-able — you must read)

Grep finds *syntactic* patterns. The highest-impact re-render bugs are *data-flow* problems a grep can't see — they're found by reading a hook's return path and how values flow into children. For a re-render-heavy screen, do this read pass:

- **Hook return stability** — does a custom hook build an array/object/function inline and return it **without `useMemo`/`useCallback`**? New ref every render defeats every downstream `useMemo`. → [mm-unstable-hook-return.md](mm-unstable-hook-return.md) *(this was the CRITICAL miss on SimulationDetails — the catalogue grep didn't catch it)*
- **Props into `.map()`'d children** — is a fresh array/object passed to mapped children that aren't `React.memo`'d, or keyed by `index`?
- **Render-phase side effects / setState** — any `setState(...)`, `dispatch(...)`, or `trackEvent(...)` in a render body (not inside `useEffect`/`useCallback`)? Triggers extra render passes.
- **O(n²) reduce-with-spread** — `reduce((acc, x) => ({ ...acc, ... }), {})` rebuilt every render.
- **Per-item subscription hooks** — trace each into its manager; shared subscription = fine, per-subscriber whole-dataset snapshot = bug. → [mm-streaming-realtime.md](mm-streaming-realtime.md)

Confirm any hit with the Profiler ("why did this render?") before asserting — see [mm-tools.md](mm-tools.md).

## Review checklist (paste into a PR review)

- [ ] No new `createSelector` with identity/mutation/new-collection-without-deep-equal
- [ ] No new `useSelector(x, isEqual)` (fix the selector instead)
- [ ] No real-time / high-frequency data dispatched to Redux
- [ ] `Context.Provider value` is memoized (not an inline object)
- [ ] No `JSON.stringify` in a hot dependency array
- [ ] Layout animations use Reanimated v3, not `Animated` + `useNativeDriver:false`
- [ ] Growable lists use FlashList with stable keys (+ `getItemType` if mixed)
- [ ] New event listeners / timers / subscriptions have cleanup
- [ ] New deps justified for bundle size; no main-package lodash / barrel imports
- [ ] Flow instrumented with `trace()` if it's a critical user flow; Reassure test if it's a re-render-heavy component

## Output format

```
## CRITICAL (n)
- path/file.ts:LINE — one-line description
  Fix: <recipe> (see mm-….md)
## HIGH (n) … ## MEDIUM (n) … ## LOW (n)
## Summary: total, hottest files, verdict PASS/FLAG/FAIL
```

## Guardrails (don't over-flag)

- FlashList v2: `estimatedItemSize` is not missing — it's removed.
- No `useMemo`/`useCallback`/dep suggestions without profiler evidence or a real bug.
- No speculative stale-closure claims — show the read path or repro.
- Don't suggest installing `react-native-performance` / `reassure` / `quick-crypto` (present) or Jotai/Zustand (Redux is committed).
- A primitive-returning selector that filters internally is Low, not a re-render bug.

## Related

- [mm-tools.md](mm-tools.md) — measure to confirm a flagged issue is real
- the per-pattern `mm-*.md` guides for fixes
