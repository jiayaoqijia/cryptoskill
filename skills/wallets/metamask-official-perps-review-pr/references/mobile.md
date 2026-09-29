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

- [ ] **Only the header back action is fixed**: Apply the same history/fallback policy to header back, Android hardware back and native gestures. Preserve entry/history provenance through push, replace and reset paths. Runtime QA must name any gesture path it cannot prove.

<a id="native-modal-layout"></a>

## Native Modal Layout

- [ ] **Modal wrapper omitted in width-constrained layouts** — in the Pro layout, parent columns are width-constrained; bottom sheets must be wrapped in a Modal so they are not clipped. Android additionally requires `onRequestClose` on the Modal and a plain `View` (not a styled container) as the immediate wrapper child.

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

<a id="mobile-test-layers"></a>

## Mobile Test Layers

Cover every test in its best-fit layer (view, integration, unit); broad mock-heavy unit tests are a review smell. **Same rule as the testing domain's `knowledge/testing-layers.md` (Mobile; installed beside the testing skills):** Screen/view behavior through rendered UI and app state defaults to `*.view.test.tsx`; app-to-controller flows (real `HyperLiquidProvider` / `TradingService` behavior with only the I/O boundary mocked) belong in `*.integration.test.ts` via the perps harnesses; unit tests only for pure logic, narrow contracts, or when the higher layers cannot cover (smallest focused test + reason). Broad unit tests that render a page and mock hooks/selectors, or that mock the controller to fake a flow, are a review smell.

Perps-specific enforcement:

- [ ] **Component-view behavior tested as a unit test** — files such as `app/components/UI/Perps/**/*.test.tsx` that render a whole page/view and assert UI behavior should be converted to `*.view.test.tsx` using the component-view test framework/skill.
- [ ] **Controller/provider flow faked with mocks** — order/close/flip/validation flows that mock `HyperLiquidProvider` or `TradingService` to simulate behavior should be covered by `*.integration.test.ts` through the perps harnesses (`tests/integration/harnesses/perps*`), which run the real controller code with only the I/O boundary mocked. See `mobile-testing` → `references/integration.md`.
- [ ] **Hook/selector mocking in a page behavior test** — mocking selectors, hooks, or service modules to force page state bypasses the real state wiring. Drive behavior through framework state presets/renderers instead. If the framework cannot cover the case yet, keep the unit test focused and link a follow-up for the missing framework support.
- [ ] **Coverage drops during conversion** — converting to component-view or integration tests must preserve the same coverage intent. If a scenario cannot move layer, document why and retain the smallest focused unit test needed to keep coverage.
