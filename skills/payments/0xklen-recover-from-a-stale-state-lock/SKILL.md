---
name: recover-from-a-stale-state-lock
description: Use when terraform refuses to run because the state lock is held by a crashed or killed run. Verifies the holder is dead before force-unlocking, never disabling locking.
---

# Recover from a stale state lock

A crash or killed CI job leaves a lock with no process behind it. Force-unlocking a lock that is still held corrupts state; confirm the holder is gone first.

## Procedure

1. Read who holds the lock; the error names the ID, path, and operation:
       Error: Error acquiring the state lock
       ID: 8f3c...  Operation: OperationTypeApply  Who: ci-runner@...
2. For S3+DynamoDB, inspect the lock row:
       aws dynamodb get-item --table-name tf-locks \
         --key '{"LockID":{"S":"acme-tfstate/prod/terraform.tfstate"}}'
3. Confirm no live process holds it: the CI job that owns the ID is finished or failed, and no `terraform apply` runs on that runner.
       ps aux | grep '[t]erraform apply'
4. Only then force-unlock with the exact ID from the error:
       terraform force-unlock 8f3c-...
5. If a run genuinely is in progress, wait for it; `-lock-timeout=5m` makes waiting automatic.
6. After force-unlock, immediately `terraform plan` to confirm state is intact and consistent.
7. Do not delete the DynamoDB row by hand instead of force-unlock; the CLI also notifies the backend and keeps lock metadata consistent.
8. Fix the root cause: set `-lock-timeout`, add CI concurrency limits, and ensure killed jobs do not orphan locks.

## Pitfalls

- Force-unlocking a lock held by a live apply, so two writers interleave and corrupt state.
- Deleting the lock table row manually, leaving the backend's lock metadata inconsistent.
- `-lock=false` as a "fix", removing locking for every future run.
- Force-unlocking with a guessed ID; the CLI requires the real one, and people work around it by deleting the row.
- Not running a plan after unlock, so pre-existing corruption surfaces at the next apply.

## Verification

    aws dynamodb get-item --table-name tf-locks \
      --key '{"LockID":{"S":"acme-tfstate/prod/terraform.tfstate"}}'   # Item: null after unlock
    terraform plan                                                    # acquires lock, no errors

Report: the stale lock ID, the evidence the holder was dead, the force-unlock result, and the clean plan afterward.
