---
name: graphql-interface-record
domain: software-engineering/graphql-interface-record
trigger: "Writing the record of a GraphQL or streaming interface."
anti_trigger: "Not for REST contract records, and not for schema documentation generation."
scope: "The written record: schema, limits, cost model, and ownership."
status: seedling
---

# GraphQL interface record

## Standard

The interface record states the schema's shape, its nullability decisions, the limits that bound a query, the cost model behind those limits, the ownership of each type, and the pagination and push contracts. It is written when the interface is introduced, and its function is to make the constraints explicit while they are still choices rather than inherited facts.

The record earns its place during an incident. When a query brings down a database, the first question is what bound was supposed to exist, and a record that states the depth limit, the cost budget, and the fields that fan out answers it before anyone reads the code. Without it, the answer is reconstructed from the schema at the worst possible moment.

Primary sources: <https://graphql.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the schema version and the owning subgraph for each type.
- Nullability decisions are recorded with the reason, especially for cross-service fields.
- Depth limit, cost budget, and calibration date are recorded.
- Pagination ordering and cursor encoding are recorded.
- The push contract records delivery guarantee and resume behaviour.
- Review triggers are dated: schema change, cost recalibration, owner change, capacity change.

## Procedure

1. Record the schema version and type ownership.
2. Record nullability decisions and their reasons.
3. Record the limits and the cost model with its calibration date.
4. Record pagination and push contracts.
5. Set review triggers.
6. Amend at each trigger and record what changed.

## Anti-patterns

- Recording the schema without the limits.
- Leaving the cost model's calibration undocumented.
- Omitting ownership, which is what makes a change reviewable.
- Recording the push contract without its guarantee.
- No triggers, so the record describes an interface that no longer exists.

## Done checklist

- [ ] Schema version and ownership recorded.
- [ ] Nullability decisions recorded with reasons.
- [ ] Limits and calibration recorded.
- [ ] Pagination contract recorded.
- [ ] Push contract recorded.
- [ ] Triggers dated.

The record should also name the queries that were tested against the limits, since a budget that has only been checked against small queries is a budget whose headroom is unknown. Naming the largest legitimate query and its cost turns the limit into a stated boundary rather than an untested number.


## Sources

- GraphQL specification and guidance: <https://spec.graphql.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- GraphQL foundation: <https://graphql.org/>
