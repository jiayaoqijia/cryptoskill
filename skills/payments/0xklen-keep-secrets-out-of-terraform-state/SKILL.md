---
name: keep-secrets-out-of-terraform-state
description: Use when IaC variables or resources may hold credentials. Keeps plaintext secrets out of state and plan files, which sit in a bucket and a CI artefact by default.
---

# Keep secrets out of Terraform state

State records every attribute of every resource, including generated passwords and keys, and it lives in a bucket and a CI artefact. A secret in state is a secret leaked.

## Procedure

1. Treat state as confidential and encrypt it: `encrypt = true` on the S3 backend, SSE-KMS on the bucket, and a bucket policy denying unencrypted PUT.
2. Never pass secrets as resource arguments that land in state. Reference a secret manager instead:
       data "aws_secretsmanager_secret_version" "db" { secret_id = "prod/db" }
       password = data.aws_secretsmanager_secret_version.db.secret_string
   Even this writes the value to state; prefer letting the platform inject it (`manage_master_user_password = true` on RDS).
3. Mark variables `sensitive = true` so values are redacted in plan output and CI logs.
4. Scan for leaked secrets before state or plan files leave the runner:
       grep -rEi 'password|secret|token|private_key' tf.plan.backup || true
5. Keep plan files out of git: add `*.tfplan`, `*.tfstate`, `*.tfvars` to `.gitignore`, and never commit `terraform.tfstate.backup`.
6. In CI pull secrets from the runner's OIDC-assumed role or the pipeline secret store at apply time, not from checked-in `terraform.tfvars`.
7. Rotate anything that was ever written to state: assume it leaked.
8. Restrict the KMS key at rest with a policy that excludes roles which only need to read.

## Pitfalls

- `variable "db_password"` with a default sitting in a committed `terraform.tfvars`.
- A plan file committed for review that carries a resource's generated password in cleartext.
- Marking a variable sensitive but then routing it through a `local` used in a non-sensitive output, which un-redacts it.
- Assuming `sensitive = true` removes the value: it only hides the display, the value stays in state and plan JSON.
- An output marked `sensitive = true` reused by another output that is not, leaking the value.

## Verification

    aws s3api get-bucket-encryption --bucket acme-tfstate   # SSEConfigured
    grep -rEi 'password|secret|token|private_key' tf.plan.backup   # no hits

Report: the state encryption config, the secret-manager references used, and the scan result showing no plaintext credentials.
