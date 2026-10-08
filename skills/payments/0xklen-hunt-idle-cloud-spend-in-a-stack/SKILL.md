---
name: hunt-idle-cloud-spend-in-a-stack
description: Use when a stack's bill exceeds its workload. Finds unattached volumes, orphaned IPs, empty load balancers and stopped-instance storage, and routes each to delete, codify, or right-size.
---

# Hunt idle cloud spend in a stack

Most runaway bills are not scale; they are idle resources: unattached volumes, unassociated elastic IPs, empty load balancers, and stopped instances still paying for disks.

## Procedure

1. List unattached EBS volumes (billed per GB, no attachment):
       aws ec2 describe-volumes --filters Name=status,Values=available \
         --query 'Volumes[].{id:VolumeId,size:Size,type:VolumeType,created:CreateTime}'
2. List unassociated Elastic IPs (billed when detached on older accounts):
       aws ec2 describe-addresses --query 'Addresses[?AssociationId==null].[PublicIp,AllocationId]'
3. Find load balancers with no healthy targets:
       aws elbv2 describe-target-health --target-group-arn <arn> | jq '[.TargetHealthDescriptions[]|select(.TargetHealth.State!="healthy")]|length'
4. Check stopped instances: the instance is free, its EBS volumes and attached public IP are not.
5. Find orphaned NAT gateways and old snapshots; NAT is frequently the top surprise line:
       aws ec2 describe-nat-gateways --query 'NatGateways[?State==`available`].NatGatewayId'
6. For each idle resource decide: delete (nobody owns it), codify (needed but not in Terraform), or right-size.
7. Add a monthly report grouped by tag and resource type; a one-off sweep regrows within a quarter.
8. Before deleting, check nothing references it: describe-tags for owner and search the repo for the ID.

## Pitfalls

- Deleting an unattached volume that is the only backup of a failed instance.
- Confusing a low-utilisation instance with an idle one: a monthly batch job looks idle 29 days a month.
- An unassociated Elastic IP reserved for a failover path, so deleting it breaks the DR plan.
- Ignoring data-transfer and NAT costs while chasing instance spend, and cutting the wrong thing.
- Sweeping once and declaring victory; idle resources reappear with every abandoned experiment.

## Verification

    aws ce get-cost-and-usage --metrics UnblendedCost --granularity MONTHLY \
      --group-by Type=DIMENSION,Key=USAGE_TYPE --time-period Start=2026-09-01,End=2026-10-01 \
      | jq '.ResultsByTime[].Groups[] | {k:.Keys[0],c:.Metrics.UnblendedCost.Amount}'

Report: each idle resource, its monthly cost, the decision (delete/codify/right-size), and the bill trend after the sweep.
