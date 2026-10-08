---
name: deduplicate-work-across-agents
description: Use when fanning out tasks that may overlap so two children do the same work. De-overlaps the roster before launch and reconciles any duplicate output at fan-in.
---

# Deduplicate Work Across Agents

Duplicate assignment wastes budget and produces two versions of one artifact that then conflict. Normalise the roster before launch and reconcile overlaps at fan-in.

## Procedure

1. Normalise every task key before comparing: lowercase, trim, collapse whitespace, strip trailing punctuation.
2. Treat near-identical keys as duplicates: two slugs differing only by hyphen placement are the same job.
3. Build the roster keyed by the normalised task id; a second assignment of an existing key is rejected, not appended.
4. Detect residual overlap with a sorted check: `sort -k2 notes/tasks.tsv | uniq -d -f1` lists repeated task ids.
5. Where two children must touch the same file, that is a partition problem, not a dedupe one — split by path.
6. At fan-in, dedupe outputs on the child key: `jq -s 'unique_by(.slug)' out/all.jsonl`.
7. When two files describe the same artifact with different content, do not keep both — pick by evidence and note the loser.
8. Count assignments before and after dedupe and reconcile the drop in `notes/waves.log`.
9. Never let dedupe silently drop a distinct task that only looked like a duplicate; confirm intent when unsure.
10. Report the dedupe count to the requester so a later "why did this run fewer tasks than I listed" question has an answer.

## Pitfalls

- Comparing raw slugs so `foo-bar` and `foobar` both run and produce competing artifacts.
- Dropping a duplicate that was actually a re-run of a failed task, losing the intended retry.
- Deduping outputs by file content when two children legitimately produce identical bytes for different inputs.
- Merging duplicates at fan-in only, after paying for both children in full.
- Treating "same directory" as "same task" and collapsing two genuinely different files.

## Verification

```bash
sort notes/tasks.tsv | uniq -d; jq -s 'length, (unique_by(.slug)|length)' out/all.jsonl
# passes when no duplicate keys print and merged length equals deduped length
```

Report to the user: the assignments before and after dedupe, and any artifact produced twice.
