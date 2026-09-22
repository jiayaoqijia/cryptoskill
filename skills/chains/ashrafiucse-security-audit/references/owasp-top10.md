# OWASP Top 10 Coverage Matrix

Walk this table in Phase 2 as a **completeness gate**. For every category with
project surface but no recorded findings, either scan it or write "not assessed"
in the report — never skip silently. Ratings are honest; thin areas are
improvement targets (see repo `COVERAGE.md`).

| # | Category (OWASP 2021) | Primary skill(s) | Key checks | Coverage |
|---|---|---|---|---|
| A01 | Broken Access Control | auth-review | IDOR, missing authz middleware, horizontal/vertical escalation, trusted-header spoofing, realtime (WebSocket/SSE) authz, TOCTOU races, mass assignment | strong |
| A02 | Cryptographic Failures | crypto-review, secrets-detection | weak hashes/ciphers, static IVs, hardcoded keys, TLS verify off | strong |
| A03 | Injection | injection-flaws | SQLi, XSS, command, path traversal, SSTI, deserialization, LDAP/XPath, XXE, prototype pollution, open redirect, ReDoS | strong (Node/Python/Java); see `../injection-flaws/references/frameworks.md` |
| A04 | Insecure Design | security-audit (design pass) | missing rate limits, business-logic abuse, trust boundaries, replay/idempotency, negative values, step-skipping | good — grep-anchored checklist below (judgment still required) |
| A05 | Security Misconfiguration | config-hardening, container-iac-security | headers, CORS, debug, CI/CD, Docker/K8s/Terraform | strong |
| A06 | Vulnerable & Outdated Components | dependency-vulns, cve-research | live OSV scan, lockfile hygiene, KEV | strong (live data) |
| A07 | Identification & Auth Failures | auth-review | password storage, sessions, JWT, OAuth, MFA, enumeration | strong |
| A08 | Software & Data Integrity Failures | injection-flaws, config-hardening, dependency-vulns | unsafe deserialization, CI supply chain, curl\|sh, unpinned actions, dependency confusion, typosquats | strong (hygiene pack in dependency-vulns Step 2.5) |
| A09 | Logging & Monitoring Failures | data-exposure | audit events, log forging (CWE-117), verbosity, monitoring hooks | partial — see `../data-exposure/references/logging-a09.md`; minimum bar below |
| A10 | SSRF | injection-flaws | user-controlled URLs, cloud metadata, redirect bypass, egress-config review (NetworkPolicy, IMDSv2) | strong |

## A04 design pass (run when the table shows no code-level findings for it)

**AI/LLM stacks**: walk `../llm-security/SKILL.md` additionally — OWASP LLM
Top 10 issues (prompt injection, excessive agency, insecure output handling)
fall outside this 2021 table; the LLM skill is the completeness gate for them.

Work the checklist; each item has a grep to find candidates, then reason about the abuse case. Record as design-level findings (usually Medium):

| Abuse case | Grep for candidates | Ask |
|---|---|---|
| Client-controlled money/scope | `rg -n -i "(price|amount|total|discount|quantity|credits|role|is_admin|plan)"` in request mappings/DTOs | does the server derive it, or trust the client's copy? |
| Replay / double-submit | `rg -n "idempotency|Idempotency-Key|dedup"` (absence is the signal) | what happens if the same webhook/order/payment message arrives twice? |
| Check-then-use races | see TOCTOU greps in `../auth-review/SKILL.md` | can two concurrent requests both pass the check? |
| Negative/overflow values | `rg -n "quantity|amount" ` then check validators | negative quantity, 0, INT_MAX, float rounding on refunds? |
| Step-skipping | route census table (auth-review §1) | can checkout/privilege steps be called out of order? |

## A09 minimum bar

- Are login success/failure, password change, permission change, and admin actions logged with actor + timestamp?
- Is user input embedded in logs without sanitization? → log forging (CWE-117)
- Do error logs carry enough context to investigate, without secrets? (see `../data-exposure/SKILL.md`)
