---
name: split-a-monolithic-state-file
description: Use when one state file holds unrelated stacks and every apply is slow and risky. Splits it by blast radius using moved blocks so resources are not destroyed and recreated.
---

# Split a monolithic state file

One giant state means any apply can touch anything and a corrupt file loses everything. Split by ownership and blast radius, but move resources without destroying them.

## Procedure

1. Choose the boundary by lifecycle and ownership, not resource type: networking changes rarely, app resources hourly.
2. Move resources with `moved` blocks so Terraform rewrites the address instead of destroying:
       moved { from = aws_db_instance.main  to = module.data.aws_db_instance.main }
3. Or extract into a second state without recreating:
       terraform state mv -state-out=networking.tfstate aws_vpc.main aws_vpc.main
   Prefer `moved` plus a separate apply so the change lives in code, not a manual state edit.
4. After the split, run `terraform plan` in both stacks and require `No changes`; a non-empty plan means a resource was recreated or lost.
5. Update outputs: cross-stack references become `data` sources or `terraform_remote_state`, not a shared root.
6. Migrate the backend key: create `prod/networking` and `prod/app` keys under the same bucket.
7. Split in a low-traffic window; the split itself is a state write and takes a lock.
8. Document which stack owns which resource so the next person imports into the right one.

## Pitfalls

- Removing a resource from the new config with no `moved` block or `state rm`, destroying it on the next apply.
- Using `terraform state mv` across two local files and omitting `-state-out`, so the resource is in neither.
- Splitting mid-incident to shrink the blast radius and adding a second failure mode.
- Cross-stack `terraform_remote_state` on a stack being applied concurrently, causing a stale output.
- A split with a non-empty plan that is then applied, silently recreating a database.

## Verification

    terraform -chdir=app plan         # "No changes"
    terraform -chdir=networking plan  # "No changes"
    terraform state list | wc -l      # each resource present in exactly one stack

Report: the split boundary, each moved address, and the two empty plans proving nothing was recreated.
