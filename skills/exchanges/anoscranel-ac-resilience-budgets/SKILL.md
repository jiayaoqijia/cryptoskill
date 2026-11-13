---
name: ac-resilience-budgets
description: "Bounding failure so it stays local: timeout budgets that add up across a call chain, retry budgets and why retries amplify outages, jittered backoff, circuit breaking and half-open recovery, bulkheads and pool isolation, load shedding and admission control, degradation modes chosen in advance, and the written resilience record. It explains how failure propagates and how to bound it; it never guarantees availability and never replaces capacity planning. Use when asking \"timeout budget\", \"retry storm\", \"exponential backoff\", \"jitter\", \"circuit breaker\", \"bulkhead\", \"load shedding\", \"admission control\", \"graceful degradation\", \"brownout\", \"why did one slow service take everything down\". Not for SLO definition and error budgets (ac-reliability), not for failure injection and capacity testing (ac-chaos-and-capacity-testing), not for provider SDK retry policy (ac-llm-api-integration)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Resilience budgets

## Overview

Failure spreads through the paths that connect services, and the mechanism is usually time rather than errors. A caller waits on a dependency with no timeout, its own connection pool fills with waiting requests, its callers queue behind it, and a single slow dependency becomes a system-wide outage without a single error being returned. Resilience budgets are the set of limits that stop that propagation.

This skill covers those limits: how timeouts compose across a call chain, why retries amplify an outage unless they are bounded by a budget, how circuit breakers and bulkheads isolate a failing path, how load shedding protects the requests that can still be served, and how to choose a degradation mode before it is needed. Capacity testing and SLO definition belong to other skills.

Primary sources: <https://sre.google/> and <https://aws.amazon.com/builders-library/>.

## When to use

- When designing the failure behaviour of a service that calls others.
- When an outage was caused by one dependency rather than by the service itself.
- When retry policy is being set and its amplification is not considered.
- When deciding what to shed or degrade under overload.

## When NOT to use

- For SLO definition, error budgets, and alerting (use ac-reliability).
- For failure injection and capacity measurement (use ac-chaos-and-capacity-testing).
- For a specific SDK's built-in retry behaviour (use ac-llm-api-integration).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/timeout-budgets.md` | `software-engineering/timeout-budgets` | How per-call timeouts compose, and the deadline that must propagate. |
| `subskills/retry-budgets.md` | `software-engineering/retry-budgets` | Why retries amplify, and the budget that bounds them. |
| `subskills/backoff-and-jitter.md` | `software-engineering/backoff-and-jitter` | Exponential backoff, jitter, and the synchronisation it prevents. |
| `subskills/circuit-breaking.md` | `software-engineering/circuit-breaking` | Open, half-open, closed, and the recovery that must be proven. |
| `subskills/bulkheads-and-pools.md` | `software-engineering/bulkheads-and-pools` | Isolating a failing dependency's resource use from everything else. |
| `subskills/load-shedding.md` | `software-engineering/load-shedding` | Admission control and dropping work deliberately rather than failing. |
| `subskills/resilience-record.md` | `software-engineering/resilience-record` | The written record: budgets, degradation modes, and their tests. |

## Status and honest limits

Resilience mechanisms add failure modes of their own: a circuit breaker that opens too eagerly removes a working dependency, a timeout set too tight converts latency into errors, and a retry budget sized without measurement either does nothing or amplifies. Every mechanism here needs a test that shows it engages at the intended point, and nothing in this skill guarantees availability.
