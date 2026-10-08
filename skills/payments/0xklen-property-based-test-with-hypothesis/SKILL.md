---
name: property-based-test-with-hypothesis
description: Use when example-based tests miss input combinations — state an invariant and let Hypothesis generate hundreds of inputs, then freeze the minimized counterexample as a regression test.
---

# Property-based tests with Hypothesis

Example tests check the cases you thought of. A property test checks the rule that must hold for all inputs and hands you the smallest input that breaks it.

## Procedure

1. Name the invariant as a law, not an example: "decode(encode(x)) == x", "total >= sum(parts)", "len(sorted(x)) == len(x)".
2. Express a round-trip or invariant with `@given`:
```python
from hypothesis import given, strategies as st
import json

@given(st.dictionaries(st.text(), st.integers()))
def test_json_roundtrip(d):
    assert json.loads(json.dumps(d)) == d
```
3. Bias the strategy toward your real domain — `st.text(min_size=1)`, `st.emails()`, `st.from_regex(r"\d{4}-\d{2}-\d{2}")`, or a `@st.composite` for your own types. Unbounded `st.text()` mostly finds Unicode edge cases you never ship.
4. Set a budget so the run has a fixed cost: `@settings(max_examples=500, deadline=200)`.
5. Run it: `pytest tests/test_json_roundtrip.py -q`. On failure Hypothesis prints a minimized counterexample — read it; that input, not the first, is the bug.
6. Freeze the counterexample so it never regresses:
```python
@example({"": 0})   # frozen from the found counterexample
```
7. Cache the example database in CI so shrinking state survives between runs:
```
- uses: actions/cache@v4
  with: {path: .hypothesis, key: hyp-${{ hashFiles('**/test_*.py') }}
```

## Pitfalls

- A property that restates the implementation tests nothing. The expected value must come from a different computation — a model, a reference library, or an algebraic law.
- Generators that rarely produce interesting values (e.g. `st.integers()` for a parser) make runs slow and shallow. Constrain and `assume()`.
- A `deadline` set too low flags slow-but-correct inputs as failures. Raise it per test or set `deadline=None` for IO tests.
- Nondeterministic properties — float `==`, unordered collections — fail spuriously. Compare with a tolerance, or sort before comparing.

## Verification

```
pytest tests/test_json_roundtrip.py -q --hypothesis-seed=0
```
Passes = green with a fixed seed and the example count reported in the summary line. Report: "roundtrip property held over 500 generated dicts, zero counterexamples, seed 0 reproducible."
