# Appium E2E (justified Mobile device journeys)

**If and only if** the layer gate in installed `knowledge/testing-layers.md`
justifies E2E, implement new device coverage in **Appium**. Appium is the
_framework_ for justified E2E — not the default _layer_ for every journey.

Multi-screen / navigation journeys are **CV-first** when routes and state/API
can be driven in the CV framework. Controller seams belong in integration.

Live source of truth in the mobile repo (read these when details change):

- `docs/testing/appium-smoke-testing.md`
- `docs/testing/e2e-testing.md` (Appium org, cross-framework POM)
- `tests/docs/UNIFIED_E2E_ARCHITECTURE.md`
- Nearby examples under `tests/smoke-appium/<feature>/`

## Before writing

0. **Layer gate** — Confirm CV and integration cannot cover this scenario with
   equivalent confidence. Document: why CV is insufficient, why integration is
   insufficient, and the required device/native boundary. If you cannot fill
   those three, stop and open installed `knowledge/testing-layers.md` or
   [`placement.md`](placement.md) instead of writing Appium.
1. Inspect existing Appium specs in the same feature folder.
2. Reuse page objects, flows, fixtures, and tags already used there.
3. Prefer shared `Gestures` / `Assertions` / `Matchers` — avoid
   raw `device.*` calls.
4. POM methods must **not** use `try/catch`.

## Layout

|          | Appium smoke                                                  |
| -------- | ------------------------------------------------------------- |
| Specs    | `tests/smoke-appium/<feature>/*.spec.ts`                      |
| Runner   | Playwright (`tests/playwright.smoke-appium.config.ts`)        |
| Commands | `yarn appium-smoke:ios` / `yarn appium-smoke:android`         |
| Build    | **main-e2e release** with `HAS_TEST_OVERRIDES=true`           |
| Tags     | Same `tests/tags.js` helpers; filter with Playwright `--grep` |

Place new coverage under `tests/smoke-appium/`.

## Spec template

```typescript
import { test as appiumTest } from "../../framework/fixtures/playwright/index.js";
import { SmokeAccounts } from "../../tags.js";
import { withFixtures } from "../../framework"; // or feature helper
import FixtureBuilder from "../../framework/fixtures/FixtureBuilder";
import { loginToAppPlaywright } from "../../viewHelper"; // or flows helper
import SomePage from "../../page-objects/...";

appiumTest.describe(SmokeAccounts("My feature"), () => {
  appiumTest(
    "does the thing",
    async ({ driver: _driver, currentDeviceDetails }) => {
      await withFixtures(
        {
          fixture: new FixtureBuilder().build(),
          restartDevice: true,
          currentDeviceDetails,
        },
        async () => {
          await loginToAppPlaywright({ scenarioType: "e2e" });
          await SomePage.tapSomething();
          await Assertions.expectElementToBeVisible(SomePage.result, {
            description: "result should be visible",
          });
        },
      );
    },
  );
});
```

Required Appium patterns:

- `import { test as appiumTest }` from Playwright fixture index
- `{ driver: _driver, currentDeviceDetails }` fixture args
- Pass `currentDeviceDetails` into `withFixtures`
- `loginToAppPlaywright(...)` for login
- No raw `device.*` APIs

Always check nearby specs for the exact imports used in that feature (some use
identity/`withIdentityFixtures` helpers).

## Cross-framework page objects

`Gestures`, `Assertions`, and common `Matchers` methods route at runtime.
Prefer them.

When selectors or flows must differ by runtime:

| Need                               | API                                                     |
| ---------------------------------- | ------------------------------------------------------- |
| Different testIDs per runtime      | `resolve({ detoxTestID, appiumTestID, ... })`           |
| Different selector strategy        | `encapsulated({ detox: () => ..., appium: () => ... })` |
| Structurally different action flow | `encapsulatedAction({ detox: ..., appium: ... })`       |

Only branch when the flow genuinely differs. See
`docs/testing/e2e-testing.md` and `tests/docs/UNIFIED_E2E_ARCHITECTURE.md`.

## Golden rules (Appium + shared framework)

1. Always use fixtures (`withFixtures` / feature fixture helpers) — no ad-hoc app state.
2. Always use Page Object Model — no raw selectors in specs.
3. Import framework utilities from the shared framework entrypoints used by
   neighboring specs — not one-off deep imports unless examples do.
4. Add `description` to every `Gestures.*` and `Assertions.*` call.
5. Never use `TestHelpers.delay()` / arbitrary `setTimeout` waits.
6. Use `FixtureBuilder` (or the feature’s fixture helper) for state — do not
   build prerequisites through UI when fixtures can set them.
7. Selectors live in `*.testIds.ts` (co-located) or shared selector modules.
8. Tag correctly via `tests/tags.js` and match existing feature tags.
9. Descriptive test names — no `should` prefix.
10. Spec helpers that perform UI steps belong in a **page object** (one page) or
    a **flow** (`tests/flows/*.flow.ts` / `e2e/flows/`) when spanning pages —
    never inline multi-step helpers in the spec.
11. Fix lint/tsc before running.
12. No `try/catch` in POM methods.

## Build and run

**Source of truth:** `docs/testing/appium-smoke-testing.md` (download, prep,
Android ABI/arm64, troubleshooting). Do not copy recipes into the skill.

Local run rules:

1. **main-e2e release** only (`HAS_TEST_OVERRIDES=true`) — not debug /
   Expo Connect-to-Metro builds.
2. Prefer **iOS** on Mac. Set `IOS_APP_PATH` (and `IOS_SIMULATOR_UDID` after
   `prepare-ios-appium-runner.mjs`) so `.e2e.env` `PREBUILT_*` debug paths lose.
3. Prefer CI artifacts via `gh run download`; warn before a local native build.
4. Run a targeted `--grep` / spec path. Do not claim green without output.

```bash
IOS_APP_PATH=build/ci-main-e2e/MetaMask.app \
IOS_SIMULATOR_UDID="$IOS_SIMULATOR_UDID" \
yarn appium-smoke:ios --grep SmokeAccounts \
  tests/smoke-appium/accounts/<spec>.spec.ts
```

## Review checklist

- [ ] Spec under `tests/smoke-appium/`
- [ ] Uses `appiumTest` + `currentDeviceDetails` + `loginToAppPlaywright`
- [ ] POM / flows only — no step helpers in the spec
- [ ] No `TestHelpers.delay()` / no raw `device.*` APIs
- [ ] Descriptions on gestures and assertions
- [ ] Correct smoke/regression tag
- [ ] Lint + tsc clean
- [ ] Ran locally against main-e2e (or documented why not) with real output
