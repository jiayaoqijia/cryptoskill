---
name: index-cost-and-tradeoffs
domain: software-engineering/index-cost-and-tradeoffs
trigger: "Deciding whether an index is worth its write and space cost."
anti_trigger: "Not for choosing a database product, and not for schema design."
scope: "Write amplification, space, and what an index is actually buying."
status: seedling
---

# Index cost and tradeoffs

## Standard

An index maintains a sorted structure alongside the table, and every insert, update, and delete must update it. The cost is therefore paid on writes and in storage, and it is paid whether or not the index is ever used. A read that never touches an index still pays for its existence, which is why an unused index is a pure loss rather than a neutral one.

The benefit side is a reduction in rows examined. An index that narrows a million-row scan to a hundred-row lookup saves the scan; an index on a low-cardinality column that narrows a million rows to four hundred thousand saves little and may not be chosen at all. The trade is legible only when both sides are measured, which is why the record states the write rate alongside the query's timing.

Primary sources: <https://www.postgresql.org/docs/> and <https://use-the-index-luke.com/>.

## Decision rules

- Record the table's write rate, since it sets the cost of every index.
- Record the index's size relative to the table.
- Record how many rows the query examines with and without the index.
- Record whether the index is used at all, from the usage statistics where available.
- Remove indexes that no query uses, rather than leaving them as insurance.
- Record the index's maintenance during bulk loads, which is the operation it slows most.

## Procedure

1. Identify the index and the queries it is meant to serve.
2. Record the table's write rate and the index's size.
3. Measure the query's rows examined with and without the index.
4. Check usage statistics for the index.
5. Compute the write cost against the read benefit.
6. Record the decision and the measurement that supported it.

## Anti-patterns

- Adding an index for every slow query without removing any.
- Keeping an index because it might be needed later.
- Measuring only the read improvement and not the write cost.
- Ignoring the cost of index maintenance during bulk ingestion.
- Assuming the planner will use an index because it exists.

## Done checklist

- [ ] Write rate recorded.
- [ ] Index size recorded.
- [ ] Rows examined measured both ways.
- [ ] Usage statistics checked.
- [ ] Write cost compared with read benefit.
- [ ] Decision recorded with its measurement.

## Sources

- Database indexing documentation: <https://www.postgresql.org/docs/>
- Index design guidance: <https://use-the-index-luke.com/>
- Query planner reference: <https://sqlite.org/optoverview.html>
