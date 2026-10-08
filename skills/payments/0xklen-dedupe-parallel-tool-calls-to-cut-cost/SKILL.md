---
name: dedupe-parallel-tool-calls-to-cut-cost
description: Use when a fan-out or batch issues many tool calls that may overlap. Collapse identical and subsumed calls before dispatch so the same work is not paid for twice.
---

# Dedupe parallel tool calls to cut cost

A wave of children often calls for the same file, the same query, or the same page. Dispatching them all pays twice for one result and risks two writers racing on one target.

## Procedure

1. Collect the planned calls before firing any: `(tool, canonical_args)` for the whole wave.
2. Canonicalise arguments — sort keys, normalise paths, strip defaults — so `{"a":1,"b":2}` and `{"b":2,"a":1}` hash equal.
3. Drop exact duplicates: one call, one result, fanned back to every child that wanted it.
4. Collapse subsumed calls: `read_file(1..500)` subsumes `read_file(1..100)`; run the superset once.
5. For writes to the same target, serialise rather than dedupe — two different writes to one file must not run in parallel.
6. Materialise the shared result in a cache keyed by the canonical arguments, with a short TTL for the run.
7. Log the saving: `dedupe wave=2 planned=18 fired=11 dup=5 subsumed=2`.
8. Re-check after the wave: a child that produced new calls may create fresh duplicates for the next round.

```python
import hashlib, json
def key(call):
    return (call["tool"], hashlib.sha256(json.dumps(call["args"], sort_keys=True).encode()).hexdigest())
seen = {}
for c in planned:
    seen.setdefault(key(c), []).append(c)
fired = [v[0] for v in seen.values()]   # one representative per unique call
```

## Pitfalls

- Deduping on the raw call string, so key order or whitespace differences hide a true duplicate.
- Collapsing two writes to one path into a single write, silently dropping one child's content.
- Caching a result for the whole wave when the underlying data changes mid-run.
- Deduping reads but not subsumed ranges, so a 500-line read and a 100-line read both fire.
- Treating a fan-out's per-child calls as unique because they carry a child id, when the payload is identical.
- Forgetting the cache when the wave repeats next round, re-fetching the same unchanged page.

## Verification

    grep -oE 'planned=[0-9]+ fired=[0-9]+ dup=[0-9]+' notes/action.log | tail -1   # fired < planned whenever duplicates existed

Report the wave's planned vs fired call counts and the duplicate/subsumed breakdown.
