---
name: parse-and-validate-model-json-output
description: Use when reading structured data out of a model response. Validate against the schema before use, repair without guessing, and fail loudly instead of passing malformed fields downstream.
---

# Parse and validate model JSON output

A model that returns "JSON" is offering a suggestion, not a contract. Treat the text as untrusted input: extract, validate, and reject before any field reaches your logic.

## Procedure

1. Never `json.loads` the whole response blindly — models wrap JSON in prose or fences. Strip fences and extract the first balanced object.

2. Validate against a schema, not by eyeballing: validate at parse time and reject unknown keys.

```python
import json, jsonschema
raw = response.strip().removeprefix("```json").removesuffix("```")
data = jsonschema.validate(json.loads(raw), SCHEMA)   # raises on bad shape
```

3. On a `JSONDecodeError` or validation error, retry once with the error echoed back: "your previous output failed: <error>; return only valid JSON matching the schema."

4. Cap retries at 2. A model that fails the schema twice on the same input is failing, not warming up — route it to the fallback or the human queue.

5. Coerce types deliberately: a numeric string is not a number for arithmetic. Convert explicitly and record when you did.

6. Validate business rules after shape: the JSON can be well-formed and still wrong (date in the future, amount negative).

7. Log the raw response with every validation failure, so you can see the actual malformed text rather than your exception.

## Pitfalls

- Trusting the shape because it parsed; well-formed JSON with the wrong values passes `json.loads` and corrupts downstream records.
- Silent coercion like `int("abc")` crashing deep in a pipeline far from the model call.
- Retrying a schema failure forever — a stuck prompt loops and bills; cap at 2, then escalate.
- Stripping only triple backticks and missing a leading "Here is the JSON:" prefix.
- Allowing extra keys the schema says are absent, which later mask a renamed field.
- Rejecting the whole batch on one bad record; quarantine it and keep processing the rest.

## Verification

    python3 parse.py fixture_malformed.jsonl   # prints pass/repair/reject; reject path must fire on exactly the 2 known-bad cases

Report: "parsed 500 responses: 493 valid first try, 6 repaired on retry, 1 rejected to the human queue; 0 malformed rows reached the database."
