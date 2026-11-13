---
name: access-paths
domain: software-engineering/access-paths
trigger: "Reading a query plan and understanding which path it chose."
anti_trigger: "Not for tuning a specific product's optimizer, and not for schema design."
scope: "Sequential scan, index scan, index-only, bitmap, and when each wins."
status: seedling
---

# Access paths

## Standard

A planner has a small set of ways to reach rows: read the whole table sequentially, walk an index and fetch matching rows, walk an index that already contains every needed column, build a bitmap of matching row locations then read them in physical order, or merge several index results. Each has a cost that depends on how many rows match and how they are physically arranged.

The counter-intuitive case is the one worth learning. A sequential scan beats an index when the predicate matches a large fraction of the table, because reading every block in order is cheaper than jumping between blocks at random. A query that returns twenty percent of a table is often correctly planned as a full scan, and an engineer who forces an index on it makes it slower.

Primary sources: <https://www.postgresql.org/docs/> and <https://use-the-index-luke.com/>.

## Decision rules

- Record the plan's node types and the estimated rows at each.
- Record the estimated cost and the actual rows where the plan includes them.
- Identify whether the chosen path is a scan, an index scan, an index-only scan, or a bitmap.
- Record the fraction of the table the predicate matches, since it decides the path.
- Record whether a sort is happening and whether an index could supply the order.
- Record where the estimate and the actual diverge by more than an order of magnitude.

## Procedure

1. Capture the plan with actual row counts.
2. Record each node and its estimate.
3. Compare estimates with actuals.
4. Note the matching fraction and the path chosen.
5. Identify the node where the cost is concentrated.
6. Write the reading with the divergence named.

## Anti-patterns

- Forcing an index on a predicate that matches a large fraction of rows.
- Reading estimated cost without actual row counts.
- Ignoring a sort that an index could have supplied.
- Treating a plan change as a regression without checking the data.
- Assuming one product's plan format transfers to another.

## Done checklist

- [ ] Plan captured with actuals.
- [ ] Nodes and estimates recorded.
- [ ] Estimates compared with actuals.
- [ ] Matching fraction recorded.
- [ ] Cost concentration identified.
- [ ] Divergence named.

The correlated case is worth recording separately: a nested loop over an outer set of ten rows and an inner index lookup costs ten lookups, while a hash join over the same data reads both sides once, and the planner will switch between them as the outer set grows. A plan that was a nested loop last month and a hash join today is not a regression, it is the estimate crossing that boundary.


## Sources

- Query planner documentation: <https://www.postgresql.org/docs/>
- Index and plan guidance: <https://use-the-index-luke.com/>
- SQLite query planner notes: <https://sqlite.org/optoverview.html>
