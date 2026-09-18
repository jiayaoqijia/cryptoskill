---
maturity: experimental
name: selector-antipattern-scan
description: Review and diagnose Redux selector antipatterns that cause render cascades, pre-merge and post-merge
---

# Selector Anti-Pattern Review

**Scope:** Redux selector antipatterns are the dominant cause of React render cascades in the MetaMask UI. This skill covers both review phases: pre-merge PR review (grep-driven checklist) and post-merge diagnosis (WDYR-driven workflow). Both modes resolve to the same root cause and the same fix set, catalogued in the **`selector-antipatterns`** and **`render-cascade`** knowledge files — the single source for their definitions (installed alongside this skill under `knowledge/`).

Both `metamask-extension` and `metamask-mobile` share the same React + Redux architecture; this skill applies to both (see overlays for repo-specific paths).

## When To Use

- **Pre-merge.** Reviewing a PR that touches a `selectors/` directory, adds a `useSelector` call, or modifies a `createSelector` / `createDeepEqualSelector` definition
- **Post-merge.** Re-renders are disproportionate to state change size, performance degrades non-linearly with user data size, or components re-render during idle
- **Triage.** A WDYR counter jumps 5+ times per action, or a React render counter shows unexpected re-renders

## Do Not Use When

- Non-selector performance concerns (effects → use `effect-antipattern-scan`, context providers, virtualization)
- Network-bound slowness (use the Network panel, not WDYR)
- Startup or initial-mount perf (use startup profiling)
- Non-React trees (worker messaging, background script perf)

## Mode A: Pre-Merge Review (grep-driven)

1. **List changed selector/consumer files.** `git diff --name-only origin/main...HEAD | grep -E '(selectors|useSelector)'`
2. **Run the [grep checklist](#grep-checklist)** against the changed files.
3. **Match each hit to a pattern** in `selector-antipatterns` or to one of the [team-specific workarounds](#team-specific-workarounds) below.
4. **Block on Jest warning.** If the PR's test run surfaces `"result function returned its own inputs"`, the PR introduces an identity/passthrough result (`selector-antipatterns` §2). Do not merge.
5. **Require a fix, not a justification.** None of the eight patterns have a valid use case. See [Pitfalls](#common-pitfalls) for the narrow `createDeepEqualSelector` exception.

## Mode B: Post-Merge Diagnosis (WDYR-driven)

1. **Confirm cascade.** Add a render counter to a high-level component. If count jumps 5+ per action, cascade is confirmed.
   ```tsx
   const [count, increment] = useReducer((n) => n + 1, 0)
   useEffect(() => { increment() })
   console.log('Render:', count)
   ```
2. **Enable WDYR.** `ENABLE_WHY_DID_YOU_RENDER=true yarn start` (same env var on extension and mobile).
3. **Identify root component.** The first WDYR log is the cascade origin. Do not fix downstream symptoms first.
4. **Classify via the [WDYR message table](#wdyr-message-interpretation).** If the root cause is a selector, return to [Mode A](#mode-a-pre-merge-review-grep-driven) and apply the fix set. If it is a context value or prop identity issue, see the `render-cascade` knowledge file.
5. **Verify.** Repeat the action. Confirm the counter stabilizes (e.g. 0→2, not 0→25). React Strict Mode's amplification compounds non-linearly through a cascade, so compare before/after under the same Strict Mode setting rather than dividing by a fixed factor.

## Grep Checklist

| Pattern (`selector-antipatterns` §) | Detection |
|---|---|
| §1 Unmemoized selector | `grep -rE 'export function get' <selectors-dir>/` |
| §2 Identity / passthrough result | Jest warning `result function returned its own inputs` |
| §3 New collection in the result function | `grep -rnE 'new Set\|new Map\|Object\.(values\|keys\|entries)\|\?\? \{\}\|\?\? \[\]\|=> \(\{\|=> \[' <selectors-dir>/` |
| §4 Mutation in the result function | `grep -rnE '\.sort\(\|\.reverse\(\|\.push\(\|\.splice\(' <selectors-dir>/` |
| §5 Over-broad input | `grep -rn 'state) => state\b' <selectors-dir>/` |
| §6 Unnecessary deep equality | `grep -rn 'createDeepEqualSelector' <selectors-dir>/` then verify each input is genuinely unstable |
| §7 O(n) lookup | `grep -rnE '\.find\(.*=>.*address' <selectors-dir>/` |
| §8 Chained unmemoized transforms | `grep -rnE 'export function get.*\{' <selectors-dir>/ -A5`, then look for several `.filter/.map/.sort` without memoization |

The `=> ({` and `=> [` alternates catch a result function that *returns* a fresh literal rather than constructing a named collection. A trial run missed a real instance without them: `(metamask) => ({ userRegion: ..., ... })` builds a new object every recompute and matches none of the collection constructors.

See the repo overlay for the concrete `<selectors-dir>` path.

## Team-Specific Workarounds

Two patterns show up beyond those in the knowledge file. Both are workarounds for broken selectors downstream. The fix is always to fix the selector, never to propagate the workaround.

### `useSelector(selector, isEqual)` from `react-redux`

```typescript
// Workaround that hides the real problem
const accounts = useSelector(getAccounts, isEqual)
```

- **Detection:** `grep -rnE 'useSelector\([^,]+,\s*(isEqual|shallowEqual)'`
- **Review action:** Find `getAccounts` (or whichever selector). Fix it to return a stable reference. Remove the `isEqual` argument in the same PR.
- **Why it's wrong:** Deep equality at the consumption site adds O(n) per render and leaves every other consumer of the same selector broken.

### Overuse of `createDeepEqualSelector`

```typescript
// Unnecessary when input is from Immer-managed Redux state
const getTokens = createDeepEqualSelector(
  (state) => state.metamask.tokens,
  (tokens) => transformTokens(tokens),
)
```

- **Detection:** `grep -rn createDeepEqualSelector <selectors-dir>/`
- **Review action:** For each instance, check if the inputs come from Redux state. If yes, swap to `createSelector`. Immer already gives stable references.
- **The narrow exception:** Inputs that are genuinely not from Immer/Redux state (e.g. derived from a non-Redux source, or passed in as props). These stay.

## WDYR Message Interpretation

For post-merge diagnosis, map the WDYR log message to the root cause:

| Message | Root Cause | Fix |
|---------|------------|-----|
| `different objects that are equal by value` | Object recreated | `useMemo` (or fix selector that produced it) |
| `different functions with the same name` | Callback recreated | `useCallback` with stable deps |
| `different React elements` | JSX passed as prop | Extract to constant |
| `props object itself changed but values equal` | Parent cascade | Fix parent, not child |
| `[hook useContext result]` | Context value unstable | `useMemo` provider value |

## Diagnostic Signals

| Red | Green |
|-----|-------|
| Same component 5+ times in WDYR | Re-render count ≤ expected per action |
| Counter jumps 5+ per action | No WDYR logs during idle |
| Render count scales with data size | Render count stable regardless of data |
| Re-renders during idle | — |

## Common Pitfalls

| Mistake | Correct approach |
|---|---|
| Accept `useSelector(sel, isEqual)` because "it works" | The underlying selector is broken; fix it and remove the workaround |
| Approve `createDeepEqualSelector` without checking input source | Trace every input to verify it's not already Immer-stable |
| Treat the eight patterns as preferences | They are measurably broken — each generates CI warnings |
| Ask the author to justify rather than fix | None of the patterns have a valid use case except the narrow exception above |
| Review only the selector definition, not consumption sites | Pattern 1 (plain function) hides at the call site |
| Fix downstream components first during post-merge diagnosis | Fix the root-cause selector; downstream fixes become wasted work |
| Add `React.memo` to symptom component | Requires stable parent. Fix the parent (usually a selector) first |
| Divide WDYR counts by 1 | React Strict Mode double-renders, but not by a clean factor through a cascade. Compare before/after under the same setting |
