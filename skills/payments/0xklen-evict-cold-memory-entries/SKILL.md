---
name: evict-cold-memory-entries
description: Use when a memory store has grown large and much of it is never read. Ranks entries by access recency and evicts the cold tail under a size budget.
---

# Evict Cold Memory Entries

A store with no eviction rule grows until search degrades and nobody trusts it. Eviction is a policy, not a mood: rank by use, keep the hot set, cut the cold tail.

## Procedure

1. Set a size budget first, in entries or bytes: "memory stays under 2,000 lines".
2. Record access where you can — a `last_used` field, or a grep of the logs for the key.
3. Rank entries: hot (used this month), warm (this quarter), cold (older or never).
4. Evict from cold only; never evict a hot entry to make room for a new one.
5. Protect pinned entries: mark load-bearing facts `pin: true` and skip them in the sweep.
6. Before deleting a cold entry, check if it is cheap to regenerate from a source; if yes, delete it confidently.
7. Move rather than destroy when unsure: `mv notes/facts/old.md notes/archive/` keeps it greppable but out of the hot set.
8. Re-run the size count after the sweep and compare against the budget.
9. Schedule the sweep on a trigger (every N sessions, or when the store crosses the budget), not "sometime".
10. If the store is under budget and nothing is cold, do nothing — eviction is not a ritual.

## Pitfalls

- Evicting the least-recently-read entry when it is the one fact every task needs at step 1.
- Deleting without a source to regenerate from, so a needed value is gone for good.
- Keeping everything "just in case", so the budget is never met and search keeps degrading.
- Sweeping during a task and evicting the entry that task is using.
- Evicting by recency alone when a rarely-used fact is load-bearing (a disaster-recovery endpoint).

- Evicting by file mtime when a bulk tool rewrites the file, resetting every clock.
- Archiving to a directory the retriever still scans, so nothing was actually evicted.
- Running the sweep once and not scheduling the next, so the cold set regrows unchecked.

## Verification

    wc -l ~/.hermes/memories/*.md | tail -1; grep -c "pin: true" ~/.hermes/memories/*.md
    # passes when the total is under budget and no pinned entry was removed

Report to the user: the budget, the size before and after, how many entries moved to archive, and any eviction you could not regenerate.
