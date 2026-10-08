---
name: attribute-a-cloud-change-to-its-actor
description: Use when a resource changed and you need to know who or what did it. Uses cloud audit logs to attribute the change before blaming code or reverting blindly.
---

# Attribute a cloud change to its actor

Before reverting a surprising change, find out who made it. Audit logs distinguish a console edit, a Terraform apply, and an automation from a security event.

## Procedure

1. Query the audit log for the resource around the change window:
       aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=acme-sg \
         --start-time 2026-10-01T00:00:00Z --end-time 2026-10-08T00:00:00Z \
         --query 'Events[].[EventTime,EventName,Username]'
2. Read `userIdentity`: `type=AssumedRole` with a session name like `terraform-ci` means an apply; `type=IAMUser` on a console session means a human.
3. Check the principal and source IP: an unexpected IP or an access key you do not recognise is a security incident, not config drift.
4. Correlate with the deploy log: find the Terraform run at that timestamp and the commit SHA it applied.
5. If it was a console change, capture before/after from the event and reconcile the code.
6. If it was a Terraform run, check whether it was a `-target`, an import, or a full apply.
7. Preserve evidence: export the events to S3 for retention before the CloudTrail window ages out.
8. Rotate keys or session policies if the actor is unrecognised.

## Pitfalls

- Reverting before attributing, erasing the evidence and possibly undoing a legitimate fix.
- Assuming a change is Terraform because the resource is in state; a console edit also shows in the next plan.
- Reading only the most recent event, missing the earlier IAM policy edit that enabled the change.
- Ignoring `AssumedRole` session names, so `terraform-ci` and a human in a break-glass role look identical.
- Overlapping time zones between the incident report and CloudTrail UTC, missing the event by hours.

- An account with CloudTrail data events off, so the specific API call on the resource is missing and only management events remain.
- Reading `Username` for an AssumedRole, which shows the role, not the session name that identifies the caller.

## Verification

    aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=acme-sg \
      --query 'Events[].[EventTime,EventName,Username]' --output table

Report: the event time, the acting principal and type, the source IP, and the correlation to a commit or a console action.
