---
name: n-plus-one-and-batching
domain: software-engineering/n-plus-one-and-batching
trigger: "Diagnosing resolver fan-out and batching the queries behind it."
anti_trigger: "Not for database index design, and not for general query optimisation."
scope: "Resolver fan-out, dataloader batching, and the request-scoped cache."
status: seedling
---

# N+1 and batching

## Standard

A GraphQL resolver runs once per field per object, so a query that returns a list of a hundred items and asks for a related field invokes that field's resolver a hundred times. If each invocation issues a query, the database sees a hundred and one round trips where a single join would have done. That is the N+1 problem, and in GraphQL it is the default rather than an accident.

Batching addresses it by deferring the individual lookups within a single tick and combining them into one request. The dataloader pattern does this: the resolver asks for a key, the loader collects keys from all resolvers running in that execution, and dispatches one batched query. The technique is request-scoped, which means it must not be shared across requests or it will serve stale data and leak between users.

Primary sources: <https://graphql.org/> and <https://github.com/graphql/dataloader>.

## Decision rules

- Record which fields fan out and the multiplier a typical query produces.
- Record whether each fan-out field uses a batching loader or a direct query.
- Record the loader's cache scope and confirm it is per-request, not global.
- Record the batch size limit, since an unbounded batch is a different problem.
- Record the behaviour when a batched lookup fails for one key, since a whole batch can fail together.
- Record how the pattern is measured: query counts per request, not latency alone.

## Procedure

1. Trace a representative query and count the database calls per resolver.
2. Identify the fields where calls equal list length.
3. Introduce batching for those fields and record the loader's scope.
4. Set a batch size limit and record the failure behaviour.
5. Re-measure query count per request.
6. Write the findings with the before and after counts.

## Anti-patterns

- Batching by caching globally, which serves one user's data to another.
- Setting a batch size so large that the combined query times out.
- Assuming latency alone reveals the problem, when a fast database hides it.
- Batching a field whose lookup is already a join.
- Ignoring per-key failures within a batch.

## Done checklist

- [ ] Fan-out fields identified with multipliers.
- [ ] Batching status recorded per field.
- [ ] Loader scope confirmed per-request.
- [ ] Batch size limit recorded.
- [ ] Per-key failure behaviour recorded.
- [ ] Query counts measured before and after.

## Sources

- GraphQL execution and batching guidance: <https://graphql.org/>
- Dataloader reference implementation: <https://github.com/graphql/dataloader>
- GraphQL specification: <https://spec.graphql.org/>
