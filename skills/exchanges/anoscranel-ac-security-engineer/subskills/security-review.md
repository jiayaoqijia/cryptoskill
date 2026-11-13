---
name: security-review
domain: security-hardening/security-review
trigger: A change is ready to merge and someone must read the diff for security — the pre-merge pass against the verification target.
anti_trigger: Choosing the verification target or level (subskills/verification-level.md); running automated scanners in CI (subskills/security-testing.md).
scope: Pre-merge security review of a diff, ASVS-mapped
status: seedling
---

# Security Review

## Standard

- The review checks one diff against the target in `subskills/verification-level.md` — ASVS 5.0 chapters: **V1** Encoding & Sanitization · **V2** Validation · **V3** Web Frontend · **V4** API · **V6/V7** Authentication · **V8** Authorization · **V11** Cryptography · **V13** Configuration · **V16** Logging & Errors. L1 baseline; L2 for personal or payment data.
- OWASP Top 10:2025 is the quick-pass frame (A01 access control, SSRF folded in · A02 misconfiguration · A03 supply chain · A04 crypto · A05 injection · A06 design · A07 authentication · A08 integrity · A09 logging · A10 exceptional conditions).
- CISA's FY2024–25 review: **41.5% of KEV entries map to "stubborn" weakness classes** — led by input validation (CWE-20), path traversal (CWE-22), command injection (CWE-78). Ranking ≠ exploitation: CWE-79 XSS tops the Top 25 while trailing on KEV.

## Decision rules

1. Read the diff, not the file: risk lives in what the change touches — new input paths, data exposure, trust crossings.
2. Exploited classes first: input validation and canonicalisation, path traversal, command injection, access control.
3. Every finding gets a severity in *this* product's context, an owner, a ticket; unowned findings decay into advisory posture.
4. Blockers: the exploited classes plus anything touching auth, authorization, crypto, secrets, or data exposure; style is a comment.

## Procedure

1. Name the ASVS chapters exercised (auth endpoint → V6/V7/V8; data export → V1/V16; new dependency → A03).
2. Walk the diff: **input** (allow-list validation, canonicalise once, reject unknown fields) → **output** (context-correct encoding at every sink; no `dangerouslySetInnerHTML`-class APIs on untrusted data) → **interpreters** (parameterised queries, list-form OS calls — `subskills/injection.md`) → **access control** (ownership check per ID access, deny by default — `subskills/authorization.md`) → **secrets and crypto** (`subskills/secrets.md`, `subskills/crypto-use.md`) → **config and errors** (secure defaults, no debug in prod, generic errors, fail closed — a `try/except` swallowing a permission error is CWE-636) → **logging** (no tokens, session IDs, PII or secrets in lines — `subskills/security-logging.md`).
3. For machine-generated portions: secrets scan on history; registry-existence + pin on suggested dependencies; out-of-scope edits (lockfiles, CI config) reviewed — the top failure mode; a named human owner (OWASP Secure Coding with AI).
4. Run the tests covering the fixes, not just the suite; a diff fixing one injection while adding another is common.
5. Record: chapters exercised, findings with severity/owner/ticket, justified exceptions — the record is the audit sample.
6. Re-review after fixes against the same checklist; never trust "addressed" without the diff.

## Anti-patterns

- Reviewing only changed lines and never the blast radius (new route, job, dependency).
- Findings as comments nobody tracks; approving because CI is green and the diff is small.
- The author self-reviewing AI-generated code alone.

## Done checklist

- [ ] ASVS chapters for the change identified; each exercised chapter walked.
- [ ] Exploited classes checked first: input validation, path traversal, command injection, access control.
- [ ] No secrets, tokens, or PII added to logs; error paths fail closed.
- [ ] AI-generated portions passed the four-step gate.
- [ ] Findings carry severity, owner, ticket; re-review done after fixes.

## Sources

- Primary: OWASP Top 10:2025; ASVS 5.0.0; OWASP Secure Coding with AI; CWE Top 25 2025 + KEV; CISA FY2024–25 review; arXiv:2607.00107 (⚠️).
- <https://owasp.org/www-project-application-security-verification-standard/>
- <https://shostack.org>
