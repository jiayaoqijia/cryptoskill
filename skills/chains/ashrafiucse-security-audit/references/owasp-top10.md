# OWASP Top 10 Coverage Matrix

Walk this table in Phase 2 as a **completeness gate**. For every category with
project surface but no recorded findings, either scan it or write "not assessed"
in the report — never skip silently. Ratings are honest; thin areas are
improvement targets (see repo `COVERAGE.md`).

| # | Category (OWASP 2021) | Primary skill(s) | Key checks | Coverage |
|---|---|---|---|---|
| A01 | Broken Access Control | auth-review | IDOR, missing authz middleware, horizontal/vertical escalation | strong |
| A02 | Cryptographic Failures | crypto-review, secrets-detection | weak hashes/ciphers, static IVs, hardcoded keys, TLS verify off | strong |
| A03 | Injection | injection-flaws | SQLi, XSS, command, path traversal, SSTI, deserialization, LDAP/XPath | strong (Node/Python/Java); see `../injection-flaws/references/frameworks.md` |
| A04 | Insecure Design | security-audit (design pass) | missing rate limits, business-logic abuse, trust boundaries | thin — manual prompts below |
| A05 | Security Misconfiguration | config-hardening, container-iac-security | headers, CORS, debug, CI/CD, Docker/K8s/Terraform | strong |
| A06 | Vulnerable & Outdated Components | dependency-vulns, cve-research | live OSV scan, lockfile hygiene, KEV | strong (live data) |
| A07 | Identification & Auth Failures | auth-review | password storage, sessions, JWT, OAuth, MFA, enumeration | strong |
| A08 | Software & Data Integrity Failures | injection-flaws, config-hardening | unsafe deserialization, CI supply chain, curl\|sh, unpinned actions | partial |
| A09 | Logging & Monitoring Failures | data-exposure | audit events, log forging (CWE-117), verbosity, monitoring hooks | partial — see `../data-exposure/references/logging-a09.md`; minimum bar below |
| A10 | SSRF | injection-flaws | user-controlled URLs, cloud metadata, redirect bypass | partial (no egress-config review) |

## A04 design pass (run when the table shows no code-level findings for it)

Reason through and record as design-level findings (usually Medium):

- Which state-changing endpoints lack rate limiting or idempotency keys?
- Where does the app trust client-controlled values for price, quantity, discount, or permissions?
- What happens on: negative quantity, replayed webhook, double-submit, race between check and use?

## A09 minimum bar

- Are login success/failure, password change, permission change, and admin actions logged with actor + timestamp?
- Is user input embedded in logs without sanitization? → log forging (CWE-117)
- Do error logs carry enough context to investigate, without secrets? (see `../data-exposure/SKILL.md`)
