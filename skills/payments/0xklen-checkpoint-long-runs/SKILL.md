---
name: checkpoint-long-runs
description: Use when a job may exceed the step, time, or context budget: batch processing, migrations, or multi-page crawls. Persists progress after each unit so a timeout or crash resumes instead of restarting.
---

# Checkpoint Long Runs

A long job that keeps all its state in the conversation loses everything when the call times out. Write progress to disk after every unit, keyed by a resume marker, so work already done is never redone.

## Procedure

1. Design the resume marker before starting: a monotonically increasing index, a set of completed ids, or a cursor. The marker must let you reconstruct "what is left" from disk alone.
2. Prefer append-only durability: after each item, append one line to `data/done.jsonl` (`{"id": "...", "ok": true}`) rather than rewriting a big blob each time.
3. On start (or restart), load the marker and skip completed work: `done=$(jq -r .id data/done.jsonl | sort -u)`.
4. Process in bounded batches (e.g. 50 items) and flush after each batch, so at most one batch is at risk: `json.dump(state, open("data/state.json","w"))` at the batch boundary.
5. Make each item's processing idempotent (see `idempotent-operations`) so a crash mid-item and a re-run cannot double the effect.
6. Run the job as a tracked background process when it can outlive a single tool call, and poll its progress from the checkpoint file rather than blocking.
7. On completion, verify the count: `wc -l data/done.jsonl` should equal the expected total; a short count means a silent stop — investigate before declaring done.
8. Keep the checkpoint and the log together so a resume is: load checkpoint, resume from marker, continue appending.
9. Pick a checkpoint granularity that bounds loss: flush every 50 items or 30 seconds, whichever comes first.
10. Store the expected total alongside the marker (`echo 5000 > data/total.txt`) so completion is a comparison, not an assumption.
11. Make the writer atomic: write to `data/state.json.tmp` then `mv` over the target, so a crash mid-write cannot corrupt the checkpoint.

## Pitfalls

- Accumulating all results in a Python list in memory, so a timeout loses the whole run.
- Rewriting the entire state file per item, which is slow and can corrupt on interruption.
- A resume that reprocesses everything because the marker was never written to disk.
- Marking an item done before its work succeeded, so a resume skips a failed item.
- Assuming the job finished because the loop ended, without counting the outputs.
- A checkpoint recording only the index but not the item, so a resume cannot tell whether the last item finished.
- Running two instances of the same resumable job, both appending, corrupting the done list.

## Verification

    total=$(wc -l < data/items.txt); done=$(wc -l < data/done.jsonl)
    [ "$total" = "$done" ] && echo COMPLETE || echo "resume from $done"
    # passes when done == total at the end, and a mid-run kill resumes at the marker

Report to the user: the checkpoint path, total vs completed counts, and evidence that a kill-and-resume continued rather than restarted.
