---
name: automate-rollback-on-slo-breach
description: Use when a deploy needs a safety net — pins the previous image, watches the new version's SLO for a bake window, reverts automatically on breach, and drills the revert.
---

# Automate rollback on SLO breach

A rollback you have never executed is a hope. Automate it: after every deploy, watch the new version's SLO for a fixed window and revert on breach. Test the revert on a normal deploy, not during an outage.

## Procedure

1. Pin the previous good artifact by immutable tag before applying the new one:
       ROLLBACK_IMAGE=$(kubectl get deploy/app -o jsonpath='{.spec.template.spec.containers[0].image}')
   Persist that value in the pipeline as an environment variable; never rely on `latest`.

2. Define the breach condition precisely and only over the new version:
       error_ratio_5m > 2 * baseline_15m   OR   p99_5m > SLO * 1.2
   Require it to hold for three consecutive 1-minute evaluations so a single spike does not trigger.

3. Run the watch as a pipeline stage whose timeout equals the bake window (e.g. 600 s). On breach, revert and fail the pipeline:
       kubectl set image deploy/app app=$ROLLBACK_IMAGE
       kubectl rollout status deploy/app --timeout=120s

4. Gate on recovery: `rollout status` must succeed and the error ratio must fall under threshold within 3 min. If not, page a human — do not loop rollbacks.

5. Make the revert idempotent and single-flight: if two alerts fire together, only one revert runs. Use a CI concurrency group or a Kubernetes annotation lock.

6. Record the event so the incident timeline has its cause:
       deploy_events{result="rollback", version="a1b2c3", reason="error_ratio"}

7. Drill monthly: deploy a deliberately failing version in staging and confirm the pipeline reverts with no human action inside the bake window.

## Pitfalls

- Reverting the app while the database is on a forward-only migration crashes it harder than the original bug. Confirm schema compatibility before reverting.
- Watching the global error rate instead of the new version's, so a pre-existing error masks the regression or trips a false rollback.
- Auto-rollback with no notification, so the system flaps between two versions while nobody knows. Always page on rollback.
- A baseline computed over the incident window itself, so the breach inflates its own baseline and the rule never fires.

## Verification

    kubectl rollout history deploy/app    # previous revision retained
    # drill: deploy a bad image to staging; measure breach-to-healthy time
    curl -s 'localhost:9090/api/v1/query?query=changes(deploy_events{result="rollback"}[24h])' | jq

Report: the breach condition, the bake window, the staged drill's time-to-revert (target under the bake window), and confirmation the revert returned the metric under threshold.
