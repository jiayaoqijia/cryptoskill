---
name: detect-a-runaway-child-loop
description: Use when a subagent may be repeating work — retrying the same failure, cycling steps, or re-reading the same input. Detects the loop by step-signature repetition and breaks it before the budget is gone.
---

# Detect a Runaway Child Loop

A loop feels like diligence until you notice it is the same action forever. Detect repetition by hashing the child's steps, not by reading its optimistic progress messages.

## Procedure

1. Have each child log every step as a line (command plus result hash) to `notes/children/<id>.steps`.
2. Compute a rolling window of step signatures; a repeated window means the child has cycled.
3. Threshold it: three identical consecutive step signatures, or the same failure message twice, is a loop.
4. Watch the retry counter: the same command retried more than `max_retries` (e.g. 3) without a state change is a loop.
5. Distinguish progress from motion: an artifact hash unchanged across two steps is no work done, regardless of activity.
6. Detect the classic signatures: A-B-A-B alternation, fixed-point retries, and a climbing step count with constant output.
7. On detection, stop the child (cooperative first, then terminate) before it burns the wave budget.
8. Capture the last N steps and the repeated signature into `notes/loops/<id>.log` for diagnosis.
9. Fix the cause — usually a missing stop condition or an unfixable error the child keeps re-attempting — then re-dispatch.
10. Add the detected signature to a blocklist so a re-dispatched child hitting it aborts fast.

## Pitfalls

- Trusting the child's "making progress" heartbeat while its step hashes repeat.
- Counting elapsed time as a loop signal, killing a slow child that is doing genuine single-step work.
- Setting the repetition threshold at 10, so a loop runs long enough to exhaust the token budget first.
- Detecting the loop but not recording the signature, so the re-dispatched child loops identically.
- Treating A-B-A (returning to a starting state after real work) the same as a tight A-B-A-B cycle.

## Verification

```bash
awk '{print $2}' notes/children/<id>.steps | uniq -c | awk '$1>=3{print "loop: "$2}'
# passes when no signature repeats 3+ times, or the loop was stopped and logged
```

Report to the user: the repeated signature, the step count when detected, and whether the child was stopped or re-dispatched.
