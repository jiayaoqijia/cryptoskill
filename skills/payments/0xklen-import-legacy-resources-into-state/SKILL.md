---
name: import-legacy-resources-into-state
description: Use when resources exist in the cloud but not in Terraform. Imports them one at a time with a no-op plan as the success criterion, adopting infrastructure without recreating it.
---

# Import legacy resources into state

Import binds an existing cloud resource to a state address. It never creates or deletes; the win is a plan that shows no changes after import.

## Procedure

1. Write the resource block by hand first, matching the live resource's real attributes read from `aws describe-*`, not from guesswork.
2. Import by address, per resource, not in bulk:
       terraform import aws_s3_bucket.data acme-data-bucket
3. Immediately run `terraform plan`. The success criterion is `No changes`; any diff means your code does not match reality. Fix the code or add `ignore_changes`, never `apply` to "correct" a resource you are adopting.
4. Use import blocks (Terraform 1.5+) for reviewable, repeatable adoption:
       import { to = aws_s3_bucket.data  id = "acme-data-bucket" }
   Generate the config with `terraform plan -generate-config-out=generated.tf`.
5. Adopt resources in dependency order (bucket before bucket policy) so a plan does not propose re-parenting.
6. Do not import a resource the module will name differently; reconcile the name first or accept a replace.
7. For resources under `for_each`/`count`, import to the correctly keyed address: `aws_subnet.this["az-a"]`.
8. Commit the code and the state change together; an imported resource with no code is drift the moment someone applies.

## Pitfalls

- Running `terraform apply` after a partial import, so the diff reshapes or destroys the live resource.
- Importing into the wrong state or workspace and orphaning it from prod.
- Hand-writing attributes that differ cosmetically (tags, casing), producing a permanently non-empty plan.
- Importing a resource a `for_each` module manages under a different key, causing a duplicate or a replace.
- Assuming import proves parity; it only binds. The no-op plan is the proof.

- Importing a resource created under a different provider version, so attributes drift immediately after import.
- `-generate-config-out` overwriting an existing file and losing hand-written review notes.

## Verification

    terraform plan
    # expect: "No changes. Your infrastructure matches the configuration."

Report: each imported address, its cloud ID, and the empty plan proving the code matches reality.
