---
name: tenant-context-propagation
domain: software-engineering/tenant-context-propagation
trigger: "Carrying the tenant identity through every call that touches data."
anti_trigger: "Not for session management, and not for request authentication."
scope: "Carrying the tenant through every call, and the paths where it is lost."
status: seedling
---

# Tenant context propagation

## Standard

The tenant identity has to reach every operation that reads or writes tenant data, and the failures happen where it does not. A background job that iterates all tenants starts without a context; a queued message that carries the payload but not the tenant; a retry that reconstructs the request from a log; a cached result keyed without the tenant. Each is a path where the context is absent and the code either fails or, worse, defaults.

The design that survives is one where the absence of a tenant is an error rather than a default. A data access layer that refuses to run without a tenant context converts a silent leak into a loud failure, and that failure mode is the point: it is better for a job to break in staging than to process one tenant's data under another's identity in production.

Primary sources: <https://owasp.org/> and <https://csrc.nist.gov/>.

## Decision rules

- Record how the tenant is established: token claim, hostname, path, or header.
- Record how it is propagated: request scope, explicit parameter, or message attribute.
- Record the behaviour when the context is missing, which should be an error.
- Record every asynchronous path and whether it carries the tenant explicitly.
- Record the cache key composition, since a missing tenant in a key serves the wrong data.
- Record how a support or admin path sets a tenant, and whether that is audited.

## Procedure

1. Record the source of the tenant identity and its validation.
2. Record propagation through synchronous calls.
3. Record each asynchronous path and its tenant attribute.
4. Make the data layer reject a missing context and record that behaviour.
5. Record cache key composition per store.
6. Write the propagation map with the missing-context behaviour.

## Anti-patterns

- A default tenant, which silently routes unlabelled work.
- Propagating the tenant in a thread-local that does not survive an async boundary.
- Queueing a message without the tenant attribute.
- Cache keys that omit the tenant because the key "is already unique".
- An admin path that bypasses context without an audit record.

## Done checklist

- [ ] Tenant source recorded.
- [ ] Synchronous propagation recorded.
- [ ] Asynchronous paths recorded.
- [ ] Missing-context behaviour recorded.
- [ ] Cache keys recorded.
- [ ] Admin path and audit recorded.

## Sources

- Application security guidance: <https://owasp.org/>
- Security control catalogue: <https://csrc.nist.gov/>
- Authentication context: <https://owasp.org/www-project-top-ten/>
