---
name: teardown-ephemeral-review-environments
description: Use when per-PR or per-branch environments are created and must not outlive their review. Drives a full, verified teardown plus a reaper so no orphaned stack keeps billing.
---

# Teardown ephemeral review environments

Per-PR environments are cheap to create and expensive to forget. A teardown that leaves half a stack alive is worse than none: it hides in the bill and the attack surface.

## Procedure

1. Namespace everything by PR/branch so teardown is one scoped destroy: `env = "pr-1432"` and all names prefixed `pr1432-`.
2. Destroy a scoped state, never a shared one:
       terraform -chdir=envs/ephemeral destroy -auto-approve -var pr=1432
3. Trigger teardown on PR close, not merge only; a closed-without-merge PR otherwise leaks the env.
4. Add a scheduled reaper as a backstop that destroys any `pr-*` stack older than 72 h:
       aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE,UPDATE_COMPLETE \
         --query 'StackSummaries[?starts_with(StackName,`pr-`) && CreationTime<`2026-10-05`].StackName'
5. Make teardown failures loud: a destroy that errors (bucket not empty, ENI in use) must page, not warn.
6. Clear non-Terraform leftovers before destroy: `force_destroy = true` on ephemeral buckets, delete k8s namespaces.
7. Revoke the env's DNS record, secrets, and IAM role as part of teardown; a live role after the stack is gone is a standing risk.
8. Verify zero spend after teardown by tag or namespace, not by trusting the exit code.

## Pitfalls

- Teardown keyed on merge: a PR closed after a force-push or abandoned leaves the stack running.
- Shared state across PRs, so `destroy` cannot target one env and either fails or destroys a neighbour.
- `force_destroy` left off, so the S3 bucket blocks the destroy and the whole stack persists.
- Deletion protection still on the RDS instance, so every teardown partially fails and leaves a database.
- A reaper name pattern that also matches a long-lived `pr-` staging env.

- A reaper running in the same account as production and, on a bad name pattern, destroying a stack it should not touch.
- Deleting the env's IAM role before the destroy, so the destroy itself lacks permission and fails.

## Verification

    aws resourcegroupstaggingapi get-resources --tag-filters Key=env,Values=pr-1432 | jq '.ResourceTagMappingList | length'
    # expect 0 after teardown

Report: the teardown trigger, the reaper's max age, and the observed resource count (zero) and spend after a destroy.
