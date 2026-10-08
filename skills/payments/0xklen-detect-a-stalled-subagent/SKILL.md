---
name: detect-a-stalled-subagent
description: Use when a spawned child has produced no output for a while. Distinguishes slow-but-working from wedged using heartbeat timestamps and progress deltas, then acts on the verdict.
---

# Detect a Stalled Subagent

A stalled child looks identical to a slow one until you measure output against time. Track a heartbeat and a progress delta, and treat "no new output for N minutes" as a verdict, not a feeling.

## Procedure

1. Have each child append a heartbeat line to `notes/children/<id>.heartbeat` on every major step: `date -u +%s` plus the step name.
2. Poll with a threshold, not a vibe: if now minus the last heartbeat exceeds `stall_seconds` (start at 180), the child is suspect.
3. Distinguish stalled from finished: check for a terminal marker `notes/children/<id>.done`; absence plus silence means stalled.
4. Measure progress, not just liveness: a heartbeat stuck on the same step name for three polls is a loop, not progress.
5. Check the child is still alive with `ps -o pid,etime,command -p <pid>`; a dead pid is a crash, not a stall.
6. Inspect partial output: `wc -c out/<id>/*` — bytes growing means working, frozen means wedged.
7. On a true stall, capture the last heartbeat and step name before acting, so the failure stays diagnosable.
8. Act in order: send a nudge or steering message, wait one more interval, then kill and re-dispatch from the last checkpoint.
9. Never silently absorb a stalled child as "still running"; an unreaped stall blocks the fan-in forever.
10. Log the detection and the action taken (`nudged`, `killed`, `confirmed-done`) in `notes/children/<id>.state` so the outcome is auditable.

## Pitfalls

- Using wall-clock wait time as the only signal, so a child that heartbeats but repeats step 3 forever reads as healthy.
- Killing before checking `ps`, when the child already exited and its artifact is complete.
- Setting the threshold so low that normal tool latency trips it, causing spurious restarts that lose work.
- A heartbeat written by the parent's poll loop rather than the child, which proves nothing about the child.
- Treating "no output" as "no work" when the child is quiet during one long tool call.

## Verification

```bash
for f in notes/children/*.heartbeat; do echo "$f $(($(date -u +%s) - $(tail -1 "$f" | cut -d' ' -f1)))s"; done
# passes when every child is under stall_seconds or has a .done marker
```

Report to the user: each child's seconds since last heartbeat and whether it was nudged, killed, or confirmed done.
