---
name: rotate-and-scope-api-keys
description: Use when provisioning credentials for an integration. Grant the narrowest scope, store the key in a secret manager, rotate on a schedule, and revoke the old key — broad non-expiring keys are the default failure.
---

# Rotate and scope API keys

A single admin key with no expiry, pasted into an environment file, is the credential that ends
up in a public repo. Provision narrowly, store centrally, rotate, and revoke.

## Procedure

1. Read the provider's scope model and grant only what each job needs (read-only where possible).
2. Create a distinct key per service and environment; never share one across prod and dev.
3. Store in a secret manager (`aws secretsmanager get-secret-value`, Vault, SOPS), not in committed `.env` or code.
4. Set an expiry/rotation cadence and automate rotation with an overlap window where both keys work.
5. Revoke the old key after the new one is confirmed, then prove the old key now fails:
   ```bash
   curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $OLD" "$API/v1/me"   # expect 401
   ```
6. Log which key id made which call so a leaked key can be traced.
7. Alert before expiry so rotation is not a surprise outage.

## Pitfalls

- Keys pasted into source, CI logs, or chat leak on the first push; assume compromise and rotate.
- An admin-scoped key on a read-only job violates least privilege.
- Rotating with no overlap window breaks consumers at the switch instant.
- Some providers display a key only once at creation; losing it forces a recreate, so store immediately.
- Unused keys linger; audit and revoke anything with no calls in 90 days.

## Verification

    curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $OLD" "$API/v1/me"   # 401
    curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $NEW" "$API/v1/me"   # 200
    curl -s -H "Authorization: Bearer $NEW" "$API/v1/scopes" | jq .    # narrow scope list

Report: "Rotated key id k-92; old revoked (401), new active (200), scopes items:read."
