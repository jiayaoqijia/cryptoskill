---
name: buffer-pools
domain: software-engineering/buffer-pools
trigger: "Reading or sizing a database's page cache behaviour."
anti_trigger: "Not for application-level caching (ac-caching-and-invalidation)."
scope: "What stays in memory, what gets evicted, and the fix-up cost of a miss."
status: seedling
---

# Buffer pools

## Standard

A buffer pool is the database's own page cache: a fixed region of memory holding pages read from disk, governed by an eviction policy that decides which page leaves when a new one arrives. A read that finds its page in the pool costs computation only; a miss costs a disk read plus the pool's bookkeeping, which can include writing the evicted page back if it was modified.

The pool is not a second cache alongside the operating system's; many engines either read through their own pool exclusively or use direct I/O so the two do not double-hold the same page. The consequence for diagnosis is that available memory splits between the pool, the sort and join workspace, and the operating system's own cache, and a pool sized without that split in mind simply moves the miss cost elsewhere.

Primary sources: <https://postgresql.org/docs/current/runtime-config-resource.html> and <https://dev.mysql.com/doc/refman/en/innodb-buffer-pool.html>.

## Decision rules

- Record the pool size and its share of the machine's memory.
- Record the eviction policy and the write-back behaviour for modified pages.
- Record the read path: through the pool, through the OS cache, or both.
- Record the working set's size for the workload, not just the pool size.
- Record the sort and join workspace share of memory that competes with the pool.
- Record the hit-rate measurement and the workload it was measured under.

## Procedure

1. Record pool size as a share of system memory.
2. Record eviction policy and write-back mechanics.
3. Record the read path and any direct-I/O configuration.
4. Estimate or measure the working set size for the workload.
5. Record the pool's competition for memory from sorts, joins, and the OS.
6. Write the record with the hit rate and the workload it was measured under.

## Anti-patterns

- Sizing the pool by a rule of thumb without the working set.
- Ignoring the pool's competition from sort and join workspace.
- Treating the OS cache and the pool as additive without checking the read path.
- Measuring a hit rate under a workload unlike the one being sized for.
- Assuming a bigger pool helps once the working set is resident.

## Done checklist

- [ ] Pool size and memory share recorded.
- [ ] Eviction and write-back recorded.
- [ ] Read path recorded.
- [ ] Working set size estimated or measured.
- [ ] Memory competition recorded.
- [ ] Hit rate recorded with its workload.

## Sources

- PostgreSQL buffer configuration documentation: <https://postgresql.org/docs/current/runtime-config-resource.html>
- MySQL InnoDB buffer pool documentation: <https://dev.mysql.com/doc/refman/en/innodb-buffer-pool.html>
- Operating system page cache and direct I/O: <https://man7.org/linux/man-pages/man2/open.2.html>
