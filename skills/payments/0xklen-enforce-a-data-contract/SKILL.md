---
name: enforce-a-data-contract
description: Use when a producer and consumer must agree on a schema and semantics before a change ships. Pins fields, types, nullability, and freshness as an enforceable contract tested in CI.
---

# Enforce a Data Contract

A data contract is the producer's promise about a dataset and the consumer's expectation, made machine-checkable. Without it, every producer change is a surprise and every consumer bug is a mystery.

## Procedure

1. Write the contract as code beside the dataset: an Avro/Protobuf schema, or YAML listing fields, types, nullability, and required freshness. Commit it.
2. Include semantics, not just types: units (`amount` in cents or dollars), enum meaning, the uniqueness key, and allowed ranges.
3. Pin a version and a compatibility mode: BACKWARD (consumers upgrade first) or FULL (both directions).
4. Enforce producer-side: the producing job validates its output against the contract before publishing; a violation fails the job, not the consumer.
5. Enforce consumer-side: the consuming job runs its contract tests in CI, not only in production.
6. Test the contract on every PR:
   - `dbt test --select source:orders` with `not_null`, `unique`, `relationships`.
   - Avro: `curl -s -X POST $REGISTRY/compatibility/subjects/orders-value/versions/latest -d @new_schema.json`.
7. Make freshness part of the contract: an SLA (available by 06:00 UTC, within 1h lag) tested by `dbt source freshness`.
8. Version with expand/contract: add the new field, migrate consumers, remove the old field in a later release.
9. Name an owner in the contract file so a violation has somewhere to go, not a generic data-platform queue.
10. Run the same checks in the producer's CI and the consumer's CI, so a break is caught before either deploys.

## Pitfalls

- A contract that only pins types misses unit changes (cents to dollars) that corrupt every downstream sum.
- Enforcing only on the consumer side blames the victim; the producer must fail first.
- Registry compatibility mode NONE lets any breaking change register.
- A contract with no owner is never updated and is quietly bypassed.
- Testing freshness only in the scheduler misses a dataset that is fresh but wrong.
- Contract tests run only on a schedule give hours of bad data before the alarm.
- A contract that lists fields but not the uniqueness key cannot catch duplicate rows.
- Checking compatibility at publish time only means consumers on an old version break without warning.

## Verification

```sh
dbt test --select source:raw+ --store-failures
dbt source freshness --select source:raw
curl -s -X POST $REGISTRY/compatibility/subjects/orders-value/versions/latest -d @new_schema.json
```

All tests pass, freshness is within SLA, and the compatibility check reports `is_compatible: true`. Report the contract version, the checks that ran, and any violation found.