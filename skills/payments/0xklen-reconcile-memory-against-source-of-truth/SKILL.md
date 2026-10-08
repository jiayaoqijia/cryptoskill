---
name: reconcile-memory-against-source-of-truth
description: Use when a remembered value may have drifted from the real system. Re-reads the authoritative source and corrects the memory to match it.
---

# Reconcile Memory Against Source of Truth

Memory records what was true when written; the system has moved on. Reconciliation means reading the live source and making memory match it, not the reverse.

## Procedure

1. Name the source of truth for the value: a config file, a database row, an `aws describe-*` call, a repo file.
2. Read the live value, not a cached or remembered one.
3. Diff it against the stored memory entry for the same key.
4. If they match, stamp the entry with today's date to record the check.
5. If they differ, the live value wins: edit the memory entry in place.
6. Record the source and time on the corrected entry: `2026-10-08 host=prod-2 (aws describe-instances, i-0abc)`.
7. If the memory was right and the live read wrong (stale cache, wrong region), fix the read, not the memory — verify before overwriting.
8. Never write the memory value back into the live system without a separate, deliberate change task.
9. Re-read the memory entry after the edit to confirm the correction landed.
10. Where several entries key off the same source, reconcile them in one pass and log the batch.

## Pitfalls

- Re-reading the memory store and calling that a source check.
- Assuming the live value is right when the read used a stale cache or the wrong environment.
- Correcting memory but leaving the old value greppable elsewhere in the store.
- Pushing the remembered value back into the live system as a "fix", changing the system to match a possibly wrong memory.
- Checking once at write time and never again, so the entry is correct only on the day it was made.

- Querying a replica or cache and treating it as the source of truth.
- Reconciling the same key in several files but fixing only the first.
- Skipping the check because the memory "looks recent", when recent means only when it was last copied.

## Verification

    diff <(your-live-read) <(grep -h "host=" ~/.hermes/memories/*.md)
    # passes when the diff is empty and the entry carries today's date

Report to the user: the key, the live value, the remembered value, and which one changed.
