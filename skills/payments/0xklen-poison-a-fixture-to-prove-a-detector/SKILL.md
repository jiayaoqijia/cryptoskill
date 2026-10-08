---
name: poison-a-fixture-to-prove-a-detector
description: Use when you must trust a test, linter or alert that has never failed — plant a known fault in a fixture and confirm the detector fires before believing its silence.
---

# Poison a fixture to prove a detector fires

A detector that has never failed is unproven. Before trusting a green test, scanner or alert, inject a fault it is supposed to catch and confirm it goes red; a detector that stays green on poison is detecting nothing.

## Procedure

1. State the exact fault the detector claims to catch in one line, e.g. "test_invoice_total catches an off-by-one in tax rounding". If you cannot name the fault, you cannot poison for it.
2. Locate the specific fixture the detector reads — read it, do not guess:
```
grep -n "load_fixture\|read_json\|FIXTURE" tests/test_invoice_total.py
```
3. Plant the fault at the smallest granularity — change one value, delete one branch, invert one comparison — and keep the poison inside the fixture, never production code:
```
cp tests/fixtures/invoice_42.json /tmp/invoice_42.json.bak
python - <<'PY'
import json,pathlib
p=pathlib.Path("tests/fixtures/invoice_42.json")
d=json.loads(p.read_text()); d["tax_cents"]+=1     # off-by-one poison
p.write_text(json.dumps(d))
PY
```
4. Run exactly the detector under test and record the outcome:
```
pytest tests/test_invoice_total.py::test_invoice_total -q; echo "exit=$?"
```
Required result: **exit=1** (the detector's red state). Exit 0 means the detector is blind to this fault.
5. If it stayed green, the detector does not cover the fault. Add an assertion that reads the field you poisoned, re-run, and confirm it now fails.
6. Restore the fixture and confirm the suite is green again:
```
mv /tmp/invoice_42.json.bak tests/fixtures/invoice_42.json
pytest tests/test_invoice_total.py -q
```
7. Record the pair (fault → observed red) in the test docstring so the next reader knows the coverage is demonstrated, not assumed.

## Pitfalls

- Poisoning production code instead of the fixture tests the poison, not the detector, and risks committing it. Keep the fault inside `tests/`.
- A detector can go red for the wrong reason (import error, missing fixture). Read the message; it must name the poisoned field or value.
- Forgetting to restore leaves a poisoned fixture that fails the whole suite tomorrow. Keep the `.bak` and restore in the same shell session.
- Poisoning several fields at once hides which assertion actually fired. One fault at a time.

## Verification

```
git diff --stat tests/ && pytest -q
```
Passes = `git diff --stat tests/` is empty and the full suite is green after restore. Report: "planted off-by-one in invoice_42.tax_cents, detector went red with message X, restored, suite green (N passed)."
