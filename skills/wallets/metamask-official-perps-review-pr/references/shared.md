# Shared Perps review rules

<a id="blocking-review-checks"></a>

## Blocking review checks

Every confirmed violation of an applicable Perps anti-pattern is blocking and requires `REQUEST_CHANGES`; never downgrade it to a non-blocking nit. Style suggestions outside these anti-patterns may remain non-blocking.

<a id="controller-portability-core"></a>

## Controller Portability (Core)

`PerpsController` lives in `core/packages/perps-controller` and is published as `@metamask/perps-controller`; Mobile, Extension and Terminal consume the package. Controller code must stay platform-agnostic, and app code must go through the published surface.

- [ ] **Platform import in controller** — `react-native`, `Engine`, `Sentry`, `DevLogger`, browser APIs, or extension globals imported in `packages/perps-controller`. All platform services must flow through `PerpsPlatformDependencies` (DI), passed as the `infrastructure` constructor param. No `__DEV__`, `window`, `chrome.*` or other host globals. When `PerpsPlatformDependencies` supplies a capability (e.g. `performance`), use it; web-standard `fetch`/`WebSocket` are allowed only where DI offers none.
- [ ] **Deep import from app code** — app files importing controller internals by path (`@metamask/perps-controller/dist/...`, a relative path into a linked checkout) instead of the package's public exports.
- [ ] **New dependency not in DI interface** — controller code reaching outside its boundary (e.g., importing a hook, React context, or an app utility). Everything the controller needs must come through `PerpsPlatformDependencies`.
- [ ] **Breaking the publisher contract** — changing PerpsController's public API (state shape, method signatures, event names) without considering its consumers. Controller is a publisher — Mobile, Extension and Terminal consume it.

<a id="perps-math-comes-from-the-controller"></a>

## Perps Math Comes From the Controller

Perps trading math (PnL, RoE, TP/SL trigger ↔ RoE/percentage, leverage, margin, liquidation, fees, account summary) must come from `@metamask/perps-controller`. Adding, changing or porting such math in a client (Mobile, Extension or Terminal) is blocking unless the PR moves it into the controller or, only when the resolved controller version exports no equivalent, links the Core ticket that does (TAT-4477).

- [ ] **Client-side trading math** — a client file computes one of these values itself instead of importing it from the controller package. Check the controller version the client's lockfile resolves (then core `main`) for equivalent math, pure formatters and constants. 'Equivalent' means same inputs, units and boundary behaviour; a same-named helper with different semantics is renamed, not reused. `shared-packages.md` lists the math that must move. Fee previews come from controller `calculateFees` quotes through the existing client fee hooks: `usePerpsOrderFees` on Mobile/Extension and `usePerpsCloseAllCalculations` for Mobile close-all. Paid fees come from fills through `usePerpsRecordedOrderFees`. Screens never compute rates, discounts or notional inline; close-all reuses the fee hook helpers. Controller 18+ quotes already contain the discounted `metamaskFeeRate`; never apply rewards/VIP discount twice. An older resolved controller applies it once inside the fee hook until it bumps.
- [ ] **Copy or port of existing logic** — a formula or behavior already present in the controller, shared utilities, another client or the same diff gets a second implementation, or a fix lands in only one copy. Copies drift (TP/SL price ↔ RoE existed three times with different results).

<a id="missing-numeric-data-stays-undefined"></a>

## Missing numeric data stays undefined

Missing Perps numeric data must remain `undefined` through provider adapters, controller state, selectors, hooks and calculations. Zero means an observed or computed zero from known inputs. It must never stand for missing, loading, failed or invalid data. This applies to prices, balances, PnL, fees, margin, leverage and percentages.

- [ ] **Missing data converted to zero**: Reject `value ?? 0`, `value || 0`, default parameters of `0`, and parsing or arithmetic that turns absent or invalid input into zero. Check availability before conversion or calculation; if a required input is missing, the result stays `undefined`. An explicit accumulator seed for known values is valid, but must not conceal an unavailable collection or missing required member.
- [ ] **Unknown treated as confirmed zero**: Preserve a genuine `0` with explicit availability checks. Do not use truthiness to decide whether a value exists. Keep actions that require the missing value disabled until it is available. Keep unresolved balance and other async blockers distinct from zero or absence; never substitute another account's balance. Submission requires valid selected account/token inputs and a separate unresolved-state check even when no alert is shown.
- [ ] **Reviewer proposes a fabricated value**: Review fixes follow the same rule. A crash or type error caused by missing data requires explicit missing-state handling, never a numeric fallback. Require separate cases for absent input, invalid input and genuine zero; verify missing inputs cannot enable submission or feed financial calculations as zero.
- [ ] **Placeholder written into numeric state**: Render missing values with display placeholders only at the formatting boundary:
  - `PERPS_CONSTANTS.FallbackPriceDisplay` (`'$---'`) — price not yet loaded
  - `PERPS_CONSTANTS.FallbackPercentageDisplay` (`'--%'`) — percentage not yet loaded
  - `PERPS_CONSTANTS.FallbackDataDisplay` (`'--'`) — generic data not yet loaded
  - `PERPS_CONSTANTS.ZeroAmountDisplay` (`'$0'`) / `ZeroAmountDetailedDisplay` (`'$0.00'`) — ONLY for actual confirmed zero values (e.g., no volume), never for "loading" or "unavailable"

<a id="magic-strings-magic-numbers-placeholder-values"></a>

## Magic Strings, Magic Numbers & Placeholder Values

Constants live in the controller package (`core/packages/perps-controller/src/constants/perpsConfig.ts`, exported by `@metamask/perps-controller`) and in the reviewed client's UI constants module. PRs must use these — not inline literals.

- [ ] **Inline timeout/delay values** — hardcoded `5000`, `10000`, `300` instead of `PERPS_CONSTANTS.WebsocketTimeout`, `PERPS_CONSTANTS.ConnectionTimeoutMs`, `PERFORMANCE_CONFIG.ValidationDebounceMs`, etc. Every timing constant has a named export.
- [ ] **Hardcoded leverage fallback** — using `3` or `50` instead of `PERPS_CONSTANTS.DefaultMaxLeverage` or `MARGIN_ADJUSTMENT_CONFIG.FallbackMaxLeverage`.
- [ ] **Hardcoded precision** — using `6`, `2`, `5` for decimal places instead of `DECIMAL_PRECISION_CONFIG.MaxPriceDecimals`, `MaxSignificantFigures`, `FallbackSizeDecimals`, or `CLOSE_POSITION_CONFIG.UsdDecimalPlaces`.
- [ ] **Hardcoded API URLs** — inline `'https://perps.api...'` instead of `DATA_LAKE_API_CONFIG.OrdersEndpoint`.
- [ ] **Hardcoded validation thresholds** — `20` for high leverage warning, `0.1` for price deviation, instead of `VALIDATION_THRESHOLDS.HighLeverageWarning`, `VALIDATION_THRESHOLDS.PriceDeviation`.
- [ ] **Hardcoded cache durations** — inline `5 * 60 * 1000` instead of `PERFORMANCE_CONFIG.MarketDataCacheDurationMs`, `FeeDiscountCacheDurationMs`, etc.

<a id="protocol-abstraction"></a>

## Protocol Abstraction

- [ ] **Execution identity inferred from display fields**: Preserve the venue's documented identity at the provider boundary and expose a stable opaque ID shared by REST and WebSocket paths. Equal order ID, time, size and price need not identify one fill. Do not deduplicate without that guarantee or key navigable history by array position. Check prepend stability and tied timestamps. Equality checks that suppress a snapshot or stream update must include the stable entity ID and every field a consumer reads (trigger price, order type, reduce-only). A valid empty snapshot replaces the cache. Test an ID-only replacement, a trigger-only change and populated-to-empty.

- [ ] **Entity ownership lost in transit**: Carry the entity's `providerId`, and any requested `accountId` or network, through transforms, fill aggregation, mutation params, batch partitioning, follow-up writes (edit, cancel, post-open TP/SL), cache keys and subscription params. Never fall back to the default provider or selected account when the entity names its owner. Apply provider-specific classification at the normalization boundary. Test two providers with a colliding symbol or order ID, and an explicit non-selected account.

All provider access must go through `AggregatedPerpsProvider` → `ProviderRouter`. HyperLiquid is primary; Lighter is feature-flagged (`perpsLighterProviderEnabled`).

- [ ] **Hardcoded provider** — uses a provider's API directly instead of going through `AggregatedPerpsProvider` / `ProviderRouter`. All operations must route through the abstraction.
- [ ] **Provider identity or capability hardcoded in client code**: no provider literal, venue-specific limit or request shape in components, hooks or feature code. Read provider and network from the entity (`market.providerId`, active network) and feature availability or limits from controller capabilities. Never compare against a provider literal or `PROVIDER_CONFIG.DefaultProvider` to decide ownership or support; `DefaultProvider` is only the routing default for an entity with no owner. Test a non-default provider and a changed default.
- [ ] **Provider-specific error handling** — catches errors from one provider but not others. All providers must have consistent error boundaries via the aggregated layer. Map controller `errorCode`, never message prose, to copy through the client's code table covering every exported code. Classify venue prose only at the provider boundary. Grep UI for regexes on error messages and raw `result.error` rendering.
- [ ] **Hardcoded market symbols** — string literals `"BTC"` or `"ETH"` instead of market config constants. Breaks when new markets or providers are added.
- [ ] **Executable precision differs from what the user confirms**: Round executable prices and sizes with the controller's provider-precision helpers and market `szDecimals`, never `toFixed(n)`, `Math.trunc` or raw float division. Any value the user confirms (input, preview, review dialog) equals the normalized value submitted. Read-only labels may use the `MarketDataFormatters` documented display rounding. Test a sub-cent price (0.0000123), a float-noise size (0.58×0.5 at szDecimals 2) and a 6+ significant-figure mid.
- [ ] **`detailedOrderType` rendered directly in UI** — `detailedOrderType` is provider-native text, not an enum. HyperLiquid returns, e.g., `Limit`, `Market`, `Stop Limit`, `Stop Market`, `Take Profit Limit`, `Take Profit Market`. Any UI that renders `detailedOrderType` directly is provider-dependent by construction. **Grep for `detailedOrderType` in any PR touching order display** — it should be mapped through a locale string or normalized constant, not rendered raw.

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
- [ ] **Per-consumer subscription bypasses the shared channel**: a hook or component subscribes directly to the controller or a transport instead of the client's ref-counted stream channel (`PerpsStreamManager` on Mobile/Extension). Flag it whether or not sockets multiply; claim extra connections only after showing two concurrent production consumers open separate sockets.
- [ ] **WS subscription leak** — subscribing on mount without unsubscribing on unmount or market switch. `PerpsStreamManager` handles ref counting but custom subscriptions must clean up.
- [ ] **Stale data after async gap** — reading position/order state, awaiting something, then using the stale read. WS updates change state between awaits. Re-read after async boundaries. After submitting an order, wait for its transaction receipt or poll with backoff rather than reading order state before WebSocket confirmation.
- [ ] **Static WebView work coupled to live ticks** — a payload containing both `currentPrice` and static overlays can resend teardown/recreate work on every tick. Compare the static subset before mutating chart lines, do not force autoscale on a no-op update, and cover skip/clear behavior with executable helper tests rather than source-string assertions.

<a id="data-flow-state"></a>

## Data Flow & State

- [ ] **Delayed balance tracker loses its initiating context**: Bind the initiating account, provider and network. The first channel delivery may replay persisted preload data; it is not proof of fresh credit. Channel clearing also occurs on reconnect, so it is not an account-change signal. A timeout means credit was not observed, not that funds are available. Test provider and network changes while the account address stays fixed.
- [ ] **A changed classification leaves old priority rules**: When a validation becomes advisory, audit message ranking and CTA gating together. A finished-input warning needs commit/blur state that clears on the next edit; interaction alone is insufficient. Test mixed blockers/advice and editing an already committed value.
- [ ] **State persists outside the rendered control**: Disabling new presses does not dismiss an open keypad or active gesture. Test the transition while editing, and preserve the intended input when live limits update.
- [ ] **React persistence mistaken for WebView synchronization**: Inline and fullscreen charts can remain mounted together. Prove the handoff updates each chart's local range/state, including subsequent stream updates.

- [ ] **Old context remains actionable**: On account, provider or network change, clear or re-key committed display/action state immediately. A generation guard against late writes does not invalidate data already shown. Test with the next request held open.
- [ ] **Late defaults overwrite a user choice**: Typing, percent and MAX controls must all mark a value as user-edited. Hold metadata resolution until after each interaction and confirm the chosen value remains. Apply authoritative limit changes explicitly; a delayed persistence acknowledgment is not a new limit.

Controller → Redux → Hooks → Components. Standalone mode for lightweight queries without full init.

- [ ] **Direct controller call from component** — components calling `PerpsController.method()` directly instead of going through hooks (`usePerpsTrading`, `usePerpsAccount`, etc.).
- [ ] **Missing `accountState` check** — accessing positions/orders/balances without verifying accountState is loaded. Causes undefined errors on first load or account switch.
- [ ] **Derived flag promoted to structural state without its own lifecycle** — define initialization, every set condition, and every clear condition independently of the old string or transient value that first produced the flag. Test both set and clear paths.
- [ ] **Async flow loses ownership of cleanup** — fire-and-forget timers and navigation listeners need a generation guard plus `dispose()` on retry, unmount, and failure. Treat nested confirmation routes as part of the same flow so cleanup does not fire while the user is still inside it. A lookup added before startup, unlock or deeplink navigation needs a short explicit deadline that falls back to the prior offline result; test with the request held pending.
- [ ] **One in-flight mutation lock replaces earlier accepted outcomes** — serialize active requests separately from post-success reconciliation. Keep each accepted result keyed by provider and stable entity ID until an authoritative read or stream confirms it; clear the set when account, provider, network, or connection generation changes. Test sequential successes followed by a partial terminal update.
- [ ] **Preload data not seeded** — new hook not using `getPreloadedData()` lazy initializer. First render shows skeleton instead of cached data from the 5-minute preload cycle.
- [ ] **Leverage/validation bypass** — allowing values outside market's `maxLeverage` or skipping pre-trade checks (balance, market open, position limit).

<a id="trade-flow-order-execution"></a>

## Trade Flow & Order Execution

- [ ] **Numeric meaning changes in transit**: Preserve each value's unit (coin vs USD, notional vs margin), price source (mark vs oracle vs mid) and sign/direction (long vs short, gain-side vs loss-side RoE) through adapters, conversions, clamps and labels. Test a short beside a long at the accepted boundary, leverage > 1 so notional ≠ margin, and mark ≠ oracle/mid.

Order submission runs the shared pre-trade checks, carries the user's slippage, and refreshes state after confirmation.

- [ ] **Pre-trade checks missing** — submitting trade without verifying: sufficient balance, market open, position limit, leverage within bounds, slippage tolerance set.
- [ ] **Post-trade state not refreshed** — after a confirmed trade, withdrawal or position change, refresh balances, positions and orders through `PerpsCacheInvalidator.invalidate()` for affected cache types (`positions`, `accountState`), including standalone token-detail queries. A closed position must clear from local or WebSocket-fed state. Branch on per-item results/`failureCount` before `success` (Core sets `success: true` on partial batches). Keep post-success refresh outside the mutation's catch so a failed read never reports a failed, retryable write. Test 2-of-3 partial and a throwing refetch after success.
- [ ] **Missing or hardcoded slippage**: Every market leg (open, close, flip/reverse, TP/SL trigger) sends `maxSlippageBps` resolved from the saved user preference, falling back to `ORDER_SLIPPAGE_CONFIG` only when none is saved; never an inline literal. Test a strict saved value and an unset preference per action.

<a id="test-layer-coverage"></a>

## Test Layer Coverage

- [ ] **Degenerate fixtures hide formula errors**: Choose values where competing calculations differ, such as a deeper order-book row with size unequal to cumulative total. Exercise each changed numerator, denominator or branch independently. Simulations must use real call-site inputs and the producer's quantization grid.
- [ ] **Numeric control units change partially**: A percent-domain conversion must preserve caller units, step, accessibility increments and echo suppression. Exercise changing bounds during a gesture; remounting on streaming values can reset input even when accessibility metadata is correct.

Mobile and Extension use their owning testing skill for the following two generic checks; clients without an applicable testing owner apply these fallback checks here:

- [ ] **Clock control changes the test mechanism**: Pin the clock the component reads without disabling timers needed by asynchronous view assertions. Restore spies in shared teardown, including failure paths; cover active-to-terminal transitions as well as static states.
- [ ] **Assertions miss the behavior under review**: For order, visibility, size or color claims, assert the rendered outcome rather than component presence or arguments passed to a mocked hook. Confirm the assertion fails when that behavior is removed.

<a id="embedded-signer-boundaries"></a>

## Embedded Signer Boundaries

An embedded signer receives sensitive key material only after its communication boundary is established.

- [ ] **Navigation policy mistaken for network isolation**: An origin allowlist does not block fetch, XHR, WebSocket or subresource requests. Enforce and test outbound denial before handing key material to embedded code.
- [ ] **Bridge messages trusted by assertion**: Parse messages as unknown and validate message-specific inputs/results. Missing transport and unmount must reject pending work promptly. Bound recovery retries and use one deadline across readiness and execution.
