# Writing Tests

Reference: [SKILL.md](../SKILL.md) · [Navigation & Mocking](navigation-mocking.md) · [Reference](reference.md)

**Layer choice:** Component-view is the default for Mobile screen/view behavior. See installed `knowledge/testing-layers.md` before choosing unit tests instead.

---

## Read Before Writing

Before writing any test, read:

- The component file under test
- Any existing `*.view.test.tsx` for the same component
- The relevant preset(s) in `tests/component-view/presets/`
- The relevant renderer(s) in `tests/component-view/renderers/`
- If the view calls an external HTTP API: `tests/component-view/api-mocking/` and any existing `api-mocking/<feature>.ts` for that API (see navigation-mocking.md, External Service / API Mocking)

---

## Enumerate Use Cases

**Do this before writing a single test line.** Build a candidate list scoped and deduplicated against existing tests.

### 1. List user-facing actions

Ask: "What can a user **do** on this screen?" — type/paste input, press a button, select from a list, scroll/refresh, open/dismiss a modal, navigate to a sub-screen, wait for async data, long-press/swipe, toggle a setting.

### 2. Map each action to a valid test pattern

| User action / system event                            | Valid pattern                                         |
| ----------------------------------------------------- | ----------------------------------------------------- |
| Presses button → UI changes                           | `fireEvent.press` → `waitFor`                         |
| Types input → value appears                           | `userEvent.type` or `fireEvent.changeText` → `findBy` |
| Selects item → navigates                              | `userEvent.press` → route probe                       |
| Redux action dispatched → Engine called               | `store.dispatch` + `act` → Engine spy                 |
| Async data arrives → list renders                     | `findBy` / `waitFor`                                  |
| User triggers action → API called with correct params | interaction → spy assertion                           |
| Chained user journey → end state visible              | Multiple `fireEvent` → final `findBy`                 |

Drop anything that only produces a render scenario: "The screen shows X when state is Y", "Button is disabled without input", "Token name appears in header".

### 3. High-leverage interaction pitfalls (from Mobile CV migrations)

These patterns prevent false-green CV and weak unit→CV migrations:

**Loading / skeleton honesty** — Match the pending phase to production UX. If the screen shows a skeleton while `isLoading`, assert skeleton (or that the loaded title is not yet visible), then resolve, then assert post-load behaviour. Do not name a test “shows title while waiting” when production keeps the skeleton until data resolves.

```typescript
// ✅ Pending phase matches real UX
it('shows the loading skeleton until the market request resolves', async () => {
  getMarketSpy.mockImplementation(() => new Promise(() => undefined));

  const { findByTestId, queryByTestId } = renderMyDetailView({
    initialParams: { marketId: 'm1' },
  });

  expect(await findByTestId(MyDetailSelectorsIDs.SKELETON)).toBeOnTheScreen();
  expect(queryByTestId(MyDetailSelectorsIDs.TITLE)).not.toBeOnTheScreen();
});
```

**Await the content, not just its container** — a screen or row can mount well before the values inside it resolve. Anything fed by its own query, debounce, or skeleton (a live price, a sell-order preview, a computed balance) settles *after* its container, so `await findByTestId(CONTAINER)` followed by a synchronous `getByText(value)` is a race. Static props in the same row render immediately, which is why neighbouring assertions keep passing while the gated one flakes only under CI load. Await the gated value, then re-query the container so the scoped assertions run against the settled tree:

```typescript
// ✅ Each async source gets its own await
await findByTestId(MyViewSelectorsIDs.POSITIONS_TAB_CONTENT);
// The value stays behind a skeleton until the preview query settles.
await findByText('$60');

const positionsTab = getByTestId(MyViewSelectorsIDs.POSITIONS_TAB_CONTENT);
expect(within(positionsTab).getByText('$50 on Yes to win $50')).toBeOnTheScreen();
expect(within(positionsTab).getByText('$60')).toBeOnTheScreen();
```

When a test like this fails, the render dump shows the container present with empty `pointerEvents="none"` views where the value belongs — those are the skeleton placeholders.

**Do not nest `find*` inside `waitFor`** — `findBy*` already polls (`waitFor` + `getBy`, default 1000 ms). An outer `waitFor` uses the same budget, so under CI load the outer timeout fires first with a useless `Timed out in waitFor.` Pick one waiter:

```typescript
// ✅ findBy* already waits
expect(await findByText('Token A')).toBeOnTheScreen();

// ✅ waitFor + synchronous getBy* when you need extra time or a count
await waitFor(
  () => {
    const rows = getAllByTestId(MyViewSelectorsIDs.ROW);
    expect(rows).toHaveLength(3);
  },
  { timeout: 5000 },
);

// ❌ double polling — both timers are 1s; the outer one wins in CI
await waitFor(async () => {
  expect(await findByText('Token A')).toBeOnTheScreen();
});
```

**RefreshControl** — Prefer calling the prop handler; `fireEvent(scrollView, 'refresh')` often never hits `onRefresh` in RNTL:

```typescript
await act(async () => {
  await scrollView.props.refreshControl.props.onRefresh();
});
```

**Flag-gated sheets / branches** — UI behind remote flags only mounts when the flag is on in Redux. Drive via preset / `RemoteFeatureFlagController` overrides; do not assert a sheet `testID` if the flag routes to a full screen instead.

**Migration assert parity** — When moving unit → CV, compare deleted unit expects field-by-field. If the unit checked `tabId` / `filterId` / formatted dates / full analytics payloads, the CV replacement must keep that specificity. Partial `objectContaining({ feedId })` after deleting a full payload assert is a regression. See [`../placement/unit-cv-overlap.md`](../placement/unit-cv-overlap.md).

### 4. Deduplicate against existing tests

Read `ComponentName.view.test.tsx` (if it exists) and remove any candidate already covered.

### 5. Run coverage and prioritize

```bash
yarn test:view:coverage:folder app/components/UI/MyFeature
```

Focus on low branch coverage. Prioritize candidates that cover the most uncovered paths. Proceed directly to writing.

---

## Write a New Test File

### File naming

```
ComponentName.view.test.tsx   ← always *.view.test.tsx
```

### What makes a good test

A good test is driven by **user interaction or a meaningful business condition** — not by what is statically visible after render. If your test has no `fireEvent`, no `act`, no `waitFor`, and no Engine spy, ask yourself: am I just checking the initial render? If yes, it's a render scenario and it's an antipattern.

Antipattern examples are in [`reference.md — What NOT to Do`](reference.md#what-not-to-do). **Good tests are interaction-driven or verify a meaningful business rule:**

```typescript
// ✅ User types on keypad → fiat value reacts in real time
it('types 9.5 with keypad and displays $19,000.00 fiat value', async () => {
  const { getByTestId, getByText, findByText, findByDisplayValue } =
    defaultBridgeWithTokens({
      bridge: {
        sourceAmount: '0',
        sourceToken: ETH_SOURCE,
        destToken: undefined,
      },
    });

  await waitFor(() =>
    expect(
      getByTestId(BuildQuoteSelectors.KEYPAD_DELETE_BUTTON),
    ).toBeOnTheScreen(),
  );

  fireEvent.press(getByText('9'));
  fireEvent.press(getByText('.'));
  fireEvent.press(getByText('5'));

  expect(await findByDisplayValue('9.5')).toBeOnTheScreen();
  expect(await findByText('$19,000.00')).toBeOnTheScreen();
});

// ✅ Redux dispatch → Engine called with correct params (proves the wiring, not just the UI)
it('calls quote API with custom slippage when user has set 5% and quote is requested', async () => {
  const updateQuoteSpy = jest.spyOn(
    Engine.context.BridgeController,
    'updateBridgeQuoteRequestParams',
  );
  const { store } = defaultBridgeWithTokens({
    bridge: { selectedDestChainId: '0x1' },
  });
  updateQuoteSpy.mockClear();

  act(() => {
    store.dispatch(setSlippage('5'));
  });

  await waitFor(
    () => {
      expect(updateQuoteSpy).toHaveBeenCalledWith(
        expect.objectContaining({ slippage: 5 }),
        expect.anything(),
      );
    },
    { timeout: 1000 },
  );

  updateQuoteSpy.mockRestore();
});

// ✅ Async data completeness — waits for API mock to resolve, then validates every
// field of every item. Valid because data arrival is async (findBy / waitFor).
// One of these per view — proves the full data pipeline end-to-end.
it('user sees all items with complete data after async load', async () => {
  const { findByText, findByTestId } = renderMyFeatureWithRoutes();

  // Wait for the first item to confirm data has loaded (findBy* already polls)
  expect(await findByText('Token A')).toBeOnTheScreen();

  // Validate all fields of each item in the base mock dataset
  const tokenARow = await findByTestId('token-row-item-eip155:1/erc20:0xAAA');
  const tokenAScope = within(tokenARow);
  expect(tokenAScope.getByText('Token A')).toBeOnTheScreen();
  expect(tokenAScope.getByText(/\+5\.2/)).toBeOnTheScreen(); // % change
  expect(tokenAScope.getByText(/\$/)).toBeOnTheScreen(); // price

  const tokenBRow = await findByTestId('token-row-item-eip155:1/erc20:0xBBB');
  const tokenBScope = within(tokenBRow);
  expect(tokenBScope.getByText('Token B')).toBeOnTheScreen();
  expect(tokenBScope.getByText(/-1\.8/)).toBeOnTheScreen();
  expect(tokenBScope.getByText(/\$/)).toBeOnTheScreen();
});

// ✅ User navigates to a new screen — proves the navigation wiring end-to-end.
// When you only need to confirm navigation occurred (not render the destination screen),
// omit the Component key. The framework renders a probe element with
// testID=`route-${routeName}` automatically when navigation arrives at that route.
it('navigates to dest token selector on press', async () => {
  const state = initialStateBridge()
    .withOverrides({ bridge: { sourceToken: ETH_SOURCE } })
    .build();
  const { findByTestId, findByText } = renderScreenWithRoutes(
    BridgeView as unknown as React.ComponentType,
    { name: Routes.BRIDGE.ROOT },
    [{ name: Routes.BRIDGE.TOKEN_SELECTOR }],
    { state },
  );

  fireEvent.press(await findByText('Swap to'));

  await findByTestId(`route-${Routes.BRIDGE.TOKEN_SELECTOR}`);
});
```

### Local helper pattern

For test files where most tests share a common baseline, extract a local helper instead of repeating the same overrides:

```typescript
// Define the baseline once — each test only overrides its delta from here
const DEFAULT_BRIDGE = {
  sourceToken: ETH_SOURCE,
  destToken: USDC_DEST,
  sourceAmount: '1',
};

const defaultBridgeWithTokens = (overrides?: Record<string, unknown>) => {
  const { bridge: bridgeOverrides, ...rest } = overrides ?? {};
  return renderBridgeView({
    deterministicFiat: true,
    overrides: {
      bridge: {
        ...DEFAULT_BRIDGE,
        ...(bridgeOverrides as Record<string, unknown>),
      },
      ...rest,
    } as unknown as DeepPartial<RootState>,
  });
};
```

Then each test only specifies its delta from this baseline.

### describe / it and platform (iOS + Android)

Import from `tests/component-view/platform`. All helpers accept an optional **filter** (3rd arg): `'ios'` | `'android'` | `['ios','android']` | `{ only: 'ios' }` | `{ skip: ['android'] }`. Env: `TEST_OS=ios` or `TEST_OS=android` to run only one OS.

| Helper                                                                  | Use                                                                                                           |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `describeForPlatforms(name, define, filter?)`                           | One describe per OS. Inside, `define({ os })`; use `it()` or `itForPlatforms()` — each runs once per that OS. |
| `itForPlatforms(name, (ctx) => {}, filter?)`                            | One `it` per OS. Callback receives `{ os }`.                                                                  |
| `itOnlyForPlatforms(name, fn, filter?)`                                 | Same as `itForPlatforms` but registers `it.only`.                                                             |
| `itEach(table)(name, (row) => {}, filter?)`                             | One `it` per table row × per OS. Use `$key` in name to interpolate row fields.                                |
| `describeEach(table)(name, (row) => { it('...', () => {}); }, filter?)` | One describe per row × per OS. Use `$key` in name.                                                            |
| `getTargetPlatforms(filter?)`                                           | Returns `['ios','android']` (or filtered list) for custom loops.                                              |

Example — `itEach` (each case runs on iOS and Android):

```typescript
import { itEach } from '../../../../../../tests/component-view/platform';

const cases = [
  { name: 'renders empty', amount: '0' },
  { name: 'displays fiat', amount: '1' },
];
itEach(cases)('$name', ({ amount }) => {
  const { findByDisplayValue } = renderDefault({
    bridge: { sourceAmount: amount },
  });
  expect(findByDisplayValue(amount)).toBeOnTheScreen();
});
```

Jest modifiers (`it.only`, `it.skip`, `describe.only`, `describe.skip`) work as usual inside these blocks.

### Minimal template

```typescript
import '../../../../../../tests/component-view/mocks';
import { renderMyFeatureView } from '../../../../../../tests/component-view/renderers/myFeature';
import {
  describeForPlatforms,
  itForPlatforms,
} from '../../../util/test/platform';
import { act, fireEvent, waitFor, within } from '@testing-library/react-native';
import { MyViewSelectorsIDs } from './MyView.testIds'; // ← always import from the component's testIds file
import type { DeepPartial } from '../../../../../util/test/renderWithProvider';
import type { RootState } from '../../../../../reducers';

// Local helper — encapsulates the common baseline, each test only overrides its delta
// Define the baseline before the helper
const DEFAULT_MY_FEATURE = {
  sourceToken: ETH_SOURCE,
  destToken: USDC_DEST,
  sourceAmount: '1',
};

const renderDefault = (overrides?: Record<string, unknown>) => {
  const { myFeature: featureOverrides, ...rest } = overrides ?? {};
  return renderMyFeatureView({
    deterministicFiat: true,
    overrides: {
      myFeature: {
        ...DEFAULT_MY_FEATURE,
        ...(featureOverrides as Record<string, unknown>),
      },
      ...rest,
    } as unknown as DeepPartial<RootState>,
  });
};

describeForPlatforms('MyView', () => {
  // ✅ User interaction → UI reacts
  it('types an amount with the keypad and updates the fiat display', async () => {
    const { getByTestId, getByText, findByDisplayValue, findByText } =
      renderDefault({
        bridge: {
          sourceAmount: '0',
          sourceToken: ETH_SOURCE,
          destToken: USDC_DEST,
        },
      });

    await waitFor(() =>
      expect(
        getByTestId(MyViewSelectorsIDs.KEYPAD_DELETE_BUTTON),
      ).toBeOnTheScreen(),
    );

    fireEvent.press(getByText('1'));
    fireEvent.press(getByText('0'));

    expect(await findByDisplayValue('10')).toBeOnTheScreen();
    expect(await findByText('$20,000.00')).toBeOnTheScreen();
  });

  // ✅ Redux dispatch → Engine method called with correct params
  it('calls updateBridgeQuoteRequestParams with the selected dest chain when chain changes', async () => {
    const updateQuoteSpy = jest.spyOn(
      Engine.context.BridgeController,
      'updateBridgeQuoteRequestParams',
    );
    const { store } = renderDefault({
      bridge: { sourceToken: ETH_SOURCE, sourceAmount: '1' },
    });
    updateQuoteSpy.mockClear();

    act(() => {
      store.dispatch(setDestChain('0xa'));
    });

    await waitFor(() => {
      expect(updateQuoteSpy).toHaveBeenCalledWith(
        expect.objectContaining({ destChainId: '0xa' }),
        expect.anything(),
      );
    });

    updateQuoteSpy.mockRestore();
  });

  // ✅ User press → navigates to a new screen
  it('opens the destination token selector when the dest token area is tapped', async () => {
    const state = initialStateMyFeature()
      .withOverrides({ bridge: { sourceToken: ETH_SOURCE } })
      .build();
    const { findByText, findByTestId } = renderScreenWithRoutes(
      MyView as unknown as React.ComponentType,
      { name: Routes.MY_FEATURE },
      [{ name: Routes.MY_FEATURE_TOKEN_SELECTOR }],
      { state },
    );

    fireEvent.press(await findByText('Swap to'));

    await findByTestId(`route-${Routes.MY_FEATURE_TOKEN_SELECTOR}`);
  });
});
```

### Import order

`tests/component-view/mocks` **must be the very first import** — it installs Engine and native mocks before anything else loads. For remaining imports follow project ESLint rules: renderer → platform helpers → testIds constants → `@testing-library/react-native` → other.

---

## Choose the Right Renderer and Preset

### Use an existing renderer when available

| View area      | Renderer                                                    | Preset                      |
| -------------- | ----------------------------------------------------------- | --------------------------- |
| Bridge         | `renderBridgeView`                                          | `initialStateBridge`        |
| Wallet         | `renderWalletView`                                          | `initialStateWallet`        |
| Trending       | `renderTrendingView`                                        | `initialStateTrending`      |
| Wallet Actions | `renderWalletActionsView`                                   | `initialStateWalletActions` |
| Perps          | `renderPerpsView`                                           | `initialStatePerps`         |
| Predict        | `renderPredictFeedView` / `renderPredictFeedViewWithRoutes` | `initialStatePredict`       |

### Passing state overrides

Always start from a preset, then narrow down with minimal overrides:

```typescript
// Good — minimal delta from preset
renderBridgeView({
  deterministicFiat: true,
  overrides: {
    bridge: { sourceAmount: '1' },
  },
});

// Good — complex override via engine background state when needed
renderBridgeView({
  overrides: {
    engine: {
      backgroundState: {
        BridgeController: {
          state: { quotesLastFetched: 0 },
        },
      },
    },
  },
});
```

### Bridge: enabling the confirm CTA

To enable the Bridge confirm CTA (requires a valid quote), use the `withBridgeRecommendedQuoteEvmSimple` helper on the state fixture — it's the easiest path:

```typescript
const state = initialStateBridge()
  .withBridgeRecommendedQuoteEvmSimple({ sourceAmount: '1' })
  .build();
```

Alternatively, set these fields manually in `engine.backgroundState.BridgeController`:

- `quotes: [recommendedQuote]`
- `recommendedQuote: recommendedQuote`
- `quotesLastFetched: Date.now()`
- `quotesLoadingStatus: 'SUCCEEDED'`

Also ensure remote feature flags enable Bridge for the target chain(s) via `RemoteFeatureFlagController.remoteFeatureFlags.bridgeConfigV2`.

---

### When no renderer exists for the view yet

Create one. Pattern (copy from `tests/component-view/renderers/bridge.ts`):

```typescript
// tests/component-view/renderers/myFeature.ts
import '../mocks';
import React from 'react';
import type { DeepPartial } from '../../../app/util/test/renderWithProvider';
import type { RootState } from '../../../app/reducers';
import { renderComponentViewScreen } from '../render';
import Routes from '../../../app/constants/navigation/Routes';
import MyView from '../../../app/components/Views/MyFeature';
import { initialStateMyFeature } from '../presets/myFeature';

interface RenderMyFeatureOptions {
  overrides?: DeepPartial<RootState>;
  deterministicFiat?: boolean;
}

export function renderMyFeatureView(
  options: RenderMyFeatureOptions = {},
): ReturnType<typeof renderComponentViewScreen> {
  const { overrides, deterministicFiat } = options;
  const builder = initialStateMyFeature({ deterministicFiat });
  if (overrides) builder.withOverrides(overrides);
  const state = builder.build();
  return renderComponentViewScreen(
    MyView as unknown as React.ComponentType,
    { name: Routes.MY_FEATURE },
    { state },
  );
}
```

### When the view uses React Query (`@tanstack/react-query`)

If the view (or any child component) calls `useQuery` / `useMutation`, wrap the component in a `QueryClientProvider` inside the renderer — otherwise tests throw `No QueryClient set`:

```typescript
// tests/component-view/renderers/myFeature.tsx
import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { renderComponentViewScreen } from '../render';
import { initialStateMyFeature } from '../presets/myFeature';
import MyView from '../../../app/components/UI/MyFeature/MyView';
import Routes from '../../../app/constants/navigation/Routes';

export function renderMyFeatureView(options = {}) {
  const state = initialStateMyFeature(options).build();
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });

  return renderComponentViewScreen(
    () => (
      <QueryClientProvider client={queryClient}>
        <MyView />
      </QueryClientProvider>
    ),
    { name: Routes.MY_FEATURE },
    { state },
  );
}
```

Key points:

- Set `retry: false` so failed queries surface immediately in tests without retry delays
- Create a **new `QueryClient` per call** to avoid state leaking between tests

### When the view reads route params (`initialParams`)

`renderComponentViewScreen` and `renderScreenWithRoutes` accept a 4th `initialParams` argument for views that read params from the route (e.g. via `useRoute().params`):

```typescript
// For a view that expects { marketId: string } as route params
renderComponentViewScreen(
  MyDetailView as unknown as React.ComponentType,
  { name: Routes.MY_FEATURE.DETAIL },
  { state },
  { marketId: 'market-abc-123' }, // ← initialParams as 4th argument
);
```

In tests using `renderScreenWithRoutes`, pass `initialParams` in the route object:

```typescript
renderScreenWithRoutes(
  MyDetailView as unknown as React.ComponentType,
  { name: Routes.MY_FEATURE.DETAIL, params: { marketId: 'market-abc-123' } },
  [],
  { state },
);
```

If the component crashes with `Cannot read properties of undefined (reading 'marketId')`, the view is reading a required route param — pass it via `initialParams` or `params`.

---

And the matching preset (`tests/component-view/presets/myFeature.ts`):

```typescript
import { createStateFixture } from '../stateFixture';

export const initialStateMyFeature = (options?: {
  deterministicFiat?: boolean;
}) => {
  const builder = createStateFixture()
    .withMinimalAccounts()
    .withMinimalMainnetNetwork()
    .withMinimalKeyringController()
    .withRemoteFeatureFlags({});

  if (options?.deterministicFiat) {
    builder.withOverrides({
      /* currency rate overrides */
    });
  }
  return builder;
};
```
