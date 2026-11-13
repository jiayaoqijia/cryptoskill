---
name: error-and-resilience
domain: software-engineering/llm-api-integration
trigger: "Handling LLM API error codes, rate limits, context-length overflows, content filters, fallback routing, and telemetry"
anti_trigger: "Structuring standard successful requests (subskills/request-shape.md); implementing streaming chunk parsers (subskills/streaming-and-timeouts.md)"
scope: "Error taxonomy, retry policies, fallback degradation paths, and observability for token counts, latency, and cost"
status: "seedling"
---

# Error and Resilience

## Standard

- **OWASP LLM Top 10**: mitigating risks related to prompt injection, excessive agency, and unsafe output handling in application integrations. <https://genai.owasp.org/llm-top-10/>
- **Provider Error Handling Guides**: identifying HTTP status codes for rate limits (`429`), authentication failures (`401`), invalid requests (`400`), and server overloads (`503`). <https://platform.openai.com/docs/guides/error-codes>

## Decision rules

- Categorize API errors into transient failures (rate limits, server errors, timeouts) which warrant exponential backoff retries, and permanent failures (invalid keys, malformed requests, context length overflows) which fail fast without retry.
- Implement circuit breakers and fallback model routing when primary provider endpoints experience prolonged outages or severe degradation.
- Log token consumption, request latency, and estimated cost metrics for every API call while sanitizing prompts and response content to protect user privacy and sensitive data.
- Handle content filter blocks gracefully, informing users when safety classifiers trigger without exposing raw internal error traces.

## Procedure

1. Wrap API invocation logic in robust error-handling blocks that capture specific HTTP status codes and provider error objects.
2. Inspect error codes; trigger exponential backoff with jitter on `429` (rate limit) and `503` (server overload) responses.
3. Fail immediately on `400` (bad request) or `401` (unauthorized) errors, logging the diagnostic details without exposing sensitive credentials.
4. Record structured telemetry events containing token counts, latency duration, model identifiers, and cost metrics for operational monitoring.
5. Fall back to secondary backup models or providers if primary availability checks fail repeatedly.

## Anti-patterns

- Implementing endless retry loops on permanent client-side errors (such as `400` invalid requests).
- Logging raw prompt text containing personally identifiable information or sensitive code into shared telemetry systems.
- Failing to monitor rate limit headers and token consumption metrics in production environments.
- Crashing client applications ungracefully when upstream LLM services experience temporary outages.

## Done checklist

- [ ] Transient errors trigger exponential backoff retries while permanent errors fail fast.
- [ ] Fallback routing is configured for primary provider outages.
- [ ] Token counts, latency, and cost telemetry are logged per request.
- [ ] Prompt content is sanitized or excluded from sensitive logging channels.

## Sources

- OWASP, "LLM Top 10 Security Guidance", <https://genai.owasp.org/llm-top-10/>
- OpenAI, "Error Codes and Handling Guide", <https://platform.openai.com/docs/guides/error-codes>

⚠️ Provider-specific error response bodies and rate-limit header naming conventions differ across platforms; verify exact field structures for each integrated service.


⚠️ Provider API pricing models and parameter default behaviors vary across releases; always verify operational metrics against current production traffic.