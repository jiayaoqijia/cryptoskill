# Methodology Mirror — WSTG × PortSwigger Academy × OWASP CRG

External methodology catalogs diffed against the skills (2026-09-23, category
level). Purpose: no category of real-world testing exists that our skills
silently ignore — every row is owned, a documented gap, or runtime-only.

## WSTG v4 categories (from the authoritative OWASP/WSTG repo) → owning skill

| WSTG category | Owning skill | Status |
|---|---|---|
| 4.1 Information Gathering | security-audit Phase 0 recon | covered (static subset; search-engine/DNS recon = runtime-only, noted) |
| 4.2 Configuration & Deployment Management | config-hardening + container-iac-security | covered |
| 4.3 Identity Management | auth-review | covered |
| 4.4 Authentication | auth-review | covered |
| 4.5 Authorization | auth-review (+ course-platform-security personas) | covered |
| 4.6 Session Management | auth-review sessions | covered |
| 4.7 Injection | injection-flaws (+ framework skills) | covered |
| 4.8 Error Handling | data-exposure | covered |
| 4.9 Weak Cryptography | crypto-review | covered |
| 4.10 Business Logic | flow-security | covered |
| 4.12 API Testing | graphql-security + config-hardening (API4/10) + auth-review route census | covered |
| 4.13 WebAssembly Testing | — | **GAP (documented)**: wasm module review (`.wasm` blobs, wasm-sandbox escapes) — niche; COVERAGE help-wanted |

## PortSwigger Web Security Academy topics (40 scraped) → owning skill

Covered (28): sql-injection, cross-site-scripting, csrf, xxe, clickjacking,
cors, ssrf, os-command-injection, server-side-template-injection,
deserialization, file-path-traversal, access-control, authentication, oauth,
logic-flaws, websockets, dom-based, host-header, information-disclosure,
file-upload, jwt, nosql-injection, prototype-pollution, race-conditions,
graphql, llm-attacks, api-testing, web-cache-deception.

Converted after this diff (2):
- **web-cache-poisoning** → config-hardening (unkeyed inputs into cacheable
  responses; repo-detectable subset + runtime-verify note)
- **request-smuggling** → config-hardening (custom proxy/middleware +
  absolute-URI/X-Forwarded handling in repo proxy configs; runtime-verify note)

## OWASP Code Review Guide

v3 is the substantive guide (PDF at owasp.org/www-project-code-review-guide/);
the GitHub `current/` tree is a thin v2 draft (verified). Category-level
mirror is satisfied by the WSTG + Academy maps above; the CRG's
review-methodology chapters map to security-audit Phases 0–3 (recon → scans →
triage → report). Revisit when v3 lands in markdown.

## Rule

When a new Academy topic or WSTG category appears (they add a few per year),
re-run this diff and disposition the new row — same completeness gate the
audit skill enforces on projects, applied to the skills themselves.

## Detection-logic catalog diff (2026-09-23, batch 1)

**CodeQL query help** (javascript 124 / java 110 / python 54 / ruby 52
security-relevant queries scraped from codeql.github.com): class-level diff
vs our skills — **~95% covered** (strong regression evidence: full/partial
SSRF, stored+reflected XSS, prototype pollution family, zip-slip, regex
injection, partial path traversal, log injection, cookie flags, CSRF
disabled/missing, weak crypto/keys/seeds, XPath, XXE, SSTI, system-prompt
injection). Converted after this diff:

- **case-sensitive middleware path** → auth-review route census
- **host-header poisoning in email generation** → auth-review §5 (generic;
  django Step 1 had the ALLOWED_HOSTS instance)
- **world-writable file permissions** → config-hardening
- **untrusted WASM compilation/loading** (CodeQL `polymorphic-wasm`-adjacent) → config-hardening §8

Converted after this diff (2026-09-23 knowledge-gap-closure round):
**LDAP authentication/injection** → auth-review pack (anonymous binds, DN/filter
injection, py + JNDI) + surface-vuln-app plants (ldap_route.py, LdapAuth.java
+ safe counterparts). Niche notes (loop-bound injection,
deep-traversal exhaustion, relative-path command execution) remain known-minor.

**Semgrep registry** (shape verified: language dirs at repo ROOT —
javascript/express/react/vue/jsonwebtoken/vm2, python/django/flask/fastapi,
java/spring/servlets, ruby/rails, php/laravel/symfony/wordpress-plugins,
go/generic/ai, typescript/mcp): the per-framework dirs map 1:1 onto our
framework skills — the weekly `watch-semgrep-rules.yml` digest is the
ongoing conversion feed; php/laravel + typescript/mcp + ai/ dirs are the
highest-yield triage targets for laravel-security and llm-security.
