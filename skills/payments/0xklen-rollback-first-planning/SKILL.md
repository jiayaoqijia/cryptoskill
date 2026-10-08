---
name: rollback-first-planning
description: Use when about to change live, shared, or hard-to-recreate state. Requires a tested undo path to exist before the change is attempted.
---

# Rollback First Planning

If you cannot describe how to undo a change in one exact command, you are not ready to make it. Decide the undo, prove it works, then apply.

## Procedure

1. Classify the change: local file (cheap undo), database (needs snapshot), deployed service (needs prior version), or external side effect (email, published package, payment — often irreversible).
2. For file and config changes, take a timestamped copy before editing:
   `cp config/app.yaml config/app.yaml.$(date +%Y%m%dT%H%M%S).bak`.
3. For database work, snapshot first: `pg_dump -Fc dbname > /tmp/dbname.dump` or `sqlite3 app.db ".backup '/tmp/app.db.bak'"`. Verify the dump is non-empty: `ls -l /tmp/dbname.dump`.
4. For a deployed service, record the current artifact identity: the image digest (`docker inspect --format='{{.RepoDigests}}' <container>`), the git tag, or the release id. Rollback is redeploy of that exact identity.
5. Write the rollback command into the plan file beside the forward command. Both must be one-liners you can paste.
6. Prove the undo works on a copy or in a scratch directory before touching the real target. Do not "trust" a backup you never restored.
7. Enumerate external side effects explicitly. For anything that cannot be undone (a sent email, a pushed tag, a minted token), mark it `IRREVERSIBLE` and require a gate as in `irreversible-action-gate`.
8. Only after steps 1-7, execute the forward change.
9. After success, keep the backup until verification passes; delete it only when the change is confirmed good.
10. Name the trigger that would force the rollback ("error rate over 1% for 5 minutes") so the decision is not made under pressure.
11. Store the rollback command in the plan file, not in your head, so another actor can execute it.
12. After applying, record the forward-change timestamp and the current good version so "roll back to" is unambiguous.

## Pitfalls

- A backup produced by `mv` of the original, so "restore" just moves the broken file back.
- Rolling back code but not the schema migration that shipped with it.
- Assuming `git revert` undoes a deploy — it does not redeploy anything.
- Deleting the backup in the same script that makes the change, before the change is verified.
- Forgetting a side effect: a cron job edited, a webhook fired, a cache warmed with the new values.
- A rollback plan that requires the very service that is down in order to run.
- Rolling back the deploy but leaving the config change that accompanied it in place.

## Verification

    ls -l config/app.yaml.*.bak /tmp/dbname.dump
    # passes when the pre-change copies exist and are non-empty

Report to the user: the forward command, the rollback command, and whether the rollback was tested on a copy or only reasoned about.
