---
name: columnar-and-sort-design
domain: software-engineering/columnar-and-sort-design
trigger: "Choosing table layout, sort order, and partitions for analytical scans."
anti_trigger: "Not for B-tree index tuning of a transactional store, and not for a product choice."
scope: "How columnar layout, sort order, and partitioning serve analytical scans."
status: seedling
---

# Columnar and sort design

## Standard

Columnar storage reads only the columns a query touches, so a scan of three columns over a billion rows reads a fraction of the data a row store would. The cost is on write: inserting one row means touching every column file, so columnar suits bulk loads and batch updates rather than transactional writes. Most analytical engines also sort within partitions and can prune partitions, and both mechanisms serve the same purpose — not reading what the query does not need.

Sort order is the decision with the most leverage. Sorting the daily facts by date puts each day's rows together, so a month's scan skips the rest of the table; sorting by customer fragments every customer across the whole file, unless customer is the almost-only filter. The chosen sort keys should match the most common filter and roll-up path, and a second-level sort key clusters rows for the second most common, at which point the remaining queries get whatever remains.

Primary sources: <https://www.postgresql.org/docs/> and <https://parquet.apache.org/>.

## Decision rules

- Record the physical layout available and what it costs to write and to read.
- Choose the sort keys from the most frequent filter and roll-up path, and record why.
- Record the partition key and its intended pruning benefit.
- Record the compression behaviour of each measure column, especially wide strings.
- Record the write pattern the layout requires: bulk loads, micro-batches, or appends.
- Measure the top queries before and after layout choices; do not reason alone.

## Procedure

1. List the top queries by frequency and by cost.
2. Choose sort keys from their filters.
3. Choose a partition key consistent with the sort keys.
4. Confirm the write pattern the engine requires.
5. Load a representative sample and measure the top queries.
6. Record the final layout and the rejected alternatives.

## Anti-patterns

- Sorted by the primary key because that is the transactional habit.
- Partitions so small the engine spends more time planning than scanning.
- A partition key that fights the sort keys, forcing cross-partition scans.
- High-cardinality string columns compressed as an afterthought.
- Layout chosen from vendor defaults, never measured against the real queries.

## Done checklist

- [ ] Top queries listed with frequencies.
- [ ] Sort keys chosen with reasons.
- [ ] Partition key recorded.
- [ ] Compression of wide columns recorded.
- [ ] Write pattern confirmed.
- [ ] Layout measured before and after.

## Sources

- Columnar table layout: <https://www.postgresql.org/docs/>
- Columnar file format: <https://parquet.apache.org/>
- Analytical engine docs hub: <https://www.kimballgroup.com/>
