# Extension E2E

Router for Selenium E2E under `test/e2e/`. Confirm the layer gate in
`knowledge/extension-testing-layers.md` first (why unit is insufficient).

## Open next

| If the work is… | Open |
| --- | --- |
| Write or update a spec / page object / flow / fixture | [`writing-tests.md`](e2e/writing-tests.md) |
| Fix a flaky or failing E2E, or clean bad practices | [`maintain.md`](e2e/maintain.md) |
| Diagnose a known CI flake pattern | [`flakiness.md`](e2e/flakiness.md) |
| Audit POM anti-patterns (locators, try/catch, delays, …) | [`pom-antipatterns.md`](e2e/pom-antipatterns.md) |

## Create process

1. Layer gate — document the browser/extension/dapp/window boundary.
2. Inspect the feature folder: nearby `*.spec.ts`, page objects, flows, fixtures.
3. Prefer `FixtureBuilderV2`; put locators in page objects; use flows only for
   multi-page workflows.
4. Run: `yarn build:test` (or `yarn start:test`) then
   `yarn test:e2e:single <path> --browser=chrome`.
5. Self-check against [`pom-antipatterns.md`](e2e/pom-antipatterns.md).

## Maintain process

1. Reproduce / classify via [`flakiness.md`](e2e/flakiness.md).
2. If structural POM smell → [`pom-antipatterns.md`](e2e/pom-antipatterns.md).
3. Prefer deterministic waits and mocks over retries or `driver.delay`.
4. Re-run the single affected spec.

## Out of scope

- Visual verification with `mm` CLI → `visual-testing` skill
- Unit-only failures → [`../unit.md`](unit.md)
