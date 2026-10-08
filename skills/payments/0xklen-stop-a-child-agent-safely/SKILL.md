---
name: stop-a-child-agent-safely
description: Use when a subagent must be halted before it finishes — wrong direction, budget breach, or shutdown. Stops it so partial writes are known and every resource it held is released.
---

# Stop a Child Agent Safely

A hard kill can leave half-written files and held locks. Stop a child deliberately: signal, wait, collect what it wrote, and release everything it held.

## Procedure

1. Record why you are stopping it — runbook rule, budget, or user request — in `notes/stopped.log`.
2. Prefer a cooperative stop first: send a "finish the current write and exit" signal if the runtime supports one.
3. If cooperative fails after one grace interval (e.g. 15s), escalate to terminating the process.
4. Capture the child's last output and partial artifact before anything overwrites them: copy `out/<id>/` to `out/<id>.partial/`.
5. Identify resources the child may not release on kill: lock files, temp directories, background servers.
6. Clean up deliberately: remove the child's lock file and its `$TMPDIR/child-<id>/` subtree only after copying partial output.
7. Mark the child's slot as stopped in `notes/roster.json` so the fan-in does not wait forever.
8. Never treat stopped output as complete: if the artifact is partial, downstream consumers must be told so explicitly.
9. If the stop was for a budget or loop reason, record the threshold that tripped so the next run avoids it.
10. Confirm no orphaned process remains: `ps -o pid,command -p <pid>` returns nothing.

## Pitfalls

- `kill -9` as the first move, leaving a half-written `SKILL.md` that a later glob picks up as valid.
- Leaving a lock file behind, so the next child blocks forever on a slot nobody holds.
- Stopping the child but not updating the roster, so the fan-in waits for a result that will never come.
- Deleting the partial artifact to "clean up", destroying the only evidence of what the child had done.
- Orphaning a background server the child spawned, which keeps the port busy for the next run.

## Verification

```bash
ps -o pid,command -p "$(jq -r .pid notes/children/<id>.json)" 2>&1; ls out/<id>.partial/
# passes when the process is gone, no lock remains, and partial output is preserved
```

Report to the user: the reason for the stop, whether it was cooperative, and the resources released.
