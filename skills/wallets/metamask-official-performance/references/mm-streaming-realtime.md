---
title: Real-time / Streaming Data Performance (MetaMask)
impact: HIGH
tags: websocket, streaming, subscription, prewarm, cache, warm-cold, throttle, perps, realtime
---

# Skill: Real-time / Streaming Data Performance

Live data (WebSocket prices, order books, balances) is one of the easiest ways to make a screen janky — and one of the hardest to diagnose, because the cost lives in a **stream manager / subscription layer**, not in the screen's render code. A per-item hook that looks identical to a bad per-tab fetch can be a perfectly fine shared-subscription read — or a hidden O(all-items)×N copy. You have to trace the hook **into its provider/manager** to tell.

For a streaming-heavy feature, "slow to open" is usually **not** an on-mount render anti-pattern (see [mm-eager-work-on-mount.md](mm-eager-work-on-mount.md)) — it's a **connection/cache lifecycle** concern: is the cache warm at navigation time?

## Patterns that make streaming fast (what "good" looks like)

- **One shared subscription, not N.** A single manager subscribes to the feed once; components read from it. Beware the **N² trap** where each subscriber also pulls the full dataset (e.g. an `includeMarketData`-style flag that materializes everything per subscriber).
- **Per-subscriber throttling** to cap re-render rate — a 10/sec feed shouldn't cause 10 React renders/sec; throttle/coalesce before `setState`.
- **Prewarm / preload before navigation.** Warm the cache at a root provider (e.g. an always-on provider that `prewarm()`s markets + prices) so the screen hydrates instantly on open.
- **Synchronous hydrate from a snapshot** when warm — first render reads `manager.getSnapshot()` instead of waiting on a fetch.
- **Memoized context values** (the stream provider's `value`) — see [mm-context-performance.md](mm-context-performance.md).
- **TTI trace ends on data-loaded**, not mount (`conditions: [markets.length > 0]`) — see the warning in [native-measure-tti.md](native-measure-tti.md).

## Anti-patterns

### 1. Per-subscriber initial snapshot copies the entire dataset — O(all-items) × N subscribers
The subtle, high-impact one. A per-item subscription hook (`useLivePrices({ symbols: [oneSymbol] })`) calls into the manager's `subscribe()` → `getCachedData()`, which **copies the full ~200-symbol cache into a new object**, then the wrapper filters to the one symbol. With ~15 rows mounting on open, that's ~15 full-map copies on the open tick, repeated as more rows mount during scroll.

**Fix:** seed only the requested symbol(s) in `subscribeToSymbols`; or lift **one batched subscription** to the list level and pass prices down as props (removes N subscribers entirely).

### 2. Cold-open latency from cache teardown (warm-vs-cold is THE determinant)
A grace-period disconnect (e.g. `ConnectionGracePeriodMs = 20000`) that calls `clearCache()` on background wipes the prewarmed data. Re-entering after that pays the full cold path (init → ping → preload → fetch). Slowness then concentrates on **first-open** and **re-entry after > grace-period background** — i.e. it's *intermittent*, which is the tell.

**Fix (design, not always a bug):** preserve global, non-account-specific data across the grace-period disconnect (many managers already have a `clearCache(accountOnly)` distinction — reuse it so re-entry stays warm).

### 3. `key={filter}` remounts the whole list, tearing down every subscriber
Using `key={filterKey}` on the list to switch categories **fully remounts** it → all rows unmount/remount → all subscribers torn down and recreated (re-triggering #1's copies). **Fix:** filter the data, don't remount the list; let item identity (`keyExtractor`) handle row reuse.

### 4. Never put the stream in Redux
A 10/sec dispatch flows through the whole store and every `useSelector`. Keep real-time data in the manager/local state; write to Redux only to persist. See [mm-redux-antipatterns.md](mm-redux-antipatterns.md).

### 5. Perpetual wakeups
A `setInterval(updateState, 100)` for the lifetime of the mount is a constant JS wakeup even if it usually bails. Not an open-cost, but flag if you're chasing battery/idle cost — don't over-flag it as the open problem.

## Detection (scope to the feature dir)

```bash
DIR=app/components/UI/<Feature>
# subscription/stream hooks and managers
grep -rn "subscribe\|useLivePrices\|use[A-Z].*Stream\|StreamManager\|WebSocket\|\.on('message'" --include='*.ts*' "$DIR"
# the snapshot/seed path — read getCachedData/getSnapshot: does it copy ALL items?
grep -rn "getCachedData\|getSnapshot\|prewarm\|preload" --include='*.ts*' "$DIR"
# cache lifecycle / grace period (warm-vs-cold)
grep -rn "clearCache\|GracePeriod\|disconnect\|refCount\|TTL" --include='*.ts*' "$DIR"
# list remount-on-filter
grep -rn "key={.*[Ff]ilter\|key={.*[Cc]ategory" --include='*.tsx' "$DIR"
```

**The critical follow-up:** for every per-item subscription hook hit, **trace it into its manager** and answer: is it backed by a single shared subscription, and does the initial snapshot seed only what's requested? A per-row hook that looks like a bad per-tab fetch is fine *if* the manager batches — the bug, if any, is the O(all-items) seed, not the per-row call. Do **not** reflexively apply the `enabled: hasEverBeenActive` fix from [mm-eager-work-on-mount.md](mm-eager-work-on-mount.md) to a shared-subscription hook.

## Worked example (perps market list) — UNVALIDATED hypotheses

> Per the One Rule, this is a **code-evidence walkthrough, not measured fact** — treat H1/H2 as ranked hypotheses to confirm on-device (steps below), not as proven bugs.

The perps market list is *already optimized*: one shared WS price subscription (with an explicit `includeMarketData` N² guard), FlashList v2 with `removeClippedSubviews`/`drawDistance`, prewarm at the wallet root, synchronous hydrate from snapshot, memoized context, and a data-loaded TTI trace. So the likely "slow open" cost is **not** an on-mount render bug but lives outside the screen's render code:

- **H1 (most likely if slowness is *intermittent*):** cold-connection latency — the ~20s grace-period disconnect clears prewarmed market data, so re-entry after a long background pays the full cold path.
- **H2 (suspected, needs confirmation):** a per-subscriber snapshot cost — `getCachedData()` builds a new object over the full price cache on each `PerpsMarketRowItem` subscribe before the wrapper filters to one symbol. **Verify this actually dominates before fixing** — the immediate filter may make the per-component cost negligible; the real cost (if any) is the O(all-items) build at subscribe time × rows mounted. This is exactly the "trace the hook into its manager" case above.

A render/selector sweep cannot find either — both require reading the stream/connection layer.

## Verify (Measure → Optimize → Re-measure → Validate)

1. **Warm-vs-cold verdict first** — read the feature's own load log if it has one (perps: `Perps: Market data received (first load) { source: 'cache' | 'fresh_fetch', timeToDataMs }`, gated behind `SDK_DEV=DEV`). `cache`/`<100ms` ⇒ warm is fast, repro is a *cold* open; `fresh_fetch`/hundreds–thousands ms ⇒ blocked on fetch.
2. **Connection breakdown** — grep Metro for the feature's Sentry markers (perps: `PERPSMARK_SENTRY_WS`) or read the Sentry measurements / `TraceName.*`.
3. **JS-vs-UI triage** — Perf Monitor on open: both flat while skeleton lingers ⇒ data-bound (cold); JS drops/UI fine ⇒ render-compute (the snapshot-copy / per-row churn).
4. **Reproduce cold deliberately** — background past the grace period, foreground, open immediately; expect the cold path.
5. Re-measure on **Android + power-user scenario** — for streaming features the scaling axis is usually **item/stream count** (e.g. perps market count / all categories / testnet), not accounts/assets. See [mm-power-user-scenario.md](mm-power-user-scenario.md).

## Related

- [mm-eager-work-on-mount.md](mm-eager-work-on-mount.md) — the naive cousin; read its counter-example on shared-subscription hooks
- [native-measure-tti.md](native-measure-tti.md) — instrument the open; end the trace on data-loaded
- [mm-tools.md](mm-tools.md) — the warm-vs-cold branch of the navigation-TTI tree, and "check for existing instrumentation first"
- [mm-context-performance.md](mm-context-performance.md) — memoize the stream provider's value
