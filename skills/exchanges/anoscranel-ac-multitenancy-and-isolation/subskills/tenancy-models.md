---
name: tenancy-models
domain: software-engineering/tenancy-models
trigger: "Choosing how tenants share a data store and what it costs."
anti_trigger: "Not for authentication, and not for backup strategy."
scope: "Shared rows, shared schema, separate schemas, separate databases, and their costs."
status: seedling
---

# Tenancy models

## Standard

The models form a ladder. At one end, every tenant's rows sit in the same tables with a tenant column and every query filters on it; at the other, each tenant has its own database, and a query that forgets a filter cannot reach another tenant's data because it is not connected to it. Between them sit shared tables with separate schemas, and shared schema with per-tenant partitioning.

Cost moves in the opposite direction from isolation. A shared table is cheap to operate and cheap to migrate, and its boundary depends on every code path. A separate database is expensive per tenant and expensive to change, and its boundary is structural. The choice should follow the consequence of a leak rather than the convenience of the build, and the record should state that consequence explicitly.

Primary sources: <https://csrc.nist.gov/> and <https://owasp.org/>.

## Decision rules

- Record the model chosen and the reason, including the consequence of a cross-tenant leak.
- Record the per-tenant resource cost and how it scales with tenant count.
- Record the migration path: how a schema change is applied across tenants.
- Record the onboarding and offboarding cost, including data deletion per tenant.
- Record the isolation the model gives structurally versus the isolation it leaves to code.
- Record the threshold at which the model would be reconsidered.

## Procedure

1. Record the candidate models and their per-tenant cost.
2. Record the consequence of a leak for the business and its customers.
3. Choose the model and record the reason.
4. Record the migration and onboarding paths.
5. Record the structural versus disciplinary boundary.
6. Write the decision with the reconsideration threshold.

## Anti-patterns

- Choosing shared rows because it is simpler, without measuring the cost of a leak.
- Choosing separate databases for a small tenant base without the operating cost.
- Ignoring the migration path, which becomes the binding constraint later.
- Assuming per-tenant deletion is free when the data is shared.
- Treating the model as permanent when tenant count changes the answer.

## Done checklist

- [ ] Model and reason recorded.
- [ ] Per-tenant cost recorded.
- [ ] Migration path recorded.
- [ ] Onboarding and deletion cost recorded.
- [ ] Structural versus disciplinary boundary recorded.
- [ ] Reconsideration threshold recorded.

The model choice should also account for the deletion obligation: a per-tenant deletion request in a shared table is a bulk delete with its own operational risk, while in a separate database it is a drop. Recording the deletion path at the same time as the isolation choice keeps the two decisions consistent rather than discovering the conflict at the first request.


## Sources

- Security and privacy control guidance: <https://csrc.nist.gov/>
- Application security standards: <https://owasp.org/>
- Database design context: <https://csrc.nist.gov/publications>
