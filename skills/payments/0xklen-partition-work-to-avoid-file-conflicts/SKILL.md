---
name: partition-work-to-avoid-file-conflicts
description: Use when parallel agents might write the same file or directory. Assigns disjoint path ownership before launch so no two workers can overwrite each other's output.
---

# Partition Work to Avoid File Conflicts

Two agents writing the same path is a race whose winner depends on timing. Give every writer a private slice of the filesystem before anything launches.

## Procedure

1. Enumerate every path any child will create or modify, taken from the briefs, before spawning.
2. Detect collisions: `grep -rhoE 'skills/[a-z0-9-]+' notes/children/*.brief.md | sort | uniq -d` prints any path claimed twice.
3. For each collision, split the path further (per-file, not per-directory) or serialize the two children into different waves.
4. Record the ownership map in `notes/ownership.tsv` as `child-id<TAB>path-glob`.
5. Assert disjointness mechanically: no glob may match another child's path; test with a small script rather than by eye.
6. Give each child its own scratch subtree, e.g. `$TMPDIR/child-<id>/`, for intermediate files.
7. For a shared read-only input, pass the path but mark it read-only in the brief; readers do not conflict.
8. Route any unavoidable shared append through one writer: children emit to their own file, a single fan-in step concatenates.
9. At launch, re-check `notes/ownership.tsv` for entries added since the partition was made.
10. After the wave, detect residual conflicts: `git status --short` should show only paths present in the ownership map.

## Pitfalls

- Partitioning by directory when two children each edit a different file in that same directory; the glob still overlaps.
- Forgetting generated files (`*.pyc`, lock files, logs) that two children both touch under an otherwise clean split.
- Letting a child create a shared temp file with a fixed name like `/tmp/out.json`, which collides across workers.
- Assuming a "read-only" input stays read-only because the child is well-behaved.
- Missing an ownership entry added mid-wave, so the last writer silently wins.

## Verification

```bash
sort -k2 notes/ownership.tsv | awk '{print $2}' | sort | uniq -d
# passes when this prints nothing (no path owned twice) and git status shows only owned paths
```

Report to the user: the ownership map size, any overlapping glob found, and the paths touched by the wave.
