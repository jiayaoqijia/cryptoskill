---
name: partitioning-and-pruning
domain: software-engineering/partitioning-and-pruning
trigger: "Using partitioning to reduce scanned data and checking that pruning works."
anti_trigger: "Not for schema design, and not for choosing a database product."
scope: "Partition keys, pruning, and the predicates that prevent it."
status: seedling
---

# Partitioning and pruning

## Standard

Partitioning splits a table into physical pieces by a key, so a query that filters on that key can skip the pieces it does not need. The saving is real but conditional: pruning happens only when the predicate on the partition key is a form the planner can evaluate at plan time, and a query that computes the key from a parameter at execution time may scan every partition.

The classic failure is a date-partitioned table queried with a predicate on a derived value rather than a column. Storing a timestamp in a column and filtering it directly allows pruning; filtering a function of the timestamp depends on the planner's ability to fold the expression, and filtering an application-side variable that is only bound at execution time may not prune at all. The record should state which form the query uses.

Primary sources: <https://www.postgresql.org/docs/> and <https://use-the-index-luke.com/>.

## Decision rules

- Record the partition key and the granularity of the partitions.
- Record the query's predicate on the partition key and whether it is a constant or an expression.
- Record the number of partitions scanned and the number available.
- Record whether pruning occurred at plan time or at execution time.
- Record the partition count's effect on planning time, since too many partitions slows planning.
- Record the maintenance operation that partitions make cheaper, such as dropping old data.

## Procedure

1. Record the partition scheme and its granularity.
2. Capture the plan and count the partitions scanned.
3. Record the predicate form on the partition key.
4. Rewrite the predicate into a pruneable form and re-measure.
5. Note the planning-time cost of the partition count.
6. Write the finding with the pruning behaviour stated.

## Anti-patterns

- Assuming pruning happens because the column is the partition key.
- Filtering on a function of the partition key without checking.
- Partitioning into thousands of pieces and paying planning cost.
- Partitioning on a column that queries do not filter.
- Expecting partitions to accelerate queries that span all of them.

## Done checklist

- [ ] Partition key and granularity recorded.
- [ ] Predicate form recorded.
- [ ] Partitions scanned counted.
- [ ] Pruning timing recorded.
- [ ] Planning cost noted.
- [ ] Finding written.

The other side of partitioning is that constraints become local: a unique constraint on a partitioned table must include the partition key, and a foreign key pointing at one is harder to enforce. Those are design costs paid once, and they are the reason a table is often partitioned for retention rather than for query speed.


## Sources

- Table partitioning documentation: <https://www.postgresql.org/docs/>
- Index and predicate guidance: <https://use-the-index-luke.com/>
- Planner reference: <https://sqlite.org/optoverview.html>
