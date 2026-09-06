# Integration Testing Guidelines

Create, update, and fix controller-app integration tests (`*.integration.test.ts`) using the MetaMask Mobile `tests/integration/` framework.

Use this skill whenever you need to:

- Write a new integration test file
- Update tests after a controller / service / harness has changed
- Diagnose and fix a failing integration test
- Add a new per-domain harness or extend an existing one

Your job is to figure out whether the user needs to **write a new test**, **fix a failing test**, **update tests after a controller change**, or **add/extend a harness**, then follow the corresponding path and open the relevant reference when that path indicates.

## Testing layers (read first)

Follow installed `knowledge/testing-layers.md` before choosing integration vs component-view vs unit vs E2E. Prefer **CV → integration → unit fallback → E2E**. Use integration tests when the behavior crosses the app-to-controller seam and must exercise real controller, provider, or service code. Pure UI variants belong in component-view tests; pure logic belongs in unit tests; device/native journeys belong in E2E only after CV and integration are ruled out.

**Decision tree — which reference to use:**

```
Task → What do you need?
├─ Write new test or update after change
│  → Read controller/service + existing tests
│  → Open integration/writing-tests.md (use cases, harness selection, file structure, assertions)
│  → If the harness doesn't fit → also open integration/harness-extension.md
│  → After writing: run tests, then open integration/reference.md for self-review
│
├─ Fix failing test
│  → Run: yarn jest -c jest.config.integration.js <path> --runInBand --silent --coverage=false
│  → Identify error type → Open integration/reference.md (Diagnosing Failures)
│
├─ Add a new domain harness or extend an existing one
│  → Open integration/harness-extension.md (when to extend, structure, REAL/MOCKED split, AGENTS.md updates)
│
└─ Run tests or self-review after tests pass
   → Open integration/reference.md (Run the Tests, Self-Review Checklist)
```

Do not read the full reference files until the decision tree or workflow sends you there.

---

## What Are Integration Tests?

Integration tests are **controller-app integration** tests that exercise real controller / provider / service code with the I/O boundary mocked. They live alongside the code as `<feature>.integration.test.ts` and use a dedicated framework in `tests/integration/`.

Key constraint: **only the I/O boundary may be mocked** (SDK clients, wallet, subscription services, native modules, keyring). Shape B/C harnesses may also mock documented app-shell glue when the real target chain still runs. The controller, its services, validation logic, and state transitions all run for real at the chosen boundary. The harness for each domain owns the standard `jest.mock(...)` declarations; tests don't add their own.

Before changing tests, read `tests/integration/AGENTS.md`. For the full four-layer strategy and rollout plan, also read `tests/integration/STRATEGY.md`.

---

## The Framework at a Glance

```
tests/integration/
├── AGENTS.md                  ← framework rules + per-domain harness inventory
├── STRATEGY.md                ← four-layer strategy + comparison tables + rollout plan
├── coverage.svg               ← diagram (which test type runs real code at which layer)
├── coverage-and-tracking.md   ← coverage targets + bug-tracking mechanisms
├── perps-use-cases.md         ← every perps use case → primary test layer
└── harnesses/
    ├── perps.ts               ← Shape A: provider-level harness
    ├── perps-flow.ts          ← Shape B: hook-flow harness
    └── perps-component.tsx    ← Shape C: rendered-component harness
```

Tests live next to the code they test, named `<feature>.integration.test.ts`. They run via `yarn jest -c jest.config.integration.js`.

---

## Workflow (summary)

- **Write new test**: Read controller / service and existing tests → list use cases (or pull from per-domain use-case file) and map to test patterns → check coverage and deduplicate → choose Shape A/B/C based on the boundary under test → call the matching harness factory → write test (call real action, assert on state / selector output / return value). Every test must call at least one real method on the real instance returned by the harness — no harness-only setup. Run tests, then run the self-review checklist in `integration/reference.md`.
- **Fix failing test**: Run with `jest.config.integration.js` → identify error type from the table in `integration/reference.md` (Diagnosing Failures) → apply the fix (extend harness, override mock for one test, await async settlement, reset module-level singleton state, etc.) → re-run.
- **Update after change**: Same as write — review existing tests, update the harness if shape changed, update tests, run and self-review.
- **Add or extend a harness**: Open `integration/harness-extension.md` → identify whether you're adding a new domain or extending an existing one → follow the structure (jest.mock + factory + REAL/MOCKED header) → update `tests/integration/AGENTS.md` if it's a new domain.

For full detail, use the reference files when the decision tree sends you there.

---

## Run the tests

Always use `jest.config.integration.js` — the default Jest config excludes integration tests.

**Run a single test (no coverage):**

```bash
yarn jest -c jest.config.integration.js <path> --runInBand --silent --coverage=false
```

Example: `yarn jest -c jest.config.integration.js app/components/UI/Perps/hooks/usePerpsFlipPosition.integration.test.ts --runInBand --silent --coverage=false`

**Run the full integration suite:**

```bash
yarn jest -c jest.config.integration.js
```

**Coverage for a feature folder** (run with `--collectCoverageFrom` pointed at the controller / provider you're exercising — coverage on the test file itself will always be near zero):

```bash
yarn jest -c jest.config.integration.js <test-path> \
  --coverage \
  --collectCoverageFrom="app/controllers/perps/providers/HyperLiquidProvider.ts"
```

For run-by-name, watch mode, or other options, see `integration/reference.md` (Run the Tests).

---

## Golden Rules (Enforced)

1. **Only the harness mocks the I/O boundary** — no arbitrary `jest.mock()` in `*.integration.test.ts` files. The harness file (`tests/integration/harnesses/<domain>.ts`) owns the full set; tests just import it. Shape B/C may also mock documented app-shell glue inside the harness when the real target chain still runs. If you find yourself wanting a new mock, extend the harness instead.

2. **Drive behaviour through real method calls on the real instance** — call `provider.placeOrder(...)`, `controller.flipPosition(...)`, etc. The harness returns the real instance; the test exercises it. No simulating state transitions by reaching inside the controller's internals.

3. **Assert on observable outcomes** — return values, post-call state, selector output. Mock-call assertions are allowed only when verifying a side effect (e.g. that the SDK was called with the right args) is the explicit point of the test.

4. **Reuse harnesses** — never rebuild the controller setup from scratch in a test. If the harness doesn't expose what you need, extend it.

5. **No fake timers** — never use `jest.useFakeTimers()`, `jest.advanceTimersByTime()`, or `jest.useRealTimers()`. Use `await` and `waitFor` for async settlement.

6. **No snapshot tests** — assert on specific values. State shape changes are caught by integration tests that exercise the relevant flow, not by snapshotting the controller output.

7. **Follow AAA** — Arrange (build harness, set mocks) → Act (call real method) → Assert (check return value / state). Blank lines between sections. One test = one user flow or one rejection path; multiple chained calls in one test are fine when they represent one user journey.

8. **No harness-only tests** — every test must call at least one real method on the harness's instance. Tests that only construct the harness and assert on default state are not integration tests; they're testing the harness defaults, which is wasted effort.

9. **One test = one use case from the matrix** — each `it` should map to a row in the per-domain use-case file (e.g. `perps-use-cases.md`). If a test doesn't fit any use case, ask whether the use case is missing from the matrix or the test is in the wrong layer.

10. **Module-level singleton state is reset per test** — the harness handles this for known singletons (`TradingReadinessCache`, etc.). If you depend on a new singleton, add its reset to the harness; don't rely on test-order.

---

## Reference files (when to use)

Documentation is split by **action**. Open only the reference that matches what you are doing.

| Action                                          | File                                                                 | When to open it                                                                                                                                |
| ----------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Writing or updating integration tests**       | [`integration/writing-tests.md`](integration/writing-tests.md)         | New test file, new use case, updated controller. Read before writing, use cases and matrix, file structure, harness usage, assertion patterns. |
| **Adding or extending a harness**               | [`integration/harness-extension.md`](integration/harness-extension.md) | New domain, new mock, new helper, new option. REAL/MOCKED split, factory shape, AGENTS.md updates.                                             |
| **Running tests, self-review, fixing failures** | [`integration/reference.md`](integration/reference.md)                 | Run the Tests, Self-Review Checklist, Diagnosing Failures, assertion patterns, module-singleton state, What NOT to Do, Quick Reference.        |

**Where self-review and What NOT to Do live:** Both are in `integration/reference.md`. Self-review is the checklist you run after tests pass. What NOT to Do is the antipatterns section in the same file. Keeping them there means when you run tests or fix failures you have run commands, the checklist, the failure table, and the antipatterns in one place — open that reference for any run/fix/review task.
