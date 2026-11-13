---
name: contract-schema-and-semantics
domain: software-engineering/contract-schema-and-semantics
trigger: "Specifying a dataset's fields so consumers know what they mean."
anti_trigger: "Not for database schema design, and not for API contract design."
scope: "Types plus meaning: units, nullability, and what a field is not."
status: seedling
---

# Contract schema and semantics

## Standard

A schema without semantics is a shape without a meaning. A column typed as a decimal could be an amount in minor units or in major units; a timestamp could be UTC or local; a nullable field could mean unknown, not applicable, or not yet arrived. Each of those ambiguities produces a defect that the type system does not catch and that a consumer discovers by producing a wrong number.

Semantics belong in the contract because they cannot be inferred from the data. Units, time zone, currency, the treatment of nulls, the meaning of a sentinel value, and the relationship a foreign key refers to are all facts the producer knows and the consumer must be told. The test of a good contract is whether a competent engineer could use the dataset without asking a question.

Primary sources: <https://www.w3.org/> and <https://csrc.nist.gov/>.

## Decision rules

- Record each field's type, unit, and time zone where applicable.
- Record the meaning of null and whether it is permitted.
- Record the treatment of sentinel values, which are usually a legacy of an earlier schema.
- Record the currency and the minor-unit convention for monetary fields.
- Record the keys and what they reference, including whether the reference is enforced.
- Record the fields that are deprecated and the replacement for each.

## Procedure

1. List the fields with their types.
2. Record unit, time zone, and currency for each.
3. Record null semantics and permitted nullability.
4. Record sentinel values and their replacement.
5. Record keys and references.
6. Write the contract and test it by having a consumer use it without asking.

## Anti-patterns

- A schema with no units, leaving the consumer to guess.
- Timestamps without a stated zone.
- Null used for three different meanings.
- Sentinel values such as negative one documented nowhere.
- Monetary values without a stated minor-unit convention.

## Done checklist

- [ ] Types recorded.
- [ ] Units and zones recorded.
- [ ] Null semantics recorded.
- [ ] Sentinels recorded.
- [ ] Keys and references recorded.
- [ ] Deprecations recorded.

The semantic gaps that survive review longest are the ones everyone on the producing team knows and nobody has written: an internal convention such as a status code whose meaning lives in one engineer's memory is exactly the field a new consumer will misread, and the contract's purpose is to move that knowledge out of memory.


## Sources

- Data interchange and schema standards: <https://www.w3.org/>
- Security and data governance guidance: <https://csrc.nist.gov/>
- Data quality context: <https://csrc.nist.gov/publications>
