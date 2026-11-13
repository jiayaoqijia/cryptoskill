---
name: query-cost-and-depth
domain: software-engineering/query-cost-and-depth
trigger: "Bounding a GraphQL query before it executes."
anti_trigger: "Not for rate limiting at the edge, and not for database tuning."
scope: "Depth limits, cost analysis, and rejecting expensive queries before execution."
status: seedling
---

# Query cost and depth

## Standard

Because the client decides the query, the server must bound what a query can ask for before running it. Two mechanisms do most of the work: a depth limit, which rejects queries nested beyond a threshold, and a cost analysis, which assigns a weight to each field and rejects a query whose total exceeds a budget. Both run before execution, which is what makes them useful.

Cost analysis is an estimate rather than a guarantee. A field's cost depends on the resolver behind it, on the size of the list it returns, and on the database's ability to answer efficiently, none of which the schema alone reveals. The honest approach is to calibrate the weights against observed query cost and treat the budget as a guard rail rather than a precise meter, then record the calibration so it can be revisited.

Primary sources: <https://graphql.org/> and <https://www.w3.org/>.

## Decision rules

- Record the maximum depth permitted and where the limit is enforced.
- Record the cost model: which fields carry weight and how the weight was calibrated.
- Record the per-request budget and the response when it is exceeded.
- Record whether list fields multiply cost by an expected size or by a declared maximum.
- Record the treatment of introspection queries, which can be expensive and are rarely needed in production.
- Record how often the calibration is revisited, since a schema change alters the model.

## Procedure

1. Record the current depth limit and its enforcement point.
2. Assign weights to fields, starting from observed query cost.
3. Set a per-request budget and record the rejection response.
4. Test with queries that are legitimate but expensive.
5. Record introspection handling.
6. Write the model with its calibration date.

## Anti-patterns

- A depth limit so high that it permits a query that never completes.
- Cost weights invented rather than calibrated.
- Rejecting queries with an error clients cannot distinguish from a bug.
- Leaving introspection open in production without considering its cost.
- Treating the budget as a security control when it is a stability control.

## Done checklist

- [ ] Depth limit recorded with its enforcement point.
- [ ] Cost weights recorded with calibration.
- [ ] Per-request budget recorded.
- [ ] Rejection response recorded.
- [ ] Introspection handling recorded.
- [ ] Calibration date recorded.

## Sources

- GraphQL security and cost guidance: <https://graphql.org/>
- GraphQL specification: <https://spec.graphql.org/>
- API security context: <https://www.w3.org/>
