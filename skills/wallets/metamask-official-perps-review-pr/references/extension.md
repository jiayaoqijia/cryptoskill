# metamask-extension review rules

<a id="extension-must-consume-the-published-controller-contract"></a>

## Extension Must Consume the Published Controller Contract

A controller bump or a `perps-events.ts` merge is proven against the shipped `@metamask/perps-controller` bundle and its `.d.cts`, not against manifests or Mobile assumptions.

- [ ] **Client patch compensates for controller state gap** — fix the shared controller contract or use explicit client-owned state.
- [ ] **Assumes Mobile-only initialization semantics** — Extension background/controller init may differ.
- [ ] **Package bump without compatibility check** — controller version changes need state/method/event compatibility validation.
- [ ] **Package bump proved only from manifests or `node_modules`** — those checks can pass while `dist` is stale. After building, verify a symbol introduced by the target controller version is present in the shipped bundle.
- [ ] **New constant accepted from main without contract check** — when resolving a merge conflict in `perps-events.ts` or similar, verify every constant added by main against `@metamask/perps-controller`'s `.d.cts` before accepting. Some constants are already supplied by the controller spread with identical string values (no-op to add); others are Extension-only aliases that must stay in the local alias layer. A constant that exists on neither side but has live consumers will cause a compile break if it is accidentally dropped.
- [ ] **Extension-only alias keys added as inline snake_case** — Extension-only analytics property keys (e.g. `query_count`, `time_in_search_ms`) must go in the alias layer of `shared/constants/perps-events.ts`, not as inline snake_case object keys. Inline snake_case keys trip `@typescript-eslint/naming-convention`.

<a id="controller-mock-must-be-kept-current"></a>

## Controller Mock Must Be Kept Current

Every new contract value that product code reads is added to the hand-maintained `test/mocks/metamask-perps-controller.js` in the same PR, otherwise tests silently see `undefined`.

- [ ] **New event name / property used in product code but absent from mock** — grep the new symbol in `test/mocks/metamask-perps-controller.js` before merging. If missing, add it.
- [ ] **Mock drift goes unnoticed** — tests do not warn when a mock returns `undefined`; they silently fail on downstream assertions. Do not assume the mock is up to date after a controller version bump.

<a id="analytics-wiring-patterns"></a>

## Analytics Wiring Patterns

- [ ] **Tracker outlives the rendered form**: Gate screen-view, abandonment and adjacent subscriptions on the same valid subject and render condition. Require subject existence before optional-chain equality, since two missing values compare equal.
- [ ] **One-shot guards reset on remount**: For events derived from persistent results, retain deduplication at that result's lifetime and stable identity. Destructive cleanup must check the stage it is permitted to undo, not just the account or transaction subject.

Screen views are emitted once, from the screen or modal that renders them, and attribution for controller-owned events is merged in `createPerpsInfrastructure`, not in UI code.

- [ ] **Screen-view double-emission on normal+error page pairs** — any page that renders both a normal screen view and an error screen view must gate the normal view on the subject existing (`Boolean(market)`) and give the error view a `resetKey`. Without this, one rendered error screen emits two events, and consecutive bad symbols each emit one instead of resetting cleanly.
- [ ] **Modal screen view at trigger site instead of in the modal** — screen views for a modal belong in the modal itself, not at its trigger sites. A modal with many triggers (e.g. a geo-block notice with 17 triggers across 11 hosts) needs one declarative `usePerpsEventTracking({conditions: isOpen})` in the modal, not 17 scattered call sites.
- [ ] **Removing client `track()` calls without checking background API** — when migrating analytics from client to controller, verify the matching background API actually accepts `trackingData`. Some APIs (e.g. `UpdateMarginParams`) do not — no `trackingData` field is needed for those.
- [ ] **Attribution split** — UI `trackingData` carries entry/discovery/hlFeeRate; stored UTM context must be merged in `createPerpsInfrastructure` via `mergeAttributionContext` for controller-emitted lifecycle events. Do not merge attribution in UI code for controller-owned events.

<a id="hook-import-boundaries"></a>

## Hook Import Boundaries

Shared perps hooks are imported from their module file, not the `hooks/perps` barrel, stream-module mocks list every hook a component uses, and no hook mutates a caller's ref.

- [ ] **Import shared hooks from their module, not the `hooks/perps` barrel** — components rendered by many hosts must import shared hooks (e.g. `usePerpsEventTracking`) directly from their module file, not from the `hooks/perps` barrel. Several test suites partially mock the barrel, so a barrel import surfaces as `usePerpsEventTracking is not a function` at render in unrelated tests.
- [ ] **Stream-module mocks are explicit whitelists** — when a covered component imports another stream hook, update the test's stream-module mock object too. A missing hook otherwise fails behind the React Router error boundary as an unrelated `is not a function` render error.
- [ ] **`react-compiler` forbids mutating a hook argument** — a hook cannot reset a caller's `hasCommittedRef`. The reset belongs in the caller's own open/reset effect. Mobile's version does mutate the ref — do not copy that part.

<a id="market-data-source-and-provider-behavior-must-be-consistent-across-paths"></a>

## Market Data Source and Provider Behavior Must Be Consistent Across Paths

A preferred market data source or provider applies to every fetch path (stream, market detail, order form, charts, fallback) through a typed, visible selection with tested fallback.

- [ ] **Preferred source wired only to stream path** — detail/order/chart fetches still use old/default source.
- [ ] **Source choice hidden in unchanged params** — make source/provider selection typed and visible.
- [ ] **Fallback path lacks evidence** — source/provider fallback should be tested and documented.

<a id="backend-routing-and-controller-preload-caches"></a>

## Backend Routing and Controller Preload Caches

A backend route or provider endpoint change updates the preload and cache-prime paths (`cachedMarketDataByProvider`, `PerpsStreamBridge`'s `startMarketDataPreload`) and the reconnect fallback, not only the explicit UI fetch, or warm restarts keep serving the stale route.

- [ ] **Preload cache not updated alongside explicit fetch path** — whenever a backend route or provider endpoint changes, grep for all preload and cache-prime call sites (`cachedMarketDataByProvider`, `PerpsStreamBridge`'s `startMarketDataPreload`) and verify they resolve through the same updated path.
- [ ] **Reconnect fallback bypasses cache invalidation** — reconnect handlers that re-init from cache without invalidating first will restore the old route after a network interruption.
- [ ] **Cache TTL assumes a route that no longer exists** — if the TTL or stale-while-revalidate window is longer than the rollout window for a backend routing change, the cache will serve the old route to users who reconnected within that window.

<a id="order-forms-must-preserve-user-input-across-toggles"></a>

## Order Forms Must Preserve User Input Across Toggles

A TP/SL sign or percent toggle transforms the existing value, and the submitted order params equal what the form displays.

- [ ] **TP/SL sign or percent toggle drops value** — toggles should transform existing state, not reset it unexpectedly.
- [ ] **Displayed value differs from submit params** — submitted order must match what user sees.

<a id="charts-and-ctas-need-feature-parity-evidence"></a>

## Charts and CTAs Need Feature-Parity Evidence

- [ ] **Loading and loaded section order differ**: Reserve space for every conditional section above stable controls, including a populated watchlist. Compare loading and loaded layouts with that data present.
- [ ] **Measurements ignore rendered state**: Invalidate cached widths when selection, icons or labels change. Keep measurement out of unused layouts and live-data render loops; prove the clear/overflow control stays reachable at the smallest supported width.

A chart or CTA change keeps the old chart context, gates the CTA by capability, and ships event coverage or an explicit deferral.

- [ ] **Advanced chart drops volume or realtime signal** — preserve old chart context unless intentionally removed.
- [ ] **CTA shown for unsupported asset/context** — gate by capability, not generic asset presence.
- [ ] **New CTA lacks analytics** — action buttons need event coverage or explicit deferral.

<a id="batch-action-and-analytics-error-path-parity"></a>

## Batch-Action and Analytics Error-Path Parity

Sibling batch-action handlers (`handleCloseAllPositions`, `handleCancelAllOrders`) share one error contract: the same catch and soft-failure analytics in every sibling, each new branch covered by a test.

- [ ] **Asymmetric catch blocks across sibling handlers** — if one batch-action handler emits `PerpsError` + `trackPerpsErrorScreenViewed` on transport throw, every parallel handler in the same component must do the same. Diff all `catch` branches in the file before declaring analytics parity.
- [ ] **Soft-failure branch without error-screen-view** — a `{ success: false }` (or equivalent `result?.success` check) branch that fires `batchActionError` but not an error-screen-view event is incomplete. Before signing off on error analytics, grep sibling components that own the same `{ success: boolean }` shape and verify their soft-failure branches are symmetric (`git grep -l 'success.*boolean\|{ success:' -- '*.tsx' '*.ts'`).
- [ ] **New analytics branch ships without a test** — every new `catch` block or `if (!result?.success)` branch that emits an analytics event must have a corresponding unit test covering that branch. Missing coverage surfaces as a hard gate failure later; add the test in the same commit as the analytics change.

<a id="cdp-e2e-proof-surfaces"></a>

## CDP / E2E Proof Surfaces

A Perps tab screenshot proves market data only when a non-zero price or position value is visible or a CDP state assertion confirms live data; a navigated route over a loading skeleton is not proof.

- [ ] **Perps tab screenshot treated as market-data-loaded proof** — a screenshot of the Perps tab can show a navigated route (e.g., `/perps/market/BTC`) while the page body is still a loading skeleton. Route navigation is *not* evidence that prices, positions, or market data have loaded. Before citing a screenshot as market-data proof, confirm a non-zero price or position value is visible in the image, or pair it with a CDP state assertion that confirms live data is present.

<a id="evidence-expected-before-extension-perps-review"></a>

## Evidence Expected Before Extension Perps Review

The PR carries a controller package version and contract compatibility note, a state-flow matrix for the selectors and hooks touched, a market data source matrix across stream, detail, order, chart and fallback paths, recordings for order form toggles and submitted params, and, for backend-routing changes, the preload cache and reconnect fallback paths explicitly addressed.

<a id="extension-test-layers"></a>

## Extension Test Layers

- [ ] **Component-view behavior tested as a unit test**: A test under `ui/pages/perps/**/index.test.tsx` that renders a whole page and asserts UI behavior belongs in the client's component-view framework as `*.view.test.tsx`. Exercise real hooks and state wiring; preserve the same scenarios when moving tests, or document why a focused unit test remains necessary.
