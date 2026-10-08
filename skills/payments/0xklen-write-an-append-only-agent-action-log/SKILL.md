---
name: write-an-append-only-agent-action-log
description: Use when an agent takes actions a human must be able to audit. Record every tool call as an append-only structured entry, never edited in place.
---

# Write an append-only agent action log

If the only record of a run is the transcript in someone's memory, nothing is reproducible. Log every call as a structured, append-only line you can grep, replay, and hand to an auditor.

## Procedure

1. Choose one append-only sink: `notes/action.log` as JSON Lines, one event per line, opened with `O_APPEND`.
2. Fix the schema before the first write. Minimum: `ts`, `turn`, `tool`, `args_hash`, `args_redacted`, `result_hash`, `exit`, `duration_ms`, `budget_pct`.
3. Redact secrets at write time, not at read time: hash or mask tokens, keys, and passwords before the line is emitted.
4. Log both the call and its outcome as separate events (`call` then `result`) so a crash mid-call is visible.
5. Never rewrite or truncate a line; corrections are new entries that reference the old one by `ts`.
6. Flush after every event (`open(..., buffering=1)`) so a killed process does not lose the tail of the log.
7. Include the workspace root and git SHA per run so the log can be tied to a checkout.
8. Keep the raw arguments where safe and the hash always, so replay can detect a changed argument.

```python
import json, hashlib, time
def log(fh, **e):
    e["ts"] = time.time()
    e["args_hash"] = hashlib.sha256(json.dumps(e.get("args", {}), sort_keys=True).encode()).hexdigest()[:16]
    fh.write(json.dumps(e, sort_keys=True) + "\n")
```

## Pitfalls

- Logging only successful calls, so a crash and its preceding bad call are both invisible.
- Buffering the whole file and flushing at the end, losing everything when the run is killed.
- Writing secrets in plaintext and "cleaning up later", which usually never happens.
- Amending old lines to hide a retry, destroying the chronological record the log exists to provide.
- Logging a human-readable string with no stable fields, so no script can parse it.
- Omitting the args hash, so two different commands look identical in the log.

## Verification

    python3 -c "import json,sys;[json.loads(l) for l in open('notes/action.log')]" && grep -c '"event": "result"' notes/action.log

Report the log path, the event count, and the schema fields every line carries.
