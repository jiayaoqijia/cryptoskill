---
name: test-strategy
domain: software-engineering/test-strategy
trigger: "\"What should we test\", \"write a test plan\", \"pyramid or trophy\", \"set a coverage target\", \"which tests gate CI\", \"our suite is too slow to trust\"."
anti_trigger: "Designing one test (subskills/writing-tests.md); test-first cycle (subskills/tdd.md); mutation, property or fuzz work (subskills/test-adequacy.md); pipeline wiring."
scope: "Choosing the test portfolio, levels, coverage policy and CI test gates"
status: "seedling"
---

# Test Strategy

## Standard

- **Portfolio shapes**: Cohn's pyramid — many unit, fewer integration, thin end-to-end (https://martinfowler.com/articles/practical-test-pyramid.html). Dodds' trophy — integration as the largest band (https://kentcdodds.com/blog/the-testing-trophy-and-testing-classification). Spotify honeycomb for microservices.
- **Level definitions**: unit = one module, in memory, milliseconds; integration = component plus real infrastructure, often containers; end-to-end = real client through the deployed stack.
- **Test process standard**: ISO/IEC/IEEE 29119 frames testing by level, type and technique. ⚠️ ISO text paywalled; structure from secondary sources.
- **Coverage**: line coverage measures reach, not assertion strength. Gate on the diff, not the global number.
- **Gates**: test pass, coverage delta, lint, typecheck, static analysis, contract verification, performance budget.

## Decision rules

1. Pick the shape by where bugs live: logic library → pyramid; UI or glue code → trophy; many services → honeycomb plus contracts.
2. Each test level must catch a defect class the level below cannot. If not, drop the test.
3. Coverage gate: at least 80% of changed lines covered. ⚠️ Convention. Never mandate 100% global coverage.
4. Google-class global guide: about 60% acceptable, 75% commendable, 90% exemplary. ⚠️ Numbers vary by post and year. Use as a reference, not a gate.
5. Pair coverage with a strength signal: mutation score on critical modules, escaped-defect rate (subskills/test-adequacy.md).
6. Pre-merge suite budget: about 10 minutes. ⚠️ House line. Slower suites get skipped.
7. End-to-end tests cover only the few journeys that earn money or lose data. ⚠️ "3–10 journeys" is a house heuristic.
8. Production checks (canary, synthetics) complement pre-merge tests. They never replace them.
9. Risk-tier the code: payment, auth, data-loss paths get the strictest gate.

## Procedure

1. List the top risks: what failure costs most, and where it would come from.
2. Map each risk to the cheapest level that catches it.
3. Write the strategy, one page:
   ```markdown
   ## Scope and risks
   ## Levels (unit / integration / contract / e2e): what each owns
   ## Tools per level
   ## Test data and environments
   ## CI gates: pre-merge, post-merge, nightly
   ## Coverage and strength targets
   ## Flake policy (owner, time box)
   ## Exit criteria for a release
   ```
4. Measure the current suite: count per level, runtime p50/p95, flake rate, slowest 10 tests.
5. Set gates in CI: unit + integration + lint + diff coverage pre-merge; e2e smoke post-merge; full e2e, mutation and fuzz nightly.
6. Review the strategy monthly against escaped defects. For each escape ask: which level should have caught it? Add that test.

## Anti-patterns

- Ice-cream cone: mostly manual and e2e tests.
- Global 100% mandate met by assertion-free tests.
- The same check duplicated at every level.
- No exit criteria.

## Done checklist

- [ ] Risks listed and mapped to levels.
- [ ] One-page strategy written.
- [ ] Pre-merge gates set, suite inside budget.
- [ ] Diff-coverage gate on; no global 100% rule.
- [ ] Escaped-defect review scheduled.

## Sources

- <http://martinfowler.com/articles/practical-test-pyramid.html>
- <https://en.wikipedia.org/wiki/BS_7925-1>
- <https://aiwisdom.dev/articles/testing-engineering/test-architecture-strategy>
- https://martinfowler.com/articles/practical-test-pyramid.html
