---
name: writing-tests
domain: software-engineering/writing-tests
trigger: "\"Write tests for this\", \"should I mock this\", \"how do I set up test data\", \"add an integration test\", \"add a contract test\", \"these tests are brittle\"."
anti_trigger: "Picking the overall portfolio and gates (subskills/test-strategy.md); test-first workflow (subskills/tdd.md); browser-level tests (subskills/browser-e2e-testing.md); random failures (subskills/flaky-tests.md)."
scope: "Unit and integration test design: doubles, fixtures, test data, contract tests"
status: "seedling"
---

# Writing Tests

## Standard

- **Test doubles (Meszaros, via Fowler)**: dummy (fills a parameter), stub (canned answers), spy (records calls), mock (pre-set expectations, verifies interaction), fake (light working version, such as an in-memory DB) (https://martinfowler.com/articles/mocksArentStubs.html).
- **Hermetic tests**: no shared external state, no network, no uncontrolled clocks, no order dependence (Google Testing Blog, "Hermetic Testing").
- **Test data**: fixtures for read-only reference data; factories for per-test objects; API seeding for later journey steps; ephemeral databases (Testcontainers) for real-infrastructure integration.
- **Contract tests**: consumer-driven contracts (Pact) check real interactions; OpenAPI schema checks shape only.

## Decision rules

1. One test checks one behaviour. Name it for the behaviour: `test_expired_token_returns_401`.
2. Structure: Arrange, Act, Assert. One Act per test.
3. Double ladder: real object → fake → stub → mock. Stop at the first rung that is fast and deterministic.
4. Mock only at boundaries you do not own or cannot run cheaply: payment, email, clock, third-party API. Never mock your own logic.
5. Assert on outcomes (return values, state, emitted events). Assert on calls only when the call is the behaviour (an email was sent).
6. Each test creates and cleans its own data. Factories with defaults; tests override only the fields they care about.
7. Integration tests use the real database engine in a container, not an in-memory substitute with different semantics.
8. Inject time, randomness and IDs. Pin seeds and clocks.
9. Many consumers, high churn → consumer-driven contracts. Few stable consumers → schema validation.
10. A test that cannot fail when the code is broken is worse than none. Check by breaking the code once.

## Procedure

1. Name the behaviour and its edge cases: empty, one, many, boundary, invalid, error path.
2. Pick the level: pure logic → unit; database, queue or HTTP seam → integration; service boundary → contract.
3. Build data with a factory:
   ```python
   def make_user(**over):
       return User(**{"email": "a@example.com", "active": True, **over})

   def test_inactive_user_cannot_login(db):
       user = db.add(make_user(active=False))
       result = login(user.email, "pw")
       assert result.error == "inactive"
   ```
4. Replace only boundary dependencies with doubles. Prefer a fake you can reuse.
5. For integration, start a container per test session; reset state per test (transaction rollback or truncate).
6. Run the test. Then break the code under test and confirm the test fails. Restore.
7. Run the file in random order and in parallel. Fix any order dependence.
8. Keep each unit test in milliseconds; move slow ones to the integration tier.

## Anti-patterns

- Mocking everything; tests pass while production fails.
- Asserting "getUser was called" instead of the result.
- Shared mutable fixtures across tests.
- `sleep()` to wait for async work.
- In-memory SQLite standing in for Postgres.

## Done checklist

- [ ] Behaviour and edge cases listed and covered.
- [ ] Doubles only at boundaries; ladder respected.
- [ ] Data built per test; no order dependence.
- [ ] Each test seen failing against broken code.
- [ ] Unit tests fast; slow ones moved to integration.

## Sources

- <https://helpmetest.com/blog/test-data-management>
- <http://martinfowler.com/articles/practical-test-pyramid.html>
- https://martinfowler.com/articles/mocksArentStubs.html
