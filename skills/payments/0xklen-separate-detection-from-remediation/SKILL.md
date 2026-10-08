---
name: separate-detection-from-remediation
description: Use when one automation both notices a problem and tries to fix it. Splits the detecting from the acting so a false positive cannot trigger a wrong repair.
---

# Separate detection from remediation

A job that both detects and fixes conflates two decisions: "is something wrong?" and "is this the right repair?". Split them, so a spurious detection does not silently make a wrong change.

## Procedure

1. Draw the boundary: the detector produces a finding (a row, an event); the remediator consumes findings and acts. Two jobs, two run keys.
2. Make the detector read-only. It must not be able to change the system it watches; give it a read-only credential or role.
3. Emit findings as structured records with enough context to decide: what, where, observed value, threshold, and timestamp.
       {"finding":"stale_lock","resource":"queue:orders","age_s":920,"threshold_s":600,"at":"..."}
4. Let the remediator apply a policy to findings — alert, auto-fix, or hold for approval — chosen per finding type, not hard-coded in the detector.
5. Auto-remediate only the classes with a proven, reversible fix and a low false-positive rate. Hold the rest for a human.
6. Make remediation idempotent and keyed to the `finding_id`, so the same finding cannot be fixed twice.
7. Verify the fix from the detector's side: the remediator reports success, but the detector confirms the finding is gone; disagreement is itself an alert.
8. Cap remediation frequency per resource (e.g. restart at most once per 15 min) so a flapping condition does not cause a repair loop.
9. Log every remediation with the finding it acted on and the outcome, keeping detection evidence separate from action evidence.
10. When a false positive causes a wrong repair, fix the detector's threshold — do not loosen the remediator to compensate.

## Pitfalls

- A watcher that "helpfully" deletes the thing it thinks is stale, based on a heuristic that misfires.
- Auto-remediating a class whose fix is not reversible.
- One job where the detection logic and the fix share a query, so a change to one silently alters the other.
- Remediation without a rate cap, causing a restart storm.
- Treating "the remediator said success" as "the problem is gone" without the detector confirming.
- No finding id, so replays double-remediate.

## Verification

    # detector is read-only; findings and remediations reconcile one-to-one
    psql -c "select count(*) findings from findings where at > now()-interval '1 day'"
    psql -c "select count(*) remediated from remediations where at > now()-interval '1 day'"
    # pass: detector credentials cannot write; each remediation maps to one finding id

Report the detector/remediator split, the finding schema, which classes auto-remediate, the rate cap, and how the fix is confirmed.
