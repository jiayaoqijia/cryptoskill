---
name: append-only-storage
domain: software-engineering/append-only-storage
trigger: "Choosing storage that the application can write but not rewrite."
anti_trigger: "Not for general log pipeline design, and not for backup policy."
scope: "Write-once storage, the deletion problem, and who can rotate."
status: seedling
---

# Append-only storage

## Standard

The storage under an audit log enforces what the application promises: if the writer's credentials can update or delete, then the chain and the policy are both suggestions. Append-only storage — files opened for append, database accounts with INSERT but not UPDATE or DELETE, or object stores with object-lock retention — makes the no-rewrite promise a property of the system rather than a habit of the code.

Rotation is where the property is usually lost. The same privilege that rotates an old log segment away can overwrite it, and the same tool that tidies storage can silently violate the retention the trail was built for. The record names who can rotate, how the rotated data's integrity is preserved, and what a deletion request does to the chain — because under privacy law the two obligations collide, and the design has to say which wins before a court does.

Primary sources: <https://csrc.nist.gov/pubs/sp/800/92/final> and <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>.

## Decision rules

- Grant the writer insert-only access; updates and deletes live elsewhere or nowhere.
- Record who can rotate or purge, and under what reviewed process.
- Preserve the chain across rotation by carrying the head into the new segment.
- State the deletion policy for audit data and its legal basis before the first request arrives.
- Use storage-level retention controls where the platform offers them.
- Record what happens to the chain's verification when a segment is lawfully removed.

## Procedure

1. Choose the storage and verify the writer's credentials cannot update or delete.
2. Document the rotation process and who holds the right to run it.
3. Carry the chain head across rotation boundaries.
4. Decide the deletion-and-retention policy with the accountable officer.
5. Where applicable enable storage-level object lock or retention.
6. Record privileges, rotation process, and deletion policy.

## Anti-patterns

- Audit tables in the same database account as the application, with UPDATE rights.
- Silent log cleanup by a storage housekeeping job.
- Rotation that resets the chain, discarding continuity.
- Deletion policy decided when the first legal request arrives.
- Naming it immutable while the credentials can rewrite it.

## Done checklist

- [ ] Credentials verified insert-only.
- [ ] Rotation process and privilege holders recorded.
- [ ] Chain head carried across rotation.
- [ ] Deletion and retention policy decided and recorded.
- [ ] Storage-level retention enabled where possible.
- [ ] Privileges and policy in the audit record.

## Sources

- Log storage and protection guidance: <https://csrc.nist.gov/pubs/sp/800/92/final>
- Audit-log control expectations: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- Append-only log structure and verification: <https://www.rfc-editor.org/rfc/rfc6962.html>
