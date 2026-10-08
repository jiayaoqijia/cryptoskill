---
name: guard-against-missing-and-null-fields
description: Use when parsing API JSON that may omit or null fields. Treat absent, null, and empty-string as distinct cases so a missing field never becomes a crash or a silent zero.
---

# Guard against missing and null fields

`payload["field"]` raises only when a key is absent; a present `None` slips through and crashes
later, or gets coerced to 0 and corrupts every downstream sum. Handle all three states.

## Procedure

1. Enumerate which fields may be absent: in OpenAPI, anything not in `required` and anything with `nullable: true`.
2. Distinguish three states and give each a rule: key absent, key present as `null`, key present as `""`/`[]`.
3. Use `.get()` and branch instead of subscript access:
   ```python
   total = data.get("total")
   if total is None:
       log.warning("total missing; treating as unknown, not 0")
   ```
4. Never coerce missing to `0` or `""` without logging — a missing balance read as 0 makes wrong sums.
5. For numerics, reject the string form or coerce with an explicit, documented rule.
6. Provide a default only where the default is semantically correct, and label it as a default.
7. Test with a fixture per state: absent, null, empty, and wrong type.

## Pitfalls

- `payload["field"]` raises `KeyError` only when absent; `None` passes and crashes three frames later.
- `int(x or 0)` turns `None`, `0`, and `""` into 0 indistinguishably, hiding a real zero vs missing.
- Pydantic models with defaults mask a field the server never sends; make defaults explicit and loud.
- For lists, `[]` vs `null`: treating null as empty conflates "no data" with "data unavailable".
- Optional fields appear only on some account tiers; a fixture from one tier misses them.

## Verification

    python -m pytest tests/test_missing_fields.py -q    # covers absent/null/empty per field

Report: "Handled 6 nullable fields; 3 defaulted, 3 surfaced as errors; no KeyError across 10k responses."
