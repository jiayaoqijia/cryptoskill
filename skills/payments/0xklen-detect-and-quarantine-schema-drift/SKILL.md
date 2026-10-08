---
name: detect-and-quarantine-schema-drift
description: Use when an upstream producer changes a schema without notice. Compares observed fields against the contract, quarantines mismatched records, and alerts instead of silently loading nulls.
---

# Detect and Quarantine Schema Drift

An upstream adds, renames, retypes, or drops a column and the pipeline keeps running, loading NULLs where data should be. Detect the change at ingest, quarantine the affected batch, and fail loudly.

## Procedure

1. Register the expected schema with types and nullability in a contract file (Avro, Protobuf `.proto`, JSON Schema, or a `dbt` source). The contract is the source of truth, not a sample of yesterday's data.
2. On every batch, compare observed versus expected before loading:
   - Python: `pandera.DataFrameSchema` or a `great_expectations` suite.
   - dbt: `dbt test` with `not_null`, `accepted_values`, `relationships`, plus `dbt source freshness`.
   - Spark: compare `df.dtypes` to the contract and stop on mismatch.
3. Classify the change: additive (new nullable column) is safe; rename, retype, or drop is breaking.
4. Additive drift: load the extra column and alert so the contract catches up; do not fail the batch.
5. Breaking drift: write the batch to a quarantine table or prefix and stop the load for that partition. Never partially load.
6. Alert with the exact diff: `expected int64, got string` for column `amount` from source `raw.orders`.
7. Never coerce silently. `CAST(amount AS INT64)` on `"N/A"` yields NULL, which downstream reads as missing data.
8. Compare against a registry when one exists: `curl $REGISTRY/subjects/raw.orders-value/versions/latest` and diff the registered schema too, so a producer change does not slip past.
9. Record the observed schema per run so drift is visible as a trend, not discovered on the day a report is wrong.
10. Version the contract and keep the last N versions so a revert is a config change, not a rediscovery.

## Pitfalls

- Inferring schema from the current batch lets a lenient inference (int becomes float) accept corrupt data.
- `dbt run --full-refresh` masks drift by rebuilding rather than reporting it.
- A CSV with a shifted delimiter produces valid-looking columns with wrong values; only type and range checks catch it.
- `try_cast` / `SAFE_CAST` turn an error into a NULL; acceptable only when a quarantine row records the raw value.
- Alerting on every additive column trains people to ignore the alert; separate additive noise from breaking signal.
- A schema registry in BACKWARD mode still rejects a type change only if the producer registers; check producer-side registration.
- A contract that lists only column names without types cannot catch a retype.
- Nullable-to-non-nullable changes pass an additive check and break inserts with a constraint error.

## Verification

```sh
dbt test --select source:raw+
pytest tests/test_contract.py
# the contract test must FAIL on a renamed column and PASS on a nullable addition
```

Run the contract test against a deliberately drifted fixture; it fails with the offending column named. Report the diff detected, records quarantined, and whether the contract or the producer must change.