---
name: btrees-and-pages
domain: software-engineering/btrees-and-pages
trigger: "Reading or designing a B-tree's page-level behaviour."
anti_trigger: "Not for choosing which indexes to create (ac-query-and-index-design)."
scope: "The in-place update tree, its splits, its log coupling, and its page model."
status: seedling
---

# B-trees and pages

## Standard

A B-tree stores data in fixed-size pages, each holding sorted keys with pointers to child pages, and keeps the tree balanced so every lookup touches the same number of pages. A write finds its leaf page and updates that page in place, which is the design's central commitment: no structure-level list is rebuilt, only the page that logically owns the key is rewritten.

That in-place commitment is why the write-ahead log and the page write cannot be separated. The engine acknowledges a write only after both the log record and the page change are known to survive a crash, which makes every page write at least log write plus page write. When the leaf is full, the split allocates a sibling page, copies half the keys into it, and inserts a separator key into the parent; the cost of a single insert can therefore be three pages written plus the log records for each.

Primary sources: <https://postgresql.org/docs/current/storage-page-layout.html> and <https://sqlite.org/fileformat2.html>.

## Decision rules

- Record the page size configuration used for the workload.
- Express node occupancy after splits for a given insert order rather than assuming it.
- Record the log coupling: acknowledged writes must be log-durable before page changes are relied on.
- For a page-touched analysis of a workload, count the leaf, not the whole tree.
- Record split-copy behaviour before treating write cost as one page write.
- Record the iterator-only sequential-read path for range scans since the linked-leaf design exists precisely for it.

## Procedure

1. Establish the page size and the branching factor it supports.
2. Insert the workload's key pattern and record how often splits occur.
3. Count the log records per insert for the split and non-split paths.
4. Record occupancy after splits for that same insertion sequence.
5. Record the leaf-link traversal cost for a typical range scan.
6. Write the record with the expected page-writes-per-insert for the workload's key order.

## Anti-patterns

- Treating a page write as the whole cost of an insert when splits double or triple it.
- Assuming page writes are independent of the log contract.
- Assuming occupancy is a fixed fraction of capacity for arbitrarily ordered keys.
- Reasoning about a workload's cost without the page size.
- Confusing range scans, which are leaf-link walks, with repeated individual lookups.

## Done checklist

- [ ] Page size and branching measured or configured.
- [ ] Splits counted for the workload's key order.
- [ ] Occupancy expressed for that order.
- [ ] Log coupling recorded for acknowledged writes.
- [ ] Leaf-link scan cost recorded.
- [ ] Page writes per insert estimated for the workload.

## Sources

- PostgreSQL internal storage documentation: <https://postgresql.org/docs/current/storage-page-layout.html>
- MySQL InnoDB storage and page documentation: <https://dev.mysql.com/doc/refman/en/innodb-index-types.html>
- SQLite file format page structure: <https://sqlite.org/fileformat2.html>
