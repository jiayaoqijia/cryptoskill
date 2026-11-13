---
name: browser-e2e-testing
domain: software-engineering/browser-e2e-testing
trigger: "\"Write a Playwright test\", \"add a Cypress test\", \"test the checkout flow end to end\", \"check the console for errors\", \"assert no failed network requests\"."
anti_trigger: "Unit and integration test design (subskills/writing-tests.md); random failures in any suite (subskills/flaky-tests.md); WCAG conformance; Core Web Vitals."
scope: "End-to-end and browser tests: selectors, waits, traces, DevTools checks"
status: "seedling"
---

# Browser and End-to-End Testing

## Standard

All facts are vendor-primary for their own tool.

- **Playwright locators**: prefer user-facing attributes — `getByRole`, `getByText`, `getByLabel`, `getByPlaceholder`, `getByAltText`, `getByTitle`, then `getByTestId`. Avoid CSS-class and DOM-path selectors. Locators are strict: an action throws if more than one element matches (https://playwright.dev/docs/locators; https://playwright.dev/docs/best-practices).
- **Auto-wait**: before an action Playwright checks the element is visible, stable, receives events and is enabled (https://playwright.dev/docs/actionability).
- **Web-first assertions**: `await expect(locator).toBeVisible()`, not `expect(await locator.isVisible()).toBe(true)` (best-practices).
- **Retries** default to 0; fail-then-pass is labelled "flaky". Trace option `on-first-retry` is the documented CI setting (https://playwright.dev/docs/test-retries; https://playwright.dev/docs/trace-viewer-intro).
- **Cypress**: select with `data-*` attributes (`data-cy`); never `cy.wait(Number)`; wait on route aliases or assertions (https://docs.cypress.io/app/core-concepts/best-practices).
- **Chrome DevTools Protocol**: `Runtime.consoleAPICalled`, `Runtime.exceptionThrown`, `Network.responseReceived`, `Network.loadingFailed` (https://chromedevtools.github.io/devtools-protocol/).

## Decision rules

1. E2E covers only critical journeys: sign-up, login, pay, the core task. Everything else goes lower in the stack.
2. Locator order: role with name → label → text → test ID. Use a test ID only when no accessible name exists.
3. No fixed sleeps. Wait on a visible state, a URL or a network response.
4. Each test owns its data. Seed via API, not by clicking through setup screens.
5. Fail the test on any uncaught page error or console `error`. ⚠️ House rule; allow-list known third-party noise explicitly.
6. Fail on any 5xx response or failed request to your own origin.
7. CI: retries at most 2, trace on first retry, video or screenshot on failure. A retried pass is reported as flaky.
8. Run against a production-like build, not a dev server with hot reload.

## Procedure

1. Name the journey and its success signal (URL, heading, toast, row in a table).
2. Seed data through the API in a fixture.
3. Write the test:
   ```ts
   import { test, expect } from '@playwright/test';

   test('user can log in', async ({ page }) => {
     const errors: string[] = [];
     page.on('pageerror', e => errors.push(e.message));
     page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
     page.on('response', r => { if (r.status() >= 500) errors.push(`${r.status()} ${r.url()}`); });

     await page.goto('/login');
     await page.getByLabel('Email').fill('a@example.com');
     await page.getByLabel('Password').fill('pw');
     await page.getByRole('button', { name: 'Sign in' }).click();
     await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
     expect(errors).toEqual([]);
   });
   ```
4. Config: `retries: process.env.CI ? 2 : 0`, `use: { trace: 'on-first-retry' }`.
5. Run 20 times locally (`--repeat-each=20`) before merging.
6. On failure, open the trace (`npx playwright show-trace`) and read actions, DOM snapshot, console and network at the failing step.
7. Put the smoke subset in post-merge CI; the full set nightly.

## Anti-patterns

- `.btn-primary > div:nth-child(2)` selectors.
- `waitForTimeout(3000)`.
- Testing every edge case through the browser.
- Shared test accounts mutated by parallel tests.
- Ignoring console errors because "the page looks fine".

## Done checklist

- [ ] Journey is critical; edge cases tested lower.
- [ ] Role or label locators; no CSS-path selectors.
- [ ] No fixed sleeps; web-first assertions.
- [ ] Console, page-error and 5xx checks fail the test.
- [ ] Trace on retry; 20 clean local repeats.

## Sources

- <https://contextqa.com/blog/self-healing-test-automation/>
- https://playwright.dev/docs/best-practices · https://docs.cypress.io/app/core-concepts/best-practices
