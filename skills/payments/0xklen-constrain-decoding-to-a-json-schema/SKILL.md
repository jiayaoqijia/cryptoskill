---
name: constrain-decoding-to-a-json-schema
description: Use when you need reliably-typed output from a model. Prefer the provider's structured-output or grammar-constrained decoding over prompt-and-hope, and know which constraints the engine actually enforces.
---

# Constrain decoding to a JSON schema

Asking politely for JSON is a probability, not a guarantee. When the API supports schema-constrained decoding, the sampler physically cannot emit a token that breaks the grammar — use that instead of retry loops.

## Procedure

1. Check whether your provider offers it: OpenAI `response_format: {"type": "json_schema", "json_schema": {...}}`, Anthropic tool-use with a forced tool choice, or a GBNF/grammar backend on local runners.

2. Express the contract as an actual JSON Schema, not prose: types, enums, `required`, and `additionalProperties: false`.

3. Pass the schema in the structured-output field — do not also describe it in the prompt; duplicated instructions drift apart.

4. Set `strict: true` (or the provider's equivalent) and confirm in the response metadata that it was honoured.

5. Keep the schema closed and flat where possible: constrained decoders force the model down legal paths, but an over-wide schema (free-form nested objects) still leaves the shape underdetermined.

6. Test with adversarial input designed to tempt an invalid value ("price: free") and confirm the output is still schema-valid.

7. Still validate on your side — constrained decoding guarantees the shape, not the truth of the values.

8. Fall back gracefully: if the provider rejects a schema keyword, retry without it and validate on your side rather than failing the whole request.

9. Test the schema itself: a wrong schema makes every output "invalid", so confirm a hand-written valid sample passes before blaming the model.

## Pitfalls

- Assuming the flag guarantees semantics; the model still fills a plausible-but-wrong date inside a perfectly valid schema.
- Mixing a strict schema with a prompt that describes a different shape, confusing the model about which to follow.
- Leaving `additionalProperties` open, so the decode permits invented keys your code ignores.
- Using "grammar constraints" in a provider that only suggests them — confirm the mode is really active.
- Free-form fields (unbounded strings) re-introduce exactly the unconstrained behaviour you were removing.
- Assuming every provider's "structured output" is grammar-constrained; some only validate after generation, which still permits a truncated object.
- Applying a strict schema to open-ended generation, where the grammar caps helpful prose and can push the model into a loop.
- A schema with a required field the model cannot always know (`id`), so the decode fails rather than returning null.

## Verification

    curl -s "$API" -d @req.json | jq '.choices[0].finish_reason'   # stop/valid, never length

Report: "forced tool_choice with a strict schema; 300/300 outputs schema-valid including adversarial inputs; shape guaranteed, values still validated in code."
