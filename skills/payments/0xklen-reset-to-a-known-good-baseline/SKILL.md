---
name: reset-to-a-known-good-baseline
description: Use when a working tree, cache, or environment has drifted after many failed fixes. Restores a state known to have worked before re-testing, so results are trustworthy again.
---

# Reset to a Known Good Baseline

After a dozen failed fixes the environment itself is suspect: half-applied patches, stale caches, leftover processes. Reset to a state you know worked, then re-check the bug still stands.

## Procedure

1. Save your work first: `git stash push -u -m "wip debug"` or branch it with `git switch -c wip/debug`. Never reset over uncommitted work you may need.
2. Record what you had: `git status --porcelain`, `git diff --stat`, and any running processes you started.
3. Reset the tree: `git reset --hard <known-good-sha> && git clean -fd` — the clean removes untracked artefacts a build wrote.
4. Reset process and container state: `docker compose down -v` (the `-v` drops anonymous volumes), kill stray watchers with `pkill -f 'nodemon|jest --watch'`, restart the app.
5. Clear caches that persist across builds: `rm -rf .pytest_cache __pycache__ node_modules/.cache target/debug` or the language equivalent, then reinstall if the lockfile changed.
6. Re-run the *original* reproduction on the clean baseline. If it now passes, the bug was in your accumulated edits, not the product.
7. Re-apply your work in small, separately-tested commits, or abandon it and re-derive the fix from the clean state.
8. Note the baseline sha in the bug log so the next person resets to the same point.

## Pitfalls

- `git clean -fdx` without checking the ignore rules, deleting a `.env` or local fixtures you cannot regenerate.
- Resetting before stashing, which silently discards the one patch that might have been the fix.
- Forgetting a background daemon that keeps the old code loaded, so the "clean" run is still the old process.
- Clearing a cache that takes 40 minutes to rebuild in the middle of a time-boxed session; reset the parts that matter.
- Treating a passing baseline as "bug fixed" when it merely stopped being reachable in the contaminated tree.
- Leaving the repo on a detached HEAD and losing the branch pointer.

## Verification

    git rev-parse HEAD && git status --porcelain
    # passes when HEAD is the named baseline and porcelain output is empty

    ./repro/run.sh; echo "baseline exit=$?"
    # passes when the original repro reproduces here, proving the reset is clean and the bug is real

Report to the user: the baseline sha, what you reset (tree, caches, processes), and whether the original bug still reproduces on the clean state.
