---
name: canonicalise-model-output-for-diffing
description: Use when comparing model outputs over time, caching them, or asserting on them in tests. Normalise whitespace, key order, and formatting first, or every diff is noise.
---

# Canonicalise model output for diffing

Two logically identical responses rarely differ byte-for-byte. Normalise before you compare, cache, or assert, or you will chase diffs that mean nothing.

## Procedure

1. Parse structured output and re-serialise canonically: sorted keys, fixed separators, no incidental whitespace.

```python
import json
def canon(s):
    return json.dumps(json.loads(s), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
```

2. For prose, normalise before comparing: collapse runs of whitespace, trim, unify line endings to `\n`, strip trailing spaces, and (only if case is not meaningful) lowercase.

3. Fix number and date representation: `1.0` vs `1`, `2024-01-01` vs `Jan 1, 2024`. Declare one canonical form and convert to it.

4. Exclude volatile fields from the comparison: timestamps, request ids, and random ids you injected. Compare the semantic payload.

5. Hash the canonical form for caching and change detection; key the cache on canonical content, not raw bytes.

6. When you diff, show the semantic delta (which fields changed), not a character-level diff of reformatted text.

7. Keep the raw response too — canonicalise for comparison, store the original for debugging.

## Pitfalls

- Diffing raw responses and treating key reordering or indentation as a behaviour change.
- Lowercasing when case is meaningful (IDs, codes, names) and hiding a real regression.
- Stripping volatile fields so aggressively you drop a field that genuinely changed.
- Caching on the raw string, so an identical answer re-bills because a space moved.
- Canonicalising away the very field the test exists to check.
- Normalising case or whitespace in identifiers where it is meaningful, and hiding a genuine change.

## Verification

    python3 canon.py a.json b.json   # prints 'equal' for two differently-formatted identical payloads, 'diff: <fields>' otherwise

Report: "canonicaliser (sorted keys, trimmed whitespace, fixed number form) collapsed 40 spurious diffs in a day's outputs to 2 real ones; the cache now keys on the canonical hash."
