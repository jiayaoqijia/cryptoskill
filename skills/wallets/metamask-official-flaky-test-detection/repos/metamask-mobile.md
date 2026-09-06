---
repo: metamask-mobile
parent: flaky-test-detection
---

## Pattern table

| ID | Pattern | Severity |
|----|---------|----------|
| J1 | `async` callback without `act()` wrapping a state update | Critical |
| J2 | Real timers where fake timers are needed | High |
| J3 | Missing `jest.clearAllMocks()` / `jest.resetAllMocks()` | High |
| J4 | `waitFor` without a real assertion inside | High |
| J5 | Incomplete mock store state | Medium |
| J6 | Arbitrary `setTimeout`/`sleep` in test body | High |
| J7 | Non-deterministic data: `Date.now()`, `Math.random()`, unstubbed network | Medium |
| J8 | `jest.useFakeTimers()` combined with `waitFor` | High |
| J9 | Module-level mutable `let` bindings not reset in `beforeEach` | High |
| J10 | `jest.spyOn` without `jest.restoreAllMocks()` in `afterEach` | Medium |

---

### J1 — Missing `act()` on async state updates

Symptoms: intermittent `TypeError: terminated` or `SocketError: other side closed`.

Triggers: `refreshControl.props.onRefresh()`, `button.props.onPress()` when handler is `async`, any prop callback that calls `setState` or dispatches a Redux action.

```ts
// ❌ async state-update trigger outside act() — race condition
// Real occurrence: TokenList.test.tsx, NetworkMultiSelector.test.tsx
it('calls onRefresh when triggered', () => {
  const { getByTestId } = renderComponent({ onRefresh });
  const refreshControl = getByTestId(TOKENS_CONTAINER_LIST).props.refreshControl;
  refreshControl.props.onRefresh();                  // ← missing act()
  expect(onRefresh).toHaveBeenCalledTimes(1);
});

// ✅
it('calls onRefresh when triggered', async () => {
  const { getByTestId } = renderComponent({ onRefresh });
  const refreshControl = getByTestId(TOKENS_CONTAINER_LIST).props.refreshControl;
  await act(async () => {
    await refreshControl.props.onRefresh();
  });
  expect(onRefresh).toHaveBeenCalledTimes(1);
});
```

---

### J2 — Real timers where fake timers are needed

Use when the SuT has timer-driven behavior (debounce, polling interval, timeout) that must be triggered by advancing time. When sleep is used only as a synchronization barrier, use `waitFor` instead (J6).

```ts
// ❌ wall-clock timing — flaky under load
await new Promise((r) => setTimeout(r, 3000));
expect(screen.getByTestId('error-message')).toBeOnTheScreen();

// ✅
beforeEach(() => { jest.useFakeTimers(); });
afterEach(() => { jest.useRealTimers(); });

it('shows error after retry timeout', () => {
  render(<RetryComponent />);
  act(() => { jest.advanceTimersByTime(3000); });
  expect(screen.getByTestId('error-message')).toBeOnTheScreen();
});
```

---

### J3 — Shared mock state

```ts
// ❌ call history bleeds between tests
// Real occurrence: BrazeBannerCard.test.tsx, WalletHomeOnboardingSteps.test.tsx (124 files)
it('tracks first event', () => {
  fireEvent.press(screen.getByTestId('action-button'));
  expect(mockTrackEvent).toHaveBeenCalledTimes(1); // passes
});
it('tracks second event', () => {
  fireEvent.press(screen.getByTestId('action-button'));
  expect(mockTrackEvent).toHaveBeenCalledTimes(1); // fails — count is 2
});

// ✅
beforeEach(() => { jest.clearAllMocks(); }); // clears call counts, keeps implementations
afterEach(() => { jest.resetAllMocks(); });  // resets implementations set per-test
```

---

### J4 — `waitFor` without assertion

```ts
// ❌ resolves immediately — subsequent assertion races async work
await waitFor(() => {});
expect(screen.getByTestId('result')).toBeOnTheScreen();

// ❌ async callback in waitFor — unhandled rejections can silently pass
await waitFor(async () => {
  await someAsyncSetup();
  expect(screen.getByTestId('result')).toBeOnTheScreen();
});

// ✅ synchronous assertion inside waitFor
await waitFor(() => {
  expect(screen.getByTestId('result')).toBeOnTheScreen();
});
```

---

### J5 — Incomplete mock store state

```ts
// ❌ undefined slices cause intermittent selector errors
// Real occurrence: SnapDialogApproval.test.tsx, TokenList.test.tsx
const store = mockStore({});

// ✅ every slice the component accesses must be present
const store = configureMockStore(middleware)({
  metamask: mockMetamask,
  engine: { backgroundState: { ...initialState } },
  settings: settingsInitialState,
});
```

---

### J6 — Arbitrary sleep

The most common form in this codebase is the zero-delay flush — appears in 321 places across 63 files (e.g. `ChoosePassword/index.test.tsx`, `CardHome/CardHome.test.tsx`). Even `setTimeout(resolve, 0)` is non-deterministic under load.

```ts
// ❌ zero-delay flush — still a real timer, flaky under load
// Real occurrence: ChoosePassword/index.test.tsx (35×), Wallet/index.test.tsx
await act(async () => {
  await new Promise((resolve) => setTimeout(resolve, 0));
});

// ❌ long real wait — RewardsController.test.ts
await new Promise((resolve) => setTimeout(resolve, 1000));

// ✅ wait for the actual condition
await waitFor(() => { expect(mockOnComplete).toHaveBeenCalled(); });

// ✅ or with fake timers
act(() => { jest.runAllTimers(); });
```

---

### J7 — Non-deterministic data

```ts
// ❌ assertion against live clock — fails when CI is slow
// Real occurrence: RewardsController.test.ts (10+ times)
expect(result?.lastFetched).toBeGreaterThan(Date.now() - 1000);

// ✅ pin time before the assertion
jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-01T12:00:00.000Z'));
const before = Date.now();
await doWork();
expect(result?.lastFetched).toBeGreaterThanOrEqual(before);
```

```ts
// ❌ Math.random() in mock data — different value each run
// Real occurrence: PerpsOrderView.test.tsx, TradingViewChart.test.tsx
const id = Math.random().toString();

// ✅ use a fixed value
const id = 'mock-id-1';
```

```ts
// ❌ mock registered but return value never set
jest.mock('../api', () => ({ fetchTokenPrice: jest.fn() }));

// ✅
jest.mocked(fetchTokenPrice).mockResolvedValue({ price: 1.5 });
```

---

### J8 — Fake timers + `waitFor` conflict

`waitFor` polls using real `setTimeout` internally. When `jest.useFakeTimers()` is active, `waitFor` never advances — the test hangs or times out silently.

67 files in this codebase combine fake timers with `waitFor` (e.g. `useStartupNotificationsEffect.test.ts`, `Onboarding/index.test.tsx`, `App.test.tsx`).

```ts
// ❌ waitFor hangs — fake timers prevent its internal polling
beforeEach(() => { jest.useFakeTimers(); });

it('enables notifications', async () => {
  renderHookWithProvider(() => useMyHook(), {});
  await waitFor(() => {               // ← never resolves under fake timers
    expect(mockCallback).toHaveBeenCalled();
  });
});

// ✅ option 1: advance timers inside act() before asserting
it('enables notifications', async () => {
  renderHookWithProvider(() => useMyHook(), {});
  await act(async () => { jest.runAllTimersAsync(); });
  expect(mockCallback).toHaveBeenCalled();
});

// ✅ option 2: restore real timers for the waitFor call
it('enables notifications', async () => {
  jest.runAllTimers();
  jest.useRealTimers();
  await waitFor(() => { expect(mockCallback).toHaveBeenCalled(); });
});
```

---

### J9 — Module-level mutable `let` bindings

Module-level `let` variables used as mock flags are shared across all tests in a file. Mutations made in one test persist into the next unless explicitly reset in `beforeEach`.

```ts
// ❌ mutations persist across tests — order-dependent failures
// Real occurrence: Wallet/index.test.tsx, PerpsStreamManager.test.tsx
let mockFeatureEnabled = true;
jest.mock('./featureFlags', () => ({
  selectFeatureFlag: jest.fn(() => mockFeatureEnabled),
}));

it('hides feature when disabled', () => {
  mockFeatureEnabled = false;         // ← not reset → bleeds into next test
  render(<MyComponent />);
  expect(screen.queryByTestId('feature')).not.toBeOnTheScreen();
});

// ✅ reset in beforeEach
let mockFeatureEnabled = true;

beforeEach(() => {
  mockFeatureEnabled = true;          // restore default before every test
});
```

---

### J10 — `jest.spyOn` without `restoreAllMocks()`

Spies installed with `jest.spyOn` replace the original implementation. Without restoration, the spy persists into subsequent tests, changing their behavior.

219 files in this codebase use `jest.spyOn` without `mockRestore` or `restoreAllMocks` (e.g. `useBridgeConfirm.test.ts`, `PerpsStreamManager.test.tsx`).

```ts
// ❌ spy leaks into subsequent tests
it('logs error on failure', async () => {
  jest.spyOn(console, 'error').mockImplementation();
  // ... test body
  // no restore → next test also has console.error mocked
});

// ✅
afterEach(() => {
  jest.restoreAllMocks();   // restores all spyOn originals
});
```

---

## Local reproduction loop

```bash
# Repeat 10 times in-band — catches timing and order-dependent failures
for i in $(seq 1 10); do
  yarn jest path/to/MyComponent.test.tsx --runInBand || { echo "Failed on run $i"; break; }
done

# Random order — surfaces isolation issues (J3, J9)
yarn jest path/to/MyComponent.test.tsx --randomize

# Target a specific test case
yarn jest path/to/MyComponent.test.tsx -t "test name"

# Full unit suite
yarn test:unit
```

Fix is confirmed when the test passes **10 consecutive local runs**.

## Audit mode

Open [references/gh-analysis.md](references/gh-analysis.md).
