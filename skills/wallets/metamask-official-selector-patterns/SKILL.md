---
name: selector-patterns
description: >-
  Redux selector authoring for MetaMask Mobile: named `select<Feature><Thing>`
  selectors in `app/selectors/`, `createSelector` / `createDeepEqualSelector`
  from reselect, leaf reads of `state.engine.backgroundState`, and
  `useSelector(selectX)` in UI. Use when adding or creating a selector,
  updating or refactoring an existing selector, moving inline `useSelector`
  derivation out of a component or hook, or answering questions about
  selectors, reselect, `createSelector`, `createDeepEqualSelector`,
  `app/selectors`, or `backgroundState`. Version-gated flag selectors go to
  `feature-flags`. Memoization audits of existing selectors go to
  `performance`.
---

# Selector patterns

## When To Use

- Implement / add / create a Redux selector
- Update / change / refactor an existing selector
- Questions about selectors, `useSelector`, `createSelector`, `createDeepEqualSelector`, `reselect`, `app/selectors`, or `backgroundState`

Version-gated flag selectors (`validatedVersionGatedFeatureFlag`, `selectRemoteFeatureFlags`, `app/selectors/featureFlagController/`) → **`feature-flags`**.

Memoization audits of existing selectors (broken identity, cascade re-renders) → **`performance`**.

## Workflow

Q&A: answer from the overlay, then stop.

Implement or update:

1. Search for an existing named selector before adding one.
2. Put new selectors in `app/selectors/<feature>.ts` (or the feature’s `selectors/` folder).
3. Add a leaf input selector that reads the controller slice. Compose derived selectors on top of it.
4. Narrow the input to the smallest slice. Choose `createSelector` (primitive output) or `createDeepEqualSelector` (object / array when the narrowed input still churns and the payload is small enough to compare).
5. Name it `select<Feature><Thing>`.
6. In components and hooks, call `useSelector(selectX)` with that named selector.
7. Add collocated unit tests with at least two state variants.
