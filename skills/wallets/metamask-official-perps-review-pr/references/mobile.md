# metamask-mobile review rules

<a id="agentic-testability-testids"></a>

## Agentic Testability (testIDs)

PRs that touch UI components must include testIDs so agentic recipes and E2E tests can navigate and assert on the app without manual interaction.

- [ ] **Missing testID on interactive elements** — any `TextInput`, `Pressable`, `Button`, or touchable in a new or modified component without a `testID` prop. Agentic recipes use `app-state.sh press <testID>` and `eval_sync` fiber-walk queries to interact with and assert on UI. A missing testID weakens stable automation; inspect supported semantic or accessibility selectors before claiming runtime validation is blocked. Static review reports the missing identifier separately from missing runtime evidence.
- [ ] **testID not in `Perps.testIds.ts`** — testIDs defined as inline strings instead of exported constants from `app/components/UI/Perps/Perps.testIds.ts`. All testIDs must be centralized so recipes can reference them by constant name.
- [ ] **testID missing from the element that holds the value** — adding testID to a wrapper View instead of the `TextInput` or Text that actually contains the value. CDP fiber-walk reads `value` from the React element with the matching testID — the testID must be on the element that owns the state.
- [ ] **TP/SL price inputs without testID** — the trigger price `TextInput` components in `PerpsTPSLView` (and similar order-form screens) frequently lack testIDs, making stable value assertions harder. Any PR touching these screens must add `testID` to both the Take Profit and Stop Loss price inputs.

<a id="navigation-exit-parity"></a>

## Navigation Exit Parity

A navigation fix must cover every way the user can leave the screen.

- [ ] **Only the header back action is fixed**: Apply the same history/fallback policy to header back, Android hardware back and native gestures. Preserve entry/history provenance through push, replace and reset paths. Runtime QA must name any gesture path it cannot prove. Android hardware back includes every native `Modal` (`onRequestClose`) and `react-native-modal` (`onBackButtonPress`), in every layout.

<a id="native-modal-layout"></a>

## Native Modal Layout

- [ ] **Modal wrapper omitted in width-constrained layouts** — in the Pro layout, parent columns are width-constrained; bottom sheets must be wrapped in a Modal so they are not clipped. The immediate wrapper child is a plain `View` (not a styled container).

<a id="mobile-controller-integration-mocks"></a>

## Mobile Controller Integration Mocks

- [ ] **Controller bump treated as lockfile-only** — inspect changed controller `dist` call sites against Mobile's hand-written integration mocks, then run the Perps integration suites. Object-literal mocks cast through `jest.Mocked` can hide newly required methods from typecheck.

<a id="mobile-trace-instrumentation"></a>

## Mobile Trace Instrumentation

Use `docs/perps/perps-sentry-reference.md` for Mobile trace names and lifecycle.

- [ ] **New screen without `usePerpsMeasurement`** — every new view needs a Sentry performance trace with appropriate `conditions` for when data is loaded.
- [ ] **Missing error context** — `Logger.error()` calls without `{ feature: 'perps', context: 'ClassName.method', provider, network }`. Sentry filtering depends on these fields.
- [ ] **Missing `ensureError()` wrapper** — catching errors without `ensureError(error)` before passing to `Logger.error()`. Non-Error objects crash Sentry reporting.
- [ ] **New trace without TraceName enum** — hardcoded trace name strings instead of adding to `TraceName` enum in `app/util/trace.ts`.
- [ ] **Missing `endTrace` in finally block** — `trace()` started but `endTrace()` not in a `finally` block. Orphaned traces leak in Sentry.

<a id="mobile-reference-paths"></a>

## Mobile Reference Paths

Mobile UI constants live in `app/components/UI/Perps/constants/perpsConfig.ts`.
Use `docs/perps/perps-metametrics-reference.md` for Mobile event definitions; controller constants remain the shared contract.
A change to a pattern documented in `docs/perps/` updates that document in the same PR.

<a id="mobile-test-layers"></a>

## Mobile Test Layers

- [ ] **Controller/provider flow faked with mocks** — order/close/flip/validation flows must exercise the real `HyperLiquidProvider` / `TradingService` chain through the Perps harnesses (`tests/integration/harnesses/perps*`), with only the I/O boundary mocked.
