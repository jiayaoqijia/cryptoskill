---
name: cap-memory-growth
description: Use when a memory or note store can grow without bound. Sets a size budget, a consolidation policy, and an eviction rule so growth stays bounded.
---

# Cap Memory Growth

Unbounded memory is a slow failure: search degrades, staleness rises, and trust falls. A cap is a written budget plus the policy that keeps the store under it.

## Procedure

1. Measure the current store: `du -sh ~/.hermes/memories; wc -l ~/.hermes/memories/*.md | tail -1`.
2. Set a numeric cap: e.g. 2,000 lines or 500 KB, whichever the reader cares about.
3. Add a soft threshold at 80% that triggers consolidation before the hard cap.
4. Define consolidation: merge duplicates (`dedupe-accumulated-notes`), drop cold entries (`evict-cold-memory-entries`).
5. Define the hard rule: at the cap, a new entry requires evicting an equal-sized old one.
6. Prefer editing an existing entry over adding a new one — growth comes from appending.
7. Exclude derived artefacts (indexes, caches) from the budget; they are regenerable, not memory.
8. Track the size after every write in a one-line log so the trend is visible: `date -Iseconds; wc -l < files`.
9. If the store keeps hitting the cap, the real problem is routing (`route-a-fact-to-memory-session-or-skill`), not the cap.
10. Enforce the cap in the same place that writes — a cap nobody checks is a wish.

## Pitfalls

- Setting a cap and never measuring against it, so growth resumes unnoticed.
- Counting derived indexes in the budget, so eviction deletes regenerable files and keeps stale facts.
- Raising the cap every time it is hit, which is the same as having no cap.
- Consolidating by truncating entries mid-sentence, losing the fact to save space.
- Capping by file count while one file doubles in size.

- Measuring the cap in words while the writer measures in lines, so the numbers never agree.
- Setting a per-file cap when the growth is in the file count.
- Watching the cap by hand; it must be checked where writes happen, or it drifts back over.

## Verification

    wc -l ~/.hermes/memories/*.md | tail -1; test -s notes/memory-size.log && echo tracked
    # passes when the total is at or under the cap and each write logged a size

Report to the user: the cap, the current size, the trend over recent writes, and the policy that will hold it.
