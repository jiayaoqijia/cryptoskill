---
name: validate-iac-in-ci-before-merge
description: Use when IaC changes reach apply without checks. Runs format, validate, policy, and a plan in CI so a broken or non-compliant change fails before it can touch an environment.
---

# Validate IaC in CI before merge

Every finding caught before merge is one not caught during an outage. Run a fixed gate: format, validate, policy, then a plan.

## Procedure

1. Format check that fails, without auto-fixing silently:
       terraform fmt -check -recursive || { echo "run terraform fmt"; exit 1; }
2. Static validate without a backend:
       terraform init -backend=false -input=false
       terraform validate
3. Lint and security policy:
       tflint --recursive
       checkov -d . --quiet --soft-fail-on LOW
4. Validate against the real plan in a plan-only job with read-only credentials:
       terraform plan -lock-timeout=5m -out=tf.plan
5. Run policy as code over the plan JSON (OPA/Conftest) so rules see resolved values, not source text:
       terraform show -json tf.plan | conftest test - --policy policies/
6. Post the plan to the PR as a comment so a reviewer sees the diff; a plan only in CI logs is unreviewed.
7. Keep the gate fast: cache `.terraform` and providers between runs, or people learn to skip it.
8. Make the gate required in branch protection; an advisory check is one that gets merged past at 5 pm.

## Pitfalls

- `terraform validate` alone: it checks syntax and references, not policy, not a plan, not drift.
- Running `init -upgrade`, which changes the lock file in a check job and produces spurious diffs.
- A plan job with write credentials that could apply if a later step misfires.
- Policy that runs on HCL only, missing a value injected at plan time (a variable that resolves to a public bucket ACL).
- Soft-failing everything, so the check is green on every PR and no one reads it.

- Caching `.terraform` across branches, so a stale module version passes validate and only fails at apply.
- A plan step gated behind manual approval to read, so the plan is never reviewed before merge.

## Verification

    terraform fmt -check -recursive && terraform validate && tflint --recursive
    conftest test <(terraform show -json tf.plan) --policy policies/   # exit 0

Report: the gate steps, a PR that failed each one, and the branch-protection setting making them required.
