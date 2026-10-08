---
name: detect-orphaned-resources-outside-state
description: Use when live resources may exist that no state file tracks. Cross-checks the cloud inventory against state so untracked resources, their cost and risk, are surfaced.
---

# Detect orphaned resources outside state

Resources created by hand or left by a deleted stack persist and bill while no code claims them. Detect them by diffing the cloud inventory against state.

## Procedure

1. Export tracked IDs from state:
       terraform state list | xargs -I{} terraform state show {} | grep -E '^\s+id\s+=' | awk '{print $3}' | sort -u > tracked.txt
2. Export live IDs for the resource types you manage:
       aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' --output text | tr '\t' '\n' | sort -u > live.txt
3. Diff to find untracked resources (present in cloud, absent from state):
       comm -13 tracked.txt live.txt
4. Repeat per resource type; IDs are only meaningful within a type, so scope the diff (EC2 instance IDs vs volume IDs).
5. Classify each orphan: adopt (import + code), delete (nobody owns it), or quarantine (unknown owner, tag and alarm).
6. Prefer cloud-native inventory for breadth: AWS Config `list-discovered-resources`, GCP Asset Inventory, Azure Resource Graph.
7. Run monthly, not once; manual creations and deleted stacks both produce orphans continuously.
8. Alert on new orphans in a shared account so each gets an owner within a week.

## Pitfalls

- Diffing IDs across mismatched types, producing a page of false positives.
- Adopting an orphan whose real owner uses it out of band, then destroying it in a later plan.
- A provider id attribute in a different format than the API returns (case, prefix), so a tracked resource looks orphaned.
- Imports tracked in a different workspace appear as "cloud, not state" from this one.
- Deleting an orphan that is actually a required shared resource (a peering connection, a DNS zone) with no code.

- `terraform state show` failing on a resource with sensitive attributes, so the tracked list is silently incomplete.
- A resource shared across two states appears tracked in one and orphaned in the other's diff.

## Verification

    comm -13 tracked.txt live.txt | wc -l   # count of untracked resources
    terraform state list | wc -l            # count tracked

Report: orphan counts by type, the decision per orphan (adopt/delete/quarantine), and the resulting change in the diff.
