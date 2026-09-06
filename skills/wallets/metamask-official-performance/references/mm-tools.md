---
title: Performance Tools (MetaMask)
impact: HIGH
tags: tools, profiling, trace, reassure, flashlight, sentry, release-profiler
---

# Skill: Performance Tools — symptom first

Engineers don't ask "how do I use Reassure?" — they ask "why is this screen slow?" Start from the symptom.

> All internal tool walkthroughs (recordings): **Confluence — Performance Guide for Engineers**
> https://consensyssoftware.atlassian.net/wiki/spaces/TL1/pages/400085549067/Performance+Guide+for+Engineers
> Always pair any measurement with **Android + the power-user scenario** ([mm-power-user-scenario.md](mm-power-user-scenario.md)).

## Step 0 — static sweep FIRST (before forming a hypothesis)

When debugging a specific feature, **run the anti-pattern greps against that feature's directory before theorizing.** Static evidence is cheap and stops you from going hypothesis-first and missing a catalogued cause. Scope to the suspect dir:

```bash
DIR=app/components/UI/<Feature>            # e.g. app/components/UI/Predict

# eager/redundant work on mount — the #1 "opening a screen is slow" cause
grep -rn "PagerView\|Carousel\|TabView\|ScrollView horizontal" --include='*.tsx' "$DIR"
grep -rn "use[A-Z][A-Za-z]*\(Data\|Query\|Fetch\|Market\|Prices\)" --include='*.tsx' "$DIR"   # fetch hooks per tab/item?
grep -rn "enabled" --include='*.ts*' "$DIR"                # does an enabled gate exist but go unwired?

# re-render / memoization
grep -rn "value={{" --include='*.tsx' "$DIR"               # inline Context value
grep -rn "useSelector(.*isEqual\|useSelector((state" --include='*.ts*' "$DIR"
grep -rn "\[JSON.stringify\|, JSON.stringify" --include='*.ts*' "$DIR"

# animation / bundle
grep -rn "useNativeDriver: *false" --include='*.ts*' "$DIR"
grep -rn "from 'lodash'" --include='*.ts*' "$DIR" | grep -v "lodash/"

# streaming / subscriptions (trace each per-row hook into its manager — see caveat below)
grep -rn "subscribe\|use[A-Z].*\(Live\|Stream\|Prices\)\|StreamManager\|WebSocket" --include='*.ts*' "$DIR"
```

Then route the hits into the per-pattern guides. The full sweep + severity rubric is in [mm-audit-playbook.md](mm-audit-playbook.md) — open it for any "review/audit this feature" task. The sweep won't always surface the cause (some bugs are feature-specific data-flow design, not catalogued patterns), but it reliably rules out a *second* parallel cause.

> **Sweep caveat — per-item data/subscription hooks.** A hook called per row/tab/item (`useLivePrices`, `usePredictMarketData`) shows up identically in the grep whether it's a **bad per-item fetch** (gate it — [mm-eager-work-on-mount.md](mm-eager-work-on-mount.md)) or a **fine shared-subscription read** (don't gate it — [mm-streaming-realtime.md](mm-streaming-realtime.md)). **Trace the hook into its provider/manager before flagging:** is it backed by one shared subscription, and does the initial snapshot seed only what's requested (not copy the whole dataset per subscriber)? Don't reflexively apply the `enabled: hasEverBeenActive` fix to a shared-subscription hook.

> **DevLogger gate.** Many features emit a fast-triage load log via `DevLogger`, which only prints with `SDK_DEV=DEV` (`app/.../DevLogger.ts`). Run `SDK_DEV=DEV yarn watch:clean` or you'll think the log is missing.

## Step 0.5 — check for EXISTING instrumentation before adding any

Mature features are often *already* instrumented. The fastest triage is reading what they emit, not wiring new traces. Sweep for it first:

```bash
DIR=app/components/UI/<Feature>
grep -rn "TraceName\.\|use[A-Z][A-Za-z]*Measurement\|setMeasurement\|SENTRY\|LoggingMarkers\|DevLogger" --include='*.ts*' "$DIR"
```

Then read what's emitted — a load log (e.g. `source: 'cache' | 'fresh_fetch'`, `timeToDataMs`), Sentry measurements, or named `TraceName`s often answer "warm or cold? data-bound or render-bound?" immediately. Only add a new `trace()` if the existing signals don't cover the path you care about.

## Diagnostic tree

```
"Opening / navigating to a screen is slow" (navigation TTI)
  → ASK FIRST: slow EVERY time, or only first-open / after backgrounding (intermittent)?
       Slow every time → suspect eager work on mount → mm-eager-work-on-mount.md
            (pager/tabs mounting all children; fetch hook for all N tabs when 1 is visible; request waterfall)
       Intermittent (first-open / after background) → suspect a connection/cache WARM-vs-COLD lifecycle
            (prewarm unfinished, cache TTL expired, grace-period teardown clearing the cache) → mm-streaming-realtime.md
       Already optimized, cost is inherent latency → it's a data/connection wait, not a render bug;
            the fix is prewarm/cache/preserve-on-background, or honest "this is network-bound"
  → check EXISTING instrumentation BEFORE adding any (Step 0.5 below)
  → instrument the open with trace() only if needed (end on data-loaded, NOT mount — see warning below)
  → then JS-vs-UI triage as below

"This screen/interaction feels slow"
  → Perf Monitor: is the JS thread or the UI thread dropping?
      JS thread dropping  → React Native DevTools Profiler
            re-renders found        → mm-selector-memoization.md / mm-redux-antipatterns.md
            heavy computation found → mm-hook-dependency-arrays.md
      UI thread dropping (JS fine) → native rendering / animation
            layout animation        → mm-layout-animations.md
            too many views          → native-view-flattening.md
      Both dropping → start with JS profiling

"FPS drops while scrolling a list"
  → Perf Monitor to confirm → RN DevTools Profiler (or Flashlight live vitals, if installed — js-flashlight.md) → js-lists-flatlist-flashlist.md

"Components re-render too much"
  → React Native DevTools → "why did this render?" → mm-selector-memoization.md / mm-redux-antipatterns.md

"Search/filter input lags while typing"
  → js-concurrent-react.md (useDeferredValue) — and memo() the expensive child

"Real-time / websocket screen feels slow or janky" (prices, order book, live balances)
  → mm-streaming-realtime.md — shared-vs-N subscriptions, per-subscriber snapshot copy, throttle, warm-vs-cold cache
  → trace a per-row subscription hook into its manager before flagging it

"A hook/component re-renders the whole list even though children are memoized"
  → mm-unstable-hook-return.md (a hook returns a new array/object ref every render → defeats downstream memo)


"Is this slow flow data-bound or render-bound?"
  → Network panel for request timings → js-network-panel.md
  → Performance panel for the full React+JS+network timeline → js-performance-panel.md

"Memory grows over a session / crashes after long use"
  → js-memory-leaks.md (JS)  or  native-memory-leaks.md (native)

"Slow cold start"
  → instrument with trace() (below) → native-measure-tti.md → bundle-analyze-js.md

"How do I prove my fix is faster?"
  → Reassure (render count) + trace() (duration) [+ Flashlight live FPS for a quick check, if installed — js-flashlight.md]. Baseline → fix → re-measure.

"Prevent regressions going forward"
  → Reassure perf-test in CI  +  E2E performance gates (mms-performance-testing skill)

"On an RC build" (RC tester, QA, or a flow that's only slow in release)
  → React Native Release Profiler: shake → profile the flow → hand the .cpuprofile to
    Claude Code / AI agent of choice to find the hot frames

"Production alert / user report"
  → Sentry (#metamask-mobile-release-monitoring) → Release Profiler on an RC build (as above)

"No tool isolates it"
  → Manual binary search (below)
```

## Tools

### Perf Monitor (quick JS-vs-UI triage)
- **Open:** shake device → Dev Menu → "Perf Monitor".
- **Read:** UI-thread FPS, JS-thread FPS, RAM. <55 = dropping frames.
- **Interpret:** JS drops → expensive renders/selectors/computation. UI drops → native rendering/animation. Both → start JS-side.
- **Next:** React Native DevTools.

### React Native DevTools (re-renders, timing, memory, performance) — iOS + Android
- **Open:** press `j` in Metro, or shake → "Open DevTools". Hermes is on for both platforms, so this works everywhere.
- **Profiler:** ⚙️ → enable "Record why each component rendered" → Start → reproduce the **exact** interaction → Stop.
- **Read:** flamegraph (yellow = slow), Ranked view (slowest first), right panel "why did this render?" (props/hook/parent).
- **Next:** props churn → `useCallback`/memo; selector new-ref → [mm-selector-memoization.md](mm-selector-memoization.md); parent re-render → move state down / [mm-context-performance.md](mm-context-performance.md).
- **JS CPU:** the JavaScript Profiler tab → Heavy (Bottom-Up) for non-React hot functions.
- **Performance panel:** Performance tab → Record → run the flow → Stop. Shows React scheduler phases, the Components flamegraph, the JS Thread, and Network events on one timeline. Use it when the Profiler alone doesn't explain a slow flow. See [js-performance-panel.md](js-performance-panel.md).
- **Network panel:** Network tab → records `fetch()`/`XHR`/`<Image>` automatically. Timings, headers, response previews, and an Initiator call stack. Tells you if a slow screen is data-bound vs render-bound. See [js-network-panel.md](js-network-panel.md).

### Reactotron (network on Android — pre-0.83 fallback)
- Network inspection for **pre-0.83** setups where the DevTools Network tab is unavailable on Android. On RN 0.83+ prefer the DevTools [Network panel](js-network-panel.md) (works on Android). WebSocket events still aren't captured by the Network panel — Reactotron remains useful there.

### Flashlight (optional, external — NOT installed in this repo)
- **Not in `package.json`** — it's an external, Lighthouse-type tool for mobile apps. Don't assume it's available; for day-to-day FPS use Perf Monitor + RN DevTools.
- **If you install it** (separately, from a verified release — don't pipe a remote script to a shell): **`flashlight measure`** starts a live, interactive web UI for watching Android vitals (FPS/CPU-per-thread/RAM/score) while you drive the flow by hand. Non-deterministic; good for triage. See [js-flashlight.md](js-flashlight.md). For reproducible before/after or CI numbers, use the in-repo Reassure + `trace()` path instead.

### Reassure (render-time regression gate) — INSTALLED
- **Use:** guard a component/hook against render-time regressions before merge.
- Write `app/.../Component.perf-test.tsx` (examples: `DeepLinkModal.perf-test.tsx`, `Card.perf-test.tsx`).
- `yarn test:reassure:baseline` (on main) → `yarn test:reassure:branch` (on branch; **fails on significant regression**).
- Doc: `docs/readme/reassure.md`. **Do not "install" it — it's already here.**

### trace() — the MetaMask instrumentation API (local + Sentry) — INSTALLED
- This is the in-repo "Performance Measurement Tool." `react-native-performance` is wrapped by `app/util/trace.ts`.
```ts
import { trace, endTrace, TraceName, TraceOperation } from '../../util/trace';

trace({ name: TraceName.AssetDetails, op: TraceOperation.UIStartup });  // start
// ...when the screen is interactive...
endTrace({ name: TraceName.AssetDetails });                              // end

// or callback form (auto-ends on resolve/reject)
const x = trace({ name: TraceName.Tokens, op: TraceOperation.UIStartup }, () => build());
```
- New flow → add a `TraceName` (+ `TraceOperation`) to `app/util/trace.ts`, then wrap it.
- **Component-level: use a per-feature measurement hook, not raw `trace()`.** The repo convention is a declarative `useXMeasurement` hook (e.g. `app/components/UI/Predict/hooks/usePredictMeasurement.ts`, `usePerpsMeasurement`, `useSectionPerformance`) that starts on mount and ends when conditions are true — which structurally enforces the "end on data-loaded, not mount" rule below:
  ```ts
  usePredictMeasurement({ traceName: TraceName.PredictMarketDetailsView, conditions: [dataLoaded, !isLoading] });
  ```
  Raw `trace()/endTrace()` (above) is the **core-init** pattern (`EngineService.ts`, `Vault.ts`).
- Numeric `tags` become Sentry **measurements**; spans nest via `parentContext`; traces buffer until metrics consent then flush.
- ⚠️ **Your `endTrace` condition must represent _interactive / data-loaded_, not _mounted_.** A condition that is already `true` on the first render (e.g. `!isSearchVisible`, `!!component`, `isMounted`) closes the span at mount, before data loads — so it silently measures ~zero and gives false confidence. End on the active view's data being ready (e.g. `[!isSearchVisible, hasActiveTabData]`). This is a real bug found in the wild.
- Details: [native-measure-tti.md](native-measure-tti.md).

### E2E performance gates (merge gate)
- Flow-level timing in CI (account/network listing+switching, more added over time). Owned by the **`mms-performance-testing`** skill — go there to add a gate for your flow.

### Bundle analysis (no script wired — run manually)
```bash
# Expo Atlas (this is an Expo SDK 54 project)
yarn expo install expo-atlas                                     # one-time, pinned
EXPO_ATLAS=1 yarn expo export --platform ios && yarn expo-atlas
```
- See [bundle-analyze-js.md](bundle-analyze-js.md). Look for barrel-imported libs, lodash main-package, dayjs+luxon overlap.

### Sentry (production)
- Dashboards + `#metamask-mobile-release-monitoring` alerts. `trace()` spans/measurements already flow here. Correlate regressions with release tags.

### React Native Release Profiler (production-like CPU profile)
Best way to root-cause a slow flow on a real build — and the lowest-effort to read:

1. Grab an **RC build** — a release build; dev builds aren't representative.
2. **Shake** the device → the **Performance Profiler** menu appears.
3. **Start** the profiler, run the slow flow, then **Stop**. The `.cpuprofile` (a `sampling-profiler-trace*.cpuprofile`) saves to **Downloads**.
4. **Analyze it — two ways:**
   - **Visualize the flame graph:** symbolicate with `yarn react-native-release-profiler --local <file.cpuprofile> [--sourcemap-path <maps>]`, then open it in **SpeedScope** (speedscope.app) / `chrome://tracing` / Perfetto.
   - **Or let AI read it:** hand the `.cpuprofile` to **Claude Code / your AI agent of choice** and ask "why is this slow?" — it parses the sampling profile and names the hot frames / culprit function for you, no flame-graph reading.

See `docs/readme/release-build-profiler.md`.

### Manual binary search (last resort)
1. Android device, go to the slow screen.
2. Remove the most complex block until it's fast again (pair with Perf Monitor).
3. Last-removed block is the culprit; re-add, go one level deeper, repeat to the exact line.

## The loop (every time)

**Measure → Optimize → Re-measure → Validate.** Capture a baseline on the target interaction, apply one fix, re-measure the same thing, confirm it moved. If not, revert and try the next hypothesis.

### When you can't measure in-session (no device/simulator)

A code session often has no running device, so "Measure first" isn't literally possible. That's fine — use the **static-evidence mode**, and be honest about its status:

1. Run the **Step 0 static sweep** on the suspect dir.
2. Read the code paths and form a **ranked, code-evidence-based hypothesis** (cite `file:line`).
3. Hand the user the **exact Measure → Validate steps** to run on-device (which log/Profiler/Perf-Monitor reading would confirm it, and the expected before/after numbers).
4. Mark the diagnosis **UNVALIDATED** until on-device measurement confirms it. Don't present a code-evidence hypothesis as a measured fact.

## Related

- [mm-power-user-scenario.md](mm-power-user-scenario.md) · [js-measure-fps.md](js-measure-fps.md) · [js-flashlight.md](js-flashlight.md) · [js-profile-react.md](js-profile-react.md) · [js-performance-panel.md](js-performance-panel.md) · [js-network-panel.md](js-network-panel.md) · [native-measure-tti.md](native-measure-tti.md)
