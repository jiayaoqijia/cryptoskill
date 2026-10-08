---
name: prune-stale-facts-from-memory
description: Use when memory may contain facts that are no longer true. Checks each entry against a live source and deletes, dates, or flags the expired ones.
---

# Prune Stale Facts from Memory

A store that only grows becomes a liability: old facts masquerade as current ones. Pruning means checking each entry against a source, not guessing which look old.

## Procedure

1. List entries with their dates: `grep -rn "^20[0-9][0-9]-" ~/.hermes/memories/ | sort`.
2. Bucket by age: older than 90 days, 30-90 days, under 30 days. The old bucket is the pruning queue.
3. For each old entry, identify the source that could re-confirm it (a config file, an API call, a repo path).
4. Re-run the check: `aws ec2 describe-instances --instance-ids i-0abc` rather than trusting the stored value.
5. Classify each: `confirmed` (still true), `changed` (value differs), `unverifiable` (no live source).
6. Edit `changed` entries in place to the new value with a fresh date; do not leave both.
7. Delete `unverifiable` entries older than 180 days — a fact nobody can check is a liability, not knowledge.
8. Add an expiry to entries that decay on their own: `expires: 2026-11-01` on a note about a short-lived resource.
9. Never prune an entry mid-task that the current task is actively using; finish the task first.
10. Log the sweep: counts confirmed, changed, and deleted, in `notes/memory-sweep.md`.

## Pitfalls

- Deleting a fact because it "looks old" without a source to confirm the change.
- Re-confirming by reading the memory store itself — that is circular and confirms nothing.
- Leaving a corrected value beside the old one, so both are greppable and one is wrong.
- Pruning during a task and losing the fact the task needed two steps later.
- Treating every fact as permanent, so nothing is ever evicted and the store bloats.
- Assuming a value is stale because the resource is old, when it is still correct.

- Flagging but not fixing, so the same false entry survives the next sweep.
- Pruning the store but not the caches derived from it, so a stale copy still answers reads.
- Checking only the newest entries, leaving the oldest — the likeliest stale — unchecked.

## Verification

    grep -rc "confirmed\|changed\|deleted" notes/memory-sweep.md
    # passes when the sweep lists a live source check for every changed or deleted entry

Report to the user: how many entries were checked, how many changed, how many deleted, and the source used for each change.
