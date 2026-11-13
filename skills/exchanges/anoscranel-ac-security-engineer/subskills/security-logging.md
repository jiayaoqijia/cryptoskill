---
name: security-logging
domain: security-hardening/security-logging
trigger: Deciding which security events to record, where they live, how long they are kept, and which should page someone.
anti_trigger: Privacy duties over personal data (subskills/privacy-data.md); the first hour of a live breach (subskills/security-incident.md).
scope: What to log, what never to log, audit trails, alerts
status: seedling
---

# Security Logging

## Standard

- **OWASP Logging Cheat Sheet** — always log: input validation failures; authentication successes and failures; authorization failures; session-management failures; application errors; start-ups/shut-downs; higher-risk functionality (privilege changes, break-glass use, sensitive-data and key access, object create/delete, uploads); suspicious business-logic activity (out-of-order actions, bypasses, exceeding limits).
- Never log (remove, mask, hash or encrypt): source code; **session IDs**; **access tokens**; PII; passwords; connection strings; **encryption keys and primary secrets**; payment data; anything classified above the store.
- **CIS Control 8**: 8.9 centralise into an append-only repository — an attacker with admin rights can wipe local logs; **8.10 retain ≥90 days** (https://www.cisecurity.org/controls/audit-log-management). ASVS 5.0 **V16** verifies it.
- IBM 2025: average breach lifecycle 241 days — 30 days of logs means the evidence of entry is gone before you learn of the breach.

## Decision rules

1. The replay test: if a field could authenticate (token, session ID, password), identify a person (PII), or breach a customer (secret), it does not belong in the log.
2. One JSON object per line (JSONL), UTC, shipped to a store in a **different trust domain** from the app host; local files are convenience, never the record. Store the actor as a salted hash — useful for correlation, useless as a PII trove.
4. Retention ≥90 days (CIS 8.10); extend toward 2 years if a regulator may ask for populations, not samples (⚠️ CIRCIA draft duty, secondary).
5. Every alert names its first action or it is noise; a few high-signal alerts beat a dashboard nobody reads.
6. Tamper evidence: read-only storage, versioning on, and log access itself logged (OWASP).

## Procedure

1. Emit one schema for all security events: `{"ts","app","event","actor","action","object","result","reason","src_ip","req_id","severity"}`, e.g. `{"ts":"...Z","app":"billing","event":"auth.login","actor":"u_h:9f2c…","action":"login","object":"account:acct_88","result":"failure","reason":"bad_password","src_ip":"203.0.113.7","severity":"warn"}`.
2. Log the OWASP categories at the security boundary (auth middleware, authorization check, admin route).
3. Ship to a central store with a write-only credential in a separate account, ≥90-day retention, versioning on.
4. Configure alerts, each with a written first action: auth anomaly (new country/ASN, new MFA device, failed-login spike → revoke, force re-auth); privilege change (verify or revert); error spike (5xx × baseline → check for exploit); spend; cert expiry; scanner hit (rotate).
5. Wire the spend detector: a cloud cost spike is the cheapest real detector for a compromised key — budget alert for the ceiling, anomaly detection for the shape (latency up to 24h, so the cap guards).
6. Alert on log-store deletes, retention changes, or event-stream gaps; review monthly — an alert firing weekly without action gets fixed or deleted.

## Anti-patterns

- Logging full request/response bodies "for debugging" — they carry tokens and PII.
- Alerts with no first action; 30-day retention against a 241-day average breach lifecycle.

## Done checklist

- [ ] All OWASP "always log" categories wired at the security boundary; excluded list enforced (no tokens, session IDs, PII, secrets).
- [ ] JSONL schema in use; actor hashed; UTC timestamps.
- [ ] Central append-only store, separate trust domain, ≥90-day retention; each alert has a written first action and one destination.
- [ ] Spend detector + budget cap armed; tamper and gap alerts armed.

## Sources

- Primary: OWASP Logging Cheat Sheet; CIS 8.9/8.10 (cisecurity.org); ASVS 5.0 V16; OWASP Top 10 A09:2025; IBM Cost of a Data Breach 2025; CIRCIA retention (⚠️ secondary).
- <https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html>
- <https://csrc.nist.gov/pubs/sp/800/92/final>
