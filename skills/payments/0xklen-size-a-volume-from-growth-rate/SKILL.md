---
name: size-a-volume-from-growth-rate
description: Use when provisioning a disk, volume, or database. Sizes it from measured growth, headroom margin, and overhead so it survives to the next review without emergency expansion.
---

# Size a Volume from Growth Rate

A volume is sized from the write rate, the retention window, and the overhead the filesystem and database impose — plus explicit headroom. Picking a round number "to be safe" is either wasteful or, more often, still too small in three months.

## Procedure

1. Estimate the steady-state footprint: rows/day × bytes/row, or events/s × bytes/event.
2. Multiply by the retention window the data must live for, then add indexes and overhead — a table with four indexes can be 2-3x the raw row bytes.
3. Add the database's non-row storage: WAL and its archive (often 1-2x the write volume), temp files for sorts, and `maintenance_work_mem` peaks.
4. Add filesystem and provider overhead: ZFS/Btrfs metadata ~1-3%, distributed stores keep a 3x replication factor, and RAID wastes one disk per parity.
5. Reserve headroom sized to the time to expand: if provisioning a new volume takes 3 days, keep at least 3 days of growth plus 20-30%.
6. Sanity-check the growth rate against a real trend, not a launch-day spike: `predict_linear` over 14 days.
7. Add a hard floor so a surprise import does not fail writes: alert before 90% and keep the alert owner able to expand.
8. Re-run the estimate when retention or write volume changes by >2x; a volume sized for last year's traffic is the wrong shape.

## Pitfalls

- Sizing from raw row bytes and forgetting indexes, WAL, and bloat — the number that matters is total on-disk, not logical.
- Ignoring the 3x replication factor of a distributed store, sizing for a single copy and getting "out of space" at 1/3 usage.
- No headroom reserve, so a single backfill fills the disk before the expansion ticket is approved.
- Keeping a `df` threshold low (95%) and only alerting there, when the useful buffer ended at 85%.
- Sizing a filesystem for its largest-ever single file; filesystems fragment and the last 5% is often unusable for large writes.
- Assuming thin provisioning means unlimited; the underlying pool can be oversubscribed and fill when you least expect it.
- Forgetting the backup target also needs the space — a full backup requires N× the live dataset somewhere.

## Verification

    # projected footprint at current rate
    df -B1 --output=used,avail /mnt/data
    # trend over 14d versus the retention window
    # expected: avail at next review date > 20% of total

Projected usage at the next review stays below 80% of provisioned size with the stated growth rate, and the alert floor leaves room to expand without failing writes.

Report: "Sized <volume> for <d>d retention at <r>/day → <n> GB usable + <m>% headroom; projected <p>% full at next review, expand trigger at 80%."
