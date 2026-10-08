---
name: tag-resources-for-cost-and-ownership
description: Use when cloud spend or on-call ownership cannot be attributed. Enforces a tag schema at the provider and policy layer so every resource names its owner, env, and cost centre.
---

# Tag resources for cost and ownership

Untagged resources are unowned: nobody knows who pays for them or who to wake when they break. Enforce tags in code and at the policy layer, not by convention.

## Procedure

1. Define the minimum schema once and apply it to every taggable resource: `env`, `owner` (team handle), `cost_center`, `managed_by = "terraform"`, `repo`.
2. Set it centrally with `default_tags` (AWS) or an org policy so a resource that omits tags still inherits them:
       provider "aws" { default_tags { tags = local.common_tags } }
3. Reject untagged resources at plan time with a policy tool (Conftest/OPA or Checkov). A tag that is only recommended is a tag that goes missing.
4. Backfill existing resources: tag in code, apply, then confirm the cloud side with a Cost Explorer group-by-tag report.
5. In AWS activate the cost-allocation tag keys in the Billing console (`owner`, `cost_center`); tags not activated do not appear in Cost Explorer.
6. Make `owner` resolve to a real escalation path: a team, not a departed individual. Rotate on reorg.
7. For resources that cannot be tagged (some data-transfer line items), attribute by account or project boundary instead.
8. Alert on untagged spend: query the billing API grouped by tag and flag a growing "no tag" bucket.

## Pitfalls

- Tags set in `default_tags` overridden by a resource's own `tags = {}`, which replaces rather than merges in some providers.
- `owner = "jay"` on an account that outlives Jay's tenure.
- Cost-allocation tags defined in code but never activated in Billing, so the report is empty.
- Tagging EC2 and forgetting the load balancers, NAT gateways, and EBS volumes that dominate the bill.
- A tag policy scoped to new resources only, leaving a decade of untagged spend in the "no tag" bucket.

- Enforcing the tag policy in one account while the org has several, so resources in the others stay untagged.
- Renaming a tag key mid-year (`cost_center` to `cost_centre`), splitting attribution across two keys.

## Verification

    aws resourcegroupstaggingapi get-resources --tag-filters Key=owner,Values='' | jq '.ResourceTagMappingList | length'
    aws ce get-cost-and-usage --group-by Type=TAG,Key=owner --metrics UnblendedCost \
      --time-period Start=2026-09-01,End=2026-10-01

Report: the tag schema, the policy enforcement point, and the share of spend now attributed to a tag.
