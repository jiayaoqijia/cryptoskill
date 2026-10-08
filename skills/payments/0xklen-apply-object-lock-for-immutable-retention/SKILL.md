---
name: apply-object-lock-for-immutable-retention
description: Use when ransomware or a rogue operator could delete backups. Applies WORM object-lock or legal hold so backups cannot be altered or deleted inside a retention window.
---

# Apply Object Lock for Immutable Retention

An attacker with delete rights owns your backups. Write-once-read-many locking makes objects unchangeable for a fixed window, so the only copy that survives a compromise is one the compromised credentials cannot touch.

## Procedure

1. Decide the failure you are countering: ransomware, disgruntled admin, accidental bulk delete. All require immutability, not just versioning.
2. Object Lock can only be enabled at bucket creation: `aws s3api create-bucket --bucket acme-vault --object-lock-enabled-for-bucket`.
3. Set a default retention so every write is locked without per-object work:
   `aws s3api put-object-lock-configuration --bucket acme-vault --object-lock-configuration '{"ObjectLockEnabled":"Enabled","Rule":{"DefaultRetention":{"Mode":"COMPLIANCE","Days":90}}}'`.
4. Choose the mode deliberately. GOVERNANCE can be overridden with `s3:BypassGovernanceRetention`; COMPLIANCE cannot be shortened by anyone, including root — set the window carefully.
5. For a record under litigation, apply a legal hold instead of or alongside retention; a hold has no expiry and survives until removed.
6. Keep the write credential separate from the delete/read credential, in a different account or role with no retention-bypass permission.
7. Verify a locked object: `aws s3api get-object-retention --bucket acme-vault --key backup.tar` returns the mode and `RetainUntilDate`.
8. Attempt a delete as the backup role and confirm it is refused: `aws s3api delete-object ...` should return `AccessDenied`.

## Pitfalls

- Trying to enable Object Lock after the bucket exists — it cannot be added retroactively; plan the vault bucket upfront.
- COMPLIANCE mode with a too-long window set by mistake; nobody, not even support, can shorten it, so bytes are billed for the full term.
- Relying on GOVERNANCE mode without removing `BypassGovernanceRetention` from the backup role's policy; the lock is then advisory.
- Assuming the lock protects the IAM and KMS paths; a credential that can delete the customer KMS key can still make the data unreadable.
- Forgetting that a legal hold blocks deletion even after retention expires, stalling cleanup until someone removes it.
- Locking the entire bucket including scratch areas you need to rotate, forcing a new bucket and a migration.
- Not replicating the vault to a second account, so a compromised root on the vault account can still act within what the policy allows.

## Verification

    aws s3api get-object-lock-configuration --bucket acme-vault
    aws s3api get-object-retention --bucket acme-vault --key backup.tar
    # deletion as the backup role must fail
    aws s3api delete-object --bucket acme-vault --key backup.tar   # expect AccessDenied

Object Lock is Enabled with the intended mode and term, a sample object reports its `RetainUntilDate`, and deletion by the write role is refused.

Report: "Object Lock COMPLIANCE/90d on <vault>; deletion by backup role returns AccessDenied; lock config id <id>."
