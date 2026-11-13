---
name: covering-and-partial-indexes
domain: software-engineering/covering-and-partial-indexes
trigger: "Using a covering or partial index to avoid a lookup or shrink the index."
anti_trigger: "Not for choosing columns to index in general, and not for schema design."
scope: "Including columns to avoid a lookup, and indexing a subset of rows."
status: seedling
---

# Covering and partial indexes

## Standard

A covering index includes every column a query needs, so the database can answer from the index alone without visiting the table. That saves one lookup per matching row, which matters most when the query returns many rows, and it costs space because the included columns are stored in the index.

A partial index covers only the rows that meet a condition, and it is smaller and cheaper to maintain than a full index when the queries only ever touch a subset. The classic case is a status column: an index on the pending rows is a fraction of the size of an index on all rows, and it stays small because the pending set is bounded. The condition must match the query's predicate exactly for the planner to use it.

Primary sources: <https://www.postgresql.org/docs/> and <https://use-the-index-luke.com/>.

## Decision rules

- Record the query's selected columns and whether the index can supply all of them.
- Record the row count the query returns, since a single-row lookup gains little from covering.
- Record the index's size with and without the included columns.
- Record the partial index's condition and whether it matches the query's predicate.
- Record how the partial index's size behaves as the subset grows.
- Record the maintenance cost of each index on the table's write path.

## Procedure

1. Record the query's columns and its returned row count.
2. Check whether the current index requires a table lookup.
3. Add the included columns and measure the size change.
4. For a partial index, record the condition and its expected cardinality.
5. Verify the predicate matches so the planner can use it.
6. Record the decision with both costs.

## Anti-patterns

- Adding covering columns to every index.
- Creating a partial index whose condition does not match the query.
- Assuming a partial index stays small when the subset is unbounded.
- Using a covering index for a single-row lookup where the saving is trivial.
- Forgetting that included columns still consume space and cache.

## Done checklist

- [ ] Query columns and row count recorded.
- [ ] Lookup requirement identified.
- [ ] Size measured with included columns.
- [ ] Partial condition and cardinality recorded.
- [ ] Predicate match verified.
- [ ] Decision recorded with both costs.

## Sources

- Index documentation on covering and partial indexes: <https://www.postgresql.org/docs/>
- Index design guidance: <https://use-the-index-luke.com/>
- Query planner reference: <https://sqlite.org/optoverview.html>
