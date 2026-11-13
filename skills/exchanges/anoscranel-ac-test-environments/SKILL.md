---
name: ac-test-environments
description: "Environments where tests run beyond the developer's machine: local parity with CI, ephemeral preview environments per change, shared versus isolated test data, seeded data and its realism, environment drift and how it breaks tests, concurrent test execution and shared-state conflicts, and the written environment record. It explains how to make environments reproducible and trustworthy; it never recommends a cloud vendor and never promises a functional test suite. Use when asking \"works on my machine\", \"CI environment\", \"preview environment\", \"ephemeral environment\", \"test data seed\", \"environment drift\", \"flaky in CI\", \"shared staging\", \"parallel test conflicts\". Not for test case design (ac-testing), not for CI pipeline wiring (ac-ci-and-release), not for deployment strategy (ac-ci-and-release)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Test environments

## Overview

A test is a claim about behaviour in an environment, and the environment is half the claim. Tests written against a developer's warm machine fail in a cold CI runner; tests written against seeded data pass until the data ages; tests pointed at a shared staging environment interfere with each other and with whoever else is using it. The environment is not background — it is a co-author of every result the suite reports.

This skill covers environments as an engineering subject: what parity between local and CI actually requires, what preview environments buy and cost, the seeded-versus-shared data decision, drift and its detection, and concurrency when many suites share a stage. Writing the tests belongs elsewhere; this is about making what they run against worthy of trust.

Primary source: <https://martinfowler.com/>.

## When to use

- When tests pass locally and fail in CI, or vice versa.
- When designing preview or ephemeral environments for a team.
- When deciding between shared staging infrastructure and isolated instances.
- When flakiness correlates with concurrent runs or aging data.

## When NOT to use

- For test case design and coverage (use ac-testing).
- For CI pipeline wiring (use ac-ci-and-release).
- For deployment strategy and rollback (use ac-ci-and-release).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/local-parity.md` | `software-engineering/local-parity` | Making the developer machine and CI agree. |
| `subskills/preview-environments.md` | `software-engineering/preview-environments` | A throwaway environment per change, and its cost. |
| `subskills/seeded-versus-shared-data.md` | `software-engineering/seeded-versus-shared-data` | Where test data comes from and why it ages. |
| `subskills/environment-drift.md` | `software-engineering/environment-drift` | Detecting when environments stop matching. |
| `subskills/concurrent-execution.md` | `software-engineering/concurrent-execution` | Parallel suites against shared stages. |
| `subskills/environment-cost.md` | `software-engineering/environment-cost` | What environments cost and how to keep them finite. |
| `subskills/environment-record.md` | `software-engineering/environment-record` | The written record of every environment class. |

## Status and honest limits

Environment differences are unbounded in principle — any two machines can differ infinitely — and the practical discipline is to make the differences declared rather than discovered. Contracts and pinned provisioning define what an environment promises; everything outside the contract is outside the test's guarantee. Nothing here recommends a vendor, and a perfectly reproducible environment running tests that do not matter produces very reliable noise.
