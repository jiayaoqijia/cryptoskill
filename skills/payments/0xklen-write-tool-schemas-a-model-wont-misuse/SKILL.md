---
name: write-tool-schemas-a-model-wont-misuse
description: Use when exposing tools or functions to a model. Name and describe each parameter for the choosing model, constrain types and enums, and make side-effecting calls hard to invoke by accident.
---

# Write tool schemas a model won't misuse

The model picks and fills tools from the schema alone — it never sees your implementation. Every ambiguous description becomes a wrong call.

## Procedure

1. Name tools as `verb_noun` and be specific: `schedule_meeting`, not `do_thing`. Names blur together in the model's mind across a large registry.

2. Write the description for the model, not for a human reader: when to use it, when not to, and what it returns. "Use for confirmed bookings only; returns the booking id."

3. Type every parameter and use enum/format wherever the space is closed.

```json
{"name":"set_priority","parameters":{"type":"object",
 "properties":{"level":{"type":"string","enum":["low","normal","high"]}},
 "required":["level"],"additionalProperties":false}}
```

4. Mark required honestly; a parameter the model can omit is one it will omit randomly.

5. For destructive tools, require an explicit `confirm` field or a `dry_run` boolean defaulting to true.

6. Describe units and ranges in the field description: "amount in minor units (cents), integer > 0".

7. Keep parameters flat; deeply nested objects are mis-filled far more often than top-level scalars.

8. Test with the model: log every call's arguments and validate them against the schema and against intent before the real handler runs.

## Pitfalls

- Vague descriptions ("updates the record") leave the model guessing which of two similar tools to call.
- Two tools that overlap in purpose; the model alternates between them unpredictably — merge or rename.
- `additionalProperties` left open lets the model invent fields your handler silently drops.
- Stringly-typed enums (`"status": "string"`) produce typos and near-miss values that never match.
- No required fields: the model returns a call that passes schema validation but does nothing.

## Verification

    python3 validate_calls.py calls.jsonl schema.json   # every logged call validates; 0 schema failures

Report: "11 tools, all params typed with enums closed; replayed 200 logged calls, 0 schema violations and 0 ambiguous-tool choices after renaming the two overlapping write tools."
