---
name: checkpoint-agent-state-for-resumable-runs
description: Use when an agent run is long or costly enough that a crash should not restart it. Persist step state and completed work so the run resumes instead of redoing.
---

# Checkpoint agent state for resumable runs

A run that holds all its progress in memory loses everything on a kill. Write checkpoints so a restart resumes from the last good step rather than re-spending the whole budget.

## Procedure

1. Define the state record up front: completed steps, current step, accumulated artefacts, budget spent, and the idempotency keys used.
2. Checkpoint after every step that costs more than a trivial read — not only at the end.
3. Write atomically: write to `state.json.tmp` then `os.replace` onto `state.json`, so a crash cannot leave a torn file.
4. Make each step's resume decision from the checkpoint: if `completed_steps` contains step N, skip it and do not re-fire its side effect.
5. Store external-action keys (idempotency keys, message ids) in the checkpoint so a resumed write dedupes instead of duplicating.
6. Keep artefacts by path on disk and reference them in state; never serialise the artefact data into the checkpoint.
7. On resume, validate the checkpoint's schema version before trusting it; a stale format is discarded, not guessed at.
8. Record the checkpoint line in the log: `checkpoint step=6 spent=14/40 signames=3`.

```python
import json, os
def save(state, path="state.json"):
    tmp = path + ".tmp"
    json.dump(state, open(tmp, "w"))
    os.replace(tmp, path)   # atomic on POSIX; a crash never leaves a partial file
```

## Pitfalls

- Checkpointing only at the very end, which resumes the run at "start over".
- Writing state non-atomically, so a crash mid-write leaves invalid JSON that blocks every future resume.
- Re-firing side-effecting steps because the checkpoint recorded "step done" but not which external call it made.
- Serialising large artefacts into the checkpoint, bloating it and slowing every write.
- Trusting a checkpoint from an older schema without a version check, resuming into corrupt assumptions.
- Resuming without re-reading live state, when the environment changed while the run was down.

## Verification

    python3 -c "import json;s=json.load(open('state.json'));print(s['schema'],s['completed_steps'],s['spent'])"   # parses, shows schema and progress

Report the checkpoint path, the last completed step resumed from, and the budget preserved.
