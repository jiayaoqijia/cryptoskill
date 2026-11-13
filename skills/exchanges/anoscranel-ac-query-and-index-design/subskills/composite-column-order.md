---
name: composite-column-order
domain: software-engineering/composite-column-order
trigger: "Ordering the columns of a composite index for a query set."
anti_trigger: "Not for choosing which columns to index, and not for schema design."
scope: "Why the leftmost column dominates, and how to order for the query set."
status: seedling
---

# Composite column order

## Standard

A composite index is sorted by its first column, then by its second within each value of the first, and so on. That structure means the index can serve a query that filters on the first column, or on the first and second, but not one that filters only on the second. The leftmost column is therefore a constraint rather than a preference.

Two ordering principles follow. Equality predicates should come before range predicates, because a range on an earlier column stops the index from being used to narrow the later ones. And the column that appears in the most queries, or that has the highest cardinality among the equality predicates, is usually the better first column — but the deciding factor is the actual query set, which is why the record lists the queries and not just the index.

Primary sources: <https://use-the-index-luke.com/> and <https://www.postgresql.org/docs/>.

## Decision rules

- Record every query the index is meant to serve, with its predicate shape.
- Order equality columns before range columns.
- Put the column shared by the most queries leftmost, subject to the equality rule.
- Record which queries the index cannot serve because they omit the leading column.
- Record whether a separate index is needed for the omitted-column queries.
- Record the index's sort order, since a descending column serves a descending sort.

## Procedure

1. List the queries and their predicates.
2. Classify each predicate as equality or range.
3. Choose the leading column from the shared, equality predicates.
4. Order the remainder by the same rule.
5. Identify queries the index cannot serve.
6. Record the index and the query set it addresses.

## Anti-patterns

- Ordering columns by intuition rather than by the query set.
- Placing a range column first and expecting the later columns to narrow.
- Assuming a composite index serves a query on its second column alone.
- Adding a separate index before checking whether reordering would serve both.
- Ignoring sort order when the query orders by a column.

## Done checklist

- [ ] Query set listed with predicate shapes.
- [ ] Predicates classified.
- [ ] Leading column chosen and justified.
- [ ] Remaining order recorded.
- [ ] Unserved queries identified.
- [ ] Index and query set recorded.

## Sources

- Composite index guidance: <https://use-the-index-luke.com/>
- Database index documentation: <https://www.postgresql.org/docs/>
- Query planner reference: <https://sqlite.org/optoverview.html>
