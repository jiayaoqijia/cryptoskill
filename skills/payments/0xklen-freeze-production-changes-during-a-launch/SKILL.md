---
name: freeze-production-changes-during-a-launch
description: Use when a release, migration, or campaign must not be disturbed by infrastructure changes. Implements a change freeze you can enforce, with an explicit logged break-glass path.
---

# Freeze production changes during a launch

A freeze is a policy; without enforcement it is a hope. Make it a denied window in the pipeline, with a documented, logged exception path.

## Procedure

1. Define the window and scope precisely: resources, environments, and start/end in UTC.
       freeze: 2026-10-08T00:00Z -> 2026-10-11T06:00Z   scope: env=prod
2. Enforce in CI: fail any prod apply whose target env matches during the window:
       if [ "$ENV" = prod ] && [ "$(date -u +%Y%m%d%H%M)" -ge 202610080000 ] \
          && [ "$(date -u +%Y%m%d%H%M)" -lt 202610110600 ]; then echo "prod frozen"; exit 1; fi
3. For IaC block at the policy layer too: an OPA rule denying mutating plans tagged `env=prod` inside the window, so a CI bypass still trips policy.
4. Allow non-mutating operations (plan, read) so reviewers can still see what would change.
5. Define break-glass: one approver, a logged reason, and a post-hoc review. Without it, people disable the freeze ad hoc.
       pre-commit run --hook-stage manual breakglass   # records approver + ticket
6. Announce the window to on-call and to teams with automated jobs (cert renewals, backups) that touch prod.
7. Watch the jobs that legitimately write during a freeze: cert renewal, autoscaling, backups. The freeze is on human infra changes, not managed writes.
8. Lift the freeze deliberately and re-enable auto-apply; a freeze never lifted silently kills deploys.

## Pitfalls

- A freeze with no enforcement, broken the first time an urgent fix appears.
- No break-glass, so an emergency requires disabling the check for everyone.
- Freezing autoscaling or cert renewal along with human changes, causing an outage the freeze was meant to prevent.
- A window in local time, so it starts or ends hours off relative to the launch.
- Forgetting to lift it, so prod drifts as normal work queues up and then lands in one risky batch.

## Verification

    date -u +%Y%m%d%H%M   # inside window: a prod apply must fail with 'prod frozen'
    conftest test prod.plan.json --policy policies/freeze.rego   # deny during window

Report: the window in UTC, the enforcement point(s), the break-glass path used (if any), and confirmation deploys resume after the lift.
