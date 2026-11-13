---
name: ac-llm-api-integration
description: "The craft of calling model APIs from application code, provider-agnostic: authentication and key handling, the core completion request, streaming and timeouts, the tool-use loop on the client side, prompt caching and batching, error taxonomy and resilience, and the evaluation/migration lifecycle. Use when asking \"call the Claude API\", \"integrate an LLM into my app\", \"add streaming to my AI feature\", \"tool use loop\", \"handle rate limits\", \"migrate to a new model\", \"prompt caching\". Not for prompt-design craft (ac-prompt-engineer), not for exposing tools to agents (ac-mcp-authoring), not for service SLOs (ac-reliability), not for product security review (ac-security-engineer)."
license: MIT
metadata:
  domain: software-engineering
---

# LLM API Integration

## Overview

Client-side model integration is code craft: calling APIs robustly from application code. This skill teaches provider-agnostic integration patterns including secure authentication, request structuring, streaming response handling, client-side agent tool loops, prompt caching optimization, error resilience, and model migration lifecycles.

## When to use

- Connecting application backend code to hosted or local model provider APIs.
- Implementing robust error handling, rate-limit retries, and fallback routing for AI features.
- Building client-side tool use loops and agentic execution handlers.
- Optimizing latency with streaming responses and reducing costs through prompt caching and batch endpoints.
- Migrating between model versions or provider endpoints safely with regression testing.

## When NOT to use

- Designing prompts, writing system instructions, or tuning few-shot examples (use `ac-prompt-engineer`).
- Authoring Model Context Protocol servers that expose tools to agents (use `ac-mcp-authoring`).
- Managing service-level objectives, error budgets, or system telemetry infrastructure (use `ac-reliability`).
- Conducting product security reviews or threat modeling for application codebases (use `ac-security-engineer`).

## Subskill index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/provider-and-endpoint.md` | software-engineering/llm-api-integration | Choosing the integration surface, base URLs, versioning paths, auth headers, and secret-manager key hygiene |
| `subskills/request-shape.md` | software-engineering/llm-api-integration | Choosing model tiers, setting completion parameters, role separation, and structured output via JSON schema |
| `subskills/streaming-and-timeouts.md` | software-engineering/llm-api-integration | Streaming response handling, partial output parsing, connect and read timeouts, exponential backoff retries, and idempotency |
| `subskills/tool-use-loop.md` | software-engineering/llm-api-integration | Client-side agent loop, tool schema definition, tool result submission, iteration guards, and parallel execution |
| `subskills/caching-and-batching.md` | software-engineering/llm-api-integration | Prompt caching prefixes, Time-To-Live management, batch API endpoints, and cost-latency trade-off analysis |
| `subskills/error-and-resilience.md` | software-engineering/llm-api-integration | Error taxonomy, retry policies, fallback degradation paths, and observability for token counts, latency, and cost |
| `subskills/evaluation-and-migration.md` | software-engineering/llm-api-integration | Regression test execution, model version pinning versus floating aliases, deprecation lifecycle tracking, and migration safety |

## Status and honest limits

Status: `seedling`. This skill covers client-side API integration mechanics and resilience patterns. It does not replace provider API documentation, SDK release notes, or comprehensive security audits.

⚠️ Provider APIs evolve rapidly across versions; always consult current provider documentation when implementing new endpoints or migrating between model families.
