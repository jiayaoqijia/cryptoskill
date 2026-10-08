---
name: lock-remote-state-before-a-write
description: Use when multiple engineers or CI jobs can apply the same Terraform state. Verifies the backend supports locking and that apply always takes the lock, so two writers cannot corrupt state.
---

# Lock remote state before a write

Terraform state is a single mutable file; two concurrent writers lose each other's resources and produce a corrupt, hard-to-recover state. Locking serialises writes.

## Procedure

1. Use a backend with locking: S3 + DynamoDB lock table, GCS, or Terraform Cloud. The default `local` backend has no lock.
       backend "s3" {
         bucket = "acme-tfstate"  key = "prod/terraform.tfstate"  region = "us-east-1"
         dynamodb_table = "tf-locks"  encrypt = true
       }
2. Create the lock table with a `LockID` string primary key; without it the lock write fails and apply can proceed unlocked on older providers.
3. Run `terraform apply` (never `-lock=false`) so the lock is taken for the whole plan+apply.
4. In CI set `-lock-timeout=5m` so a queued job waits for a lock rather than failing on the first attempt.
5. Prove the lock is real: while an apply is paused, a second `terraform plan` must block with `Error acquiring the state lock`.
6. Never share one state file across environments or teams; encode the boundary in the key (`prod/`, `staging/`).
7. If something genuinely holds a stale lock after a crash, use the stale-lock recovery path. Do not disable locking.
8. Grant the CI identity `dynamodb:PutItem`/`DeleteItem` on the lock table only, never `*`.

## Pitfalls

- `-lock=false` in a Makefile to "avoid lock errors" removes the only protection against concurrent writers.
- Two workspaces pointing at the same key but different names, which do not collide as separate lock rows.
- A DynamoDB table without the `LockID` key, so locking quietly no-ops.
- Deleting the lock table during cleanup, then applying against a bucket no one can lock.
- Long-held locks from a killed job with no timeout, blocking all deploys until manually cleared.

## Verification

    terraform plan 2>&1 | grep 'Error acquiring the state lock'   # a second concurrent run blocks
    aws dynamodb scan --table-name tf-locks --max-items 1         # row appears during apply

Report: the backend, the lock table, the observed block on a concurrent run, and the CI lock timeout.
