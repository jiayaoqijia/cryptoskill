# Component View Testing Guidelines

Create, update, and fix component view tests (`*.view.test.tsx`) using the `tests/component-view/` framework.

## When to use

**Default Mobile layer** for screen/view UI behavior through real Redux/app state.

Use this skill whenever you need to:

- Cover new or changed screen/view behavior (prefer CV over broad unit tests)
- Write a new component view test file
- Update tests after a component or preset has changed
- Diagnose and fix a failing component view test

If the case is pure logic / helpers, or CV cannot cover it yet, open [`unit.md`](unit.md) for the smallest focused unit test and document why.

## Testing layers (read first)

Follow installed `knowledge/testing-layers.md` for the full decision tree. Choose by layer inside **mobile-testing**. Prefer **CV → integration → unit fallback → E2E**; multi-screen journeys are CV-first when routes can be registered — do not jump to Appium for “journey” alone.

Your job is to figure out whether the user needs to **write a new test**, **fix a failing test**, or **update tests after a component/preset change**, then follow the corresponding path and open the relevant reference when that path indicates.

**Decision tree — which reference to use:**

```
Task → What do you need?
├─ Write new test or update after change
│  → Read component + existing tests
│  → Open component-view/writing-tests.md (use cases, coverage, renderer/preset, file structure)
│  → If test needs navigation: also open component-view/navigation-mocking.md
│  → After writing: run tests, then open component-view/reference.md for self-review
│
├─ Fix failing test
│  → Run: yarn jest -c jest.config.view.js <path> --runInBand --silent --coverage=false
│  → Identify error type → Open component-view/reference.md (Diagnosing Failures)
│     including sibling-skeleton, empty-state load, list hydration, mockReset
│
└─ Run tests or self-review after tests pass
   → Open component-view/reference.md (Run the Tests, Self-Review Checklist)
```

Do not read the full reference files until the decision tree or workflow sends you there.


## What Are Component View Tests?

Component view tests are **integration-level** tests that test views through real Redux state — no mocked hooks or selectors. They live alongside the component as `ComponentName.view.test.tsx` and use a dedicated framework in `tests/component-view/`.

Key constraint: **only Engine and allowed native modules may be mocked** (enforced at runtime by `app/util/test/testSetupView.js` and by ESLint override in `.eslintrc.js` for `**/*.view.test.*`).


## The Framework at a Glance

```
tests/component-view/
├── mocks.ts              ← Engine + native mocks (import this first, always)
├── render.tsx            ← renderComponentViewScreen, renderScreenWithRoutes
├── stateFixture.ts       ← StateFixtureBuilder (createStateFixture)
├── platform.ts           ← describeForPlatforms, itForPlatforms (run per iOS/Android)
├── api-mocking/          ← HTTP API mocks (nock) — extensible, one file per feature
├── presets/              ← initialState<Feature>() builders — one file per feature area
└── renderers/            ← render<Feature>View() functions — one file per feature area
```


## Workflow (summary)

- **Write new test**: Read component and existing tests → list use cases and map to test patterns → check coverage and deduplicate → use or create renderer/preset → write test (use `renderScreenWithRoutes` if asserting navigation). Every test must have at least one of: `fireEvent`, `waitFor`/`findBy`, `store.dispatch`/`act`, or Engine spy (no render-only scenarios). Run tests, then run the self-review checklist in `component-view/reference.md`.
- **Fix failing test**: Run with `jest.config.view.js` → identify error type from the table in `component-view/reference.md` (Diagnosing Failures) → apply the fix (remove disallowed mock, add state override, add preset, wrap in `waitFor`, add `deterministicFiat`, etc.) → re-run.
- **Update after change**: Same as write — review existing tests, extend preset/renderer if needed, update tests, run and self-review.

For full detail (use cases, coverage, presets, route probes, self-review checklist, failure table), use the reference files when the decision tree sends you there.


## Run the tests

Always use `jest.config.view.js` — the default Jest config does not apply component view test rules.

**Run tests (no coverage):**

```bash
yarn jest -c jest.config.view.js <path> --runInBand --silent --coverage=false
```

Example: `yarn jest -c jest.config.view.js app/components/UI/Bridge/Views/BridgeView/BridgeView.view.test.tsx --runInBand --silent --coverage=false`

**Coverage for a feature folder** (use this instead of `--coverage` to avoid OOM):

```bash
yarn test:view:coverage:folder app/components/UI/MyFeature
```

For run-by-name, watch mode, or other options, see `component-view/reference.md` (Run the Tests).


## Golden Rules (Enforced)

1. **Only mock Engine and allowed native modules** — no arbitrary `jest.mock()` in `*.view.test.*` files. Allowed:
   - `../../app/core/Engine`
   - `../../app/core/Engine/Engine`
   - `react-native-device-info`
   - (these are already handled by `tests/component-view/mocks.ts`)

2. **Drive all behavior through Redux state** — no mocking of hooks or selectors. Provide data via state overrides.

3. **Reuse presets and renderers** — never rebuild the full state manually from scratch.

4. **No fake timers** — never use `jest.useFakeTimers()`, `jest.advanceTimersByTime()`, or `jest.useRealTimers()`.

5. **Test behavior, not snapshots** — use `toBeOnTheScreen()`, `not.toBeOnTheScreen()`, interaction assertions.

6. **Follow AAA** — Arrange → Act → Assert, blank lines between each section. One test = one user journey or business outcome; multiple chained actions in a single test are fine.

7. **No render scenarios** — every test must have at least one of: `fireEvent`, `waitFor`/`findBy`, `store.dispatch`/`act`, or an Engine spy. Static visibility checks are not tests. See [`component-view/writing-tests.md`](component-view/writing-tests.md) for examples.

8. **Use constants and i18n helpers, never raw strings** — every `getByTestId` / `findByTestId` / `queryByTestId` must reference a constant from `ComponentName.testIds.ts`. Every `getByText` / `findByText` / `getAllByText` that targets a localised label must use `strings('key')` from `locales/i18n`, not a hardcoded string literal. Dynamic testIds (e.g. `trader-row-${trader.id}`) must be derived from fixture data, not embedded as `'trader-row-trader-1'`. Create the testIds file if it does not exist.

9. **Every view with async data needs one data-completeness test** — wait for the load and validate all significant fields of all items in the base mock using `within()` per row. One per independent async data flow.

10. **Filter / segmentation tests must assert both sides** — after selecting a filter, assert both what appears (positive `findByTestId`) and what disappears (negative `queryByTestId(...).not.toBeOnTheScreen()`). Spy-only checks (refetch count / analytics) are not enough — seed distinct before/after rows.

11. **Match loading asserts to real UX** — pending-phase tests assert skeleton / not-yet-visible content, not optimistic titles the production screen does not show while loading.

12. **Pull-to-refresh via `refreshControl.props.onRefresh`** — prefer the prop handler inside `act`; `fireEvent(scrollView, 'refresh')` often never hits the handler.

13. **Await the content, not just its container** — a container arriving on screen says nothing about values inside it that have their own async source (a child query, a debounce, a skeleton). Await the gated value with `findBy*`, then re-query the container and scope the remaining synchronous assertions with `within()`.

14. **Do not nest `find*` inside `waitFor`** — `findBy*` already *is* `waitFor` + `getBy` (default timeout 1000 ms). Nesting them shares that budget, so CI can fail with a bare `Timed out in waitFor.` and no assertion detail. Use `await findBy*` **or** `waitFor(() => { getBy*; expect(...) })` with an explicit `{ timeout }` when you need extra time. Never `waitFor(async () => { await findBy*(...) })`.

15. **Reset mock implementations between tests** — `jest.clearAllMocks()` clears call history but keeps the last `mockResolvedValue` / `mockImplementation`. If a case changes an Engine or `controllerMessenger.call` implementation, `mockReset()` (or restore/recreate) in `beforeEach`. Otherwise later cases in the same file or shard can flake.

16. **Do not wait on a sibling loading proxy** — header, list, and action rows can load independently. Await the control or value under test, or the loading UI that *owns* it. A details skeleton clearing is not proof that a share button or buy CTA is mounted.

17. **Empty-state and list completeness** — wait until list loading is gone, then assert copy unique to the selected filter (shared empty `testID`s can detach). For lists, wait until every expected row test ID is present before asserting per-row fields. The first row is not hydration complete.

18. **Negative assertions after the positive path could have rendered** — wait for the owning load phase or skeleton to finish, then assert absence. Immediate `queryBy*` after render is a false green.

19. **Run the tests before declaring done** — run `yarn jest -c jest.config.view.js <file> --runInBand --silent --coverage=false` and confirm all tests are green. A test file that has never been run is not done.

20. **Run format:check before declaring done** — run `npx prettier --check <file>` (or `yarn format:check`) on the new test file and every new supporting file (renderer, preset, api-mock). Auto-fix with `npx prettier --write <file>` if needed, then re-check.


## Reference files (when to use)

Documentation is split by **action**. Open only the reference that matches what you are doing.

| Action                                          | File                                                                   | When to open it                                                                                                                                |
| ----------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Writing or updating view tests**              | [`component-view/writing-tests.md`](component-view/writing-tests.md)           | New test file, new or updated preset/renderer. Read before writing, use cases and coverage, file structure, renderers, presets, route params.  |
| **Testing navigation**                          | [`component-view/navigation-mocking.md`](component-view/navigation-mocking.md) | Route probes, single nav push, multi-screen renderer, cross-screen journey, external/API mocking.                                              |
| **Running tests, self-review, fixing failures** | [`component-view/reference.md`](component-view/reference.md)                   | Run the Tests, Self-Review Checklist, Diagnosing Failures, assertion patterns, Deterministic Fiat Assertions, What NOT to Do, Quick Reference. |

**Where self-review and What NOT to Do live:** Both are in `component-view/reference.md`. Self-review is the checklist you run after tests pass. What NOT to Do is the antipatterns section in the same file. Keeping them there means when you run tests or fix failures you have run commands, the checklist, the failure table, and the antipatterns in one place — open that reference for any run/fix/review task.
