---
name: encryption-and-keys
domain: software-engineering/encryption-and-keys
trigger: "Encrypting stored personal data and managing the keys that protect it."
anti_trigger: "Not for application security review, and not for protocol design."
scope: "Encryption at rest, key custody, and rotation that does not break data."
status: seedling
---

# Encryption and keys

## Standard

Encrypting data at rest protects it against one threat: someone who obtains the storage without obtaining the key. That is a real threat and a valuable protection, but it is not a general answer to data exposure, because the application that must read the data also has access to the key, and an attacker who reaches the application reads plaintext.

The engineering that matters is therefore key custody and rotation. A key held in the application's configuration and shared across environments is a key that cannot be rotated without an outage and cannot be scoped to a tenant. A key held in a managed service with per-tenant keys, versioned, and rotated on a schedule is one that can be revoked for a single tenant without touching the others.

Primary sources: <https://www.nist.gov/> and <https://csrc.nist.gov/>.

## Decision rules

- Record what is encrypted, at which layer, and against which threat.
- Record the key custody: where the key lives and who can retrieve it.
- Record the key scope: global, per-environment, per-tenant, or per-record.
- Record the rotation schedule and the re-encryption path for existing data.
- Record the revocation path: what happens to data when a key is destroyed.
- Record the fields that are searched or sorted, since encryption affects those operations.

## Procedure

1. Record the encrypted fields and the layer that encrypts them.
2. Record key custody and the retrieval authority.
3. Choose the key scope and record the reason.
4. Record rotation and the re-encryption procedure.
5. Record the revocation path and its effect.
6. Record the operations that encryption breaks and their mitigation.

## Anti-patterns

- Encrypting at rest and treating the data as protected from the application.
- One key shared across environments and tenants.
- No rotation path because rotation would require downtime.
- Encrypting a field that must be searched without a plan for the search.
- Assuming key destruction is instant across backups and replicas.

## Done checklist

- [ ] Encrypted fields and layers recorded.
- [ ] Key custody recorded.
- [ ] Key scope recorded.
- [ ] Rotation and re-encryption recorded.
- [ ] Revocation path recorded.
- [ ] Broken operations recorded with mitigation.

The threat model sentence is worth writing literally: encryption at rest addresses storage media leaving the perimeter, and it does not address an attacker with application credentials, a misconfigured access policy, or an insider. Stating what it does not cover prevents the false confidence that a compliance checklist rewards.


## Sources

- Cryptographic standards and guidance: <https://csrc.nist.gov/>
- Key management recommendations: <https://www.nist.gov/>
- Web cryptography standards: <https://www.w3.org/>
