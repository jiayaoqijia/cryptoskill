---
name: ac-privacy-engineering
description: "Building systems that hold personal data to a standard you can evidence: data inventory and purpose mapping, minimisation and the cost of collecting, retention schedules and the deletion that actually propagates, subject access and erasure request handling, pseudonymisation versus anonymisation, encryption and key management for stored data, third-party and subprocessor flows, and the written privacy record. Use when asking \"data retention\", \"right to be forgotten\", \"subject access request\", \"GDPR engineering\", \"anonymisation\", \"pseudonymisation\", \"data minimisation\", \"where is personal data stored\", \"DPIA\", \"data residency\". Not for application security controls (ac-security-engineer), not for regulatory standards catalogues (ac-security-standards), not for legal advice on compliance obligations."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Privacy engineering

## Overview

Privacy engineering is the discipline of knowing where personal data is, why it is there, and how it leaves. The hard part is not the policy document; it is that personal data spreads: into logs, caches, backups, analytics, support tickets, and third-party services, and each copy has to be found before a deletion request can honestly be answered.

This skill covers the engineering that makes those promises true: an inventory that is maintained rather than assembled under pressure, minimisation that treats collection as a cost, retention that deletes on a schedule rather than on request, deletion that propagates to derived stores, the distinction between pseudonymisation and anonymisation, encryption and key management for data at rest, and the flow to subprocessors. Application security and legal obligations belong to other skills.

Primary sources: <https://ico.org.uk/> and <https://www.nist.gov/privacy-framework>.

## When to use

- When designing a system that stores or processes personal data.
- When a retention schedule or deletion mechanism needs implementing.
- When handling a subject access, erasure, or portability request.
- When assessing whether data is genuinely anonymised.

## When NOT to use

- For application security controls and threat modelling (use ac-security-engineer).
- For standards catalogue questions (use ac-security-standards).
- For legal interpretation of obligations (consult a professional; this is engineering).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/data-inventory-and-purpose.md` | `software-engineering/data-inventory-and-purpose` | What personal data exists, where, and why each field is collected. |
| `subskills/minimisation-and-collection.md` | `software-engineering/minimisation-and-collection` | Collection as a cost, and the fields that should not exist. |
| `subskills/retention-and-deletion.md` | `software-engineering/retention-and-deletion` | Retention schedules, and deletion that reaches derived stores. |
| `subskills/subject-requests.md` | `software-engineering/subject-requests` | Access, erasure, and portability requests as an engineering workflow. |
| `subskills/pseudonymisation-and-anonymisation.md` | `software-engineering/pseudonymisation-and-anonymisation` | Reversible identifiers versus data that cannot be re-identified. |
| `subskills/encryption-and-keys.md` | `software-engineering/encryption-and-keys` | Encryption at rest, key custody, and rotation that does not break data. |
| `subskills/privacy-record.md` | `software-engineering/privacy-record` | The written record: inventory, retention, subprocessors, and gaps. |

## Status and honest limits

Anonymisation claims are fragile and frequently overstated: datasets that look anonymous can be re-identified by joining against another source, and the risk changes as more data becomes available. Nothing here constitutes legal advice, and the specific obligations depend on jurisdiction and on the data's sensitivity. This skill describes engineering practice; a determination of whether a dataset is personal data belongs with a qualified adviser, and the record should say which questions were left to one.
