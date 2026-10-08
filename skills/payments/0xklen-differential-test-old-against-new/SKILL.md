---
name: differential-test-old-against-new
description: Use when rewriting a function or service and you need behavior equivalence — run old and new on the same corpus in parallel and diff every output until they match or the difference is documented.
---

# Differential test old against new

A rewrite is safe only if it produces the same observable output as the original on real inputs. Run both side by side on a corpus and diff; every divergence is either a bug or an intentional change to document.

## Procedure

1. Keep the old implementation importable, renamed: `legacy.calc_total` vs `new.calc_total`. Do not delete it until the diff is empty.
2. Build a corpus from production-shaped data — 1000+ inputs including the weird ones (zero, negative, max, unicode):
```
sqlite3 prod.db "SELECT * FROM orders ORDER BY random() LIMIT 1000" > corpus/orders.tsv
```
3. Run both and record each pair:
```python
for row in corpus:
    a, b = legacy.calc_total(row), new.calc_total(row)
    if a != b:
        divergences.append((row, a, b))
```
4. Classify each divergence: bug in new (fix it), bug in old that new intentionally changes (document and add to an allow-list with the reason), or undefined behavior in both (canonicalize the input).
5. Shrink to the smallest divergent input and treat it like a fuzz crash (see `shrink-a-fuzz-crash-to-a-minimal-repro`), then add it to the corpus so it stays checked.
6. Wire the diff into CI as a test that fails on any new divergence not in the allow-list:
```
grep -v -f accept.txt divergences.txt | wc -l   # must be 0
```
7. Only after the diff is empty modulo the allow-list delete the legacy implementation and its imports.

## Pitfalls

- Comparing float outputs with `==` produces false divergences. Compare to a fixed precision or exact integer cents.
- A corpus of only happy inputs gives false confidence. Seed it with boundary and malformed cases.
- Nondeterministic outputs (timestamps, dict/map order) must be canonicalized before diffing, or you chase ghosts.
- Deleting the old code before the diff is empty removes the reference you need to explain a later failure.

## Verification

```
python tools/diff_impl.py --corpus corpus/orders.tsv | grep -v -f accept.txt | wc -l
```
Passes = prints `0`. Report: "new.calc_total matches legacy on 1000 corpus rows, 3 allow-listed intentional changes documented, legacy removed."
