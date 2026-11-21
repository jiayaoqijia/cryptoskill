Reference: [MetaMask Unit Testing Guidelines](https://github.com/MetaMask/contributor-docs/blob/main/docs/testing/unit-testing.md)

# Unit Testing Guidelines

Part of **mobile-testing**. Choose the layer first via installed `knowledge/testing-layers.md`; unit tests are not the default for screen/view UI behavior or app-to-controller flows.

## When to use

Use this skill when you need to:

- Write or fix **focused** unit tests for pure helpers, local utilities, or narrow component contracts
- Keep the **smallest** unit coverage for a case the CV framework cannot cover yet (document why)
- Apply Jest/RTL conventions (naming, AAA, matchers) for allowed unit cases

Do **not** use unit tests as the default for full-screen / view UI behavior — open [`component-view.md`](component-view.md) (`*.view.test.tsx`) instead.

## Testing layers (read first)

Follow installed `knowledge/testing-layers.md` before choosing unit vs component-view vs integration vs E2E.

- **Default for screen/view behavior:** `*.view.test.tsx` via [`component-view.md`](component-view.md) — not a broad RTL unit test that mocks hooks/selectors.
- **This skill applies when:** pure helpers, local utilities, narrow component contracts, or the CV framework cannot cover the case yet (smallest focused unit test + note why).
- **Do not** add new full-page `*.test.tsx` files that render a screen and mock Redux/hooks to force UI state; convert or write CV instead.
- **Do not** add a unit test for static styling (component-library defaults, or `twClassName` / `style` / color-prop overrides that depend on no logic). The layer policy marks it GAP / ACCEPT — see [Do Not Test Static Presentation](#do-not-test-static-presentation).

## Do Not Test Static Presentation

Do not unit test static styling: component-library defaults, or overrides
passed through props (`twClassName`, `style`, color props) that don't depend on
any logic. The design system already tests that its props apply, and visual
changes are verified with screenshots (`mobile-visual-testing`) and the PR's
before/after evidence. A diff that only changes static styling needs no new
test, even inside an existing `*.test.tsx`; such assertions don't guard
behavior and break whenever a design token changes. Mobile bans snapshots of
rendered UI — `toMatchSnapshot()` in any form, and `toMatchInlineSnapshot()` of
rendered UI — so do not add one to cover a styling change. If an existing
rendered-UI snapshot fails because class names or static styles changed,
replace it with explicit assertions (or update it) so CI stays green; that
change is not coverage of the styling change.

An existing test that asserts only static styling is safe to delete — keep any
behavioral assertions it also makes, and if the repo's coverage gate flags the
removal, assert what the user sees instead of keeping a style assertion.

Test presentation only when JS logic decides it (state, props or data choose
between styles, e.g. error vs default, selected, disabled). Prefer asserting
what the user sees (text, disabled or accessibility state), and use a style
assertion only when the style itself is the outcome of that logic.

```tsx
// ❌ WRONG - asserts padding values after a spacing fix
const style = StyleSheet.flatten(
  screen.getByTestId(SelectorsIDs.PRICE_SUMMARY).props.style,
);
expect(style.paddingLeft).toBeUndefined();

// ❌ WRONG - asserts fixed truncation props; Jest never renders the overflow
expect(title.props.numberOfLines).toBe(1);
expect(title.props.ellipsizeMode).toBe('tail');

// ❌ WRONG - asserts margins set by a Tailwind class
expect(StyleSheet.flatten(divider.props.style)).toEqual(
  expect.objectContaining({ marginBottom: 0, marginTop: 20 }),
);

// ❌ WRONG - asserts a static twClassName override that no logic chooses
expect(screen.getByTestId('token-list-item').props.twClassName).toBe(
  'bg-background-default',
);

// ✅ CORRECT - the error style is chosen by logic (amount exceeds balance)
it('marks the amount input invalid when the amount exceeds the balance', () => {
  render(<SendForm amount="1000" />);

  expect(screen.getByTestId('send-amount-input').props.twClassName).toContain(
    'bg-error',
  );
});
```

- **Do not** add a `testID` whose only use is reading `style`.
- **Do not** remove a `useTailwind` mock so `StyleSheet.flatten` can see real spacing.
- **Do not** justify a test by coverage alone. A render that touches a new JSX line adds coverage without protecting behavior.

## Test Naming Rules

- **NEVER use "should" in test names** - this is a hard rule with zero exceptions
- **Use action-oriented descriptions** that describe what the code does
- **Be specific about the behavior being tested**
- **AVOID** weasel words like "handle", "manage", or other non-specific action verbs
- **AVOID** subjective outcome words like "successfully", "correctly", "invalid" - instead indicate what the actual result should be
- **BE SPECIFIC** about conditions: use "email without domain" instead of "invalid email"

```ts
// ❌ WRONG
it('should return fixed timestamp', () => { ... });
it('should ignore events', () => { ... });
it('should display error when input is invalid', () => { ... });
it('handles invalid input correctly', () => { ... });

// ✅ CORRECT
it('returns fixed timestamp for privacy events', () => { ... });
it('ignores events without privacy timestamp property', () => { ... });
it('displays error when email is missing @ symbol', () => { ... });
it('returns false for email without domain', () => { ... });
```

## Test Structure and Organization - MANDATORY

- **EVERY test MUST follow the AAA pattern** (Arrange, Act, Assert) with blank line separation
- **Each test must cover ONE behavior** and be isolated from others
- **Use helper functions** for test data creation
- **Group related tests** in `describe` blocks

```ts
it('returns false for email without domain', () => {
  const input = 'user@';

  const result = validateEmail(input);

  expect(result).toBe(false);
});
```

**Helper Functions**:

```ts
const createTestEvent = (overrides = {}) => ({
  type: EventType.TrackEvent,
  event: 'Test Event',
  timestamp: '2024-01-01T12:00:00.000Z',
  ...overrides,
});
```

## Element Selection - PREFER DATA TEST IDs

- **ALWAYS prefer `testID` props** for selecting elements in tests
- **Use `getByTestId`** as the primary query method for reliable element selection
- **Add `testID` props** when a justified behavior test needs a stable query — not just because a component was touched, and never only to read `style`
- **Avoid selecting by text** when the text might change (i18n, copy updates)

```tsx
// ✅ CORRECT - Use testID for reliable selection
<Button testID="submit-button" onPress={handleSubmit}>
  {t('common.submit')}
</Button>;

// In test:
const submitButton = screen.getByTestId('submit-button');
expect(submitButton).toBeOnTheScreen();

// ✅ ALSO GOOD - Locale keys (safe from content updates)
const button = screen.getByText(strings('common.submit'));

// ❌ AVOID - Selecting by hardcoded text content
const button = screen.getByText('Submit'); // Breaks when text changes
const input = screen.getByPlaceholderText('Enter email'); // Fragile
```

### CHILD PROP OBJECTS - ALL COMPONENTS SUPPORT THIS

**ALL `@metamask/design-system-react-native` and `app/component-library` components support child prop objects for passing testIDs to internal elements.** This is a universal design pattern - prefer not to mock these components just to inject testIDs.

Common child prop object patterns:

- `closeButtonProps` - for close/dismiss buttons
- `backButtonProps` - for back navigation buttons
- `startAccessoryProps` / `endAccessoryProps` - for accessory elements
- `iconProps` - for icon elements
- `labelProps` - for label text elements
- `inputProps` - for input elements within compound components
- `*Props` - any prop ending in `Props` is likely a child prop object

```tsx
// ❌ WRONG - Mocking to add testID (141 lines of unnecessary code!)
// The testID capability ALREADY EXISTS via child prop objects!
jest.mock('BottomSheetHeader', () => {
  return ({ onClose }) => (
    <TouchableOpacity testID="close-button" onPress={onClose}>Close</TouchableOpacity>
  );
});

// ✅ CORRECT - Use the component's child prop object API
<HeaderCenter
  title="Select a region"
  onClose={handleClose}
  closeButtonProps={{ testID: 'region-selector-close-button' }}
/>

// ✅ CORRECT - BottomSheetHeader supports child prop objects
<BottomSheetHeader
  onClose={handleClose}
  closeButtonProps={{ testID: 'modal-close-button' }}
  onBack={handleBack}
  backButtonProps={{ testID: 'modal-back-button' }}
>
  {title}
</BottomSheetHeader>

// In test - no mocking needed!
const closeButton = screen.getByTestId('region-selector-close-button');
fireEvent.press(closeButton);
```

### This Is Universal - No Exceptions

| Library                                | testID Support                                                 |
| -------------------------------------- | -------------------------------------------------------------- |
| `@metamask/design-system-react-native` | ✅ All components support `testID` prop AND child prop objects |
| `app/component-library/*`              | ✅ All components support `testID` prop AND child prop objects |

**If you need to add a testID to one of these components, check for child prop objects first.** Most components support this functionality. If not available, suggest adjusting the component to support it in another change set.

### How to Find Child Prop Objects

1. **Check TypeScript types** - Look at the component's props interface for props ending in `Props`
2. **Check component source** - Search for `Props` suffix patterns
3. **Check Storybook** - Component stories demonstrate these props

```tsx
// Example: BottomSheetHeader TypeScript interface shows:
// - closeButtonProps?: ButtonIconProps
// - backButtonProps?: ButtonIconProps

// Example: Design system Button with icon
<Button
  testID="submit-button"
  iconProps={{ testID: 'submit-icon' }}
  labelProps={{ testID: 'submit-label' }}
>
  Submit
</Button>
```

### TestID Naming Conventions

```tsx
// Use kebab-case for testIDs
testID="settings-screen"
testID="submit-button"
testID="error-message"
testID="token-list-item"

// Include context for list items
testID={`token-item-${token.symbol}`}
testID={`network-option-${network.chainId}`}
```

## Snapshot Testing Policy - MANDATORY

### The Rule

- ❌ **`toMatchSnapshot()` is BANNED** — Do not use it. Do not add it. Do not approve it.
- ❌ **`toMatchInlineSnapshot()` on rendered UI is BANNED** — the serialized blob locks in styles, class names, and layout, so a design-token or class-name change fails the test even though no behavior regressed.
- ✅ **`toMatchInlineSnapshot()` on serialized data is ALLOWED** — use it only when the serialized value itself is the assertion (a data object, a formatted string), never as a lazy substitute for explicit `expect` calls.

### Why `toMatchSnapshot()` Is Banned

External snapshot files (`.snap`) have three critical problems:

1. **Invisible in review** — The diff lives in a separate `.snap` file that reviewers routinely rubber-stamp. Regressions hide there.
2. **No code ownership** — `CODEOWNERS` explicitly assigns `**/*.snap` to *nobody*, meaning no team is accountable for snapshot correctness.
3. **Brittle by design** — Any style tweak, whitespace change, or unrelated refactor regenerates the snapshot and silently passes CI.

### Why Inline Snapshots of Rendered UI Are Banned

An inline snapshot of a component locks in rendered output (styles, class
names, layout), so a design-token or class-name change fails the test even
though no behavior regressed. Assert what the component does and shows with
explicit matchers (`toBeOnTheScreen`, text, disabled state) instead of
snapshotting the serialized tree.

### When to Use `toMatchInlineSnapshot()`

Only use it when the serialized shape of the output **is** the assertion — for example, verifying a complex object structure, a formatted string, or a serialized data payload. Never snapshot rendered UI with it, and do not use it as a lazy substitute for explicit `expect` calls.

```ts
// ❌ BANNED — writes to an external .snap file
expect(tree).toMatchSnapshot();
expect(component).toMatchSnapshot();
expect(result).toMatchSnapshot();

// ❌ BANNED — snapshots rendered UI (styles, class names, layout)
expect(screen.getByTestId('send-amount-input')).toMatchInlineSnapshot();

// ✅ ALLOWED — the serialized value itself is the assertion (data, not UI)
expect(result).toMatchInlineSnapshot(`
  {
    "chainId": "0x1",
    "name": "Ethereum Mainnet",
  }
`);

// ✅ PREFERRED — explicit assertions are always better than snapshots
expect(result.chainId).toBe('0x1');
expect(result.name).toBe('Ethereum Mainnet');
```

### Migrating Existing `toMatchSnapshot()` Calls

When you encounter an existing `toMatchSnapshot()` call:
1. **Prefer replacing it** with explicit `expect` assertions targeting the specific values that matter.
2. If the full serialized output is genuinely meaningful — and not rendered UI — convert to `toMatchInlineSnapshot()`.
3. Delete the corresponding `.snap` file entry once migrated.

Migrate opportunistically when you are already modifying a test file; do not block a PR solely to force migration.


## Assertions - PREFER toBeOnTheScreen

- **ALWAYS use `toBeOnTheScreen()`** to assert element presence - NOT `toBeTruthy()` or `toBeDefined()`
- **Use specific matchers** that communicate intent clearly
- **Avoid weak matchers** that don't actually verify the expected behavior

```tsx
// ✅ CORRECT - Clear, specific assertions
expect(screen.getByTestId('submit-button')).toBeOnTheScreen();
expect(screen.queryByTestId('error-message')).not.toBeOnTheScreen();
expect(screen.getByTestId('balance-text')).toHaveTextContent('100 ETH');

// ❌ WRONG - Weak matchers that don't verify presence properly
expect(screen.getByTestId('submit-button')).toBeTruthy(); // Misleading
expect(screen.getByTestId('submit-button')).toBeDefined(); // Doesn't verify render
expect(element).not.toBeNull(); // Use toBeOnTheScreen() instead
```

### Recommended Matchers

| Instead of                           | Use                                                       |
| ------------------------------------ | --------------------------------------------------------- |
| `toBeTruthy()` for elements          | `toBeOnTheScreen()`                                       |
| `toBeDefined()` for elements         | `toBeOnTheScreen()`                                       |
| `not.toBeNull()`                     | `not.toBeOnTheScreen()` or `queryByTestId` returning null |
| `toHaveLength(1)` for single element | `toBeOnTheScreen()`                                       |

## Mocking Rules - CRITICAL

### Exception: UI Components and TestIDs

**Prefer not to mock `@metamask/design-system-react-native` or `app/component-library` components just to inject testIDs.** All these components support testIDs via:

- Direct `testID` prop on the component
- Child prop objects (`closeButtonProps`, `iconProps`, etc.) for internal elements

```tsx
// ❌ WRONG: Mocking to inject testID
jest.mock('BottomSheetHeader', () => ({ onClose }) => (
  <TouchableOpacity testID="close-button" onPress={onClose}>
    Close
  </TouchableOpacity>
));

// ✅ RIGHT: Use child prop objects
<BottomSheetHeader
  onClose={handleClose}
  closeButtonProps={{ testID: 'modal-close-button' }}
/>;
```

See [PR #25548](https://github.com/MetaMask/metamask-mobile/pull/25548) for refactoring example.

### General Mocking Rules

- **EVERYTHING not under test MUST be mocked** - no exceptions
- **NO** use of `require` - use ES6 imports only
- **NO** use of `any` type - use proper TypeScript types
- **Mock all external dependencies** including APIs, services, hooks
- **Use realistic mock data** that reflects real usage

### Theme Mocking Rules

- **Prefer shared `mockTheme` from `app/util/theme`** instead of hard-coded color literals in tests.
- **Never hardcode design token hex values** in assertions or theme mocks (enforced by `@metamask/design-tokens/color-no-hex`).
- **Avoid local hex color objects** for `useTheme`, `useStyles`, or tailwind mock color functions.
- **If a test only needs a specific theme field**, derive it from `mockTheme` (or spread `mockTheme` and override minimally).

```ts
// ✅ CORRECT: use shared mockTheme for useTheme mocks
import { mockTheme } from '../../util/theme';

jest.mock('../../util/theme', () => ({
  useTheme: () => mockTheme,
}));
```

```ts
// ✅ CORRECT: return { styles, theme } for useStyles mocks
import { mockTheme } from '../../util/theme';

jest.mock('../../../../../component-library/hooks', () => ({
  useStyles: jest.fn((styleFn, vars) => ({
    styles: styleFn({ theme: mockTheme, vars }),
    theme: mockTheme,
  })),
}));
```

```ts
// ✅ CORRECT: mock useTailwind with the right shape
jest.mock('@metamask/design-system-twrnc-preset', () => ({
  useTailwind: () => ({
    // Most components only need tw.style(...)
    style: jest.fn(() => ({})),
  }),
}));
```

```ts
// ✅ ALSO CORRECT: match real useTailwind() return type (callable function + helpers)
import { mockTheme } from '../../util/theme';

jest.mock('@metamask/design-system-twrnc-preset', () => ({
  useTailwind: () => {
    const tw = () => ({});
    tw.style = jest.fn(() => ({}));
    return tw;
  },
}));
```

```ts
// ❌ AVOID: local hex color mocks
const mockColors = {
  text: { default: '#000000' },
  background: { default: '#FFFFFF' },
  border: { muted: '#E5E7EB' },
};
```

```ts
// ✅ CORRECT
import { apiService } from '../services/api';
jest.mock('../services/api');
const mockApiService = apiService as jest.Mocked<typeof apiService>;

interface MockEvent {
  type: EventType;
  event: string;
  timestamp: string;
}

// ❌ WRONG
const mockApi = require('../services/api'); // ❌ no require
const mockApi: any = jest.fn(); // ❌ no any type
```

## Test Isolation and Focus - MANDATORY

- **Each test MUST be independent** - no shared state between tests
- **Use `beforeEach` for setup, `afterEach` for cleanup**
- **Reset all mocks between tests**
- **Tests MUST run in any order**
- **Avoid duplicated or polluted tests**
- **Use mocks for all external dependencies**

```ts
// ✅ CORRECT Test Isolation
describe('MetaMetricsCustomTimestampPlugin', () => {
  let plugin: MetaMetricsCustomTimestampPlugin;

  beforeEach(() => {
    plugin = new MetaMetricsCustomTimestampPlugin({
      timestampStrategy: 'fixed',
      customTimestamp: '1970-01-01T00:00:00.000Z',
    });
    jest.clearAllMocks();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('returns fixed timestamp for privacy events', () => {
    const event = createTestEvent({ privacyTimestamp: true });

    const result = plugin.execute(event);

    expect(result.timestamp).toBe('1970-01-01T00:00:00.000Z');
  });
});
```

## Test Coverage (MANDATORY)

Apply this list only after the layer policy says a unit test is justified. Cover the behavior branches the code actually has. A static styling change adds no branch, so it adds no test.

**When a unit test is justified, it MUST cover:**

- ✅ **Happy path** - normal expected behavior
- ✅ **Edge cases** - null, undefined, empty values, boundary conditions
- ✅ **Error conditions** - invalid inputs, failure scenarios
- ✅ **Different code paths** - all if/else branches, switch cases
- ✅ **Method chaining** - for builder patterns
- ✅ **Side effects** - property changes, state updates, cleanup

```ts
// ✅ CORRECT Coverage Example
describe('MetaMetricsCustomTimestampPlugin', () => {
  describe('execute', () => {
    it('returns fixed timestamp for privacy events', () => {
      // Happy path
    });

    it('ignores events without privacy timestamp property', () => {
      // Edge case
    });

    it('throws error when strategy is null', () => {
      // Error condition
    });

    it('uses event-specific timestamp strategy when provided', () => {
      // Different code path
    });

    it('removes privacy properties from event', () => {
      // Side effect
    });
  });
});
```

## Parameterized Tests

- Parameterize tests to cover all values (e.g., enums) with type-safe iteration.

```ts
it.each(['small', 'medium', 'large'] as const)('renders %s size', (size) => {
  expect(renderComponent(size)).toBeOnTheScreen();
});
```

## Test Determinism

- **EVERYTHING** not under test must be mocked - no exceptions.
- Avoid brittle tests: do not test internal state or UI snapshots for logic. **`toMatchSnapshot()` and rendered-UI `toMatchInlineSnapshot()` are banned** — see Snapshot Testing Policy above.
- Only test public behavior, not implementation details.
- Mock time, randomness, and external systems to ensure consistent results.

```ts
// Mock all external dependencies
jest.mock('../services/api');
jest.mock('../utils/date');
jest.mock('../hooks/useAuth');

jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-01'));
```

- Avoid relying on global state or hardcoded values (e.g., dates) or mock it.

## Async Testing and act() - CRITICAL

**ALWAYS use `act()` when testing async operations that trigger React state updates.**

### When to Use act()

Use `act()` when you:

- Call async functions via component props (e.g., `onRefresh`, `onPress` with async handlers)
- Invoke functions that perform state updates asynchronously
- Test pull-to-refresh or other async interactions

### Symptoms of Missing act()

Tests fail intermittently with:

- `TypeError: terminated`
- `SocketError: other side closed`
- Warnings about state updates not being wrapped in act()

### Examples

```ts
// ❌ WRONG - Causes flaky tests
it('calls Logger.error when handleOnRefresh fails', async () => {
  const mockLoggerError = jest.spyOn(Logger, 'error');
  render(BankDetails);

  // Async function called without act() - causes race condition
  screen
    .getByTestId('refresh-control-scrollview')
    .props.refreshControl.props.onRefresh();

  await waitFor(() => {
    expect(mockLoggerError).toHaveBeenCalled();
  });
});

// ✅ CORRECT - Properly handles async state updates
it('calls Logger.error when handleOnRefresh fails', async () => {
  const mockLoggerError = jest.spyOn(Logger, 'error');
  render(BankDetails);

  // Wrap async operation in act()
  await act(async () => {
    await screen
      .getByTestId('refresh-control-scrollview')
      .props.refreshControl.props.onRefresh();
  });

  await waitFor(() => {
    expect(mockLoggerError).toHaveBeenCalled();
  });
});
```

### Common Patterns Requiring act()

```ts
// RefreshControl callbacks
await act(async () => {
  await refreshControl.props.onRefresh();
});

// Async button press handlers
await act(async () => {
  await button.props.onPress();
});

// Any async callback that updates state
await act(async () => {
  await component.props.onSomeAsyncAction();
});
```

### Why This Matters

Without `act()`:

1. Async function starts executing
2. Test continues and waits only for specific assertion
3. Jest cleanup/termination happens while promises are still pending
4. Results in "terminated" or "other side closed" errors

With `act()`:

1. React Testing Library waits for all state updates
2. All promises resolve before test proceeds
3. Clean, deterministic test execution

# Reviewer Responsibilities

- Validate that tests fail when the code is broken (test the test).

```ts
// Break the SuT and make sure this test fails
expect(result).toBe(false);
```

- Ensure tests use proper matchers (`toBeOnTheScreen` vs `toBeDefined`).
- **Reject any new `.snap` files or new `toMatchSnapshot()` calls, and any `toMatchInlineSnapshot()` of rendered UI** — require explicit assertions, or an inline snapshot only when the serialized value is the assertion.
- Reject tests with complex names combining multiple logical conditions (AND/OR).

# Refactoring Support

- Ensure tests provide safety nets during refactors and logic changes. Run the tests before pushing commits!
- Encourage small, testable components.
- Unit tests must act as documentation for feature expectations.

# Quality Checklist - MANDATORY

Before submitting any test file, verify:

- [ ] **No `toMatchSnapshot()` calls and no rendered-UI `toMatchInlineSnapshot()`** — BANNED; use explicit assertions (an inline snapshot is allowed only when the serialized value is the assertion)
- [ ] **No static style assertions** — no `StyleSheet.flatten` padding/margin/color checks, fixed layout-prop checks, or style-only testIDs; a style assertion is allowed only when the style itself is the outcome of logic
- [ ] **No mocking to inject testIDs** - Use component's built-in testID support
- [ ] **testIDs via child prop objects** - Use `closeButtonProps={{ testID }}` not mocks
- [ ] **No "should" in any test name**
- [ ] **All tests follow AAA pattern**
- [ ] **Each test has one clear purpose**
- [ ] **All code paths are tested**
- [ ] **Edge cases are covered**
- [ ] **Test data is realistic**
- [ ] **Tests are independent**
- [ ] **Assertions use `toBeOnTheScreen()`** - NOT `toBeTruthy()` or `toBeDefined()`
- [ ] **Assertions are specific**
- [ ] **Elements selected by `testID`** - NOT fragile text queries
- [ ] **Test names are descriptive**
- [ ] **No test duplication**
- [ ] **Async operations wrapped in act()** when they trigger state updates

# Common Mistakes to AVOID - CRITICAL

- ❌ **Using `toMatchSnapshot()`, or `toMatchInlineSnapshot()` on rendered UI** — BANNED; use explicit assertions instead (inline snapshots of serialized data are fine)
- ❌ **Mocking to inject testIDs** - Components already support testID (see guidelines above)
- ❌ **Testing static styling** - Spacing, color, and fixed layout props are verified visually, not in Jest
- ❌ **Using "should" in test names** - This is the #1 mistake, use action-oriented descriptions
- ❌ **Testing multiple behaviors in one test** - One test, one behavior
- ❌ **Sharing state between tests** - Each test must be independent
- ❌ **Not testing error conditions** - Test both success and failure paths
- ❌ **Using unrealistic test data** - Use data that reflects real usage
- ❌ **Not following AAA pattern** - Always Arrange, Act, Assert
- ❌ **Not testing edge cases** - Test null, undefined, empty values
- ❌ **Using weak matchers** - Use `toBeOnTheScreen()` instead of `toBeTruthy()`/`toBeDefined()`
- ❌ **Selecting elements by text** - Use `testID` props for reliable selection
- ❌ **Not wrapping async state updates in act()** - Causes flaky "terminated" errors

# Unit tests developement workflow

- Always run unit tests after making code changes.
- **NEVER** use npm, npx, or other package managers - ONLY use yarn

## Testing Commands

### Single File Testing

```shell
# Use this command for testing a specific file
yarn jest <filename>
# Use this command for testing specific test cases
yarn jest <filename> -t "<test-name-pattern>"
# Use this command for running all unit tests
yarn test:unit
# Run a specific test file
yarn jest MyComponent.test.tsx
yarn jest utils/helpers.test.ts
```

### Coverage Reports

```shell
# Use this command for coverage reports
yarn test:unit:coverage
```

## Workflow Requirements

- Confirm all tests are passing before commit.
- **Do not add new `toMatchSnapshot()` calls, and never snapshot rendered UI with `toMatchInlineSnapshot()`** — see Snapshot Testing Policy.
- When modifying a test file that contains `toMatchSnapshot()`, opportunistically migrate those calls to explicit assertions or `toMatchInlineSnapshot()` (data only) — do not block a PR solely to force migration, but do not add new ones.

# Reference Code Examples

**Proper AAA**:

```ts
it('indicates expired milk when past due date', () => {
  const today = new Date('2025-06-01');
  const milk = { expiration: new Date('2025-05-30') };

  const result = isMilkGood(today, milk);

  expect(result).toBe(false);
});
```

## ❌ Banned: Snapshots of Rendered UI

```ts
// ❌ BANNED — toMatchSnapshot() writes to an external .snap file:
// no code owner, hidden regressions, breaks on trivial changes.
// toMatchInlineSnapshot() on rendered UI is banned too — the blob locks
// in styles and class names.
it('renders the button', () => {
  const { container } = render(<MyButton />);
  expect(container).toMatchSnapshot(); // 🚫 BANNED — do not use
  expect(container).toMatchInlineSnapshot(); // 🚫 BANNED — do not use
});
```

## ✅ Robust UI Assertion

```ts
it('displays error message when API fails', async () => {
  mockApi.failOnce();
  const { findByText } = render(<MyComponent />);

  expect(await findByText('Something went wrong')).toBeOnTheScreen();
});
```

**Test the Test**:

```ts
it('hides selector when disabled', () => {
  const { queryByTestId } = render(<Selector enabled={false} />);

  expect(queryByTestId('IPFS_GATEWAY_SELECTED')).toBeNull();

  // Break test: change enabled={false} to enabled={true} and verify test fails
});
```

## Reviewer Responsibilities

Validate tests fail when code breaks • Ensure proper matchers • **Reject new `toMatchSnapshot()` calls, rendered-UI `toMatchInlineSnapshot()`, and new `.snap` files** • Reject complex names with AND/OR

```ts
// OK
it('renders button when enabled');

// NOT OK
it('renders and disables button when input is empty or missing required field');
```

## Workflow

Always run tests after changes • Confirm all pass before commit • **Do not add new `toMatchSnapshot()` calls, and never snapshot rendered UI inline** — migrate existing ones to explicit assertions when touching a test file

**Resources**: [Contributor docs](https://github.com/MetaMask/contributor-docs/blob/main/docs/testing/unit-testing.md) • [Jest Matchers](https://jestjs.io/docs/using-matchers) • [React Native Testing Library](https://testing-library.com/docs/react-native-testing-library/intro/)
