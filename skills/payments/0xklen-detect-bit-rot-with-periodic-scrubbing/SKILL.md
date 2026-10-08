---
name: detect-bit-rot-with-periodic-scrubbing
description: Use when silent data corruption is a risk on a storage volume. Schedules background scrubs that read every block against its checksum and reports mismatches before they serve bad data.
---

# Detect Bit Rot with Periodic Scrubbing

Disks return wrong bytes without an error, and a filesystem that never re-reads cold blocks never notices. A scheduled scrub reads all blocks and compares them to stored checksums, turning silent corruption into a reportable event.

## Procedure

1. Confirm the stack actually stores checksums: ZFS and Btrfs do natively; on ext4 you need dm-integrity or application-level hashes; on object stores, per-object `ETag`/`Content-MD5`.
2. Schedule a full scrub on a cadence that completes before it restarts — monthly for multi-TB pools is typical.
3. ZFS: `zpool scrub tank`; check `zpool status tank` for `scan: scrub repaired 0B ... with 0 errors`.
4. Btrfs: `btrfs scrub start -Bd /mnt/data`; watch `btrfs scrub status /mnt/data` for `csum_errors`.
5. md-RAID: `echo check > /sys/block/md0/md/sync_action` and read `/sys/block/md0/md/mismatch_cnt` afterward.
6. For object stores, verify on read with the stored checksum and run a periodic full read pass (`aws s3api head-object` returns `ETag`; a `get` recomputes and compares).
7. Alert on any `repaired > 0B`, `csum_errors > 0`, or `mismatch_cnt > 0`; a single corrected block means a disk is decaying.
8. Record scrub results over time; rising repair counts on the same device predict failure before SMART does.

## Pitfalls

- Running scrubs on a pool that is already heavily loaded and starving application IO; scrub at low traffic and cap its priority.
- Treating a scrub that reports `repaired` as harmless — repairs mean real corruption was found and corrected from a good replica.
- Believing RAID prevents bit rot; classic RAID-5 without checksums cannot tell which mirror is correct and can "repair" good data with bad.
- Never re-reading cold or archival data, so corruption surfaces only at restore time when no good copy remains.
- Assuming an object store's `ETag` is always an MD5 — multipart uploads set it to a composite, so verify differently.
- Scheduling scrubs so rarely that a failing disk is caught after two more have failed (a second failure during rebuild is unrecoverable).
- Ignoring `mismatch_cnt` because the array is "working"; the mismatches are exactly the blocks you cannot trust.

## Verification

    zpool scrub tank && zpool status -v tank | grep -E 'scan:|errors:'
    # expect: "scrub repaired 0B ... with 0 errors" and "No known data errors"

Scrub completes with zero repaired bytes and zero checksum errors, or every reported mismatch is tied to a device under replacement.

Report: "Scrubbed <pool> (<size>): repaired <b>, csum_errors <n>, mismatch_cnt <n> — <pass/fail>; device <id> flagged for replacement."
