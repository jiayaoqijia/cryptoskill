---
name: evolve-a-schema-without-breaking-readers
description: Use when adding or changing a field other services or old code still read — roll out additive changes first and gate the change with a schema-registry compatibility check.
---

# Evolve a schema without breaking readers

Schemas are read by code you do not control: old app versions, downstream services, stored data. Evolve additively, keep every new field optional with a default, and gate the change with a compatibility check in CI.

## Procedure

1. Classify the change against the registry's rule. In Avro/Protobuf/gRPC the safe set is: add a field **with a default**, add an enum value never used as a default, delete a field that had a default, widen a type. Renaming or renumbering is always breaking.
2. Never reuse a Protobuf field number — removed tags go to `reserved`:
```proto
message Order {
  reserved 4, 7;               // never reuse these numbers
  reserved "legacy_total";
  int64 total_cents = 8;       // new field, new number
  optional string currency = 9 [default = "USD"];
}
```
3. Check compatibility before publishing (Confluent Schema Registry):
```
curl -s -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data @order_v8.json \
  http://registry:8081/compatibility/subjects/orders-value/versions/latest
```
Required response: `{"is_compatible": true}`. `false` means you are about to break a reader.
4. For JSON/HTTP add fields and keep old ones for one deprecation window; remove only after telemetry shows zero readers.
5. Backfill defaults so old rows read cleanly under new code without null checks:
```
UPDATE orders SET currency = 'USD' WHERE currency IS NULL;
```
6. Add the check to CI so it cannot be skipped:
```
buf breaking --against '.git#branch=main'
```
7. Record the compatibility mode explicitly — BACKWARD, FORWARD, or FULL. FULL means old readers read new data and new readers read old data.

## Pitfalls

- Making a new field `required` breaks every producer not yet updated; defaults exist precisely so fields can be added safely.
- Deleting a field readers still use is invisible until runtime deserialization fails. Check reader usage first.
- Changing a field's meaning without renaming it (cents → dollars on `amount`) passes schema checks and corrupts data. Version the name.
- Enum value removal breaks stored data. Only add enum values, never remove or renumber.

## Verification

```
buf breaking --against '.git#branch=main' && echo COMPATIBLE
```
Passes = prints `COMPATIBLE` (or the registry returns `is_compatible: true`) with no breaking-change list. Report: "added optional total_cents (tag 8, default 0); is_compatible=true; old readers unaffected."
