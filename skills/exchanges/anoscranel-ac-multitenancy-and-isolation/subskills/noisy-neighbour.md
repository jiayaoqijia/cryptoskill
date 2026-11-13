---
name: noisy-neighbour
domain: software-engineering/noisy-neighbour
trigger: "One tenant's load degrading everyone else's service."
anti_trigger: "Not for load testing methodology, and not for capacity sizing."
scope: "Shared resource contention, fair scheduling, and the tenant that starves others."
status: seedling
---

# Noisy neighbour

## Standard

In a shared deployment, tenants compete for the same connection pool, the same worker threads, the same cache, and the same database. A single tenant running an expensive query can consume the pool and leave every other tenant waiting, which means one customer's behaviour becomes everyone's outage. The problem is not malicious and does not require unusual load; a legitimate bulk export is enough.

The response is to make the shared resource allocatable rather than first-come. Connection pool partitioning, per-tenant concurrency caps, queue priorities, and separate pools for interactive and batch work each limit how much of a shared resource one tenant can take. The design question is which resource is the binding one, because protecting a resource that is not contended adds complexity without changing behaviour.

Primary sources: <https://sre.google/> and <https://owasp.org/>.

## Decision rules

- Record the shared resources and which one is binding under load.
- Record the mechanism that bounds per-tenant consumption of that resource.
- Record the behaviour when a tenant exceeds its bound: queue, reject, or degrade.
- Record whether batch and interactive work share a pool.
- Record the fairness property claimed, and how it is tested.
- Record the tenant whose behaviour prompted the control, since the mechanism should address an observed case.

## Procedure

1. Identify the shared resources and measure which saturates first.
2. Record the current allocation, which is usually first-come.
3. Introduce a bound on the binding resource.
4. Record the exceedance behaviour.
5. Separate batch from interactive where they share a pool.
6. Test with one tenant at high load and record the others' latency.

## Anti-patterns

- Partitioning a resource that is not the bottleneck.
- A per-tenant cap so low that legitimate bursts are rejected.
- Sharing a connection pool between a bulk export and interactive traffic.
- Assuming fair scheduling is automatic when the allocator is first-come.
- Adding limits without measuring the effect on other tenants.

## Done checklist

- [ ] Shared resources and binding one recorded.
- [ ] Bounding mechanism recorded.
- [ ] Exceedance behaviour recorded.
- [ ] Batch and interactive separation recorded.
- [ ] Fairness property and test recorded.
- [ ] Observed case recorded.

The control should also name the resource the tenant cannot be allowed to consume, since the business consequence differs: exhausting connection pool slots delays everyone, exhausting worker threads stops processing, and exhausting storage fails writes. Which one matters determines whether the fix is a cap, a queue, or a separate deployment.


## Sources

- Site reliability engineering guidance: <https://sre.google/>
- Application security and abuse controls: <https://owasp.org/>
- Capacity and load context: <https://sre.google/workbook/table-of-contents/>
