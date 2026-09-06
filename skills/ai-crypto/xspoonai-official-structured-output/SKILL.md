---
name: structured-output
description: Stable structured JSON output for agents using strict schemas. Use when you need deterministic JSON responses, schema validation, or streaming JSON object assembly (generateObject/streamObject-style) with retry-and-repair loops.
---

# Structured Output (Strict JSON)

Implement stable, schema-validated JSON outputs for agents. Use this when responses must be valid JSON, match a schema exactly, and be reliable under retries/streaming.

## Core Workflow

1. Define a strict schema (JSON Schema or Pydantic).
2. Generate JSON-only output (no prose).
3. Validate output against schema.
4. If invalid, run a repair pass with a minimal error-focused prompt.
5. For streaming, emit incremental JSON with a deterministic assembly buffer.

## Prompt Pattern (Non-Streaming)

Use a strict system instruction and a minimal user prompt. Always require JSON only. Input can be empty; output must still match the schema.

Template:

```
SYSTEM:
You are a JSON generator. Output ONLY valid JSON that matches the given schema.
Do not include Markdown, comments, or trailing text.
If a field is unknown, use null (unless schema disallows it).

USER:
Return JSON that matches this schema:
<SCHEMA>

Input:
<INPUT>
```

## Prompt Pattern (Streaming)

Use the same schema but ensure the model emits a single JSON object and nothing else. Stream tokens and buffer until a valid JSON parse succeeds.

## Implementation References

- JSON Schema + retry/repair loop: see `references/json_schema_patterns.md`
- Pydantic models + parsing: see `references/pydantic_patterns.md`
- Python examples: `scripts/generate_object.py`, `scripts/stream_object.py`

## Guardrails

- Reject non-JSON output immediately; re-prompt with error-only instructions.
- Disallow extra keys unless `additionalProperties` is explicitly true.
- Keep schemas small and explicit; prefer enums for constrained values.
- Log schema + error details for debugging (do not expose stack traces to end users).
