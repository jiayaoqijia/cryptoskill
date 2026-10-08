---
name: resolve-merge-conflicts-from-parallel-agents
description: Use when two agents changed the same file or branch and git reports conflicts. Resolves by re-deriving each child's intent from its brief rather than picking a side blindly.
---

# Resolve Merge Conflicts from Parallel Agents

A conflict means two writers disagreed on the same lines. Resolve by understanding what each child was told, then produce one edit that satisfies both briefs — or an explicit decision to drop one.

## Procedure

1. Confirm the conflict is real and scoped: `git status --short --branch` lists conflicted paths.
2. List the conflicted files concretely with `git diff --name-only --diff-filter=U`.
3. Read both children's briefs (`notes/children/*.brief.md`) before touching markers; intent tells you which side is correct.
4. View the markers with context: `git diff --check` and open each file's `<<<<<<< ======= >>>>>>>` block.
5. Prefer a union where both edits are additive (two new sections); keep both and reorder by dependency.
6. Where both edited the same line, choose the version matching the frozen interface, and note the loser in `notes/merge-log.md`.
7. Never leave a marker in place: `grep -rn '^<<<<<<<' .` must return nothing after resolving.
8. Re-run each child's acceptance check after resolving, not just one, since the merge can break either.
9. If the two intents genuinely conflict with no union, that is a spec problem: stop and ask the requester which behaviour wins.
10. Commit the resolution with a message naming both child ids, so the provenance is recoverable.

## Pitfalls

- Resolving by choosing "theirs" or "ours" wholesale, silently discarding a child's valid work.
- Deleting one side's block without recording why, so the rationale is unrecoverable.
- Declaring the merge clean because the file parses, when one child's feature was dropped.
- Re-running only the check for the side you kept, missing that the merge broke the other.
- Hand-resolving markers in a 500-line file and missing one, leaving the repo unbuildable.

## Verification

```bash
grep -rn '^<<<<<<<' . ; python3 tools/validate.py --only foo
# passes when the marker grep is empty and both children's checks still pass
```

Report to the user: the conflicted paths, which child's change won on each axis, and the post-merge check output.
