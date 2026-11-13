---
name: request-shape
domain: software-engineering/llm-api-integration
trigger: "Structuring completion requests, setting parameters, defining system roles, and enforcing schema-constrained JSON output"
anti_trigger: "Configuring base URLs and auth headers (subskills/provider-and-endpoint.md); handling streaming response chunks (subskills/streaming-and-timeouts.md)"
scope: "Choosing model tiers, setting completion parameters, role separation, and structured output via JSON schema"
status: "seedling"
---

# Request Shape

## Standard

- **JSON Schema Specification**: defining machine-readable structural constraints for data payloads and structured model outputs. <https://json-schema.org>
- **Anthropic API Reference**: structuring message roles, system instructions, and completion parameters. <https://docs.anthropic.com/en/api/getting-started>

## Decision rules

- Select model tiers based on task complexity: lightweight models for high-throughput classification and extraction, and frontier reasoning models for complex synthesis and code generation.
- Separate system instructions from user inputs, placing global constraints, tone directives, and formatting rules in the system role rather than mixing them into user prompts.
- Set temperature deterministically (`0.0`) for data extraction, code generation, and structured output tasks where consistency is required, and use higher temperatures (`0.7` to `1.0`) only for creative writing and brainstorming.
- Enforce strict JSON output schemas using provider-native structured output parameters rather than relying solely on prompt instructions to guarantee parseable responses.

## Procedure

1. Construct the API request payload containing the model identifier, system instruction array, and ordered message history.
2. Configure generation parameters including maximum output tokens, temperature, top_p sampling thresholds, and explicit stop sequences.
3. Attach structured output definitions or JSON schemas to the request parameters when downstream code requires guaranteed schema compliance.
4. Dispatch the completion request and capture the response envelope, extracting the generated text content and token usage statistics.
5. Validate the returned JSON payload against the expected schema before passing data to downstream application logic.

## Anti-patterns

- Mixing system instructions and user messages into a single unstructured text block.
- Relying on natural language prompt instructions alone to enforce JSON output format without schema constraints.
- Leaving maximum output token limits unbounded, risking runaway generation and high latency.
- Hardcoding model names without supporting fallback aliases or configuration-driven model selection.

## Done checklist

- [ ] Completion requests separate system guidance from user message history.
- [ ] Generation parameters (temperature, max tokens) match task requirements.
- [ ] Structured JSON outputs are validated against formal schemas.
- [ ] Token usage metadata is captured from response envelopes.

## Sources

- JSON Schema, "Standard Specification", <https://json-schema.org>
- Anthropic, "API Reference and Message Structure", <https://docs.anthropic.com/en/api/getting-started>

⚠️ Provider-specific parameter names (such as `max_tokens` versus `max_output_tokens` or schema enforcement flags) vary across API versions; consult current provider documentation for exact payload schemas.


⚠️ Provider API pricing models and parameter default behaviors vary across releases; always verify operational metrics against current production traffic.

⚠️ Production deployment guidelines require thorough monitoring of token latency distributions and error retry frequency to maintain reliable client-side integrations.