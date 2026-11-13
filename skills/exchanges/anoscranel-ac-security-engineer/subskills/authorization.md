---
name: authorization
domain: security-hardening/authorization
trigger: "Deciding and enforcing who may do what to each object: RBAC/ABAC/ReBAC choice, per-object checks, multi-tenancy isolation, IDOR/BOLA defence."
anti_trigger: "Proving identity (subskills/authentication.md) or session lifetime (subskills/sessions-tokens.md); API-specific consumption limits (subskills/api-security.md)."
scope: "RBAC/ABAC, object-level checks, IDOR/BOLA, deny by default"
status: "seedling"
---

# Authorization

## Standard

- OWASP API Security Top 10 **2023**: BOLA (Broken Object Level Authorization) is API1, Exploitability Easy, Prevalence Widespread. Its defining rule: comparing the session's user ID with the ID parameter "isn't a sufficient solution" — a per-object policy check is required on **every** endpoint that takes an object ID (https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/).
- OWASP Authorization Cheat Sheet: deny by default, validate permissions on every request, prefer attribute- and relationship-based control over RBAC.
- OWASP Authorization Testing Automation Cheat Sheet: wire the checks into CI.
- OWASP Multi-Tenant Security Cheat Sheet: separate database per tenant, separate schema per tenant, or a shared database with Row-Level Security; run tenant-scoped paths under a non-RLS-bypassing role; long random identifiers "reduce enumeration, but they are not authorization controls".
- NIST SP 800-162 for ABAC vocabulary. ASVS 5.0 V8 Authorization.

## Decision rules

1. Single-tenant app: one reusable `authorize(user, action, object)` call on every object access; deny by default.
2. Multi-tenant: `tenant_id` on every row, always filtered, backed by RLS under a role that cannot bypass RLS; scope tenant context to the transaction.
3. RBAC for a small app with few roles; ABAC when attributes (plan, department, owner) drive access; ReBAC/Zanzibar only when sharing and collaboration is the product.
4. Every privileged route gets a server-side role check (API5, Broken Function Level Authorization) — a UI-hidden button is not a control.
5. Writable-field allow-lists stop property-level abuse (API3, BOPLA): never bind a request body onto an entity.

## Procedure

1. Deny by default in the framework: an unmatched route returns 403, not 200.
2. Implement one `authorize(user, action, object)` predicate; call it on every object read and write, including list endpoints.
3. Add the tenant filter to every query path; enable RLS where the database supports it, under a non-bypass role.
4. Build the two-account test suite: log in as A, request B's object ID (and a random GUID) on every ID-taking endpoint; **expect 403 or 404, never 200**.
5. Cover four cases: horizontal (other user, BOLA), vertical (lower role hitting an admin function, API5), property level (writable-field allow-list, API3), and tenant boundary.
6. Wire the suite into CI. API1's prevention text: "Write tests to evaluate the vulnerability of the authorization mechanism. Do not deploy changes that make the tests fail."

## Anti-patterns

- Treating "logged in" as "authorised".
- Hiding object IDs behind unguessable UUIDs and calling that access control.
- Per-route inline checks that one new endpoint forgets.
- Sharing one database role across tenants so RLS is bypassed by design.

## Done checklist

- [ ] One authorize predicate called on every object access.
- [ ] Deny by default for unmatched routes and roles.
- [ ] Tenant filter on every query; RLS under a non-bypass role where used.
- [ ] Writable fields allow-listed per endpoint.
- [ ] Two-account cross-access suite runs in CI; expects 403/404 everywhere.
- [ ] No control depends on identifier secrecy.

## Sources

- Primary: OWASP API Security Top 10 2023 API1/API3/API5; OWASP Authorization, Multi-Tenant and Authorization Testing Automation Cheat Sheets; NIST SP 800-162; OWASP ASVS 5.0 V8.
- <https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html>
- <https://owasp.org/www-project-application-security-verification-standard/>
