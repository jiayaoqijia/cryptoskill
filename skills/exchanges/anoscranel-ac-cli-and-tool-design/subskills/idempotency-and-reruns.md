---
name: idempotency-and-reruns
domain: software-engineering/idempotency-and-reruns
trigger: "Making a command safe to run twice."
anti_trigger: "Not for HTTP idempotency keys, and not for transaction design."
scope: "Making a command safe to run twice."
status: seedling
---

# Idempotency and re-runs

## Standard

A command that a person or a script may run twice should produce the same result the second time. That property is what makes a failed run recoverable: instead of reasoning about how far the first attempt got, the operator re-runs and the tool reconciles. Without it, every failure requires a manual investigation before the retry is safe.

The design techniques are few and well known. Check for the desired state before acting rather than acting unconditionally; use a temporary file and rename rather than writing in place; mark work completed so that a resumed run skips it; and make the operation's identity explicit so a duplicate can be detected. Each converts a partially completed run into a resumable one.

Primary sources: <https://pubs.opengroup.org/> and <https://clig.dev/>.

## Decision rules

- Record whether the command is safe to run twice, and the evidence for the claim.
- Record the state check that precedes each mutation.
- Record the write technique: temporary file and rename, or in-place.
- Record the resumption marker and where it is stored.
- Record the operations that are genuinely not idempotent, such as sending a message, and how they are guarded.
- Record the dry-run capability, which lets a re-run be inspected before it acts.

## Procedure

1. For each mutation, record the state check that precedes it.
2. Replace in-place writes with a temporary file and an atomic rename.
3. Record a resumption marker for multi-step operations.
4. Identify non-idempotent effects and guard each with a key or a prior check.
5. Provide a dry run and record what it inspects.
6. Test by running the command twice and comparing results.

## Anti-patterns

- Writing in place, so an interrupted run leaves a truncated file.
- No state check, so a second run duplicates what the first created.
- A resumption marker that is written before the work completes.
- Treating a message send as idempotent because it usually succeeds.
- A dry run that performs the check differently from the real run.

## Done checklist

- [ ] Idempotency claim recorded with evidence.
- [ ] State checks recorded per mutation.
- [ ] Atomic write technique recorded.
- [ ] Resumption marker recorded.
- [ ] Non-idempotent effects guarded.
- [ ] Double-run test performed.

The dry run should share its check logic with the real run rather than approximate it, because a dry run that inspects different state from the one the real run acts on gives confidence it has not earned, and the divergence is usually discovered at the moment the real run does something the dry run did not anticipate.


## Sources

- POSIX utility design: <https://pubs.opengroup.org/>
- CLI and tooling guidance: <https://clig.dev/>
- Distributed systems practice: <https://martinfowler.com/>
