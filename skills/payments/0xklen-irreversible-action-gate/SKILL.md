---
name: irreversible-action-gate
description: Use when about to take an action that cannot be undone: delete, force-push, drop, deploy, publish, send, or spend. Forces an explicit checkpoint, minimal scope, and confirmation so one command cannot destroy irreplaceable state.
---

# Irreversible Action Gate

Some commands are one-way doors. Treat them differently from reversible ones: stop, enumerate what cannot be recovered, shrink the scope, and confirm before the command runs.

## Procedure

1. Name the action and its irreversibility class: file destruction, history rewrite, data loss, external communication, publication, or money movement.
2. Enumerate blast radius in writing: which paths/rows/recipients/targets are hit, and which are outside the blast. Example: `rm -rf build/*` hits `build/`, not `src/`.
3. Take a recoverable copy where possible: `tar czf /tmp/pre-delete-$(date +%s).tgz <paths>`; for a DB, a dump; for a branch, `git branch backup/$(date +%Y%m%d) HEAD`.
4. Replace destructive wildcards with an explicit enumerated list. Run the dry variant to print targets first: `find build -maxdepth 1 -type f -print` before deleting.
5. Run the smallest-scope version first (one file, one row, one recipient), verify the effect, then widen only if the task truly needs it.
6. Require confirmation for anything with external or irrecoverable effect. State exactly what will happen: "This will delete 214 files under build/ and force-push origin/main, discarding 2 remote commits."
7. Never use `--force`/`-rf` as a reflex. Justify the flag: `git push --force-with-lease` only after `git fetch` shows no one else moved the branch.
8. Execute the single scoped command, then immediately verify the target state (see `silent-failure-detection`).
9. For an irreversible side effect that already left the machine (an email, a webhook), record its timestamp and content-hash in the handoff so a duplicate is detectable.
10. Prefer a recoverable mechanism over an irreversible one: a `git branch` backup over `git branch -D`, soft-delete over hard-delete.
11. For bulk deletion, move to a quarantine directory first (`mkdir -p .trash && mv <glob> .trash/`) and delete after verification.
12. If confirmation is unavailable, downgrade the action to its reversible form and tell the user what was deferred.

## Pitfalls

- `rm -rf $VAR/` with an empty or unset `VAR`, expanding to `rm -rf /`.
- `git push --force` without `--force-with-lease`, overwriting a colleague's commits.
- Dropping a table before the dump finished, or before checking the dump is non-empty.
- Sending a batch email/campaign to the full list to "test" rather than to one address.
- Deleting a branch, tag, or file that is not backed by a remote and cannot be recovered.
- Running the widened command because the one-file test "worked", without checking the full blast-radius count.
- Treating `git reset --hard` as reversible because the commit is in the reflog, when it may already be pruned.

## Verification

    ls -l /tmp/pre-delete-*.tgz && git branch --list 'backup/*'
    # passes when the recoverable copy exists and the dry-run target list matched the actual scope

Report to the user: the exact command, the blast radius count, the recovery copy path, and the confirmation that authorized it.
