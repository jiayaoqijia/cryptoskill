---
name: load-balancer-behaviour
domain: software-engineering/load-balancer-behaviour
trigger: "Understanding how traffic is distributed, ejected, and pinned."
anti_trigger: "Not for service health endpoint design, and not for CDN caching."
scope: "Algorithms, health ejection, and session affinity."
status: seedling
---

# Load balancer behaviour

## Standard

A load balancer holds a list of backends and a rule for choosing one. The rule looks trivial until the backends stop being identical: a least-connections algorithm compensates for a slow request, a round-robin does not; a hash rule pins a user to one backend, which helps a local cache and hurts when that backend dies. The algorithm choice encodes assumptions about the workload, and the failures appear when the assumptions stop holding.

Health ejection is the rule that protects the rest. A backend that fails its checks is removed from rotation independent of the algorithm, and the recovery rule — how many passes before it returns — decides how long a recovering instance shades the traffic. Ejection and re-entry tuned too tightly flap an instance in and out; too loosely, and a dead instance keeps receiving requests.

Primary source: <https://developer.mozilla.org/en-US/docs/Web/HTTP>.

## Decision rules

- Record the balancing algorithm and the workload assumption it encodes.
- Record the health check — what it asks, what passes — and distinguish liveness from readiness at the balancer.
- Record ejection thresholds, re-entry thresholds, and the slow-start behaviour if any.
- Record session affinity's key and what the application actually stores in that session.
- Record connection draining on removal and the drain duration against in-flight request length.
- Verify distribution empirically after configuration, not from the documented promise.

## Procedure

1. Record the algorithm and its tuning parameters.
2. Record the health check and its pass and fail thresholds.
3. Record ejection and re-entry rules and draining on removal.
4. Record the affinity key and what state depends on it.
5. Send synthetic traffic and observe distribution, ejection, and re-entry.
6. Record the observed behaviour against the intended configuration.

## Anti-patterns

- Readiness checks that pass while the instance cannot serve.
- Ejection tuned with no slow start, flooding recovering instances.
- Affinity chosen for convenience with large session state behind it.
- Draining shorter than the longest realistic in-flight request.
- Trusting the configuration over an empirical receipt.

## Done checklist

- [ ] Algorithm and assumptions recorded.
- [ ] Health check and thresholds recorded.
- [ ] Ejection and re-entry recorded.
- [ ] Affinity key and dependants recorded.
- [ ] Draining checked against request length.
- [ ] Distribution verified empirically.

## Sources

- HTTP semantics and connection management: <https://developer.mozilla.org/en-US/docs/Web/HTTP>
- RFC 9110, HTTP semantics including connection handling: <https://www.rfc-editor.org/rfc/rfc9110>
- Health checks in production routing: <https://sre.google/sre-book/practical-alerting/>
