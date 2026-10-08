---
name: validate-tool-arguments-against-schema-before-exec
description: Use when an agent builds tool arguments from model output. Validate them against the tool schema and check required fields and types before the call reaches the tool.
---

# Validate tool arguments against the schema before exec

Model-generated arguments are plausible, not correct. Types drift, required fields vanish, and enums arrive spelled wrong; validate before the call so the failure is a clear rejection, not a corrupt side effect.

## Procedure

1. Load the tool's declared schema and treat it as the contract: required fields, types, enums, ranges, formats.
2. Validate the argument object before execution with a real validator, not a glance: `jsonschema.validate(args, schema)`.
3. Reject on missing required fields explicitly, naming the field: `missing required: "path"`.
4. Coerce only where the schema permits and the coercion is lossless — `"3"` to `3` for an integer, never silently for a string id.
5. Check enums and constrained fields against the allowed set; a `mode` of `"overwrit"` must fail, not default.
6. Validate referenced resources exist before the call: the path is inside the sandbox, the table is in the allowlist, the host is reachable.
7. On failure, return the validation error to the model to repair — do not pad the arguments by guessing.
8. Never let a validator pass by inserting defaults the model did not intend, such as defaulting a `confirm` flag to true.

```python
import jsonschema
def guarded(tool, args):
    jsonschema.validate(args, SCHEMAS[tool])   # raises ValidationError before any side effect
    assert args.get("path", "").startswith("work/"), "path escapes sandbox"
    return tool(**args)
```

## Pitfalls

- Stringly-typed args sneaking through because the tool coerces `"false"` to a truthy value.
- Validating types but not ranges, so a `timeout` of `-1` reaches the tool and hangs.
- Accepting a path argument without checking it stays inside the declared sandbox root.
- Filling in a required field with a plausible guess to satisfy the validator, inventing data.
- Validating against the tool's current behaviour instead of its schema, so drift goes unnoticed.
- Retrying a validation failure unchanged, so the same rejected call fires again.

## Verification

    python3 -c "import jsonschema,json;s=json.load(open('tools/schemas.json'));jsonschema.validate(json.load(open('args.json')),s['write_file'])"   # exits 0 only on a valid object

Report any argument rejected, the field and rule that failed, and the repaired call that passed.
