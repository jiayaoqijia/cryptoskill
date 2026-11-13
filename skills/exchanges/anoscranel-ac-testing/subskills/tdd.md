---
name: tdd
domain: software-engineering/tdd
trigger: "\"Do it test-first\", \"use TDD\", \"red-green-refactor\", \"write the failing test before the fix\", \"is TDD worth it here\"."
anti_trigger: "Designing a single test's doubles and data (subskills/writing-tests.md); choosing the whole test portfolio (subskills/test-strategy.md); named refactorings."
scope: "Red-green-refactor cycle, when TDD pays, test-first for bug fixes"
status: "seedling"
---

# Test-Driven Development

## Standard

- **Kent Beck, *Test-Driven Development: By Example* (2002)**: red → green → refactor.
- **Three laws**: (1) no production code without a failing test; (2) no more test than needed to fail; (3) no more code than needed to pass.
- **Evidence**: Nagappan et al., *Empirical Software Engineering* 2008 (DOI 10.1007/s10664-008-9062-z) — four industrial teams, 40–90% lower pre-release defect density, 15–35% slower initial development. Controlled replications find small or no external-quality effects. Fucci et al. (ICSE 2016): gains track small steps and test cleanliness more than test-first order.
- **Bug fixes**: a fix lands with a test that fails before and passes after.

## Decision rules

1. Use TDD when behaviour is clear and testable in isolation: pure logic, parsers, rules, bug fixes, API handlers.
2. Skip strict TDD for exploratory work. Spike first, throw it away, then test-drive the real version.
3. Every bug fix is test-first, always. Write the failing reproduction test before touching the code.
4. Steps stay small: one behaviour per cycle, minutes not hours. ⚠️ "Under 10 minutes per cycle" is a house heuristic.
5. The red step must fail for the right reason. Read the failure message; a typo or import error is not red.
6. Green may be ugly. Refactor only on green; run tests after each refactoring move.
7. Test behaviour through the public interface. Never assert private internals.
8. Do not claim TDD guarantees fewer defects. Claim faster feedback and testable design (evidence is mixed).
9. Agent work: the human or a separate gate owns the failing test. An agent that writes both test and fix can game its own check.

## Procedure

1. Write a list of behaviours to add, smallest first.
2. Pick one. Write one test that expresses it:
   ```python
   def test_rejects_empty_email():
       with pytest.raises(ValidationError):
           parse_signup({"email": ""})
   ```
3. Run it. Confirm it fails, and fails on the assertion.
4. Write the least code that makes it pass. Run all fast tests.
5. Refactor test and code: remove duplication, improve names. Re-run after each change.
6. Commit on green. Cross the behaviour off. Add new ones you discovered.
7. Repeat until the list is empty.
8. Bug-fix variant:
 1. Reproduce the bug by hand.
 2. Encode the reproduction as the smallest failing test.
 3. Confirm red, fix, confirm green.
 4. Run the full suite, not just the new test.
 5. Keep the test as a regression guard.

## Anti-patterns

- Writing many tests up front, then all the code.
- Skipping the red check; the test never could fail.
- Refactoring on red.
- Testing implementation details, so every refactor breaks tests.
- Fixing a bug with no failing test first.
- Selling TDD as a defect guarantee.

## Done checklist

- [ ] Each behaviour had a test that failed first for the right reason.
- [ ] All tests green; refactor done on green.
- [ ] Bug fixes carry a fails-before, passes-after test.
- [ ] Full suite run before commit.
- [ ] Tests use only public behaviour.

## Sources

- <http://martinfowler.com/articles/practical-test-pyramid.html>
- <https://github.com/byerlikaya/claude-starter-kit/blob/main/plugin/skills/systematic-debugging/SKILL.md>
- https://doi.org/10.1007/s10664-008-9062-z
