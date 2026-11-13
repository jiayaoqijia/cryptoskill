---
name: injection
domain: security-hardening/injection
trigger: Writing or reviewing any code that builds a query, command, template or filter from data, and needing to keep data separate from interpreter structure.
anti_trigger: Generic validation and encoding rules (subskills/input-output.md); browser-executed attacks such as XSS (subskills/browser-security.md).
scope: SQL/NoSQL/OS/template/LDAP injection; parameterisation
status: seedling
---

# Injection

## Standard

- OWASP Injection Prevention Cheat Sheet: the preferred fix is a safe, parameterised API — prepared statements, ORM/entity framework — not escaping (https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html).
- OWASP Top 10 A05:2025 Injection (https://owasp.org/Top10/2025/A05_2025-Injection/): the most CVEs of any category (XSS >30k, SQLi >14k).
- OWASP ASVS 5.0: **V1.2.4 (L1)** parameterised queries for SQL, HQL, NoSQL and Cypher; **V1.2.5 (L1)** parameterised OS calls; **V1.3.7 (L2)** no templates built from untrusted input.
- CWE Top 25 2025 ranks CWE-89 SQL injection #2; MITRE's KEV ranking (updated 2026-01-27) puts CWE-78 OS command injection first with 20 KEV CVEs. CISA's FY2024-25 review: 41.5% of KEV entries map to "stubborn" weakness classes.

## Decision rules

1. Parameterise every value, everywhere. Escaping is the fallback where parameterisation is impossible, never the plan.
2. Structural names (table, column, sort key) cannot be escaped: allow-list the small set users may reference.
3. An ORM is not automatically safe — OWASP's own A05 scenario shows Hibernate HQL concatenation is injectable. Query-builder `.whereRaw()` / `$queryRaw` re-introduces the bug.
4. Stored procedures stay injectable when they build dynamic SQL (`EXECUTE IMMEDIATE`, `exec()`).
5. NoSQL is the same bug in another interpreter: `$where` and unvalidated operator objects (`{"$gt":""}`) inject.
6. Template injection (SSTI) is injection into the template engine: never render user data as a template.

## Procedure

1. Grep the codebase for string-built queries: concatenation, template literals, `.whereRaw`, `$queryRaw`, `format(`, f-strings near SQL, `exec`/`system` calls.
2. Convert each hit to parameter binding (placeholders or ORM-safe APIs).
3. Allow-list sort/filter column names against a constant list; reject anything else.
4. For OS calls, use list-form APIs (`subprocess.run([...])`) with no shell, per ASVS V1.2.5.
5. Add a lint rule (Semgrep or grep in CI) banning raw interpolation in query builders so regressions fail the build.
6. Add a test per endpoint: input `' OR '1'='1` and an operator object, assert the result set is unchanged.

## Anti-patterns

- "We use an ORM, so we are safe" — A05 scenario 2 disproves exactly this.
- Escaping quotes as the primary defence.
- Building the sort order or table name from a request parameter.
- Trusting a stored procedure that executes dynamic SQL internally.

## Done checklist

- [ ] No string-built SQL, HQL, or NoSQL query remains.
- [ ] Sort and filter columns come from an allow-list.
- [ ] OS calls use argument lists, never shell strings.
- [ ] No user data reaches a template engine as a template.
- [ ] CI bans raw query interpolation.
- [ ] Injection payload tests exist per endpoint.

## Sources

- Primary: OWASP Injection Prevention Cheat Sheet; OWASP Top 10 2025 A05; OWASP ASVS 5.0 V1.2.4/V1.2.5/V1.3.7; CWE Top 25 2025; CWE KEV ranking (2026-01-27); CISA FY2024-25 Vulnerability Review.
- <https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html>
- <https://owasp.org/Top10/2025/A05_2025-Injection/>
