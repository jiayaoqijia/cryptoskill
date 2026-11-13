---
name: isolation-levels
domain: software-engineering/isolation-levels
trigger: "Establishing what a tenancy model actually guarantees."
anti_trigger: "Not for transaction isolation levels in databases, and not for encryption."
scope: "What each model actually guarantees, and what it leaves to discipline."
status: seedling
---

# Isolation levels

## Standard

The word isolation covers two different things, and confusing them produces false confidence. Transaction isolation governs whether concurrent transactions see each other's uncommitted work. Tenant isolation governs whether one customer can read another's data, and no database's transaction isolation level provides it. A system can run at the strictest transaction isolation and still leak between tenants through a forgotten filter.

Establishing the real guarantee means enumerating the enforcement points. The database may enforce a policy, the application may filter, the cache may be keyed by tenant, the background job may iterate, and the analytics replica may not be covered by any of it. Each point either enforces the boundary or assumes another has, and the ones that assume are where leaks occur.

Primary sources: <https://owasp.org/> and <https://csrc.nist.gov/>.

## Decision rules

- Record each enforcement point: database policy, application filter, cache key, job, replica, export.
- Record for each whether it enforces the boundary or assumes it.
- Record the test that attempts a cross-tenant read at each point.
- Record whether the database enforces a policy even when the application forgets.
- Record the treatment of derived stores: caches, search indexes, and analytics.
- Record what happens on a policy bypass, since a superuser connection defeats row-level security.

## Procedure

1. List every path that reads tenant data.
2. Record whether each enforces or assumes the boundary.
3. Identify the points that assume, which are the exposure.
4. Write a cross-tenant read test for each enforcement point.
5. Record derived stores and their coverage.
6. Write the guarantee with its gaps named.

## Anti-patterns

- Treating transaction isolation as tenant isolation.
- Assuming a database policy covers connections that bypass it.
- Forgetting the search index and the analytics replica.
- Testing only the happy path, which uses a correctly scoped context.
- Accepting an enforcement point that was never tested.

## Done checklist

- [ ] Enforcement points listed.
- [ ] Enforce versus assume recorded per point.
- [ ] Cross-tenant read test written per point.
- [ ] Database policy coverage recorded.
- [ ] Derived stores recorded.
- [ ] Gaps named.

The strongest practical check is a test that runs the application's own read path with a tenant identifier belonging to another tenant and asserts an empty result: it exercises the real code, including the stack of middleware the design assumes, rather than the policy in isolation. That test belongs in the suite and not in a one-off review.


## Sources

- Application security verification: <https://owasp.org/>
- Security control guidance: <https://csrc.nist.gov/>
- Database security context: <https://owasp.org/www-project-top-ten/>
