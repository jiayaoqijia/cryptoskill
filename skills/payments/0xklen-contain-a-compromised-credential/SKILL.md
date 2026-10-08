---
name: contain-a-compromised-credential
description: Use when a token, key or session is suspected leaked — revokes and rotates it, scopes what it can still do, and reconstructs the usage window to bound the damage before rotating the rest.
---

# Contain a compromised credential

A leaked key is not one action but a sequence: stop the access first, then understand what it touched, then rotate without breaking the systems that legitimately depend on it. Acting in the wrong order either leaves the attacker access or blinds you to what they did.

## Procedure

1. Establish the blast radius of the credential *before* revoking: what can it do? List scopes/permissions and every service that presents it.
       aws iam list-access-keys --user-name svc-deploy
       aws iam get-policy-version --policy-arn $ARN --version-id v3 | jq '.PolicyVersion.Document'

2. Stop the access immediately but reversibly: deactivate rather than delete the key, so dependent systems fail fast and visibly instead of silently looping on auth errors:
       aws iam update-access-key --access-key-id AKIA... --status Inactive

3. Preserve the evidence *now* — the usage window is what tells you whether the leak was read-only recon or an active takeover. Export the audit trail before expiry:
       aws cloudtrail lookup-events --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=AKIA... \
         --start-time 2026-01-01 > /tmp/ct.json

4. Hunt for the actions that matter, not all actions: IAM changes, data exfiltration (`s3:GetObject` bursts), new key creation, security-group edits, resource claims. Sort by time to see the pattern:
       jq -r '.Events[].CloudTrailEvent | fromjson | .eventName' /tmp/ct.json | sort | uniq -c | sort -rn

5. Revoke sessions the key could have minted, not just the key: any token or session it signed is still valid until expiry. Rotate the signing key or call the provider's "revoke all sessions" endpoint.

6. Rotation order matters: issue the new credential, deploy it to consumers, confirm green, then delete the old one. Deleting first causes an outage you then have to fix during an incident.

7. Assume lateral movement: rotate anything the compromised credential could reach (same role, same secret store path, tokens it could read), and check for persistence (new IAM users, backdoor keys, webhook endpoints added).

## Pitfalls

- Deleting the key before exporting the audit trail, destroying the only record of what the attacker did.
- Rotating the key but not the sessions/tokens it minted, so the attacker stays in through a token that outlives the key.
- Rotating everything at once, taking down the whole environment and losing the ability to tell compromise from self-inflicted outage.
- Not checking for persistence: a new access key or user created by the attacker re-opens access the moment you rotate the original.

## Verification

    # the revoked credential must now be refused
    AWS_ACCESS_KEY_ID=AKIA... aws sts get-caller-identity   # expect InvalidClientTokenId
    # audit export exists and identifies the actions taken in the window
    jq '.Events | length' /tmp/ct.json
    # confirm no new keys/users created during the window
    aws iam list-users --query 'Users[].CreateDate'

Report: the credential's scope, the audit window and the action histogram, proof the key now fails, and the list of sessions/resources rotated and checked for persistence.
