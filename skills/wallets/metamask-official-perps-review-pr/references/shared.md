# Shared Perps review rules

<a id="controller-portability-core"></a>

## Controller Portability (Core)

`PerpsController` lives in `core/packages/perps-controller` and is published as `@metamask/perps-controller`; mobile and extension both consume the package. Controller code must stay platform-agnostic, and app code must go through the published surface.

- [ ] **Platform import in controller** — `react-native`, `Engine`, `Sentry`, `DevLogger`, browser APIs, or extension globals imported in `packages/perps-controller`. All platform services must flow through `PerpsPlatformDependencies` (DI), passed as the `infrastructure` constructor param.
- [ ] **Deep import from app code** — app files importing controller internals by path (`@metamask/perps-controller/dist/...`, a relative path into a linked checkout) instead of the package's public exports.
- [ ] **`__DEV__` or platform globals in controller code** — must not appear in controller files; the package has no such globals at build time.
- [ ] **New dependency not in DI interface** — controller code reaching outside its boundary (e.g., importing a hook, React context, or an app utility). Everything the controller needs must come through `PerpsPlatformDependencies`.
- [ ] **Breaking the publisher contract** — changing PerpsController's public API (state shape, method signatures, event names) without considering both consumers. Controller is a publisher — mobile and extension both consume it.

<a id="magic-strings-magic-numbers-placeholder-values"></a>

## Magic Strings, Magic Numbers & Placeholder Values

Constants live in the controller package (`core/packages/perps-controller/src/constants/perpsConfig.ts`, exported by `@metamask/perps-controller`) and in the reviewed client's UI constants module. PRs must use these — not inline literals.

- [ ] **Defaulting to `0` when data is unavailable** — the most common mistake. When price/percentage/data hasn't loaded yet, use the placeholder constants, NOT `0`, `$0`, or `0%`:
  - `PERPS_CONSTANTS.FallbackPriceDisplay` (`'$---'`) — price not yet loaded
  - `PERPS_CONSTANTS.FallbackPercentageDisplay` (`'--%'`) — percentage not yet loaded
  - `PERPS_CONSTANTS.FallbackDataDisplay` (`'--'`) — generic data not yet loaded
  - `PERPS_CONSTANTS.ZeroAmountDisplay` (`'$0'`) / `ZeroAmountDetailedDisplay` (`'$0.00'`) — ONLY for actual confirmed zero values (e.g., no volume), never for "loading" or "unavailable"
  - Defaulting to `0` hides loading states, makes bugs invisible, and can mislead users into thinking their balance/PnL is actually zero.
- [ ] **Inline timeout/delay values** — hardcoded `5000`, `10000`, `300` instead of `PERPS_CONSTANTS.WebsocketTimeout`, `PERPS_CONSTANTS.ConnectionTimeoutMs`, `PERFORMANCE_CONFIG.ValidationDebounceMs`, etc. Every timing constant has a named export.
- [ ] **Hardcoded slippage** — using `0.03` or `300` instead of `ORDER_SLIPPAGE_CONFIG.DefaultMarketSlippageBps`, `DefaultTpslSlippageBps`, `DefaultLimitSlippageBps`.
- [ ] **Hardcoded leverage fallback** — using `3` or `50` instead of `PERPS_CONSTANTS.DefaultMaxLeverage` or `MARGIN_ADJUSTMENT_CONFIG.FallbackMaxLeverage`.
- [ ] **Hardcoded precision** — using `6`, `2`, `5` for decimal places instead of `DECIMAL_PRECISION_CONFIG.MaxPriceDecimals`, `MaxSignificantFigures`, `FallbackSizeDecimals`, or `CLOSE_POSITION_CONFIG.UsdDecimalPlaces`.
- [ ] **Hardcoded API URLs** — inline `'https://perps.api...'` instead of `DATA_LAKE_API_CONFIG.OrdersEndpoint`.
- [ ] **Hardcoded provider name** — `'hyperliquid'` string instead of `PROVIDER_CONFIG.DefaultProvider`.
- [ ] **Hardcoded validation thresholds** — `20` for high leverage warning, `0.1` for price deviation, instead of `VALIDATION_THRESHOLDS.HighLeverageWarning`, `VALIDATION_THRESHOLDS.PriceDeviation`.
- [ ] **Hardcoded cache durations** — inline `5 * 60 * 1000` instead of `PERFORMANCE_CONFIG.MarketDataCacheDurationMs`, `FeeDiscountCacheDurationMs`, etc.

<a id="protocol-abstraction"></a>

## Protocol Abstraction

- [ ] **Execution identity inferred from display fields**: Preserve the venue's documented identity at the provider boundary and expose a stable opaque ID shared by REST and WebSocket paths. Equal order ID, time, size and price need not identify one fill. Do not deduplicate without that guarantee or key navigable history by array position. Check prepend stability and tied timestamps.

- [ ] **Provider identity lost during transformation**: Preserve provider identity through fill aggregation and apply provider-specific classification at the normalization boundary. Adding a provider must retain existing providers and cover equivalent inputs with different provider semantics.

All provider access must go through `AggregatedPerpsProvider` → `ProviderRouter`. HyperLiquid is primary, MYX is feature-flagged.

- [ ] **Hardcoded provider** — uses HyperLiquid or MYX APIs directly instead of going through `AggregatedPerpsProvider` / `ProviderRouter`. All operations must route through the abstraction.
- [ ] **Provider-specific branching in UI** — `if (provider === 'hyperliquid')` in components or hooks. Provider differences must be normalized in the aggregation layer, not leaked to the view.
- [ ] **Provider-specific error handling** — catches errors from one provider but not others. All providers must have consistent error boundaries via the aggregated layer.
- [ ] **Hardcoded market symbols** — string literals `"BTC"` or `"ETH"` instead of market config constants. Breaks when new markets or providers are added.
- [ ] **Hardcoded decimals/precision** — using provider-native decimal formats without normalization. HyperLiquid and MYX use different precision for prices, sizes, and leverage. Must go through `MarketDataFormatters` (DI).
- [ ] **`detailedOrderType` rendered directly in UI** — `detailedOrderType` is provider-native text, not an enum. HyperLiquid returns `Limit`, `Market`, `Stop Limit`, `Stop Market`, `Take Profit Limit`, `Take Profit Market`; MYX (`myxAdapter.mjs`) returns `Take Profit`, `Stop Loss`, `Liquidation` — which are not in that set. Any UI that renders `detailedOrderType` directly is provider-dependent by construction. **Grep for `detailedOrderType` in any PR touching order display** — it should be mapped through a locale string or normalized constant, not rendered raw.

<a id="pro-mode-ui-gating"></a>

## Pro Mode UI Gating

Pro market UI renders only when the remote flag (`selectPerpsProModeEnabledFlag`) and the controller mode (`PerpsMode.Pro`) are both active; a PR that checks one gate ships a silent no-op that looks like a feature flag bug.

- [ ] **Single-gate assumption** — checking only `selectPerpsProModeEnabledFlag` (remote feature flag) without also verifying the controller mode is `PerpsMode.Pro`. Both must be true for Pro UI to render.
- [ ] **Fixture starts in Lite mode**: A Lite fixture does not establish that Pro UI is unavailable. Runtime QA must verify the rollout flag and use supported mode/setup recipes before proof. Static review records missing runtime evidence without substituting unit tests for a visible claim.
- [ ] **Pro-only code tested only via live UI** — pure business logic shared between lite and Pro (e.g., `orderSizing`, `orderParams`, `tpslValidation`) should be extended in the shared helper, not re-inlined in either form. Tests against the shared helper work in any fixture mode.
- [ ] **Hardcoded tab index across feature gates** — derive selection from the rendered tab configuration or a stable tab ID. Test each supported gate combination so a newly inserted tab cannot move another tab's content or controls.

<a id="metametrics-events"></a>

## MetaMetrics Events

Every perps event uses one of the eight consolidated events and their typed property constants; no new event names or untyped properties.

- [ ] **Magic string event properties** — using `'status'`, `'asset'`, `'direction'` instead of `PERPS_EVENT_PROPERTY.STATUS`, `PERPS_EVENT_PROPERTY.ASSET`, etc. from `@metamask/perps-controller`.
- [ ] **Magic string event values** — using `'executed'`, `'long'`, `'market'` instead of `PERPS_EVENT_VALUE.STATUS.EXECUTED`, `PERPS_EVENT_VALUE.DIRECTION.LONG`, `PERPS_EVENT_VALUE.ORDER_TYPE.MARKET`.
- [ ] **New event instead of property** — creating a 9th event when the change should be a new `screen_type`, `interaction_type`, or `action_type` value on an existing event. The 8-event model is intentional (Segment cost optimization).
- [ ] **Missing `source` on screen view** — `PERPS_SCREEN_VIEWED` without `source` property loses navigation flow tracking. Source = current screen, not earlier in the chain.
- [ ] **Hardcoded source in reusable component** — reusable components (`PerpsMarketTypeSection`, `PerpsWatchlistMarkets`, `PerpsCard`) must receive `source` as a prop from the parent screen, not set it implicitly.
- [ ] **New screen/view without tracking** — adding a new view without `PERPS_SCREEN_VIEWED` event and a trace through the reviewed client's instrumentation.
- [ ] **Missing `completion_duration` on transaction events** — all transaction events (`PERPS_TRADE_TRANSACTION`, `PERPS_POSITION_CLOSE_TRANSACTION`, etc.) require duration tracking.

<a id="sentry-tracing"></a>

## Sentry Tracing

- [ ] **Unbounded background trace volume**: For unlock, polling, reconnect or fan-out instrumentation, estimate added spans at normal and retry load. Record sampling/deduplication and expected baseline impact before enabling the trace. Reuse an existing trace when it already measures the work.

Every async flow that affects perceived performance carries a named Sentry trace from the reviewed client's trace reference; no ad hoc trace names or missing end calls.

<a id="connection-websocket-architecture"></a>

## Connection & WebSocket Architecture

- [ ] **Cleanup has no owner for in-flight setup**: Register the owner before asynchronous initialization starts. Timeout, unmount and feature disable must retire that owner and prevent late activation. Cover pre-registration and post-ready paths separately; successful UI disposal must preserve an explicitly owned reuse/grace policy.

A single `PerpsAlwaysOnProvider` at the wallet root owns connect/disconnect; `PerpsConnectionProvider` only exposes connection state (`isEnabled`, `isFullScreen`, `suppressErrorView`) through the singleton connection manager.

- [ ] **A second lifecycle owner** — a provider, hook, or screen that calls connect/disconnect itself (or a `PerpsConnectionProvider` variant that tries to) creates reference-count bugs. Only `PerpsAlwaysOnProvider` manages the lifecycle.
- [ ] **Unthrottled WS → setState** — every WS tick triggers state update. Must use `useLivePrices` with appropriate `throttleMs` (100ms for charts, 2s for lists, 10s for order forms).
- [ ] **Per-component WS subscription** — creating a new WebSocket connection per component instead of using `PerpsStreamManager` shared subscriptions with reference counting.
- [ ] **WS subscription leak** — subscribing on mount without unsubscribing on unmount or market switch. `PerpsStreamManager` handles ref counting but custom subscriptions must clean up.
- [ ] **Stale data after async gap** — reading position/order state, awaiting something, then using the stale read. WS updates change state between awaits. Re-read after async boundaries.
- [ ] **Static WebView work coupled to live ticks** — a payload containing both `currentPrice` and static overlays can resend teardown/recreate work on every tick. Compare the static subset before mutating chart lines, do not force autoscale on a no-op update, and cover skip/clear behavior with executable helper tests rather than source-string assertions.
- [ ] **Missing cache invalidation** — after trade/withdrawal/position change, not calling `PerpsCacheInvalidator.invalidate()` for affected cache types (`positions`, `accountState`). Standalone queries on token detail pages show stale data.

<a id="data-flow-state"></a>

## Data Flow & State

- [ ] **A changed classification leaves old priority rules**: When a validation becomes advisory, audit message ranking and CTA gating together. A finished-input warning needs commit/blur state that clears on the next edit; interaction alone is insufficient. Test mixed blockers/advice and editing an already committed value.
- [ ] **State persists outside the rendered control**: Disabling new presses does not dismiss an open keypad or active gesture. Test the transition while editing, and preserve the intended input when live limits update.
- [ ] **React persistence mistaken for WebView synchronization**: Inline and fullscreen charts can remain mounted together. Prove the handoff updates each chart's local range/state, including subsequent stream updates.

- [ ] **Old context remains actionable**: On account, provider or network change, clear or re-key committed display/action state immediately. A generation guard against late writes does not invalidate data already shown. Test with the next request held open.
- [ ] **Unknown balance treated as usable balance**: Keep unresolved distinct from zero; never substitute a balance from another account. Verify the committing CTA remains disabled until the selected account/token inputs are valid.
- [ ] **Late defaults overwrite a user choice**: Typing, percent and MAX controls must all mark a value as user-edited. Hold metadata resolution until after each interaction and confirm the chosen value remains. Apply authoritative limit changes explicitly; a delayed persistence acknowledgment is not a new limit.

Controller → Redux → Hooks → Components. Standalone mode for lightweight queries without full init.

- [ ] **Direct controller call from component** — components calling `PerpsController.method()` directly instead of going through hooks (`usePerpsTrading`, `usePerpsAccount`, etc.).
- [ ] **Missing `accountState` check** — accessing positions/orders/balances without verifying accountState is loaded. Causes undefined errors on first load or account switch.
- [ ] **Derived flag promoted to structural state without its own lifecycle** — define initialization, every set condition, and every clear condition independently of the old string or transient value that first produced the flag. Test both set and clear paths.
- [ ] **Unknown async value treated as an absent blocker** — an alert may correctly stay hidden while balance or market data is unresolved, but the CTA must remain disabled through a separate unresolved-state check. Missing alert copy is not permission to submit.
- [ ] **Async flow loses ownership of cleanup** — fire-and-forget timers and navigation listeners need a generation guard plus `dispose()` on retry, unmount, and failure. Treat nested confirmation routes as part of the same flow so cleanup does not fire while the user is still inside it.
- [ ] **One in-flight mutation lock replaces earlier accepted outcomes** — serialize active requests separately from post-success reconciliation. Keep each accepted result keyed by provider and stable entity ID until an authoritative read or stream confirms it; clear the set when account, provider, network, or connection generation changes. Test sequential successes followed by a partial terminal update.
- [ ] **Stale position after close** — position in UI after close because local state not cleared or WS update not processed. Must refresh via `PerpsCacheInvalidator`.
- [ ] **Preload data not seeded** — new hook not using `getPreloadedData()` lazy initializer. First render shows skeleton instead of cached data from the 5-minute preload cycle.
- [ ] **Order state race** — submitting order and immediately reading order state. WS confirmation hasn't arrived. Use transaction receipt or poll with backoff.
- [ ] **Leverage/validation bypass** — allowing values outside market's `maxLeverage` or skipping pre-trade checks (balance, market open, position limit).

<a id="trade-flow-order-execution"></a>

## Trade Flow & Order Execution

- [ ] **Signed bounds collapsed into magnitudes**: A gain-side and loss-side RoE are different inputs. Preserve direction through clamps and conversions; test long and short positions at the accepted boundary, not only typical positive values.

Order submission runs the shared pre-trade checks, carries the user's slippage, and refreshes state after confirmation.

- [ ] **Pre-trade checks missing** — submitting trade without verifying: sufficient balance, market open, position limit, leverage within bounds, slippage tolerance set.
- [ ] **Post-trade state not refreshed** — after trade confirmation, not triggering refresh of balances, positions, orders. User sees stale data until next WS tick.
- [ ] **Missing slippage in order params** — creating order without slippage tolerance, or hardcoding slippage instead of user preference.

<a id="locale-coverage-orphaned-keys"></a>

## Locale Coverage & Orphaned Keys

- [ ] **Duplicate JSON keys shadow new copy**: Verify the containing locale object has one definition and search rendered copy across every test layer. A test accommodating duplicate labels may hide an ambiguous product label.

Removing a `strings(...)` call or deleting a helper that wrapped locale keys is a regression risk that is cheap to catch during review.

- [ ] **Hardcoded string replacing a `strings(...)` call** — verify locale coverage across `locales/languages/*.json` before accepting the change. A key translated in only some of the supported locales is a quantified regression, not a nit.
- [ ] **Orphaned locale keys** — when a PR deletes a function that called `strings(...)`, grep for the keys it used (e.g. `rg 'order_card\.(take_profit|stop|open_limit|close_limit)' app`). Dead keys accumulate silently and bloat the translation pipeline; flag them even when runtime is unaffected.
- [ ] **Test revert-sensitivity for locale keys** — mocked `strings` implementations that fall back to `|| key` render the raw key when a key goes stale, so an exact `getByText` assertion still fails on revert. Confirm that fallback exists before accepting a test as regression-proof; do not assume it.

<a id="test-layer-coverage"></a>

## Test Layer Coverage

- [ ] **Degenerate fixtures hide formula errors**: Choose values where competing calculations differ, such as a deeper order-book row with size unequal to cumulative total. Exercise each changed numerator, denominator or branch independently. Simulations must use real call-site inputs and the producer's quantization grid.
- [ ] **Clock control changes the test mechanism**: Pin the clock the component reads without disabling timers needed by asynchronous view assertions. Restore spies in shared teardown, including failure paths; cover active-to-terminal transitions as well as static states.
- [ ] **Numeric control units change partially**: A percent-domain conversion must preserve caller units, step, accessibility increments and echo suppression. Exercise changing bounds during a gesture; remounting on streaming values can reset input even when accessibility metadata is correct.

- [ ] **Assertions miss the behavior under review**: For order, visibility, size or color claims, assert the rendered outcome rather than component presence or arguments passed to a mocked hook. Confirm the assertion fails when that behavior is removed.

Choose the test layer that exercises the changed behavior with real state and dependencies. Preserve regression coverage when moving tests; use focused unit tests for isolated logic and contract tests. Client-specific file conventions and test tooling belong to the client overlay.

<a id="embedded-signer-boundaries"></a>

## Embedded Signer Boundaries

An embedded signer receives sensitive key material only after its communication boundary is established.

- [ ] **Navigation policy mistaken for network isolation**: An origin allowlist does not block fetch, XHR, WebSocket or subresource requests. Enforce and test outbound denial before handing key material to embedded code.
- [ ] **Bridge messages trusted by assertion**: Parse messages as unknown and validate message-specific inputs/results. Missing transport and unmount must reject pending work promptly. Bound recovery retries and use one deadline across readiness and execution.
