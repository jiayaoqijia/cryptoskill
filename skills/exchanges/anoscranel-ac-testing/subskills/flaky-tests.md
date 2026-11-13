---
name: flaky-tests
domain: software-engineering/flaky-tests
trigger: "\"This test fails randomly\", \"passes locally fails in CI\", \"passes alone fails in parallel\", \"should we quarantine this\", \"just add a retry\"."
anti_trigger: "A deterministic product bug; a red pipeline from infra or config; browser waits and selectors (subskills/browser-e2e-testing.md)."
scope: "Finding, quarantining and fixing nondeterministic tests"
status: "seedling"
---

# Flaky Tests

## Standard

- **Definition**: a test that passes and fails on the same code. Playwright labels a test that fails then passes on retry "flaky" (https://playwright.dev/docs/test-retries).
- **Scale**: Google reported about 16% of tests flaky at least once and about 84% of pass-to-fail transitions due to flakes (John Micco, 2016). ⚠️ Vendor talk, secondary-cited.
- **Causes, in triage order**: concurrency, async and time, shared state, infrastructure. Concurrency was the top cause in 23% of 559 fixed flake reports (SAP HANA). ⚠️ One industrial DBMS corpus.
- **Detection**: rerun-only detection undercounts. Rerun plus mutation found a median 740 flaky tests vs 163 by rerun alone (ICSE 2026, https://dl.acm.org/doi/10.1145/3744916.3773125).
- **Not every failure is a flake**: 26% of non-flaky CI failures were wrong or obsolete tests (Hilton et al., FSE 2017).

## Decision rules

1. Retries are a diagnosis tool, not a fix. Cap at 2 in CI. ⚠️ House cap. Report retried-then-passed tests as flaky; never as green.
2. Quarantine a flaky test that blocks others. Every quarantined test gets an owner, a ticket and a time box. ⚠️ Length of the time box is house convention.
3. A quarantined test still runs, on a non-blocking job, so you keep data.
4. Time box expires → fix or delete with a reason. Never leave a test in quarantine with no owner.
5. Fix the cause, not the symptom. Replace sleeps with waits on a condition.
6. If the product is nondeterministic (a real race), it is a bug. Leave the test red and fix the product.
7. Track flake rate per test. Gate: suite rerun rate under 1%.

## Procedure

1. Confirm it is flaky: rerun the same commit many times.
   ```bash
   pytest tests/test_x.py::test_y --count=50 -p no:randomly   # pytest-repeat
   npx playwright test x.spec.ts --repeat-each=50
   go test -run TestY -count=50 -race ./...
   ```
2. Force each cause: random order and isolation; workers on and off; frozen or shifted clock and timezone; CPU stress; race detector or ThreadSanitizer.
3. Compare a failing run's logs, trace and timing with a passing run. Find the first divergence.
4. Fix by cause:
 - async: await the event, or poll for the condition with a timeout;
 - shared state: own data and teardown per test;
 - time: inject a clock;
 - order: remove hidden dependence on another test;
 - infra: health-wait for the dependency, or use an ephemeral container.
5. Verify: 50+ consecutive passes, with and without parallel workers.
6. Release from quarantine. Close the ticket with the cause class.

## Anti-patterns

- Blanket retries that hide real races.
- `sleep(5)` as the fix.
- Quarantine with no owner or end date.
- Blaming the test when the product has the race.

## Done checklist

- [ ] Flakiness reproduced by repetition.
- [ ] Cause class named: concurrency, time, shared state, order or infra.
- [ ] Fix removes the cause; no added sleep or retry.
- [ ] 50+ clean repeat runs.
- [ ] Quarantine entry closed with cause.

## Sources

- <http://martinfowler.com/articles/practical-test-pyramid.html>
- <https://dl.acm.org/doi/10.1145/3744916.3773125>
- https://playwright.dev/docs/test-retries · https://docs.cypress.io/app/guides/test-retries
