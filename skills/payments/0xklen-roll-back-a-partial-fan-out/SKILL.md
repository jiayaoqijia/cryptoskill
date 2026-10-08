---
name: roll-back-a-partial-fan-out
description: Use when a parallel batch landed but some children failed or wrote bad output. Reverts the wave to a known-good state rather than accumulating half-finished work.
---

# Roll Back a Partial Fan-Out

When half a wave is good and half is broken, patching forward compounds the mess. Define the wave's pre-state, revert the wave, and re-run only the failed slice cleanly.

## Procedure

1. Establish the pre-wave state before launching: tag it with `git tag wave-01-before`, or copy `out/` to `out/.pre-wave/`.
2. On failure, first classify: which children passed their own acceptance check and which did not.
3. Prefer reverting only the failed children's paths if the wave wrote disjoint files (safe because of partitioning).
4. If children shared any file, revert the whole wave — partial reverts on shared files produce a state neither child intended.
5. Perform the revert on paths, not by hand: `git checkout wave-01-before -- <paths>` or restore from `out/.pre-wave/`.
6. Re-verify the post-revert state matches pre-wave: `git diff wave-01-before -- <paths>` is empty for the reverted paths.
7. Re-dispatch only the failed slice, with the corrected brief, into a fresh wave id.
8. Keep the failed artifacts under `out/failed/wave-01/` for diagnosis rather than deleting them.
9. Record the rollback in `notes/waves.log`: `wave-01 rolled-back reason=<...> kept=<n> rerun=<n>`.
10. Do not re-run the passing children; their output is verified and re-running wastes budget and risks new divergence.

## Pitfalls

- Reverting the whole repo when only one child's path was bad, wiping verified siblings.
- Attempting a partial revert on a file two children touched, leaving a contradictory merge.
- Deleting the failed artifacts so the failure cannot be diagnosed or the fix validated.
- Re-running passing children "for consistency", spending budget and introducing fresh variance.
- Rolling back without a recorded pre-state, so "roll back" means guessing what was there.

## Verification

```bash
git diff --quiet wave-01-before -- <reverted-paths>; echo "revert-clean=$?"
# passes when reverted paths match the tag and only the failed slice is re-dispatched
```

Report to the user: the wave id, the paths reverted, the passing children kept, and the child ids re-run.
