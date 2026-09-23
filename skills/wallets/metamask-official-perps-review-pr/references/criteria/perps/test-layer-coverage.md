# Test Layer Coverage

- **Assertions miss the behavior under review**: For order, visibility, size or color claims, assert the rendered outcome rather than component presence or arguments passed to a mocked hook. Confirm the assertion fails when that behavior is removed.

Cover every test in its best-fit layer (view, integration, unit); broad mock-heavy unit tests are a review smell. **Same rule as the testing domain's `knowledge/testing-layers.md` (Mobile; installed beside the testing skills):** Screen/view behavior through rendered UI and app state defaults to `*.view.test.tsx`; app-to-controller flows (real `HyperLiquidProvider` / `TradingService` behavior with only the I/O boundary mocked) belong in `*.integration.test.ts` via the perps harnesses; unit tests only for pure logic, narrow contracts, or when the higher layers cannot cover (smallest focused test + reason). Broad unit tests that render a page and mock hooks/selectors, or that mock the controller to fake a flow, are a review smell.

Perps-specific enforcement:

- **Component-view behavior tested as a unit test** — files such as `ui/pages/perps/**/index.test.tsx` or `app/components/UI/Perps/**/*.test.tsx` that render a whole page/view and assert UI behavior should be converted to `*.view.test.tsx` using the component-view test framework/skill.
- **Controller/provider flow faked with mocks** — order/close/flip/validation flows that mock `HyperLiquidProvider` or `TradingService` to simulate behavior should be covered by `*.integration.test.ts` through the perps harnesses (`tests/integration/harnesses/perps*`), which run the real controller code with only the I/O boundary mocked. See `mobile-testing` → `references/integration.md`.
- **Hook/selector mocking in a page behavior test** — mocking selectors, hooks, or service modules to force page state bypasses the real state wiring. Drive behavior through framework state presets/renderers instead. If the framework cannot cover the case yet, keep the unit test focused and link a follow-up for the missing framework support.
- **Coverage drops during conversion** — converting to component-view or integration tests must preserve the same coverage intent. If a scenario cannot move layer, document why and retain the smallest focused unit test needed to keep coverage.
