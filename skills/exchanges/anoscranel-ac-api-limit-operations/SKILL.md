---
name: ac-api-limit-operations
description: "Operating an application on metered or rate-limited third-party AI APIs without being broken by them: the provider's limit contract and which dimension binds, client-side request budgeting and queues, the degradation ladder that keeps serving when the API cannot, fallback chains across providers, key pools for deployments entitled to them, and metering reconciled against the bill. It treats the provider's limit as a system input to be engineered around; it never recommends a provider and never abuses a limit regime. Use when asking \"429 handling\", \"rate limit strategy\", \"API quota management\", \"fallback provider chain\", \"API key rotation\", \"degradation ladder\", \"backpressure to callers\", \"throttle my own callers\". Not for prompt packing to reduce request count (ac-single-request-value), not for retry budgets and circuit breakers across generic dependencies (ac-resilience-budgets), not for provider SDK mechanics like auth and streaming (ac-llm-api-integration)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# API limit operations

## Overview

An application that calls a metered AI API has two systems to operate: its own features and the provider's limit regime. The limit is not an error to be retried away; it is a contract published by the provider — so many requests per minute, per day, and per tier — and the application either engineers within it or is periodically broken by it. A 429 arriving at peak load is the system receiving the bill for a design that never read the contract.

This skill is the operational layer: reading the contract, budgeting client-side so the limit is respected by design rather than discovered by rejection, degrading gracefully when the budget is exhausted, falling back across providers, and metering actual usage against the provider's own accounting. The previous skill in this pair packs more value into each request; this one keeps the application alive and honest around the limits those requests hit.

Primary sources: <https://docs.anthropic.com/en/api/rate-limits> and <https://ai.google.dev/gemini-api/docs/rate-limits>.

## When to use

- When an application depends on third-party AI APIs with request or quota limits.
- When 429 responses, throttling, or daily quota exhaustion affect availability.
- When traffic varies unpredictably and the limit contract must hold across peaks.
- When usage must reconcile against a provider's metered bill.

## When NOT to use

- For packing more value into each individual request (use ac-single-request-value).
- For generic retry budgets, timeouts, and circuit breakers (use ac-resilience-budgets).
- For provider SDK mechanics — auth, streaming, tool-use loops (use ac-llm-api-integration).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/limit-contract.md` | `software-engineering/limit-contract` | Reading the provider's limit documentation and which dimension actually binds. |
| `subskills/client-side-budgeting.md` | `software-engineering/client-side-budgeting` | Token buckets and quotas enforced before the request is sent. |
| `subskills/degradation-ladder.md` | `software-engineering/degradation-ladder` | Service levels the product can drop through while staying up. |
| `subskills/fallback-chains.md` | `software-engineering/fallback-chains` | Provider and model fallbacks, and their honest switching costs. |
| `subskills/key-pools.md` | `software-engineering/key-pools` | Multiple keys and rotation for deployments entitled to them. |
| `subskills/metering-and-reconciliation.md` | `software-engineering/metering-and-reconciliation` | Counting what was spent and reconciling against the provider's meter. |
| `subskills/limit-ops-record.md` | `software-engineering/limit-ops-record` | The written record: budget, rejections, degradations, and reconciliation. |

## Status and honest limits

Provider limit regimes change without notice and differ by tier, model, and programme; every number this skill uses is read from the provider's current published page and dated. Key pooling is legitimate only where entitlement actually exists; multiplying keys to dodge a limit is abuse of the regime and this skill does not teach it. Nothing here recommends a provider: the fallback chain is a resilience pattern, not a vendor ranking, and the honest switch has costs — behavioural differences between providers mean the fallback answer must be labelled as such.
