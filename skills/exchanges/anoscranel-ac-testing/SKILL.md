---
name: ac-testing
description: "Automated software testing: test strategy and portfolios, coverage policy and CI test gates, unit and integration test design, test-driven development, property-based / mutation / fuzz testing, flaky-test triage, browser and end-to-end tests. Use when asking \"what should we test\"\"write the failing test first\", \"is this a bug or is the test wrong\",, \"write a test plan\", \"set a coverage target\", \"write tests for this\", \"should I mock this\", \"do it test-first\", \"red-green-refactor\", \"are my tests good enough\", \"this test fails randomly\", \"write a Playwright test\". Not for debugging the product bug itself, the pipeline's own wiring, or WCAG conformance checks; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Testing

## Overview

Six leaves cover the automated-testing craft: the portfolio and its gates, the design of one test, the red-green-refactor cycle, adequacy measures beyond coverage, the flake triage loop, and browser-level end-to-end checks. Strategy chooses what to test; the rest do the testing.

## When to use

- Choosing levels, coverage policy and CI test gates for a project.
- Designing unit, integration or contract tests: doubles, fixtures, data.
- Working test-first, or writing the failing reproduction test for a bug fix.
- Judging suite strength with mutation, property or fuzz testing.
- Diagnosing and fixing a nondeterministic test.
- Writing Playwright/Cypress-style browser tests for a critical journey.

## When not to use

- Reproducing or fixing the product bug the test exposed — outside this skill.
- Wiring the CI pipeline itself, its caching or its gate order — outside this skill.
- Accessibility conformance audits — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/test-strategy.md` | Test portfolio and CI gates | "what should we test" |
| `subskills/writing-tests.md` | Design one unit or integration test | "write tests for this" |
| `subskills/tdd.md` | Red-green-refactor | "do it test-first" |
| `subskills/test-adequacy.md` | Property, mutation, fuzz testing | "are my tests good enough" |
| `subskills/flaky-tests.md` | Nondeterministic tests | "this test fails randomly" |
| `subskills/browser-e2e-testing.md` | Browser and end-to-end tests | "write a Playwright test" |

## See also

- `subskills/test-strategy.md` — pick the portfolio.
- `subskills/writing-tests.md` — build one test right.
- `subskills/tdd.md` — the test-first loop.
- `subskills/test-adequacy.md` — prove the suite catches mutants.
- `subskills/flaky-tests.md` — kill the flake.
- `subskills/browser-e2e-testing.md` — the thin top layer.
