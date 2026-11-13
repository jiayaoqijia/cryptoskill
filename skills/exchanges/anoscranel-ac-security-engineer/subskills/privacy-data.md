---
name: privacy-data
domain: security-hardening/privacy-data
trigger: Deciding what personal data to collect, how long it may live, how a deletion or access request is served, whether a DPIA is owed.
anti_trigger: Log content rules (subskills/security-logging.md); breach clock mechanics (subskills/security-incident.md).
scope: GDPR/DPDP data minimisation, retention, DSARs, DPIA trigger
status: seedling
---

# Privacy & Data Handling

## Standard

- You are a **controller** the moment you decide why and how personal data is processed — GDPR has no revenue floor. Art. 4(1) reads personal data broadly (any information relating to an identifiable person); Art. 9 adds stricter rules for special categories.
- NIST SP 800-122 defines PII as information that distinguishes or traces an identity, or is linkable to one — you cannot protect data you do not know you hold (https://csrc.nist.gov/pubs/sp/800/122/final).
- India DPDP Rules 2025 (notified 13 Nov 2025): Rule 7 breach intimation to affected principals **without delay**, to the Board initial without delay then a **detailed report within 72 hours**; Rule 7 commences **13 May 2027** (⚠️ some advisers count 14 May).

## Decision rules

1. Collect only what a shipped feature consumes; data without a named purpose is deletion cost with no benefit.
2. Classify before building — four tiers (synthesis, ⚠️ not a standard): Public (no controls) · Internal (access control) · Personal — emails, names, IPs, IDs (access control, retention limit) · Sensitive — Art. 9, financial, credentials (encrypt, minimise hardest).
3. Retention is decided at collection, not later: every Personal/Sensitive element gets a period and an automated deletion job.
4. Encryption buys a safe harbour (most US state laws exempt encrypted data) but not immunity: disk encryption does not stop a compromised application or a leaked credential.
5. DPIA when processing is high-risk under Art. 35: systematic monitoring, large-scale special-category data, or evaluation/scoring of people.
6. Lawful basis and controller status are legal calls — a lawyer signs them.

## Procedure

1. Build one **data map** before writing schema: each element → where it lives (table/column, log, backup, third party) → purpose → lawful basis → retention → tier. It drives DSARs, deletion, retention jobs, and breach scoping.
2. Set retention per element; wire the deletion job the same week.
3. Wire the DSAR path: export everything held about one identifier, delete on request, prove both; test before a request arrives. ⚠️ Production deletion is **human-gated** — propose exact scope and record count; a human runs it.
4. Minimise at the edges: hash or truncate IPs in analytics, drop unused fields, keep PII out of logs (`subskills/security-logging.md`).
5. For processors, use vendors with SCC/DPF coverage; check Art. 28 clauses; record the transfer basis in the data map.
6. If a DPIA triggers, write purpose, necessity, risks, mitigations before launch.

## Anti-patterns

- "Collect everything now, decide retention later" — or analytics SDKs receiving full user records by default.
- Deletion that removes the primary row but leaves backup, log, and warehouse copies.
- Assuming a provider's consumer tier trains on nothing (consumer and API tiers differ).

## Done checklist

- [ ] Data map covers tables, logs, backups, third parties.
- [ ] Retention period + deletion job per Personal/Sensitive element; DSAR export and deletion tested end-to-end.
- [ ] No PII in logs; analytics minimised; processors under contract, transfer basis recorded.
- [ ] DPIA written where Art. 35 triggers; legal basis calls signed by a lawyer.

## Sources

- Primary: GDPR (EUR-Lex, Reg. (EU) 2016/679) Arts. 4, 9, 25, 28, 30, 35; NIST SP 800-122; DPDP Rules 2025 (⚠️ commencement from KPMG/dsci summaries).
- <https://csrc.nist.gov/privacy-framework>
- <https://owasp.org/www-project-application-security-verification-standard/>
