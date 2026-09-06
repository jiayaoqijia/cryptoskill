---
repo: metamask-mobile
parent: performance
---


# MetaMask Mobile Performance

Performance advisor for MetaMask Mobile. Covers the full lifecycle: **Planning → System Design → Development → Review → Testing → Auditing → Debugging → Fixing → Production Monitoring**.

This skill is MetaMask-specific. For generic React Native technique depth it links to the bundled Callstack reference files; for MetaMask patterns, tooling, and verified anti-patterns it uses the `mm-*` files. New here? Start with [references/onboarding.md](references/onboarding.md).

## The One Rule: Measure → Optimize → Re-measure → Validate

Never optimize blind. Every change follows the loop:

1. **Measure** — capture a baseline on the target interaction (FPS, re-render count, trace duration, render time). Not component-tree depth/count — those are context, not evidence.
2. **Optimize** — apply the targeted fix from the relevant reference.
3. **Re-measure** — run the same measurement.
4. **Validate** — confirm the metric moved (e.g. account-switch re-renders 97 → 18, FPS 42 → 60). If it didn't, revert and try the next hypothesis.

Always pair measurement with the **power-user scenario on Android** — see [references/mm-power-user-scenario.md](references/mm-power-user-scenario.md).

> **If you can't measure in-session (no device/simulator) — the agent reality.** "Measure first" is the human's job; an agent session usually has no running device. Then: run the **Step 0 static sweep**, form a **ranked, code-evidence hypothesis** (cite `file:line`), and hand the user the **exact Measure→Validate steps**. Mark the diagnosis **UNVALIDATED** until on-device numbers confirm it — never present a code-evidence hypothesis as a measured fact. Full mode in [references/mm-tools.md](references/mm-tools.md).

## Environment (verified — affects which advice applies)

| Fact | Value | Consequence |
|---|---|---|
| React Native | 0.81.5, **New Architecture ON**, Hermes on **both** platforms | React Native DevTools works on iOS too; Concurrent React available |
| Expo SDK | 54 (`babel-preset-expo`) | Bundle analysis via Expo Atlas; tree-shaking prereq already set in Metro |
| Reanimated | **v3** (`runOnJS`/`runOnUI`) | Do NOT use v4 `scheduleOnRN`/`react-native-worklets` APIs |
| FlashList | **v2** | `estimatedItemSize` is deprecated — never flag it as missing; use `getItemType` |
| Instrumentation | `app/util/trace.ts` `trace()` + `TraceName` (~230) | This is THE way to instrument flows — already wired to Sentry |
| Reassure | installed (`yarn test:reassure:baseline` / `:branch`) | Write `*.perf-test.tsx`; do not "install" it |
| React Compiler | on for `app/components/Nav` + `app/components/UI/DeepLinkModal` (`target:'18'`) | Opt new dirs in via `babel.config.js` `pathsToInclude` |
| State | Redux + reselect (committed) | Don't recommend Jotai/Zustand; move transient state to `useState`/`useRef`, not a new lib |

## Pick your stage

| You are… | Go to |
|---|---|
| Planning a feature / triaging a ticket | [references/mm-planning.md](references/mm-planning.md) |
| Reviewing a PR / auditing code | [references/mm-audit-playbook.md](references/mm-audit-playbook.md) |
| Debugging a slow screen / FPS drop | [references/mm-tools.md](references/mm-tools.md) (symptom-first tree) |
| Instrumenting or testing a flow | [references/mm-tools.md](references/mm-tools.md) + [references/native-measure-tti.md](references/native-measure-tti.md) |
| Monitoring production | [references/mm-tools.md](references/mm-tools.md) → Sentry / Release Profiler |

## Problem → reference map

| Symptom / task | Start with |
|---|---|
| Component re-renders too much; account/network switch is laggy | [mm-selector-memoization.md](references/mm-selector-memoization.md) → [js-profile-react.md](references/js-profile-react.md) |
| `useSelector` returns new refs; `useSelector(x, isEqual)` band-aids | [mm-redux-antipatterns.md](references/mm-redux-antipatterns.md) |
| Whole subtree re-renders under a Context provider | [mm-context-performance.md](references/mm-context-performance.md) |
| `useEffect`/`useMemo` re-runs constantly; `JSON.stringify` in deps | [mm-hook-dependency-arrays.md](references/mm-hook-dependency-arrays.md) |
| Animation janky; `useNativeDriver: false` on width/height | [mm-layout-animations.md](references/mm-layout-animations.md) → [js-animations-reanimated.md](references/js-animations-reanimated.md) |
| List scroll jank / unbounded list | [js-lists-flatlist-flashlist.md](references/js-lists-flatlist-flashlist.md) |
| Search/filter input blocks typing | [js-concurrent-react.md](references/js-concurrent-react.md) |
| **Opening / navigating to a screen is slow** (tabs/pager fetch everything, N fetches for 1 visible view, waterfall) | [mm-eager-work-on-mount.md](references/mm-eager-work-on-mount.md) → [native-measure-tti.md](references/native-measure-tti.md) |
| **Real-time / websocket screen slow or janky** (prices, order book, live balances); slow only on first-open / after backgrounding | [mm-streaming-realtime.md](references/mm-streaming-realtime.md) |
| **List re-renders fully even though children are memoized** (a hook returns a new array/object every render) | [mm-unstable-hook-return.md](references/mm-unstable-hook-return.md) |
| FPS drops; want to localize JS vs UI thread | [js-measure-fps.md](references/js-measure-fps.md) → [js-profile-react.md](references/js-profile-react.md) (optional device-level Android vitals: [js-flashlight.md](references/js-flashlight.md)) |
| Need a full timeline (React scheduler + JS + network) for a slow flow, not just re-renders | [js-performance-panel.md](references/js-performance-panel.md) |
| Inspect network requests / API timings; is a slow screen data-bound or render-bound? | [js-network-panel.md](references/js-network-panel.md) |
| Memory grows over a session | [js-memory-leaks.md](references/js-memory-leaks.md) / [native-memory-leaks.md](references/native-memory-leaks.md) |
| Slow startup (TTI) | [native-measure-tti.md](references/native-measure-tti.md) → [bundle-analyze-js.md](references/bundle-analyze-js.md) |
| Bundle too big / barrel imports / heavy lib | [bundle-barrel-exports.md](references/bundle-barrel-exports.md) → [bundle-analyze-js.md](references/bundle-analyze-js.md) → [bundle-library-size.md](references/bundle-library-size.md) |
| Native module / sync method blocking JS | [native-sdks-over-polyfills.md](references/native-sdks-over-polyfills.md) |
| Native lib crashes on 16KB-page Android | [native-android-16kb-alignment.md](references/native-android-16kb-alignment.md) |
| Enable automatic memoization | [mm-react-compiler.md](references/mm-react-compiler.md) → [js-react-compiler.md](references/js-react-compiler.md) |

## Verified anti-pattern catalogue (this codebase)

Ordered by impact. Each links to the guide with the fix. **The `Where` column lists instances verified at audit time — they drift; the reusable asset is the detection recipe in each linked guide. Re-run the guide's grep, don't trust the line numbers.**

| Sev | Pattern | Where (verified at audit time — may drift) | Guide |
|---|---|---|---|
| Critical | Eager/redundant work on mount (pager/tabs fetch all; N fetches when 1 visible; waterfall) — common "screen opens slow" cause | feature-specific — sweep the screen's dir | [mm-eager-work-on-mount.md](references/mm-eager-work-on-mount.md) |
| Critical | Unstable hook return (hook builds new array/object every render, no `useMemo`) — defeats all downstream memo | feature-specific — read hook return paths | [mm-unstable-hook-return.md](references/mm-unstable-hook-return.md) |
| Critical | Per-subscriber stream snapshot copies whole dataset; cold-open cache teardown | feature-specific — trace per-row hooks into the stream manager | [mm-streaming-realtime.md](references/mm-streaming-realtime.md) |
| Critical | Plain `createSelector` returning new collection / `?? {}` | `accountsController.ts:83,139`, `transactionController.ts:98,120,294` | [mm-selector-memoization.md](references/mm-selector-memoization.md) |
| Critical | Barrel exports evaluated at startup (961 barrel index files **app-wide**; e.g. `app/component-library/`, `app/selectors/`) | app-wide | [bundle-barrel-exports.md](references/bundle-barrel-exports.md) |
| High | `useSelector(x, isEqual)` band-aid for broken selector | 6 files | [mm-redux-antipatterns.md](references/mm-redux-antipatterns.md) |
| High | Layout animation on JS thread (`useNativeDriver:false` on width/height) | 12 instances, 6 files | [mm-layout-animations.md](references/mm-layout-animations.md) |
| High | `Context.Provider value={{…}}` inline object | HomepageDiscoveryTabs, Toast | [mm-context-performance.md](references/mm-context-performance.md) |
| High | `JSON.stringify` inside dependency arrays | useBalanceChanges (3×), useSimulationMetrics, usePolling | [mm-hook-dependency-arrays.md](references/mm-hook-dependency-arrays.md) |
| High | lodash main-package imports (98 files, no tree-shaking) | 98 files | [bundle-library-size.md](references/bundle-library-size.md) |
| High | FlatList missing perf props on growing lists | 65 FlatList JSX | [js-lists-flatlist-flashlist.md](references/js-lists-flatlist-flashlist.md) |
| High | AppState listener without cleanup | `app/core/SDKConnectV2/services/connection-registry.ts:487` | [js-memory-leaks.md](references/js-memory-leaks.md) |
| Medium | Inline `useSelector(state => state.x)` bypassing named selectors | 3 files | [mm-redux-antipatterns.md](references/mm-redux-antipatterns.md) |
| Medium | Lottie where Rive fits (Rive already installed) | 5 files | [js-animations-reanimated.md](references/js-animations-reanimated.md) |
| Low | dayjs + luxon both present (dedup) | 4 + 6 files | [bundle-library-size.md](references/bundle-library-size.md) |

## Review guardrails (do not over-flag)

- FlashList v2: never flag missing `estimatedItemSize` — it's deprecated here.
- Don't suggest `useMemo`/`useCallback`/dep changes without profiler evidence or a real correctness bug.
- Don't report stale closures speculatively — show the read path or a repro.
- Don't recommend installing `react-native-performance`, `reassure`, or `react-native-quick-crypto` — all already present.
- Don't recommend Jotai/Zustand — Redux is the committed architecture.
- Measure the target interaction itself; component count/tree depth is context, not evidence.

## Attribution

Generic React Native references (`js-*`, `native-*`, `bundle-*`) adapted from "The Ultimate Guide to React Native Optimization" by Callstack. MetaMask-specific guidance (`mm-*`) from the internal Performance Guide for Engineers and verified codebase audits.
