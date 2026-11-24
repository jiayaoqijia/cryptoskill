---
name: component-structure
description: >-
  How to structure React and React Native components and screens in
  MetaMask Mobile and Extension. Use when writing, splitting or
  refactoring a component or screen, when deciding where state, effects,
  handlers, subscriptions or copy belong, or when reviewing a PR that
  adds or reshapes one. Triggers include many useState calls, useReducer,
  useEffect with async work, useCallback or useMemo, sub-components in one
  file, a selector or live-data hook at the top of a large screen, and a
  list row that subscribes to a whole collection.
maturity: experimental
---

# Component Structure

How a React or React Native component is laid out: what lives in the file, in what order, where state, logic and subscriptions go, and when manual memoization is allowed. One set of rules serves two modes: authoring or refactoring a component, and reviewing a PR that adds or reshapes one.

Rules carry stable IDs (R1–R7, R9; R8 is retired and not reused). Cite the ID in every suggestion and review comment.

## When To Use

- Writing a new component or screen, or splitting an existing one.
- Deciding where state, effects, handlers, subscriptions or derived values belong.
- Reviewing a PR that adds a component or changes its state, effects or memoization.

Rules are criteria plus signals, not thresholds. A signal (for example, more than 3 `useState`) means check the rule, not apply the fix blindly.

Out of scope, and where it goes instead:

| Need | Skill |
|---|---|
| Grep-style review of new `useEffect` in a diff | `mms-effect-antipattern-scan` |
| Fixing React Compiler bailouts | `mms-react-compiler-migration` |
| Splitting a very large file by subject | `mms-decompose-large-files` |
| Creating a new Mobile component from scratch, folder and file layout | `mms-component-scaffold` |
| Component choice (MMDS first, via the hosted `components.json` manifests), tokens and Tailwind | `mms-ui-development` |
| TypeScript, naming and general file layout | `mms-coding-guidelines` |
| Writing or memoizing a selector | `mms-selector-patterns`, `mms-selector-antipattern-scan` |
| List virtualization and list keys | `mms-performance` (Mobile), `mms-perf-rendering` (Extension) |

This skill does not ask for app code to be refactored outside the change being written or reviewed.

## Workflow

1. Read the whole component, not only the diff. Most findings depend on the order and grouping of hooks across the body.
2. Walk R1–R7 and R9 in order. For each finding, record file, line range, rule ID and the fix from the rule.
3. Check the rule's exceptions before reporting. A finding that matches an exception is not a finding.
4. Apply the repo overlay below (compiler scope, copy API, navigation, folder layout). It narrows R7, says where R1 sub-components and R3 hooks go, and names the R9 live-data hooks.
5. In review mode, use the Review Checklist. Report only lines the PR adds or reshapes, unless the user asks for a full-file audit.

Before/after snippets for every rule: [references/examples.md](references/examples.md).

### R1 — One component per file

- **Rule.** One component per file. A sub-component gets its own file in a `components/` folder next to the parent. Never declare a component, or a function that returns JSX, inside another component's body.
- **Why.** A component declared in the body is a new type on every render, so React remounts it and drops its state. A module-level sibling does not remount, but its logic cannot be found, tested or reused on its own.
- **Detect.** More than one component (exported or module-level) in a `.tsx` file. A function returning JSX declared inside a component (`renderX`, `const Row = () => <...>`), including an inline render prop (`renderIcon={() => <Icon />}`). A custom hook declared in the component's file is the same signal: move it to `use<Name>.ts`.
- **Fix.** First check whether an MMDS component already covers it (`mms-ui-development`); if so, use it instead of a new file. Otherwise move the sub-component to `components/<Name>/<Name>.tsx` with its own types and test. Pass data as props. Move a same-file hook to its own `use<Name>.ts`.
- **Exceptions.** Private render helpers at module scope with no state and no hooks, under 20 lines. An inline `.map` callback that renders list items inside the JSX. Story and test files. A thin default-export wrapper that only adds a provider or router around the main component.

### R2 — Fixed body order

- **Rule.** The body follows one order: route params and context; selectors; local state; custom hooks; derived values; effects; handlers; early returns; JSX. Every derived value sits before any early return.
- **Why.** A reader finds anything by position. Derived values after an early return, or inside a `renderX` helper, are spread across the body and invisible from the top.
- **Detect.** A derived `const` after an early `return` or inside a render helper. `useState` or selectors interleaved with effects or handlers. A derived value declared after the handlers.
- **Fix.** Reorder into the sequence above. Move derived values out of render helpers to the derived block.
- **Exceptions.** Hook call order must stay valid; reordering never moves a hook below an early return. Render-time state adjustment from a previous value (`if (x !== prevX) { setPrevX(x); setY(...); }` placed right after the state it adjusts) is the React-recommended pattern, not an R2 or R4 finding.

### R3 — The component is composition

- **Rule.** The component reads state and renders. Async flows, orchestration, analytics sequencing and navigation decisions live in a colocated `use<Screen>` hook that returns `{ state, actions }`.
- **Why.** Flow logic in the body is only testable by rendering the whole screen. A hook is tested on its own, and the component shrinks to layout.
- **Detect.** A handler longer than a few lines; `try/catch` with side effects in the body; one handler that dispatches, tracks analytics and navigates; an inline JSX handler that sets several values or dispatches; a handler that coordinates several sections, refs or calls (for example `Promise.allSettled` over refs). A handler wrapped in `useCallback` can be both R3 and R7: report each rule in its own row.
- **Fix.** Extract to `use<Screen>.ts` next to the component, with its own test. The component calls `const { state, actions } = use<Screen>()` and wires `actions.x` to props.
- **Exceptions.** Single-line handlers that call one action or one setter. A short handler that sequences two steps (a transition then a navigation, `preventDefault` then navigate, a navigation then a reset) is still an R3 finding.

### R4 — `useEffect` only for external sync

- **Rule.** `useEffect` only syncs with an external system: subscriptions, native or DOM listeners, imperative APIs. Async reads go through TanStack Query or a dedicated hook. User-triggered logic goes in event handlers. Values computable from props or state are computed during render.
- **Why.** Effects that fetch, chain `setState` or react to one state change by setting another add renders, race on unmount and hide the cause of a change.
- **Detect.** An `async` function declared inside `useEffect`; a manual `cancelled` / `isMounted` flag; a `setState` chain in an effect; an effect that copies a prop or selector into state; an effect that fires analytics or navigation in response to state rather than to an event; a previous-value ref used to detect a change and reset state.
- **Fix.** `useQuery` for async reads. A dedicated hook for non-query async work. Event handlers for user actions. Compute derived values in render. Reset state on identity change with a `key` on the component.
- **Exceptions.** Effects that subscribe and return a cleanup (listeners, timers, native modules). A one-time mount event (for example, a page-view analytics call) when no event handler exists for it; this covers fire-and-forget calls only, not a mount effect that awaits a read and sets state. Render-time state adjustment from a previous value (see R2) is not an effect and not a finding.

### R5 — Mutually exclusive phases are one state

- **Rule.** Phases where only one can hold at a time are one state machine: a single discriminated-union `status` (`'idle' | 'resolving' | 'submitting' | 'failed'`), with phase-specific data on the matching variant. Never separate booleans.
- **Why.** Separate booleans allow impossible combinations (`isLoading && isReady`, `isSubmitting && hasError`), and every reader must work out which wins.
- **Detect.** Two or more booleans or flags where only one should be true at a time. A render that checks several of them in priority order. A setter that clears one flag while setting another. A `view` or mode enum held in state plus separate `loading` / `ready` booleans that gate the same render (the phase is split across them even though one part is already an enum). Flags that step through one transition (open, animating, closed), often with a `setTimeout` between steps.
- **Fix.** One `useState<Status>` (or a reducer whose state is the union), with an exhaustive `switch` on `status` in render.
- **Exceptions.** Values that can legitimately be true together are not phases; see R6. Form-tracking flags (`touched`, `hasSubmitted`, `validationArmed`), input values, search-panel open state and modal, sheet or dialog visibility are not phases. One-way latches (flags that only ever go from false to true) are not phases. A mode computed during render from other values is a derived value, not phase state.

### R6 — Values set together move to a reducer

- **Rule.** Independent state values that the component updates as a group (2 or more setters called together to reach one UI state) move to `useReducer`, with one named action per transition. More than 3 `useState` is a signal to check this, not a mandate.
- **Why.** Each caller must remember the full group. Missing one setter leaves stale state that no type catches.
- **Detect.** The same group of setters called together in more than one handler, effect or callback (for example, reset input, clear error and close a sheet). The groups need not be identical: overlapping subsets of the same fields across handlers count, such as a form value and its validation flags updated together in several change and blur handlers, or a pair like `isResolved` + `resolvedValue` set together at several sites.
- **Fix.** `useReducer` with typed actions (`{ type: 'reset' }`, `{ type: 'submitStarted' }`), so each transition is one `dispatch`. When the group is a form, one state object with a `reset` action is enough.
- **Exceptions.** Values that are never set together stay as separate `useState`. A group set together in only one place. A single mutually exclusive phase goes to R5, not R6: flags that step through one R5 transition are reported under R5 only, even when several handlers set them together.

### R7 — No reflexive manual memoization under React Compiler

- **Rule.** Do not add new `useMemo`, `useCallback` or `React.memo` by default in code that React Compiler compiles. Do not strip existing memoization as part of an unrelated change.
- **Why.** The compiler already memoizes compiled components. Manual memoization adds dependency lists that drift and noise that hides the logic. Removing it in passing can change behavior in files with a compiler bailout.
- **Detect.** New manual memoization in a compiled path without a stated reason. `useCallback` around a pure predicate or a handler only passed to a host element. In a full-file audit, existing manual memoization in a compiled path is also a finding: report it, with the fix applied when the file is restructured.
- **Fix.** Remove it from the new code. When the file is being restructured under R3, the extracted hook follows the same rule.
- **Exceptions.** API contracts that need stable identity (focus-effect callbacks, a debounced or throttled function, a dependency of an external subscription), including a callback whose only use is as the input of such a memo (the function passed to `debounce`; a callback that is also called directly or listed as an effect dependency is still an R7 finding); files the compiler does not compile (a confirmed bailout, an unsupported construct, a `'use no memo'` directive, a class component; see the repo overlay for how to confirm); paths the compiler does not cover (see the repo overlay); a measured hot path, proven with `mms-react-render-delta`.

### R9 — Subscribe where the value is used

- **Rule.** A selector, context read or live-data hook (prices, streams, polling, a countdown timer) sits in the smallest component that uses its value. When a value feeds only one JSX region, that region becomes a child component that owns the subscription. A list row reads only what it renders: it gets the value by prop, or from a selector that returns just that value, never by subscribing to a whole collection to pick out or compute one value.
- **Why.** An update re-renders the component that holds the subscription. A fast-changing value at the top of a screen re-runs the whole body (every hook and derived value) on each update, even when the compiler skips unchanged children. A row that subscribes to a whole collection re-renders whenever any entry changes, once per row.
- **Detect.** A live-data hook or a frequently changing selector in a screen or large component whose value is read by only one JSX region or one child. A list-row component (rendered from `.map`, `renderItem` or a list) that selects a whole collection (rates, market data, balances, all tokens) and indexes into it, or scans it, to get one value. Judge by where the value is used, never by how many `useSelector` calls the component has.
- **Fix.** Extract the region to a child component (R1) and move the subscription with it; the parent passes ids, not the value. For a row, pass its value as a prop from a parent that already holds the collection, or read it with a selector that returns only that value (a primitive or a stable reference), taking the item's id when the value is per item. Extraction isolates the update on its own; do not add `React.memo` for it (R7).
- **Exceptions.** A value used by several regions or children. A value that decides which children mount (feature flags, loading gates). A value that rarely changes (feature flags, settings, the selected account). A per-item live-data hook backed by one shared subscription manager, which is the intended row pattern (see the repo overlay). Moving logic into `use<Screen>` is R3, not R9: a subscription inside the screen hook still re-renders the screen.

## Review Checklist

One yes/no check per rule. A "no" is a finding; cite the rule ID.

- [ ] **R1** Does the file hold one component, with no component or JSX-returning function declared inside another component's body?
- [ ] **R2** Does the body follow the fixed order, with every derived value before any early return?
- [ ] **R3** Are async flows, orchestration, analytics and navigation decisions in a `use<Screen>` hook rather than in the component body or inline JSX handlers?
- [ ] **R4** Does every `useEffect` sync with an external system, with no async fetch, `cancelled` flag, `setState` chain or state mirroring?
- [ ] **R5** Are mutually exclusive phases one discriminated-union `status`, not separate booleans?
- [ ] **R6** Are setters that are always called together replaced by one `useReducer` action?
- [ ] **R7** Is every new `useMemo` / `useCallback` / `React.memo` in a compiled path (every one, in a full-file audit) covered by a listed exception?
- [ ] **R9** Does each selector, context read and live-data hook sit in the smallest component that uses its value, with each list row reading only the values it renders?

## Lint Candidates

Follow-up only. Nothing here changes ESLint config.

- R1: `react/no-unstable-nested-components` for components declared in a body; `react/no-multi-comp` for more than one component per file.
- R2: a custom rule for a derived `const` declared after an early `return`.
- R4: a custom rule for an `async` function or a `cancelled` / `isMounted` flag inside `useEffect`.
- R7: a custom rule that flags new `useCallback` / `useMemo` in compiler-covered paths, with an allow-list for focus-effect callbacks.

R3, R5, R6 and R9 need judgment and stay review-only.

## Related Skills

- `mms-effect-antipattern-scan`: grep checklist for new `useEffect` in a diff. R4 is the structural rule; that skill is the scan.
- `mms-perf-react-compiler` and `mms-perf-hooks-effects`: performance depth behind R4 and R7.
- `mms-react-compiler-migration`: fixing bailouts; keep linter-requested memoization during that work.
- `mms-decompose-large-files`: splitting a file by subject, before or alongside R1 and R3.
- `mms-component-scaffold`: creating a new Mobile component; owns folder layout, file set and styling.
- `mms-ui-development`: MMDS component choice, tokens and Tailwind. Check it before R1 creates a new sub-component.
- `mms-coding-guidelines`: TypeScript, naming and general file layout.
- `mms-selector-patterns` and `mms-selector-antipattern-scan`: how a selector is written and memoized. R9 decides which component calls it.
- `mms-performance` (Mobile) and `mms-perf-rendering` / `mms-perf-state-management` (Extension): measuring render cost, list virtualization and keys, and selector shape behind R9.
