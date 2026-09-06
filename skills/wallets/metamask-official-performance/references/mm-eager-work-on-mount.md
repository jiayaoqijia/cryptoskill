---
title: Eager / Redundant Work on Mount (MetaMask)
impact: CRITICAL
tags: tti, mount, pagerview, tabs, carousel, fetch, waterfall, offscreen, lazy
---

# Skill: Eager / Redundant Work on Mount

The most common reason **"opening a screen is slow"** is not a re-render or a broken selector — it's the screen doing **work for UI the user can't see yet**, all on the mount tick. Tabs/pagers/carousels that mount every child, a data hook that runs for all N tabs when only one is visible, or a chain of dependent fetches (a waterfall). This pattern is easy to miss because each individual piece looks fine — the cost is in the *multiplication* at mount.

This bug class is **feature-specific by nature** (it lives in how a screen wires its data hooks to its layout), so it rarely shows up in a global selector/animation sweep. Look for it explicitly whenever the complaint is about **opening / navigating to** a screen.

## Signatures

### 1. Pager/tab/carousel mounts all children
`react-native-pager-view`, tab views, and carousels often **mount every page immediately** unless told not to. If each page runs data hooks on mount, opening the screen runs *all* of them.

```tsx
// ❌ every tab's content mounts (and fetches) on open
<PagerView>                              // no offscreenPageLimit / lazy config
  {tabs.map((t) => <TabContent key={t.id} category={t.id} />)}
</PagerView>
```

### 2. Fetch hook with no `enabled`/`isActive` gate
A data hook called per-tab/per-item that defaults to fetching on mount:

```tsx
// ❌ enabled defaults true → fetches for EVERY tab, not just the visible one
const { data } = useMarketData({ category });   // enabled?: not passed → true
```

When there are 6–8 tabs, that's 6–8 parallel network requests + 6–8× parse/filter/dedup/`setState` on the same tick — while only one tab is on screen.

### 3. The gate exists but isn't wired
A frequent real case: the screen already computes an `isActive`/`hasEverBeenActive` flag and uses it to gate the **render** (skeleton vs list), but the **fetch** still runs eagerly. The machinery is there; it just isn't passed to the hook.

```tsx
const hasEverBeenActive = useHasEverBeenActive(isActive);
// render is gated...
{hasEverBeenActive ? <List /> : <Skeleton />}
// ...but the fetch is NOT:
const { data } = useMarketData({ category /* missing: enabled */ });
```

### 4. Request waterfall
`await a(); await b(); await c();` where b/c don't depend on a — sequential when they could be parallel, multiplying time-to-content.

## Detection (scope to the suspect feature dir)

```bash
DIR=app/components/UI/<Feature>

# data/fetch hooks rendered per-tab/item (look for them inside a .map or a TabContent component)
grep -rn "use[A-Z][A-Za-z]*\(Market\|Data\|Query\|Fetch\|Prices\)" --include='*.tsx' "$DIR"

# pagers/carousels that may mount all children
grep -rn "PagerView\|Carousel\|ScrollView horizontal\|TabView" --include='*.tsx' "$DIR"

# an `enabled` prop that exists in the hook but isn't passed at the call site
grep -rn "enabled" --include='*.ts*' "$DIR"          # then check call sites pass it

# sequential awaits that could be Promise.all
grep -rn "await .*;\s*$" --include='*.ts*' "$DIR"
```

Then read the call sites: **is a data hook running for tabs/pages/items that aren't visible?** If the hook accepts `enabled` (or similar) and the call site doesn't pass it, that's the bug.

## Fix

Gate the fetch on visibility, reusing the flag the render already uses:

```tsx
const { data } = useMarketData({
  category,
  enabled: hasEverBeenActive,   // active tab fetches now; others lazily on first view
});
```

`hasEverBeenActive` should initialize to `isActive` so the visible tab fetches immediately and the rest fetch only when first opened. If the hook has a `useLayoutEffect`/`useEffect` that handles the `false → true` transition, this is clean (no empty-state flash). For pagers, also consider `offscreenPageLimit`/lazy mounting so offscreen pages don't mount at all.

For waterfalls: `const [a, b, c] = await Promise.all([fa(), fb(), fc()])` when independent.

## Counter-example — DON'T gate a shared-subscription hook

A per-item hook backed by a **shared subscription manager** (e.g. `usePerpsLivePrices({ symbols: [oneSymbol] })` reading from one WebSocket subscription) looks identical in a grep to a bad per-tab fetch — but gating it with `enabled: hasEverBeenActive` would be **wrong**. It's not doing N fetches; it's N cheap reads off one stream. Before applying the fix above, **trace the hook into its provider/manager**: if it's a single shared subscription, leave it. The real streaming cost (if any) is a different bug — e.g. the per-subscriber initial snapshot copying the whole dataset — covered in [mm-streaming-realtime.md](mm-streaming-realtime.md). Gate **fetches**, not shared-subscription reads.

## Worked example (Predict feed)

Opening the Predict feed fired **6–8 simultaneous `getMarkets()` fetches** instead of 1: `PredictFeed` renders tabs in a `PagerView` (mounts all children), and each `PredictTabContent` called `usePredictMarketData(...)` **without `enabled`** (defaults `true`). The render was already gated by `hasEverBeenActive` — the fetch wasn't. One-line fix: pass `enabled: hasEverBeenActive`. Result: `getMarkets` 6–8 → 1, JS-thread parse/`setState` cascade in the open window collapses.

## Verify (Measure → Optimize → Re-measure → Validate)

1. **Count the fetches** — dev log of the fetch (gated behind `DevLogger`/`SDK_DEV=DEV`), or the network inspector (iOS = RN DevTools Network; Android = Reactotron). Expect N before, 1 after.
2. **JS-vs-UI triage** — Perf Monitor on open: JS FPS dropping while UI is fine ⇒ the parse/`setState` cascade.
3. **Re-render cascade** — RN DevTools Profiler: background fetches resolving re-render multiple tab contents.
4. Apply the gate, re-record: fetches drop to 1, JS FPS recovers.
5. Always re-measure on **Android + power-user scenario** ([mm-power-user-scenario.md](mm-power-user-scenario.md)).

## Related

- [native-measure-tti.md](native-measure-tti.md) — instrument the open with `trace()` (and beware traces that end at mount)
- [mm-tools.md](mm-tools.md) — the diagnostic tree (use the navigation-TTI branch) and the Step 0 static sweep
- [js-concurrent-react.md](js-concurrent-react.md) — defer expensive non-critical work after first paint
