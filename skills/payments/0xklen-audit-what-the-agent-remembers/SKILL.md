---
name: audit-what-the-agent-remembers
description: Use when you want a full inventory of stored memory before trusting it. Enumerates entries, dates, and use counts so dead weight and gaps are visible.
---

# Audit What the Agent Remembers

You cannot reason about memory you have not listed. An audit enumerates every stored fact with its age and whether it was ever used, turning a black box into a table.

## Procedure

1. Enumerate the store: `find ~/.hermes/memories -type f -name '*.md' | sort`.
2. Dump every entry with its date: `grep -rn "^20[0-9][0-9]-" ~/.hermes/memories/`.
3. Count by age bucket and print the histogram; a healthy store is mostly recent, with a small aged tail.
4. Flag entries with no date — they cannot be aged or pruned, so they are the first gap.
5. Flag entries with no source — unverifiable by construction.
6. Cross-check for the same key appearing twice: `grep -oE '^[a-z-]+ *=' ... | sort | uniq -d`.
7. List entries never referenced since creation, if use is tracked; the never-used set is the pruning queue.
8. Compare the store against the questions you actually ask — a store full of facts you never query is misrouted (see `route-a-fact-to-memory-session-or-skill`).
9. Write the audit to `notes/memory-audit.md`: counts, undated, unsourced, duplicated, unused.
10. Report the four numbers before making any change; audit first, prune second.

## Pitfalls

- Auditing by memory of what you stored instead of dumping the store to a file.
- Counting entries by file and missing that one file holds forty facts.
- Ignoring undated entries in the histogram, so the age picture is wrong.
- Treating a large store as healthy when most entries are never read.
- Deleting during the audit rather than after it, so the inventory is incomplete.

- Reporting totals without the file they came from, so the audit cannot be re-run.
- Auditing only the memory store and ignoring skills and session notes that also hold facts.
- Skipping the duplicate check, so a fact counted once is actually stored three times.

## Verification

    wc -l notes/memory-audit.md; grep -c "undated\|unsourced\|duplicate\|unused" notes/memory-audit.md
    # passes when the four counts are present and sum to the total entry count

Report to the user: total entries, and the counts of undated, unsourced, duplicated, and unused.
