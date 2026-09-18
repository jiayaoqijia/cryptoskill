---
title: Selector Dependency Cascades — Blast Radius & Repair (MetaMask)
impact: CRITICAL
tags: reselect, cascade, dependency-graph, isEqual, structural-sharing, react-compiler
---

# Skill: Selector Dependency Cascades

> **Scope.** What a broken root selector does to the component graph is defined generically
> in the **`render-cascade`** knowledge file, and the selector patterns that cause it in
> **`selector-antipatterns`** — both installed alongside this skill under `knowledge/`.
> This file is the MetaMask Mobile instance: the real dependency graph, its blast radius,
> and the repair order.

[mm-selector-memoization.md](mm-selector-memoization.md) catalogues the broken-selector *patterns*. This file is about what happens **downstream of one broken root selector** — and how to repair the whole graph instead of patching its leaves. Reference case: extension PR metamask-extension#37147, where a single identity output selector (`getInternalAccounts`) was recomputing through **15 direct + 35+ transitive consumer selectors into 50+ components on every dispatch** — every 5-second balance poll, every keystroke in the send flow.

## Anatomy of a cascade

```ts
// ❌ the root: identity output selector — memoizes nothing, new "result" every dispatch
export const getInternalAccounts = createSelector(
  (state) => state.engine.internalAccounts.accounts,
  (accounts) => accounts, // output === input: the cache can never hit meaningfully
);
```

Every consumer selector that takes the root as an input now sees a "changed" input on every dispatch, recomputes, and — because most result functions allocate (`.filter()`, `.map()`, `Object.values()`) — emits its *own* fresh reference, propagating the invalidation one layer further. Three layers down, nobody remembers the root; they see "my selector keeps firing" and reach for local fixes:

```ts
// ❌ the band-aids that accumulate downstream of a broken root
const accounts = useSelector(getAccountsByScope, isEqual);        // deep compare per dispatch
export const getX = createDeepEqualSelector(getInternalAccounts, …); // deep compare per dispatch
export const getMemoizedAccounts = createSelector(getInternalAccounts, (a) => a); // does nothing
```

Each band-aid suppresses the re-render for one consumer while *adding* an O(n) deep comparison on every dispatch — and the cascade cost scales superlinearly with power-user data (see [mm-power-user-scenario.md](mm-power-user-scenario.md)).

A live cascade also **nullifies every optimization downstream of it**: `React.memo` children re-render anyway (their props are fresh refs), virtualized rows churn, compiler-memoized components re-render (the unstable value crosses the file boundary), and `useMemo`s recompute. Fix the cascade before evaluating any other optimization on the screen — and re-measure them after.

## Step 1 — Traverse the dependency tree exhaustively before fixing

The repair PR's evidence (and its review) should enumerate the graph **to closure** — every selector reachable from the suspect, not just its immediate neighborhood — the way #37147 did:

1. **Direct consumers:** every selector that lists the suspect as an input. `grep -rn "getInternalAccounts" app/selectors --include="*.ts"`
2. **Transitive consumers:** repeat for each direct consumer until the frontier adds no new selectors. Don't stop at a fixed depth — cascades often have **more than one broken root**, and a partial map produces a wrong fix order.
3. **Component consumers:** `useSelector` call sites of anything in the graph.
4. **Recomputation count:** instrument with `selector.recomputations()` (reselect) or a `console.count` in the result function across a few dispatches (a balance poll is a convenient metronome).
5. **WDYR pass — already wired in this repo:** `wdyr.js` at the repo root tracks `useSelector` hook diffs. Run `ENABLE_WHY_DID_YOU_RENDER=true yarn start`, reproduce one dispatch, and every consumer logging *same values, different reference* is a node in the cascade — the live counterpart of the static map above.

A before/after table — *recomputations per dispatch, re-renders per poll cycle, on the same interaction* — is what distinguishes a verified cascade fix from a speculative refactor.

**Proactive mode — find the big trees without waiting for a symptom.** Rank roots by blast radius first (grep each selector's name across `app/` for consumer-file counts; appearances inside other selectors' input arrays give direct dependents), then for each large root verify its **input reference-stability**, not just its result function. The pattern that defeats every result-function grep: an input *function* that builds a fresh composite per call — spreading controller states and collecting other selectors' results into a new object. It looks disciplined, passes all pattern sweeps, and silently downgrades a `createDeepEqualSelector` into a whole-composite deep compare on **every check**. Verified instance: `getStateForAssetSelector` feeding `selectAssetsBySelectedAccountGroup` (`app/selectors/assets/assets-list.ts:107`) — the root of the asset-surface tree (15+ dependent selectors, including the per-row `selectAsset`), deep-comparing effectively the entire asset state per consumer per flush.

## Step 2 — Plan the memoization fix order from the map: roots first

Write down the fix order before writing any fix. The order is **topological** — roots, then their descendants, layer by layer:

- A descendant fix can't be *verified* while any of its inputs is still unstable: its output identity keeps changing for upstream reasons, so the before/after numbers measure the wrong thing.
- Most descendant "problems" stop being fixes once the roots are stable — they reclassify from "add memoization here" to "remove the band-aid here" (Step 4). The plan is what tells you which is which *in advance*, instead of memoizing selectors that were only recomputing because of their inputs.
- If the map surfaced multiple roots sharing consumers, fix them together — otherwise the shared consumers keep re-rendering and the first root's win never shows up in the numbers.

## Step 3 — Fix the root, not the 50 consumers

Memoizing consumers one by one is whack-a-mole: each fix adds comparison cost and the graph keeps re-deriving from a poisoned root. Trace **upward** (who are my inputs? are *they* stable?) until you hit the selector whose output identity changes without its data changing — that's the root. Fix its memoization there (patterns + recipes in [mm-selector-memoization.md](mm-selector-memoization.md)).

**Know your reference-stability contract first.** What the correct fix looks like depends on whether your store gives you stable references for unchanged data:

- With **Immer-based reducers** (Redux Toolkit), structural sharing guarantees `state.a.b` keeps its reference **iff** nothing under that path changed. Under that contract, a plain `createSelector` over a *narrow* input is already correct, and deep-equal selectors are pure overhead.
- Where state is replaced wholesale on sync, input references break even when data didn't change, and `createDeepEqualSelector` at the *root* is the pragmatic tool.

Establish which contract a slice actually follows (log `prev === next` for the input across two unrelated dispatches) before choosing — the answer differs per slice, and assuming the wrong contract either reintroduces the cascade or buys deep-compares you don't need.

Then match the tool to **which side is unstable**: an unstable *input* (slice replaced wholesale on sync) calls for a deep-equal **input** compare (`createDeepEqualSelector`); a stable input with an unstable *output* (the result function allocates a fresh collection) calls for a `resultEqualityCheck`, so an unchanged result returns the cached ref. Deep-equalizing inputs to paper over an allocating result function runs the wrong comparison on every dispatch.

Verified mechanism for this repo (`app/core/redux/slices/engine`): `UPDATE_BG_STATE` replaces only the **changed controller's key** with `Engine.state[key]`, and BaseController v2 state is Immer-produced — so an unchanged controller keeps its reference across flushes, and unchanged paths *within* a changed controller are structurally shared. Plain accessors into controller state are stable by construction; deep-equal is only warranted where a selector's *inputs* genuinely churn. And remember a deep-equal selector is output-**stable** but pays its compare per check, scaled by input size — over a power-user transaction history that is an O(n) deep compare per consumer per flush.

## Step 4 — Sweep the graph and *remove* the band-aids

This is the step most fixes skip. After the root is stable, every downstream `isEqual`, `createDeepEqualSelector`-wrapping-a-now-stable-input, and `getMemoized*` duplicate is dead weight: it still runs its deep comparison on every dispatch, and it **masks regressions** — if the root breaks again, the band-aids hide it until the app is slow everywhere again.

```bash
# downstream band-aid sweep, scoped to the fixed graph
grep -rn "useSelector(.*isEqual)" app --include="*.tsx" | grep -v ".test."
grep -rn "createDeepEqualSelector" app/selectors --include="*.ts"
grep -rn "getMemoized\|selectMemoized" app/selectors --include="*.ts"
```

For each hit that consumes the fixed root (directly or transitively): remove the equality argument / downgrade to plain `createSelector`, and re-verify the consumer doesn't re-render on unrelated dispatches. #37147 deleted the band-aids in the same PR as the root fix — that's the model.

## What the React Compiler can and cannot do here

The compiler memoizes **within a file**. A `useSelector` result, an imported hook's return value, or an external context value is opaque to it — if the selector hands back a fresh reference, the compiled component still re-renders, and any derivation from it still recomputes (from the extension performance audit):

```tsx
const tokens = useSelector(selectTokens);     // compiler cannot see/stabilize this
const rows = tokens.map(toRow);               // ❌ recomputes every render even when compiled
const rows = useMemo(() => tokens.map(toRow), [tokens]); // ✅ still needed
```

Rule of thumb: values that **cross a file boundary** (Redux selectors, imported hooks/functions, external context) keep their manual `useMemo`/`useCallback`; same-file props/state derivations can lean on the compiler. Fix the selector graph first — automatic memoization downstream of an unstable root optimizes nothing.

## Don't over-correct

- Not every busy selector is a cascade root — a selector returning a **primitive** breaks the chain at that point regardless of recomputation (allocation waste ≠ re-render bug).
- A *global* top-level cascade (an unstable value in a root provider/HOC re-rendering the whole tree on every state change) is a pattern the extension audit found at app root — worth **ruling out** with one profiler pass ("why did this render?" on a top-level component during an unrelated dispatch), but don't assume it exists here; verify before restructuring providers. See [mm-context-performance.md](mm-context-performance.md) for the provider-value mechanics.
- Don't add `useMemo` around every `useSelector` read preemptively — only where a non-primitive result feeds a derivation or a memoized child (see guardrails in [mm-hook-dependency-arrays.md](mm-hook-dependency-arrays.md)).

## Verify

1. Root selector returns the **same reference** across two unrelated dispatches (the contract test from [mm-selector-memoization.md](mm-selector-memoization.md)).
2. Recomputation counts on direct + transitive consumers drop to ~0 on unrelated dispatches.
3. Profiler on a top consumer (account list, send flow): the re-render cascade is gone during a balance poll.
4. The band-aid greps above return no hits inside the repaired graph.
5. Lock the win in CI: add a Reassure `*.perf-test.tsx` on a top consumer so the cascade can't silently return.

## Related

- [mm-selector-memoization.md](mm-selector-memoization.md) — the root-selector patterns and fix recipes
- [mm-redux-antipatterns.md](mm-redux-antipatterns.md) — `useSelector(x, isEqual)` as symptom; per-consumer view
- [mm-unstable-hook-return.md](mm-unstable-hook-return.md) — the same cascade shape, with a hook as the root
- [mm-state-normalization.md](mm-state-normalization.md) — state shape that prevents cascade-prone selectors
