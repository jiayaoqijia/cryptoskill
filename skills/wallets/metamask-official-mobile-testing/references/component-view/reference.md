# Running Tests, Self-Review, and Diagnosing Failures

Use this reference when you need to **run** component view tests, **self-review** after tests pass, or **diagnose and fix** failures. It also covers assertion patterns, deterministic fiat, and What NOT to Do.

Reference: [SKILL.md](../SKILL.md) · [Writing Tests](writing-tests.md) · [Navigation & Mocking](navigation-mocking.md)

---

## Table of contents

- [Deterministic Fiat Assertions](#deterministic-fiat-assertions)
- [Run the Tests](#run-the-tests)
- [Self-Review Checklist](#self-review-checklist)
- [Diagnosing Failures](#diagnosing-failures)
- [Assertion Patterns](#assertion-patterns)
- [What NOT to Do](#what-not-to-do)
- [Quick Reference](#quick-reference)

---

## Deterministic Fiat Assertions

Pass `deterministicFiat: true` whenever a test asserts exact currency values. This injects stable exchange rates:

```typescript
const { getByText } = renderBridgeView({
  deterministicFiat: true,
  overrides: { bridge: { sourceAmount: '1' } },
});
expect(getByText('$2,000.00')).toBeOnTheScreen();
```

---

## Run the Tests

**Always use `jest.config.view.js`** — the default Jest config does not apply the component view test rules.

```bash
# Run a single file
yarn jest -c jest.config.view.js app/components/UI/Bridge/Views/BridgeView/BridgeView.view.test.tsx --runInBand --silent --coverage=false

# Run a specific test by name
yarn jest -c jest.config.view.js <file> -t "renders the source token" --runInBand --silent --coverage=false

# Watch mode
yarn jest -c jest.config.view.js <file> --watch

# Coverage for a feature folder (use this, not --coverage directly — avoids OOM)
yarn test:view:coverage:folder app/components/UI/MyFeature
```

---

## Self-Review Checklist

Before declaring the task done, go through this checklist for every test written or modified. If any item fails, fix it and re-run.

| #   | Check                                                                                                                                                                                                                                                        | What to do if it fails                                                 |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| 1   | **No render scenarios** — every test has at least one `fireEvent`, `waitFor`/`findBy`, `store.dispatch`, or Engine spy                                                                                                                                       | Rewrite the test to add a user interaction or system reaction          |
| 2   | **No selector mocking** — no `(useSelector as jest.Mock).mockImplementation(...)` anywhere in the file                                                                                                                                                       | Remove; drive behavior through state overrides instead                 |
| 3   | **No fake timers** — no `jest.useFakeTimers()`, `jest.advanceTimersByTime()`, or `jest.useRealTimers()`                                                                                                                                                      | Remove fake timers; use `waitFor` / `findBy` for async flows           |
| 4   | **Data-completeness test exists** — if the view loads data asynchronously (API, Engine polling), there is one test that waits for the load and validates all fields of all items in the full base mock using `within()` per row                              | Add the data-completeness test                                         |
| 5   | **Filter/segmentation tests have paired assertions** — every test that selects a filter or changes a network asserts both what appears (`findByTestId`) AND what disappears (`queryByTestId(...).not.toBeOnTheScreen()`) for each item from the previous set. Spy-only checks (refetch count / analytics) are **not** enough | Seed distinct before/after rows; add the missing negative assertions |
| 6   | **No raw strings in `getByTestId` / `findByTestId` / `queryByTestId`** — all test IDs reference constants from the component's `ComponentName.testIds.ts`                                                                                                    | Create or update the testIds file; replace raw strings with constants  |
| 7   | **Any `jest.mock` for non-Engine modules is flagged** — if a service module is mocked directly, the `eslint-disable` comment is present and a tracking issue is linked                                                                                       | Add the comment and issue link                                         |
| 8   | **AAA formatting** — blank lines between the Arrange, Act, and Assert blocks in every test                                                                                                                                                                   | Add the blank line separators                                          |
| 9   | **Import order** — `mocks.ts` is first; remaining order follows project ESLint rules                                                                                                                                                                         | Ensure `mocks.ts` is the very first import; reorder the rest as needed |
| 10  | **No stale press targets** — do not `fireEvent.press` a node held across `await`s when the UI re-renders (live countdown, polling). Re-query with `getByTestId` / `findByTestId` immediately before press                                                     | Re-query right before press; see What NOT to Do                        |
| 11  | **Loading asserts match real UX** — pending-phase tests assert skeleton / “not yet visible”, not optimistic titles the production screen does not show while `isLoading`                                                                                      | Rename and assert the real pending UI; resolve then assert loaded state |
| 12  | **Pull-to-refresh uses `refreshControl.props.onRefresh`** — not `fireEvent(scrollView, 'refresh')`                                                                                                                                                            | Call the prop handler inside `act`                                     |
| 13  | **Unit→CV migrations keep assert specificity** — deleted unit payload fields (`tabId`, formatted dates, full analytics) still appear in the CV replacement                                                                                                   | Restore dropped fields in CV or KEEP a focused unit; see unit-cv-overlap |
| 14  | **Awaits cover the asserted content, not just its container** — after `await findByTestId(CONTAINER)`, no synchronous `getBy*` asserts a value that has its own async source (child query, debounce, skeleton)                                                | Await the gated value with `findBy*` first, then re-query the container and scope the sync asserts |
| 15  | **No nested `find*` inside `waitFor`** — no `waitFor(async () => { await findBy*(...) })`. `findBy*` already polls with the same 1s default timeout                                                                                                         | Use `await findBy*` **or** `waitFor(() => { getBy*; expect(...) })` with `{ timeout }` |

---

## Diagnosing Failures

### Identify the error type first

| Error pattern                                                          | Likely cause                                                                                         | Fix                                                                                                                 |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `jest.mock is not allowed in *.view.test.*`                            | Arbitrary `jest.mock` added to test                                                                  | Remove it; drive via state instead                                                                                  |
| `Unable to find an element with testID: xxx`                           | State not providing needed data, or element hidden                                                   | Add the relevant state via overrides or check rendering condition                                                   |
| `Unable to find … route-X` after press; dump still on the source screen | Held element went stale (live clock / polling re-render); `fireEvent.press` was a no-op             | Re-query immediately before press: `fireEvent.press(getByTestId(...))` — never press a node captured across `await`s |
| `Unable to find an element with text: X`, but the dump shows the container and empty `pointerEvents="none"` views where the value belongs | The value is still behind a `Skeleton` — a child query / debounce has not settled, while the container rendered on the first tick | `await findByText('X')` before the sync `within(...)` asserts; the container appearing does not mean its values have loaded |
| `Cannot read property 'X' of undefined`                                | Preset missing a required state slice                                                                | Add `.withMinimalXController()` or override in preset                                                               |
| `Warning: An update was not wrapped in act(...)`                       | Async state update not awaited                                                                       | Use `await waitFor(...)`                                                                                            |
| `No QueryClient set`                                                   | Missing provider — not in Engine mock                                                                | Add to mocks.ts or wrap with QueryClientProvider in renderer                                                        |
| Flakey number assertions                                               | Non-deterministic exchange rates                                                                     | Add `deterministicFiat: true`                                                                                       |
| Test passes locally, fails in CI                                       | Time-sensitive assertions, stale press under CI load, or a sync assert on content that is still loading | Use `waitFor` / `findBy`; re-query before press when the UI re-renders on a timer; await each async-gated value    |
| `Timed out in waitFor.` with no assertion detail                       | Nested `find*` inside `waitFor` — both share the 1s default; the outer waiter expires first             | Use `await findBy*` **or** `waitFor(() => getBy*)` with `{ timeout }`; never `waitFor(async () => findBy*)`      |
| Pull-to-refresh never refetches                                        | `fireEvent(scrollView, 'refresh')` did not hit the handler                                           | `await act(async () => { await scrollView.props.refreshControl.props.onRefresh(); })`                             |
| Sheet / branch `testID` missing                                        | Remote feature flag off in Redux; UI routes elsewhere                                                | Override `RemoteFeatureFlagController` / preset so the gated UI mounts                                            |

### Inspect what's rendered

```typescript
// Add temporarily inside the test
const { debug } = renderBridgeView();
debug(); // prints full component tree
```

### Check that state data reaches the component

Add a `console.log` in the component temporarily, or use `debug()` to confirm the Redux state is wired correctly before writing assertions.

### Check stale presets

When a controller's state shape changes (e.g. a new required field added to `BridgeController`), the preset becomes stale. Compare the component's actual selector usage against what the preset provides.

---

## Assertion Patterns

```typescript
// Presence / absence
expect(getByText('Label')).toBeOnTheScreen();
expect(queryByText('Label')).not.toBeOnTheScreen();

// Enabled / disabled state
expect(getByTestId('cta-button')).toBeEnabled();
expect(getByTestId('cta-button')).toBeDisabled();

// After interaction
fireEvent.press(getByTestId('some-button'));
await waitFor(() => expect(getByText('Result')).toBeOnTheScreen());

// findBy* already waits — do not wrap it in waitFor
expect(await findByText('Token A')).toBeOnTheScreen();

// waitFor + getBy* when you need extra time or a length check
await waitFor(
  () => {
    expect(getAllByTestId(MyViewSelectorsIDs.ROW)).toHaveLength(3);
  },
  { timeout: 5000 },
);

// Navigation assertion
await findByTestId(`route-${Routes.SOME_SCREEN}`);

// findByTestId 3rd-arg timeout (NOT 2nd arg)
await findByTestId('my-element', {}, { timeout: 3000 });

// Re-query before press when the target can re-render (live countdown, polling).
await findByTestId(MyViewSelectorsIDs.CARD);
await findByTestId(MyViewSelectorsIDs.LIVE_BADGE);
fireEvent.press(getByTestId(MyViewSelectorsIDs.CARD));

// Pull-to-refresh — call the RefreshControl handler (fireEvent 'refresh' often no-ops)
await act(async () => {
  await scrollView.props.refreshControl.props.onRefresh();
});

// Within a subtree — scope queries to avoid false positives when the same text or
// testID appears in multiple list items (e.g., every row shows a "price" label).
// Use within(rowElement) to constrain the query to a single row.
import { within } from '@testing-library/react-native';
const card = getByTestId(MyViewSelectorsIDs.TOKEN_CARD_ETH);
expect(within(card).getByText('ETH')).toBeOnTheScreen();
expect(within(card).getByText('$2,000.00')).toBeOnTheScreen();

// Async-gated value inside a container — await the value itself, then re-query the
// container so the scoped sync asserts run against the settled tree.
await findByTestId(MyViewSelectorsIDs.ROW_CONTAINER);
await findByText('$60'); // behind a skeleton until a child query resolves
const row = getByTestId(MyViewSelectorsIDs.ROW_CONTAINER);
expect(within(row).getByText('$60')).toBeOnTheScreen();
expect(within(row).getByTestId(MyViewSelectorsIDs.CASH_OUT_BUTTON)).toBeOnTheScreen();
```

---

## What NOT to Do

```typescript
// ❌ Render scenario — no interaction, no system reaction, just static visibility
it('renders input areas and hides confirm button without tokens or amount', () => {
  const { getByTestId, queryByTestId } = renderBridgeView({ overrides: { ... } });
  expect(getByTestId(SOURCE_AREA)).toBeOnTheScreen();     // render check
  expect(getByTestId(DEST_AREA)).toBeOnTheScreen();       // render check
  expect(queryByTestId(CONFIRM_BUTTON)).toBeNull();       // render check
});
// More assertions does NOT make it a better test if they're all static.
// ✅ Instead: drive the test through a user interaction, Redux action, or Engine spy

// ❌ Arbitrary mock — blocked by ESLint and runtime guard
jest.mock('../../some/hook', () => ({ useMyHook: jest.fn() }));

// ❌ Mocking a selector
(useSelector as jest.Mock).mockImplementation(...);

// ❌ Fake timers
jest.useFakeTimers();

// ❌ Snapshot assertion
expect(wrapper).toMatchSnapshot();

// ❌ Rebuilding the whole state from scratch
renderComponentViewScreen(MyView, { name: 'X' }, {
  state: { engine: { backgroundState: { /* 200 lines */ } } },
});
// ✅ Instead: use a preset + minimal overrides

// ❌ Hold a node across awaits when the UI re-renders (live countdown, polling)
const card = await findByTestId(MyViewSelectorsIDs.CARD);
await findByTestId(MyViewSelectorsIDs.LIVE_BADGE);
fireEvent.press(card); // stale under CI — press may be a no-op
// ✅ Re-query immediately before press
await findByTestId(MyViewSelectorsIDs.CARD);
await findByTestId(MyViewSelectorsIDs.LIVE_BADGE);
fireEvent.press(getByTestId(MyViewSelectorsIDs.CARD));

// ❌ Treat the container's arrival as proof its values have loaded
const row = await findByTestId(MyViewSelectorsIDs.ROW_CONTAINER);
expect(within(row).getByText('$50 on Yes to win $50')).toBeOnTheScreen(); // static prop — always there
expect(within(row).getByText('$60')).toBeOnTheScreen(); // still a skeleton under CI timing
// ✅ Await the gated value, then re-query the container for the scoped sync asserts
await findByTestId(MyViewSelectorsIDs.ROW_CONTAINER);
await findByText('$60');
const settledRow = getByTestId(MyViewSelectorsIDs.ROW_CONTAINER);
expect(within(settledRow).getByText('$60')).toBeOnTheScreen();
// Static props in the same row render immediately, so a neighbouring assert
// passing proves nothing about the gated one.

// ❌ Nest find* inside waitFor — double polling, both default to 1s
await waitFor(async () => {
  expect(await findByText('Token A')).toBeOnTheScreen();
});
// ✅ One waiter: findBy* already polls
expect(await findByText('Token A')).toBeOnTheScreen();
// ✅ Or waitFor + synchronous getBy* when you need extra time or a count
await waitFor(
  () => {
    expect(getAllByTestId(MyViewSelectorsIDs.ROW)).toHaveLength(3);
  },
  { timeout: 5000 },
);

// ❌ Custom nested navigator only to assert navigation occurred
extraRoutes: [{ name: Routes.FEATURE.ROOT, Component: NestedStackProbe }];
// ✅ Default route probe when you only need to prove navigation
extraRoutes: [{ name: Routes.FEATURE.ROOT }];

// ❌ Filter/segmentation: analytics or refetch count only
await waitFor(() => expect(listSpy.mock.calls.length).toBeGreaterThan(n));
expect(trackFilterSpy).toHaveBeenCalled();
// ✅ Assert both list membership sides (Golden Rule 10)
expect(await findByText('Games market')).toBeOnTheScreen();
fireEvent.press(getByText('Props'));
expect(await findByText('Props market')).toBeOnTheScreen();
expect(queryByText('Games market')).not.toBeOnTheScreen();

// ❌ Claim optimistic title while loading when production shows a skeleton
expect(getByText(routeTitle)).toBeOnTheScreen(); // while getMarket is pending
// ✅ Assert the real pending UI, then resolve
expect(await findByTestId(MyDetailSelectorsIDs.SKELETON)).toBeOnTheScreen();

// ❌ fireEvent(scrollView, 'refresh') — often never calls onRefresh in RNTL
// ✅ await act(async () => { await scrollView.props.refreshControl.props.onRefresh(); });

// ❌ Weaken unit→CV analytics: drop tabId/filterId after deleting the full unit assert
expect(trackSpy).toHaveBeenCalledWith(expect.objectContaining({ feedId }));
// ✅ Keep the same payload specificity the unit had
expect(trackSpy).toHaveBeenCalledWith(
  expect.objectContaining({ feedId, tabId, filterId, entryPoint }),
);

// ❌ Raw string literal in getByTestId / findByTestId / queryByTestId
getByTestId('my-view-scroll-view');
queryByTestId('confirm-button');

// ✅ Use the constant from the component's testIds file
import { MyViewSelectorsIDs } from './MyView.testIds';
getByTestId(MyViewSelectorsIDs.SCROLL_VIEW);
queryByTestId(MyViewSelectorsIDs.CONFIRM_BUTTON);

// If the testIds file does not exist yet, create it first:
// export const MyViewSelectorsIDs = {
//   SCROLL_VIEW: 'my-view-scroll-view',
//   CONFIRM_BUTTON: 'my-view-confirm-button',
// } as const;
```

---

## Quick Reference

```bash
# Run component view tests
yarn jest -c jest.config.view.js <path> --runInBand --silent --coverage=false

# Coverage for a feature folder
yarn test:view:coverage:folder app/components/UI/MyFeature

# Lint check
yarn eslint <path/to/test.tsx>
```

**Key locations:**

| What                           | Where                                                          |
| ------------------------------ | -------------------------------------------------------------- |
| Engine + native mocks          | `tests/component-view/mocks.ts`                                |
| render, renderScreenWithRoutes | `tests/component-view/render.tsx`                              |
| StateFixtureBuilder            | `tests/component-view/stateFixture.ts`                         |
| HTTP API mocks (nock)          | `tests/component-view/api-mocking/` (per-feature)              |
| Feature renderers (per view)   | `tests/component-view/renderers/` (e.g. bridge, wallet)        |
| Feature presets (per view)     | `tests/component-view/presets/` (e.g. bridge, wallet)          |
| DeepPartial type               | `app/util/test/renderWithProvider`                             |
| Routes                         | `app/constants/navigation/Routes.ts`                           |
| Skill + rules                  | `.agents/skills/mms-mobile-testing/` (SKILL.md + references/component-view/) |
