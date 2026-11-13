---
name: federation-and-schema-ownership
domain: software-engineering/federation-and-schema-ownership
trigger: "Splitting a GraphQL graph across services or teams."
anti_trigger: "Not for microservice decomposition in general, and not for API versioning."
scope: "Splitting a graph across teams without creating a distributed monolith."
status: seedling
---

# Federation and schema ownership

## Standard

Federation composes several subgraphs into one schema, so a client queries a single graph while each team owns a slice of it. The composition is the point and the risk: a change in one subgraph can break the composed schema, and the entity references that join subgraphs create coupling between services that looks like ownership but behaves like a distributed monolith.

Ownership is what makes it work. Each type must have exactly one owning subgraph, and every other subgraph that references it extends it rather than redefining it. When that rule is vague, two teams redefine the same field with different resolvers, and the composed schema resolves to whichever the gateway happens to choose, which is a failure that appears only in production.

Primary sources: <https://www.apollographql.com/docs/federation/> and <https://graphql.org/>.

## Decision rules

- Record which subgraph owns each type and which extend it.
- Record the entity keys used to join subgraphs, and whether they are stable.
- Record the composition check in CI, since a breaking composition must fail before deploy.
- Record how a field's resolver is chosen when several subgraphs could provide it.
- Record the gateway's behaviour when a subgraph is unavailable.
- Record the schema change process, including who approves a breaking change.

## Procedure

1. Assign explicit ownership for each type and record it.
2. Record the entity keys and their stability.
3. Add composition validation to CI and record the failure behaviour.
4. Record the resolution rule for fields that exist in several subgraphs.
5. Record the degradation path when a subgraph is down.
6. Write the ownership map with the change process.

## Anti-patterns

- Two subgraphs defining the same type rather than one extending the other.
- Joining on a key that changes, such as an email address.
- Composing at deploy time without a CI check that catches breaking changes.
- Treating federation as a way to avoid deciding ownership.
- Assuming the gateway degrades gracefully when a subgraph fails.

## Done checklist

- [ ] Ownership recorded per type.
- [ ] Entity keys and stability recorded.
- [ ] Composition check in CI recorded.
- [ ] Resolution rule recorded for shared fields.
- [ ] Degradation path recorded.
- [ ] Change approval process recorded.

The composition check should run on every pull request rather than at release, because a breaking composition discovered at deploy is a rollback under pressure while one discovered in review is a conversation. Recording where the check runs, and what it fails on, is part of the ownership model rather than an implementation detail of the pipeline.


## Sources

- Federation specification and guidance: <https://www.apollographql.com/docs/federation/>
- GraphQL foundation documentation: <https://graphql.org/>
- GraphQL specification: <https://spec.graphql.org/>
