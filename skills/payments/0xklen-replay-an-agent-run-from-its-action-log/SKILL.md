---
name: replay-an-agent-run-from-its-action-log
description: Use when you need to reproduce or debug what an agent did. Reconstruct the run from the append-only action log, comparing each step rather than trusting the summary.
---

# Replay an agent run from its action log

A run's summary is a claim; its log is the evidence. Replay walks the recorded calls in order, re-executes the read-only ones, and verifies the write ones against their stated effect.

## Procedure

1. Load the log and assert every line parses before doing anything: `python3 -c "import json;[json.loads(l) for l in open('notes/action.log')]"`.
2. Rebuild the sequence by `turn`, not by file order — interleaved fan-out needs the explicit index.
3. Classify each step: `read-only` (safe to re-run), `local-write` (re-run in a scratch copy), `external` (never re-run, verify from evidence only).
4. Re-execute the read-only steps and compare `result_hash` to the recorded value. A mismatch means the environment moved or the tool changed.
5. For write steps, do not re-fire them. Instead diff the resulting state against the effect the log claimed: row counts, file hashes, message ids.
6. For external steps, confirm via the target's own API or UI that the recorded effect actually happened.
7. Stop at the first divergence; replay is for locating the break, not for heroically continuing past it.
8. Produce a short divergence report: turn, tool, expected hash, observed hash, likely cause.

```bash
python3 tools/replay.py notes/action.log --reads-only --stop-on-diff
# exits nonzero at the first step whose result no longer reproduces
```

## Pitfalls

- Re-running write or send steps "to be sure", duplicating the side effect the original run already caused.
- Replaying from the summary instead of the log, which loses argument detail and exact ordering.
- Ignoring timestamps, so a step that depended on a now-expired token looks like a code failure.
- Comparing only that the tool ran, not that its result matched the recorded hash.
- Continuing past the first divergence, burying the actual break under fallout from later steps.
- Treating a harmless ordering difference in a parallel wave as a divergence when the sets are equal.

## Verification

    python3 tools/replay.py notes/action.log --reads-only | tail -1   # "all read steps reproduce" or the first diff

Report the turns replayed, the first divergence found, and the logged effect confirmed externally.
