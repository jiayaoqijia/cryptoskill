---
name: add-a-kill-switch-to-a-runaway-job
description: Use when a long-running job, migration or agent loop can run away and needs a stop an operator can pull in seconds — checked cooperatively at safe points, not via a hard SIGKILL.
---

# Add a kill switch to a runaway job

A job with no stop button is controlled only by `kill -9`, which leaves work half-applied and state inconsistent. Give the operator a cooperative switch that is polled at safe points, so the job stops after the current unit of work and lands in a resumable state.

## Procedure

1. Define the switch as an out-of-band signal the process can read cheaply: a file, a Redis key, a DB row, or an env var the supervisor can rewrite. File on a shared volume is the simplest:
       KILL_FILE=/var/run/batch/job.stop
       test -f "$KILL_FILE" && echo stopping

2. Poll it at a *safe point* — between items, not mid-write. Once per N items and once per outer loop iteration is enough; checking every microsecond wastes the very budget you are protecting:
       for i, item := range items {
         if i % 100 == 0 && stopped() { saveCheckpoint(i); return ErrStopped }
         process(item)
       }

3. Make the stop idempotent and resumable: persist a checkpoint (`last_processed_id`, offset, cursor) before returning, so a restart continues instead of reprocessing or skipping. Write the checkpoint *after* the side effect commits.

4. Handle `SIGTERM` the same way, so a normal `kubectl delete pod` also stops cleanly. Kubernetes sends `SIGTERM`, waits `terminationGracePeriodSeconds` (default 30), then `SIGKILL`s. Your handler must finish the current unit inside that window:
       signal.Notify(ch, syscall.SIGTERM, syscall.SIGINT)
       // set stop flag; do NOT os.Exit mid-write

5. Set the grace window to match: `terminationGracePeriodSeconds: 60` when one unit can take 20 s. A job whose unit of work exceeds the grace window is killed mid-write no matter how good the handler is.

6. Make the switch also pause intake, not just the current worker: a queue consumer should stop pulling new messages (`consumer.pause()`) so stopping does not race a refill.

7. Log the stop with the checkpoint and the count processed, then exit non-zero so the orchestrator records a deliberate stop rather than a success:
       log.Printf("stopped by switch at=%d processed=%d", i, i)

## Pitfalls

- Checking the switch only at the *end* of the whole job, so it does nothing until the runaway has already finished the damage.
- Returning immediately without a checkpoint, so the restart reprocesses from zero — or worse, resumes past unprocessed items.
- `os.Exit(0)` inside the loop, reporting success and skipping deferred cleanup (closing files, releasing locks, flushing).
- A file switch on a filesystem the worker container does not share, so the operator's `touch` is invisible to the process.

## Verification

    # start the job, let it reach steady state, then pull the switch
    touch "$KILL_FILE"
    # expect: logs "stopped by switch at=<n>", exit code non-zero, within the grace window
    ps -o pid,stat,etime -p "$(pgrep -f batch-job)"
    # restart and confirm it resumes from the checkpoint, not from row 0
    grep checkpoint /var/lib/batch/state.json

Report: the switch mechanism, the poll cadence and checkpoint location, and a live test where pulling the switch stopped the job within one unit of work with a resumable checkpoint and a non-zero exit.
