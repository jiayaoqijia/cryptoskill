---
name: pin-provider-and-module-versions
description: Use when IaC builds must be reproducible across machines and time. Pins providers and modules to exact versions with a committed lock file so a floating version cannot change the plan.
---

# Pin provider and module versions

An unpinned provider is an unpinned plan: a minor release can change defaults and replace resources. Pin exact versions and commit the lock file.

## Procedure

1. Constrain every provider and module to exact versions, not ranges:
       terraform { required_providers { aws = { source = "hashicorp/aws" version = "= 5.64.0" } } }
2. Commit `.terraform.lock.hcl`. It records the exact provider build and its hashes; without it two machines resolve differently.
3. Run `terraform init -upgrade=false` in CI and reject a locked-file diff in review; a lock change is a deliberate dependency change.
4. Pin module sources too: `?ref=v2.3.1`, never a branch.
       module "vpc" { source = "git::https://github.com/acme/tf-vpc?ref=v2.3.1" }
5. Verify the lock file covers every platform your CI and laptops use:
       terraform providers lock -platform=linux_amd64 -platform=darwin_arm64
6. Bump versions in a dedicated PR with the plan diff attached; never bump as a side effect of another change.
7. Record the change in a changelog entry: which provider, old to new, and the plan delta.
8. For air-gapped builds mirror the providers into an internal registry and point `host` at it.

## Pitfalls

- `version = ">= 4.0"` rolling forward on every `init`, so the same commit plans differently next week.
- `.terraform.lock.hcl` gitignored, so every machine resolves its own provider builds and hashes.
- A branch ref for a module (`?ref=main`), where a bad module commit breaks another team's deploy.
- Upgrading a provider inside an unrelated PR, hiding a replace among feature changes.
- A lock file covering only `linux_amd64`, so an `init` on an Apple laptop rewrites it and CI then rejects.

- A `~>` constraint that still floats within a minor series and rolls a patch that changes a default.
- Two modules pinning incompatible versions of the same provider, so `init` fails only at apply time.

## Verification

    terraform providers   # all versions show '=' constraints, no ranges
    git diff --exit-code .terraform.lock.hcl   # clean after init -upgrade=false

Report: the pinned provider and module versions, the lock file's platform coverage, and the plan diff of the bump.
