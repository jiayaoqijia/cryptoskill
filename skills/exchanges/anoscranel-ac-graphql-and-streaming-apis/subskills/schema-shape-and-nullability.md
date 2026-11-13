---
name: schema-shape-and-nullability
domain: software-engineering/schema-shape-and-nullability
trigger: "Deciding GraphQL types and nullability and what they force on clients."
anti_trigger: "Not for REST resource modelling, and not for database schema design."
scope: "Types, nullability, and the client behaviour each choice forces."
status: seedling
---

# Schema shape and nullability

## Standard

In GraphQL, nullability is a contract with consequences that run in the opposite direction from most type systems. A non-null field promises the server can always produce a value, so a failure anywhere in that field's resolution propagates upward and can null out the entire parent object. A nullable field lets a partial failure be represented, at the cost of forcing every client to handle the absence.

The schema's shape decides what clients can ask for, and therefore what the server must be able to answer efficiently. A deeply nested type invites clients to traverse it; a list of objects with many fields invites fan-out. Schema design is consequently a performance decision as much as a modelling one, and the record should note where the schema deliberately restricts traversal to keep cost bounded.

Primary sources: <https://graphql.org/> and <https://spec.graphql.org/>.

## Decision rules

- Record which fields are non-null and which are nullable, with the reason for each non-null choice.
- Prefer nullable for fields whose backing store can fail independently, so partial results remain representable.
- Record the maximum nesting the schema permits and whether a depth limit enforces it.
- Record which types are lists and estimate the fan-out a typical query creates.
- Record any field that resolves from a different service, since it changes failure behaviour.
- Record the schema's deprecation policy for fields being retired.

## Procedure

1. Read the schema and list the non-null fields with their data sources.
2. Identify the fields whose source can fail independently of the parent.
3. Decide nullability for each, recording the reason.
4. Record list fields and the fan-out they permit.
5. Record cross-service fields and their failure mode.
6. Write the schema summary with the nullability rationale.

## Anti-patterns

- Making a field non-null because the database column is not null.
- Using non-null on a cross-service field, which converts a dependency failure into a total one.
- Designing a schema without considering the queries clients will actually send.
- Leaving deprecated fields in place with no removal plan.
- Treating the schema as an internal detail when it is the client contract.

## Done checklist

- [ ] Non-null fields listed with reasons.
- [ ] Independently failing fields identified.
- [ ] List fields and fan-out recorded.
- [ ] Cross-service fields recorded.
- [ ] Depth limit recorded.
- [ ] Deprecation policy recorded.

## Sources

- GraphQL specification and schema guidance: <https://spec.graphql.org/>
- GraphQL foundation documentation: <https://graphql.org/>
- API design context: <https://www.w3.org/>
