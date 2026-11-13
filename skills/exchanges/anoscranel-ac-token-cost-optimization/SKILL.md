---
name: ac-token-cost-optimization
description: 'Spending the fewest dollars per completed task on model APIs: the anatomy of a pricing page (input, cached input, output all priced separately), model tiering and the cascade from cheap to strong, prompt-cache discounts and what a cache hit actually costs, batch discounts and the latency they buy, context-window economics where input tokens dominate, the spend ledger and attribution, and the written cost record. It treats dollars-per-task as the cost metric; it never recommends a provider and never quotes a price as current. Use when asking "token cost", "cost per million tokens", "why is my API bill so high", "model cascade", "cheaper model first", "prompt caching discount", "batch API discount", "output tokens cost more", "cost per task", "spend ledger", "token budget dollars". Not for packing more into each request (ac-single-request-value), not for the SDK mechanics of cache and batch endpoints (ac-llm-api-integration), not for cloud infrastructure unit economics (ac-cost-aware-engineering).'
license: MIT
metadata:
  domain: prompt-engineering
status: seedling
---

# Token cost optimization

## Overview

Every model API prices three things separately: input tokens, cached input tokens, and output tokens — and output almost always costs several times input. A request is therefore not one number but a shape: how much context it carries, how much of that context repeats across requests, and how much it writes back. Two workloads with identical token counts can differ by an order of magnitude in dollars because their shapes differ.

This skill optimizes the dollar side of model usage. Its counterpart, ac-single-request-value, minimizes the number of requests per answer; this one minimizes the dollars per answer. The mechanics it does not own: the HTTP wiring of cache and batch endpoints belongs to ac-llm-api-integration, and cloud infrastructure spend belongs to ac-cost-aware-engineering.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/pricing> and <https://platform.openai.com/docs/guides/prompt-caching>.

## When to use

- When a model API bill is higher than the work justifies.
- When choosing between model tiers for a task or a step.
- When repeated prompts could pay cache-hit rates instead of full input rates.
- When building a spend ledger that attributes dollars to tasks.

## When NOT to use

- For squeezing more out of each individual request (use ac-single-request-value).
- For cache and batch endpoint mechanics, TTLs, and payloads (use ac-llm-api-integration).
- For cloud, storage, and egress unit economics (use ac-cost-aware-engineering).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/pricing-anatomy.md` | `prompt-engineering/pricing-anatomy` | Reading a pricing page: input, cached input, output, and the shape of a request. |
| `subskills/model-tiering-cascades.md` | `prompt-engineering/model-tiering-cascades` | Routing work to the cheapest tier that clears the bar, with escalation. |
| `subskills/prompt-cache-economics.md` | `prompt-engineering/prompt-cache-economics` | Cache hits, cache writes, and arranging prompts so prefixes repeat. |
| `subskills/batch-discounts.md` | `prompt-engineering/batch-discounts` | Trading latency for the batch discount, honestly. |
| `subskills/context-window-economics.md` | `prompt-engineering/context-window-economics` | Input-token dominance: what context earns its place. |
| `subskills/output-token-economics.md` | `prompt-engineering/output-token-economics` | The expensive half of the bill: caps, format, and reasoning tokens. |
| `subskills/spend-ledger.md` | `prompt-engineering/spend-ledger` | Attributing dollars to tasks, steps, and tenants. |
| `subskills/cost-record.md` | `prompt-engineering/cost-record` | The written record: baselines, changes, and per-task dollars. |

## Status and honest limits

Prices change without notice, so this skill reads pricing pages as dated evidence and never quotes a figure as current. Every optimization here trades something — latency for batch discounts, quality risk for cheaper tiers, restructuring effort for cache hits — and the record states the trade, not just the saving. Nothing recommends a provider; the mechanics apply to any metered model API.
