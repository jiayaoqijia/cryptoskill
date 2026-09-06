---
title: Onboarding & Quick Commands
---

# Onboarding

## Step 0: The non-negotiables

Before any optimization work:

- **Develop and measure on Android.** It is more sensitive and more representative of the user base than the iOS simulator.
- **Use the power-user scenario:** ~30 accounts, ~90 assets. A feature that is fast with 1 account can be unusable with 30. See [references/mm-power-user-scenario.md](references/mm-power-user-scenario.md).
- **Measure → Optimize → Re-measure → Validate.** No baseline, no change.

## Step 1: Confirm tooling (already installed — do not re-install)

- `react-native-performance` (v6) — wrapped by `app/util/trace.ts`
- `reassure` (v1.4.0) — `yarn test:reassure:baseline` / `yarn test:reassure:branch`
- `babel-plugin-react-compiler` + eslint plugin
- `react-native-quick-crypto`, `expo-image`, `rive-react-native`

If you think one of these is missing, you're wrong — check `package.json`.

## Step 2: Open the profilers

```bash
# React Native DevTools (works on iOS AND Android — Hermes is on for both)
# Press 'j' in the Metro terminal, or shake device → "Open DevTools"

# In-app FPS overlay
# Shake device → Dev Menu → "Perf Monitor"
```

## Security guardrails

- Review any shell command before running it; prefer version-pinned tooling.
- Do not pipe remote install scripts into a shell (e.g. Flashlight — install from a verified release).
- Treat new packages as supply-chain dependencies: pin, verify provenance, review.

## Quick commands

### Profile re-renders
```
React Native DevTools → Profiler → ⚙️ → enable "Record why each component rendered"
→ Start → reproduce the exact interaction → Stop → read "why did this render?"
```

### Record a full performance timeline
```
React Native DevTools → Performance → Record → run the exact flow → Stop
→ see js-performance-panel.md
```

### Inspect network requests
```
React Native DevTools → Network → run the flow (records automatically)
→ see js-network-panel.md
```

### Guard a component against render regressions (Reassure)
```bash
# write app/.../MyComponent.perf-test.tsx (see DeepLinkModal.perf-test.tsx)
yarn test:reassure:baseline   # on main
yarn test:reassure:branch     # on your branch — fails on significant regression
```

### Instrument a flow (trace)
```ts
import { trace, endTrace, TraceName, TraceOperation } from '../../util/trace';
trace({ name: TraceName.AssetDetails, op: TraceOperation.UIStartup });
// ...later, when the screen is interactive...
endTrace({ name: TraceName.AssetDetails });
```

### Analyze the bundle (no script wired — run manually)
```bash
# Expo Atlas (recommended for this SDK 54 project)
yarn expo install expo-atlas                                     # one-time, pinned
EXPO_ATLAS=1 yarn expo export --platform ios && yarn expo-atlas
```

### Add a directory to React Compiler
```js
// babel.config.js → react-compiler plugin → sources → pathsToInclude
// then:
yarn watch:clean   # Metro caches React Compiler output aggressively
```

## When to load which reference

Use the **Problem → reference map** in [SKILL.md](SKILL.md). Load the single file that matches the symptom; don't load everything.

## Priority order (when multiple issues exist)

1. Broken selector memoization (cascades widest) — `mm-selector-memoization.md`
2. Barrel exports / bundle (startup cost) — `bundle-barrel-exports.md`
3. Re-render hotspots (Context, hooks, isEqual) — `mm-redux-antipatterns.md`, `mm-context-performance.md`, `mm-hook-dependency-arrays.md`
4. Lists & animations (scroll/interaction jank) — `js-lists-flatlist-flashlist.md`, `mm-layout-animations.md`
5. Memory & TTI — `js-memory-leaks.md`, `native-measure-tti.md`
