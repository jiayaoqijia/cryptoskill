---
name: steer-a-running-child-agent
description: Use when a running subagent needs a mid-flight correction. Delivers a minimal, explicit steering message without restarting it, and confirms the child adopted the change.
---

# Steer a Running Child Agent

Steering is cheaper than a restart but only if the child can act on it. Send one precise change, keep its existing state, and verify the next output reflects it.

## Procedure

1. Decide first whether the child is worth steering: if it is far off-course, stop it and re-dispatch with a corrected brief instead.
2. Confirm the child can receive messages — some runtimes expose a channel; if not, steering is unavailable and you must stop and re-dispatch.
3. Write the correction as a delta against the current brief, not a new brief: "stop writing SKILL.md for X; switch to slug Y."
4. Keep the scope of the change to one decision; bundling three corrections makes it a new task.
5. Re-state the parts that must not change, so the child does not over-apply the correction.
6. Send the message and timestamp it in `notes/children/<id>.steering`: `ts <text>`.
7. Wait for the next heartbeat or artifact write, then read the child's output to confirm adoption.
8. If two outputs pass without the change taking effect, stop treating it as steered and switch to stop/re-dispatch.
9. Update the child's brief on disk (`notes/children/<id>.brief.md`) to match the steering, so disk and reality agree.
10. Note the steering in the final report so the artifact's provenance explains any divergence from the original brief.

## Pitfalls

- Sending a correction the child has no way to receive (no channel, or one that only reads at startup).
- Rewriting the whole brief mid-run, which restarts the child's mental model and discards completed work.
- Assuming receipt: a message sent is not a change applied, so the output must be read to confirm.
- Steering toward an ambiguous target ("make it better") the child interprets differently than you meant.
- Leaving the on-disk brief stale after steering, so a later reader trusts the wrong instructions.

## Verification

```bash
cat notes/children/<id>.steering; tail -3 notes/children/<id>.heartbeat
# passes when a steering line is logged and the child's next artifact write reflects it
```

Report to the user: the correction sent, the timestamp, and the child output that shows it was adopted.
