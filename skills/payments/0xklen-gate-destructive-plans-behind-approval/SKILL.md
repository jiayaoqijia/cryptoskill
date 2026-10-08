---
name: gate-destructive-plans-behind-approval
description: Use when an apply can delete or replace resources in a shared environment. Routes plans that contain destroys to a human approval and keeps additive changes on auto-apply.
---

# Gate destructive plans behind approval

Auto-apply is fine for additive changes and dangerous for destructive ones. Gate on the plan's content, not on the branch name.

## Procedure

1. In CI compute the destructive set before apply and expose it as an output:
       COUNT=$(terraform show -json tf.plan | jq '[.resource_changes[]|select(.change.actions|index("delete"))]|length')
       echo "destroys=$COUNT" >> "$GITHUB_OUTPUT"
2. Route `destroys > 0` to a manual approval environment; keep `destroys == 0` on auto-apply:
       environment: ${{ steps.plan.outputs.destroys != '0' && 'prod-approval' || 'prod-auto' }}
3. Require the approver to be a different identity than the apply author (four-eyes); a pipeline cannot approve its own plan.
4. Attach the plan artefact and the destroy count to the approval so the approver reviews content, not a summary.
5. Guard stateful resources at the code layer too: `lifecycle { prevent_destroy = true }`, so even an approved pipeline cannot drop a database without a code change.
6. Expire approvals (24 h); an approval applied after unrelated commits is not approval of what runs.
7. Log the approver identity and timestamp next to the plan hash for audit.
8. Dry-run the gate on a branch that deletes a scratch resource before trusting it on prod.

## Pitfalls

- Approving on "the pipeline is green", when green includes the destroy.
- A single environment with one approver who is also the author: four-eyes in name only.
- Counting destroys from a plan regenerated after approval (a provider bump changes it).
- No `prevent_destroy`, so the only thing between a typo and an empty prod database is a human reading a diff.
- Approvals that never expire, applied days later on top of other merges.

- The destroy count read from a plan generated before a `git pull`, so it does not match what is applied.
- An approval environment without branch protection, so any collaborator can self-approve.

## Verification

    grep -q 'destroys=0' ci.outputs || echo "manual approval required"
    terraform show -json tf.plan | jq '[.resource_changes[]|select(.change.actions|index("delete"))|.address]'

Report: the gate rule, the destroy count that tripped it, the approver identity, and the plan hash applied.
