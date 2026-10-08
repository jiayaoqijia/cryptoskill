---
name: document-a-rollback-plan
description: Use when a change needs a written way back before it ships. Records the trigger, the exact revert steps, the data considerations, and the verification that the rollback worked.
---

# Document a Rollback Plan

A change without a written rollback is a one-way door nobody labelled. Decide the trigger and the steps before deploy, when you are calm and the system is healthy.

## Procedure

1. State the trigger explicitly: the metric and threshold that flips the decision, such as p99 over 800ms for 5 min or error rate over 2%.
2. Give the exact revert command, in order, for each layer changed (code, config, schema):
   `kubectl rollout undo deploy/api -n prod --to-revision=41`.
3. Distinguish code rollback from data rollback. A schema change often cannot be reverted by redeploy; say so.
4. Cover the data: if the new write path drops a column, note the backfill needed and the window of loss.
5. Name who can authorise the rollback and the time box before escalating.
6. State what the rollback does NOT undo: caches, queued messages, external side effects, sent emails.
7. Give the verification command and the value that confirms the old version is serving.
8. Note the forward-fix alternative for when rollback is too costly (a migration already ran).
9. Pin the previous artifact so the revert target exists: keep the prior image tag, not `latest`.
10. Rehearse the rollback in staging before relying on it in production.
11. Store the plan next to the change (in the PR description or the deploy issue), not in a separate tracker.
12. Time-box the decision: say how long to tolerate a bad state before rolling back regardless.

## Pitfalls

- "Revert the change" with no command, assuming the deploy tool has one-click undo it may not.
- A rollback plan that reverts code but ignores a schema migration that already ran.
- No trigger condition, so the decision to roll back becomes a debate during an incident.
- Relying on `latest` tags, so the previous image is gone when you need it.
- Forgetting irreversible side effects: emails sent, payments captured, cache entries written.
- A rollback that depends on a manual console step nobody on-call has access to at 3am.
- Testing only the happy path, so the undo path itself has never been executed.

## Verification

    kubectl get pods -l app=api -o jsonpath='{.items[0].spec.template.spec.containers[0].image}'

After the undo, this returns the previous known-good image tag, not the new one. Rehearse in staging: execute the plan, then confirm the old version serves and the documented data caveat holds.
