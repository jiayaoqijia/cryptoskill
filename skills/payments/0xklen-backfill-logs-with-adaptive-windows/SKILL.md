---
name: backfill-logs-with-adaptive-windows
description: Use when backfilling historical logs across millions of blocks. Splits the range into windows sized to the provider result cap, checkpoints each window, and resumes without refetching completed work.
---

# Backfill logs with adaptive windows

A backfill is a long job that must survive restarts and provider caps. Split by blocks, checkpoint each window, and make re-running a window harmless.

## Procedure

1. Fix the total range once: `[start, end]` from the contract's creation block to the current safe head.
2. Size the window dynamically. Start at 2000 blocks; whenever a response hits the provider cap, halve for that gap only and remember the working size.
   ```python
   width = 2000
   for s in range(start, end, width):
       logs = get_logs(s, min(s + width - 1, end), filt)
       if len(logs) >= CAP:
           width = max(50, width // 2); continue   # retry this gap smaller
   ```
3. Checkpoint after each window in the same transaction that stores its logs:
   `INSERT INTO backfill_progress(stream, range_end) VALUES ($1,$2) ON CONFLICT (stream) DO UPDATE SET range_end=EXCLUDED.range_end;`
4. On restart, resume from `range_end + 1`; never rescan from `start`.
5. Run disjoint ranges in parallel workers but write progress under a lock so two workers never claim one range.
6. Audit at the end by summing per-window counts, since a single `eth_getLogs` over millions of blocks is impossible.

## Pitfalls

- Fixed windows tuned for one contract overflow on a busier one; the working size must adapt at runtime.
- Storing progress without the logs (or logs without progress) leaves a window that claims done but holds no rows; commit them together.
- Backfilling into the same tables a live tail writes races on keys; rely on upsert, not on ordering.
- A backfill that restarts from `start` on every crash never finishes a large range.

## Verification

    psql -c "SELECT stream, range_end FROM backfill_progress;"
    # range_end advances across runs and never rewinds; per-window row counts are non-zero

Report the range covered, the window size at completion, and that a restart resumes rather than restarts.
