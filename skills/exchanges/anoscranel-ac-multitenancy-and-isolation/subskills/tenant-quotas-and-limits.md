---
name: tenant-quotas-and-limits
domain: software-engineering/tenant-quotas-and-limits
trigger: "Setting per-tenant quotas and defining what happens at the limit."
anti_trigger: "Not for pricing tiers, and not for edge rate limiting alone."
scope: "Per-tenant rate limits, storage caps, and the response when they are hit."
status: seedling
---

# Tenant quotas and limits

## Standard

A quota is a promise about a ceiling, and its value depends on the response at the ceiling being defined. A limit that returns an error at the boundary is honest; one that silently drops work is not; one that queues indefinitely converts a rate problem into a latency problem for the tenant who stayed within their allowance. The record should state which of those three applies.

The dimension matters as much as the number. A request-rate limit does not bound the cost of an expensive query, a storage cap does not bound concurrency, and a concurrency cap does not bound the total work queued behind it. Effective quotas usually combine a rate, a concurrency, and a size dimension, because each bounds a different way a tenant can consume shared capacity.

Primary sources: <https://sre.google/> and <https://owasp.org/>.

## Decision rules

- Record each quota's dimension: request rate, concurrency, storage, payload size, or compute.
- Record the limit's value and the basis for it.
- Record the response at the limit: reject, queue with a bound, or degrade.
- Record how the client learns of the limit before hitting it.
- Record whether limits are per tenant, per user, or per API key.
- Record the process for a legitimate increase, since a hard ceiling with no appeal creates support load.

## Procedure

1. Record each dimension and its limit.
2. Record the response at the boundary.
3. Record the signal the client receives before the limit.
4. Record the scoping of each limit.
5. Record the increase process.
6. Write the quota table with its responses.

## Anti-patterns

- A rate limit as the only control, which does not bound expensive queries.
- Silently dropping work at the limit.
- Queueing without a bound, which turns a limit into an outage.
- Limits with no stated increase path.
- Applying a limit at the edge only, when internal paths bypass it.

## Done checklist

- [ ] Quota dimensions recorded.
- [ ] Limits recorded with basis.
- [ ] Boundary response recorded.
- [ ] Pre-limit signal recorded.
- [ ] Scoping recorded.
- [ ] Increase process recorded.

The limit's visibility matters for support load as much as for fairness: a client that discovers the ceiling only when it fails generates a ticket, while one that receives a remaining-quota header or a documented threshold can back off. Recording how the limit is communicated turns a hard cap into a contract.


## Sources

- Reliability and capacity guidance: <https://sre.google/>
- Abuse and rate-limit controls: <https://owasp.org/>
- Service level context: <https://sre.google/workbook/table-of-contents/>
