---
name: streaming-and-timeouts
domain: software-engineering/llm-api-integration
trigger: "Implementing streaming responses, Server-Sent Events parsing, connection timeouts, and exponential backoff retries"
anti_trigger: "Structuring non-streaming completion payloads (subskills/request-shape.md); handling permanent API error codes (subskills/error-and-resilience.md)"
scope: "Streaming response handling, partial output parsing, connect and read timeouts, exponential backoff retries, and idempotency"
status: "seedling"
---

# Streaming and Timeouts

## Standard

- **MDN Server-Sent Events Guide**: consuming real-time event streams over HTTP connections using text/event-stream formatting. <https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events>
- **OpenAI API Streaming Reference**: handling incremental chunk delivery, connection drops, and stream termination events. <https://platform.openai.com/docs/api-reference/chat/streaming>

## Decision rules

- Enable streaming responses for user-facing chat interfaces and long-running generation tasks to reduce perceived latency and provide immediate visual feedback.
- Bypass streaming and use standard synchronous requests for automated background jobs, batch data pipelines, and strict request-response API endpoints where intermediate partial text is unhelpful.
- Configure explicit connection timeouts (fast failure) and read timeouts (generous chunk intervals) to prevent client threads from hanging indefinitely when LLM inference stalls.
- Implement exponential backoff with jitter on transient network errors and rate limits, ensuring retries never overwhelm recovering upstream servers.

## Procedure

1. Initialize an HTTP request with streaming enabled, configuring appropriate headers to accept `text/event-stream`.
2. Open a connection and read the response body incrementally line by line, parsing Server-Sent Events data blocks as they arrive.
3. Accumulate text deltas into a complete response buffer while emitting incremental updates to user interface renderers or logging streams.
4. Catch connection interruptions or read timeouts mid-stream, verifying whether the termination was clean (`[DONE]`) or truncated.
5. Apply retry logic with exponential backoff and randomized jitter if the initial connection fails before receiving the first data chunk.

## Anti-patterns

- Using infinite timeout thresholds on HTTP client connections waiting for LLM generation.
- Attempting automatic retries on requests that failed midway through a streamed generation without ensuring idempotency.
- Failing to handle malformed JSON chunks or network drops gracefully during event stream parsing.
- Streaming responses in background automated services where synchronous payload returns are cleaner and safer.

## Done checklist

- [ ] Server-Sent Events streams are parsed incrementally without blocking.
- [ ] Connect and read timeouts are explicitly configured on HTTP clients.
- [ ] Exponential backoff with jitter is applied to transient connection failures.
- [ ] Stream termination events are cleanly detected and handled.

## Sources

- MDN Web Docs, "Using server-sent events", <https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events>
- OpenAI, "API Reference - Streaming", <https://platform.openai.com/docs/api-reference/chat/streaming>

⚠️ Streaming chunk event formats and sentinel termination strings differ slightly between providers (such as SSE data prefixes versus binary framing); verify provider documentation when integrating new backends.


⚠️ Provider API pricing models and parameter default behaviors vary across releases; always verify operational metrics against current production traffic.