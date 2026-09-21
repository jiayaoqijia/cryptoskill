---
name: data-exposure
description: Finds sensitive data exposure risks — PII/secrets written to logs, over-returning API responses, data at rest without encryption, sensitive data in URLs, test fixtures with real data, secrets in git history, and temporary/backup file leaks. Use when auditing how a project handles, stores, logs, or transmits sensitive data.
license: MIT
---

# Data Exposure Review

## 1 — Map sensitive data

From recon, identify what the project considers sensitive: PII (names, emails, phones, addresses), auth data (tokens, passwords, SSNs, card numbers), health/financial records, internal identifiers. Check models/schemas/DTOs for field names to build this list before grepping flows.

## 2 — Logs

```bash
rg -n "console\.(log|error|info)|logger\.(info|warn|error)|logging\.|print\(" | rg -i "password|token|secret|ssn|card|authorization|api.?key|session"
```
- Tokens/passwords/full PII logged → HIGH (logs ship to aggregators with broader access and longer retention than the DB)
- Full request/response bodies logged (debug middleware like morgan `dev`+body, axios interceptors logging config) → HIGH if auth flows pass through
- Stack traces with SQL → MEDIUM
- Recommend structured logging with field-level redaction/allowlists.
- Deep A09 checks (audit-event coverage, log forging, verbosity, monitoring): `references/logging-a09.md`.

## 3 — API responses

```bash
rg -n "res\.(json|send)\(|JSONResponse|serializer|to_json|to_dict|as_dict|@JsonProperty"
```
- Endpoints returning full ORM objects (`res.json(user)` instead of a DTO) → HIGH when the model has password hashes, tokens, reset codes, or PII beyond need — even if "unused today"
- `to_json`/`__dict__` serialization on models with sensitive fields → same
- Over-returning list endpoints (100+ records/page without pagination) → LOW
- IDs that are sequential integers for sensitive objects → LOW/MEDIUM (enumeration, see `../auth-review/SKILL.md`)

## 4 — Data at rest & in transit

- DB files / SQLite in repo or mounted volumes without encryption → MEDIUM (judged by data class)
- Backups/exports (`dump.sql`, `*.csv` exports) committed → HIGH if real data, LOW if synthetic
- Sensitive data in URLs (GET query params: `?token=`, `?email=`, `?ssn=`) → HIGH (URLs hit logs, proxies, browser history, referrers)
- Internal service calls over plain HTTP inside the cluster → MEDIUM
- Sensitive data sent to third parties (analytics/error trackers capture request bodies: Sentry `send_default_pii`, loggers to SaaS) → MEDIUM/HIGH

## 5 — Files, history, fixtures

```bash
git ls-files | rg -i '\.(sql|csv|xlsx?|dump|bak|sqlite3?|db)$'
rg -n -i "lorem|john.?doe|test@test|555-|4111 ?1111 ?1111 ?1111|0000-0000" tests/ fixtures/ 2>/dev/null | head -20
```
- Real-looking PII in fixtures/tests (real emails, real card numbers beyond obvious test patterns) → MEDIUM
- Git history secrets — already covered by `../secrets-detection/SKILL.md`; here verify large data files aren't in history: `git rev-list --objects --all | head` + look for big blobs
- Temp files written to shared/world-readable locations, `/tmp` with predictable names → MEDIUM
- `TODO`/`FIXME` near data handling mentioning "encrypt"/"hash later" → report as confirmation of known debt

## 6 — Compliance overlays (optional, if project context implies)

If the stack/domain implies a regime, add a short mapping section: GDPR (lawful basis hints, right-to-erasure reachability of PII), HIPAA (PHI at rest/in transit), PCI-DSS (card data scope). Keep it a checklist of "likely gaps" — not legal advice — and recommend expert review.

## Reporting

Per finding: data class involved, where it's exposed (`file:line`), exposure path (logs/response/history), severity by data class, and the fix (redact, DTO-allowlist, encrypt, purge). Include a one-paragraph "sensitive data inventory" summary — teams usually don't have one and it's instantly useful.
