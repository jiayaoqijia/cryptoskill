---
name: scope-object-permissions-to-least-privilege
description: Use when a bucket or container is shared or public. Audits and rewrites object-store IAM so each principal reads and writes only the prefix it needs, with no wildcard grants.
---

# Scope Object Permissions to Least Privilege

Object stores default to wide grants because broad access "just works" during development. Every bucket you own should answer one question per principal: exactly which prefixes, which actions, under what condition. Anything else is a leak waiting for a scanner.

## Procedure

1. Enumerate access: `aws s3api get-bucket-policy`, `aws s3api get-bucket-acl`, and list every IAM role/user with a matching `Resource: arn:aws:s3:::acme/*` statement.
2. Flag the three dangerous shapes: `Principal: "*"`, `Action: "s3:*"`, and `Resource: ".../*"` with no condition.
3. Check block-public-access first: `aws s3api get-public-access-block --bucket acme` — all four flags should be `true` unless the bucket is a deliberate CDN origin.
4. Rewrite grants per principal to a prefix and an action set: writer role gets `s3:PutObject` on `arn:aws:s3:::acme/uploads/${aws:PrincipalTag/tenant}/*`, never `s3:*` on `acme/*`.
5. Add conditions where they exist: `aws:SecureTransport`, `s3:prefix`, or a VPC endpoint condition.
6. Enable access logging and audit for `GetObject` spikes — a permission that is never used is a candidate for removal.
7. Remove ACL-based grants entirely where the policy can express them; ACLs bypass policy and are the usual source of a surprise public object.
8. Re-scan after the change: a public object should fail `curl -sI https://acme.s3.amazonaws.com/key` with 403.

## Pitfalls

- A `get-bucket-policy` that looks scoped but an object ACL grants `public-read` on one key, which a scanner finds regardless of the policy.
- Blocking public access on a bucket that is meant to serve a static site, breaking the site silently.
- `s3:ListBucket` granted broadly: listing leaks key names and object counts even when reads are scoped.
- Granting the CI role write access to production prefixes so a compromised workflow can overwrite artifacts.
- Forgetting `s3:PutObjectAcl` is implied by `s3:*`, letting a writer re-open public access after you locked it down.
- Using account-level "Block Public Access" off to fix a broken upload, then never restoring it.
- Not applying the same review to the GCS/Azure equivalent, where the policy model and default differ.

## Verification

    aws s3api get-public-access-block --bucket acme
    aws s3api get-bucket-policy --bucket acme | grep -c '"Principal":"\*"'   # expect 0
    curl -sI https://acme.s3.amazonaws.com/some-key | head -n1               # expect 403

All four public-access-block flags are `true`, no statement uses a wildcard principal, and an unauthenticated GET returns 403.

Report: "Audited <N> principals on <bucket>: rewrote <M> grants to prefix-scoped actions; public-access-block all true; anonymous GET returns 403."
