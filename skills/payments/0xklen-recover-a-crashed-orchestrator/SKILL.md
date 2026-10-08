---
name: recover-a-crashed-orchestrator
description: Use when the parent agent process died mid-run and children may be orphaned or half-collected. Reconstructs state from disk before resuming so work is not redone blindly.
---

# Recover a Crashed Orchestrator

When the parent dies, its memory of what it launched is gone but the disk still holds the roster and artifacts. Reconstruct from files, not recollection, before relaunching anything.

## Procedure

1. Do not relaunch anything yet; a blind restart double-spawns children that are still alive.
2. Read the last known plan from disk: `notes/roster.json`, `notes/waves.log`, `notes/dag.tsv`.
3. Find live children with `ps -axo pid,ppid,etime,command | grep -i child`; adopt or kill them deliberately.
4. Reconstruct progress per child from artifacts: a child with a full output file is likely done even if unrecorded.
5. Check terminal markers (`notes/children/<id>.done`) and heartbeats to separate done, stalled, and never-started.
6. Reconcile the roster with reality into `notes/recovery.md`: `child-id state=done|partial|missing process=alive|dead`.
7. Resume from the first incomplete wave; skip children whose artifacts pass their acceptance checks.
8. Clean up orphans from the crash: stray locks, `$TMPDIR/child-*` directories, and half-written outputs marked partial.
9. Re-record state at each step so a second crash resumes from a later point than this one.
10. Only after reconciliation, launch the missing and partial children into a fresh wave id.

## Pitfalls

- Immediately re-running the whole roster, duplicating work from children that survived the crash.
- Killing live-but-unknown children because the parent forgot it started them, losing their partial output.
- Trusting an artifact's presence as proof of completion when it is a truncated write from the crash.
- Resuming from the crash-time wave without noticing a lock left by a dead child still blocks the queue.
- Recovering state into memory only, so the next crash loses it again.

## Verification

```bash
cat notes/recovery.md; ps -axo pid,command | grep -i child | grep -v grep
# passes when every roster child has a reconciled state and no unaccounted process is running
```

Report to the user: children found done, partial, and missing, plus any orphan adopted or killed during recovery.
