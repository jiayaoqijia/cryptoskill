---
name: row-level-security
domain: software-engineering/row-level-security
trigger: "Enforcing tenant isolation in the database and knowing where it fails."
anti_trigger: "Not for authentication, and not for encryption at rest."
scope: "Policy enforcement in the database, and the application paths that bypass it."
status: seedling
---

# Row-level security

## Standard

Row-level security moves the tenant filter from application code into the database, so a query that omits the tenant condition returns only rows the policy permits. That is a stronger guarantee than discipline, because it holds for every query the connection makes rather than the ones a developer remembered to filter.

Its limit is the connection that bypasses it. A migration script, an analytics job, a superuser connection, or a connection pool that reuses a session with a stale setting all operate outside the policy, and those are exactly the paths that touch the most data. The mechanism is only as good as the enumeration of the roles and connections that are exempt, which is why the record should list them.

Primary sources: <https://owasp.org/> and <https://csrc.nist.gov/>.

## Decision rules

- Record the policy per table and the predicate it enforces.
- Record which roles bypass the policy and why.
- Record how the session's tenant setting is established and reset.
- Record the connection pool behaviour, since a reused session can carry a stale setting.
- Record the coverage of background jobs, migrations, and analytics.
- Record the test that attempts a cross-tenant read through a policy-enforced role.

## Procedure

1. Record the policies and their predicates.
2. Enumerate roles that bypass and record the reason for each.
3. Record how the tenant setting is set per session.
4. Record pool behaviour at checkout and return.
5. Record job, migration, and analytics coverage.
6. Write the analysis with the bypass list.

## Anti-patterns

- Assuming a policy covers the analytics user.
- A pooled connection that retains the previous tenant's setting.
- Migrations run as an owner role that bypasses every policy.
- Policies that rely on a setting the application must remember to apply.
- Testing only with a role that enforces, never with one that bypasses.

## Done checklist

- [ ] Policies and predicates recorded.
- [ ] Bypass roles recorded with reasons.
- [ ] Session setting recorded.
- [ ] Pool behaviour recorded.
- [ ] Job and migration coverage recorded.
- [ ] Cross-tenant test written per role.

The pool reset is worth a specific test: a connection returned with a tenant setting still applied will serve the next request under the previous tenant's policy, and that failure is intermittent, load-dependent, and invisible in a single-request test. Forcing a reset and asserting the setting is clear is the check that catches it.


## Sources

- Application security verification: <https://owasp.org/>
- Security control guidance: <https://csrc.nist.gov/>
- Database security practice: <https://owasp.org/www-project-top-ten/>
