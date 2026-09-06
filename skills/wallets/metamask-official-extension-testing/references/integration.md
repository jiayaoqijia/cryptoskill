# Extension integration tests

Integration owns behavior that crosses a meaningful in-process boundary but
does not require a real browser. Extension already has two integration homes;
choose between them by the seam under test.

## Choose the home

| Behavior under test | Existing home |
| --- | --- |
| Full UI tree consuming real Redux state, with background RPC mocked | `test/integration/**/*.test.tsx` |
| Real `MetaMaskController` and child-controller composition, with external I/O mocked | `app/scripts/metamask-controller.test.js` or `app/scripts/metamask-controller.actions.test.js` |

These homes are part of the same Integration layer. Do not add a new
`*.integration.test.ts` convention or a Mobile-style harness tree. Do not add
the same scenario to both homes unless they protect distinct boundaries.

## UI + state integration

Use this home when the regression is visible through the full UI and Redux
state, but no browser, extension window, service worker, or dapp boundary is
required.

### Existing pattern

- Render with `integrationTestRender` from `test/lib/render-helpers.js`.
- Run the real `Root` component and real Redux store.
- Supply realistic preloaded state and vary only scenario-specific fields.
- Mock the background RPC (`submitRequestToBackground`) and external HTTP with
  nock.
- Interact through React Testing Library and assert observable UI behavior.

Keep hooks, selectors, reducers, and relevant child components real. Native,
WASM, or animation stubs are acceptable when jsdom cannot execute them. Treat
other hook or child-component mocks as exceptions and explain why they are
required.

Before adding coverage, inspect the nearest suites and shared helpers under
`test/integration/`. Reuse their state builders and mocks rather than creating
a parallel harness.

Run:

```bash
yarn test:integration
yarn test:integration:coverage
```

## Composed-background integration

Use this home when isolated controller tests are insufficient because the
regression depends on `MetaMaskController` initialization, messenger wiring,
delegation between child controllers, or composed state transitions.

### Existing pattern

- Add the scenario next to the relevant existing `describe` in
  `app/scripts/metamask-controller.test.js`.
- Use `app/scripts/metamask-controller.actions.test.js` for the action-facing
  surface already covered there.
- Construct and call the real `MetaMaskController` and relevant child
  controllers.
- Reuse existing test tools such as `createTestProviderTools`, `mockEncryptor`,
  nock, browser API mocks, and shared setup helpers.
- Mock external I/O boundaries only: network requests, browser APIs, providers,
  hardware/native bridges, encryption, or unavailable services.
- Drive behavior through public methods/actions and assert observable return
  values, controller state, emitted actions/events, or delegated calls.

Do not replace a real child controller with a mock when its composition is the
behavior being tested. If only one controller's logic matters, keep the test
colocated with that controller and use [`unit.md`](unit.md).

These files currently run through the unit Jest configuration. That command
name does not change the boundary they exercise:

```bash
yarn test:unit app/scripts/metamask-controller.test.js
yarn test:unit app/scripts/metamask-controller.actions.test.js
```

## When E2E is still required

Use [`e2e.md`](e2e.md) when confidence requires a real browser/extension
boundary, such as popup or notification windows, dapp/provider injection, MV3
service-worker lifecycle, browser permissions, or built-extension wiring.

“This is a user journey” is not enough when either integration home exercises
the responsible boundary with equivalent confidence.

## Hard rules

1. Pick the home by boundary, not by nearby file convention.
2. Keep external I/O deterministic; do not call live services.
3. Reuse existing setup and helpers before adding mocks or fixtures.
4. Do not create a third integration home without team agreement.
5. Keep one scenario focused on one observable contract.

## Pointers

- UI suites: `test/integration/**/*.test.tsx`
- UI render helper: `test/lib/render-helpers.js`
- UI config: `jest.integration.config.js`
- Composed background: `app/scripts/metamask-controller.test.js`
- Composed actions: `app/scripts/metamask-controller.actions.test.js`
- Testing philosophy: `docs/testing.md`
