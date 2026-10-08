---
name: validate-a-response-body-against-its-schema
description: Use when parsing third-party JSON. Validate the payload against a schema before use so a silent field change fails loudly at the boundary, not deep in business logic.
---

# Validate a response body against its schema

Parsing a third-party payload on trust turns a removed field into a `KeyError` three layers down
or, worse, a silent `None` that flows into a sum. Check the shape at the boundary.

## Procedure

1. Derive a schema from the OpenAPI spec or, absent one, from observed responses, and commit it as `schemas/item.schema.json`.
2. Validate before touching any field:
   ```python
   import jsonschema
   try:
       jsonschema.validate(instance=r.json(), schema=SCHEMA)
   except jsonschema.ValidationError as e:
       raise ValueError(f"schema mismatch at {list(e.absolute_path)}: {e.message}")
   ```
3. Set `"required": [...]` explicitly to the fields you depend on rather than trusting `additionalProperties`.
4. Type-check numbers: a schema `"type": "number"` catches the server that stringifies an id.
5. Validate once at the boundary in a `parse_*` function per endpoint, then pass typed objects inward.
6. For huge payloads, validate the structural keys plus a sampled subset to keep cost bounded.
7. Fail closed in production (raise/alert); log-and-continue only where the run genuinely survives without the field.

## Pitfalls

- `additionalProperties: false` breaks on additive server changes; set it true and require what you need.
- Validating only page one misses variant shapes on later pages.
- `NaN`/`Infinity` pass some parsers but fail strict schema numbers; normalise before validating.
- A schema copied once drifts from the API and becomes fiction; regenerate from the spec.
- `{}` validates against a schema with no `required` fields, hiding a total failure.

## Verification

    python -m jsonschema -i fixture.json schemas/item.schema.json && echo OK

The fixture passes and a deliberately corrupted fixture fails with a named path. Report: "Validated 10,000 responses; 3 rejected with field paths; 0 reached business logic malformed."
