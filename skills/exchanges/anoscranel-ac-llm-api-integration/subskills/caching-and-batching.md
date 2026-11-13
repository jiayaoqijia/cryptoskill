---
name: caching-and-batching
domain: software-engineering/llm-api-integration
trigger: "Configuring prompt caching, optimizing context window prefixes, and submitting asynchronous batch jobs for cost reduction"
anti_trigger: "Real-time streaming response handling (subskills/streaming-and-timeouts.md); handling real-time rate limit errors (subskills/error-and-resilience.md)"
scope: "Prompt caching prefixes, Time-To-Live management, batch API endpoints, and cost-latency trade-off analysis"
status: "seedling"
---

# Caching and Batching

## Standard

- **Anthropic Prompt Caching Guide**: identifying static prefix structures, cache retention windows, and read-versus-write pricing differentials. <https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching>
- **OpenAI Batch API Documentation**: submitting asynchronous batch JSONL workloads for discounted batch processing and high-throughput ingestion. <https://platform.openai.com/docs/guides/batch>

## Decision rules

- Use prompt caching for large static contexts such as codebase repositories, system instructions, documentation libraries, and extensive few-shot examples to reduce latency and input token costs.
- Structure prompt prefixes consistently across requests, placing static system instructions and reference materials at the very beginning of the prompt to maximize cache hit rates.
- Use asynchronous batch APIs for non-latency-sensitive workloads (such as nightly log analysis, corpus translation, or dataset labeling) to benefit from reduced pricing tiers.
- Reserve real-time synchronous endpoints for interactive user experiences where immediate response latency is paramount.

## Procedure

1. Identify static reference materials and system instructions that remain unchanged across multiple sequential requests.
2. Structure the prompt payload so static cacheable blocks appear first, followed by dynamic user inputs at the end.
3. Include provider-specific caching declaration flags or cache control headers in the API request payload.
4. Monitor cache hit metrics and token usage headers in API responses to verify that cached tokens are successfully registered.
5. For offline bulk processing, format input datasets as JSONL files, upload them via batch endpoints, and poll for asynchronous job completion.

## Anti-patterns

- Placing dynamic user inputs or timestamps at the beginning of prompt prefixes, destroying cache locality.
- Using real-time synchronous APIs for large-scale bulk processing tasks where asynchronous batch endpoints are cheaper.
- Neglecting cache TTL expiration rules, leading to unexpected cache misses on intermittent workloads.
- Failing to verify cache hit utilization headers in API response metadata.

## Done checklist

- [ ] Static instructions and reference materials are positioned at prompt beginnings.
- [ ] Prompt caching flags or control headers are configured in requests.
- [ ] Bulk workloads utilize asynchronous batch APIs for cost reduction.
- [ ] Cache hit performance and token savings are verified via response metadata.

## Sources

- Anthropic, "Prompt Caching Documentation", <https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching>
- OpenAI, "Batch API Guide", <https://platform.openai.com/docs/guides/batch>

⚠️ Caching pricing structures, minimum prompt length thresholds, and Time-To-Live retention periods vary across providers and model tiers; consult current documentation before relying on cache economics.


⚠️ Provider API pricing models and parameter default behaviors vary across releases; always verify operational metrics against current production traffic.