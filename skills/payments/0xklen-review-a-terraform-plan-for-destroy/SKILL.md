---
name: review-a-terraform-plan-for-destroy
description: Use when a plan may delete or replace resources. Extracts every destroy and replace action and forces a one-line justification for each before anyone approves the apply.
---

# Review a Terraform plan for destroy

`terraform apply` deletes whatever the plan says to delete. An accidental destroy of a database or a load balancer is silent until traffic drops. Review the destroy set explicitly.

## Procedure

1. Generate a machine-readable plan and extract destructive actions:
       terraform plan -out=tf.plan
       terraform show -json tf.plan | jq -r '.resource_changes[]
         | select(.change.actions | index("delete"))
         | "\(.change.actions|join("+")) \(.address)"'
2. `actions: ["delete","create"]` is a replacement (recreate). On `aws_db_instance` or `aws_ebs_volume` it means data loss unless the resource is stateless.
3. For each destroy, write one line of justification in the PR: why the resource is safe to remove. No justification, no apply.
4. Guard stateful resources in code: `lifecycle { prevent_destroy = true }` on RDS, S3 buckets, KMS keys, the state bucket itself. A destroy plan against these must fail loudly.
5. Watch for cascading destroys: deleting a VPC, security group, or IAM role in use elsewhere shows as one delete here and a broken resource there.
6. Beware `create_before_destroy` on resources with unique names or IPs: the create fails because the old one still holds the name.
7. For a targeted fix prefer `terraform plan -target=<addr>` and review that scoped plan; do not eyeball a 400-line diff.
8. Count the destroys and paste the number in the PR; a number a reviewer can check beats "looks fine".

## Pitfalls

- Approving on the green check alone; the summary line says `Plan: 1 to add, 2 to destroy` and nobody reads it.
- A replace of a stateful resource where the old volume is not snapshotted first.
- `terraform state rm` to "avoid" a destroy, silently orphaning the live resource and the bill.
- A count taken from a different plan than the one applied (regenerated after a provider bump).
- Ignoring ordering: a replacement whose new resource depends on the old one being destroyed cycles or fails.

## Verification

    terraform show -json tf.plan | jq '[.resource_changes[] | select(.change.actions|index("delete"))] | length'
    grep -rn 'prevent_destroy' *.tf   # stateful resources are guarded

Report: destroy and replace counts, each destroy's justification, and which stateful resources carry `prevent_destroy`.
