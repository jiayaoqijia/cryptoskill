---
name: correlation-across-services
domain: software-engineering/correlation-across-services
trigger: "Following one request's path across several services' logs."
anti_trigger: "Not for building tracing instrumentation (that is ac-reliability's observability leaf)."
scope: "Correlation and trace IDs: following one request through a system that fans out."
status: seedling
---

# Correlation across services

## Standard

A single user request through a distributed system becomes many events in many logs on many machines, and the only thing connecting them is an identifier somebody attached early. A correlation ID is that identifier: generated at the edge, propagated through every hop, and printed by every service on every line it logs about the request. Without it, production debugging across services is grep archaeology with no thread to pull.

The failure mode of the pattern is propagation loss. The ID must be carried through synchronous calls, asynchronous queues, background jobs spawned later — and each place it is dropped severs the chain precisely where the interesting fan-out happens. A system with ninety percent propagation has logs that look correlated and are not, which is worse than one with no IDs at all, because a broken trail gets trusted.

## Decision rules

- Record which entry points generate the ID and in what format.
- Enumerate the propagation paths: sync calls, queues, scheduled jobs, and anything that crosses a process boundary.
- Record where propagation is known to be broken rather than assuming completeness.
- Include the ID in crash reports and dead-letter messages, not only in logs.
- Verify by synthetic request: one seeded ID must appear in every expected service's output.
- When debugging, search by ID first, then reconstruct timing from the timestamps across services.

## Procedure

1. Establish where IDs are generated and how they are formatted.
2. Trace one synthetic request through the system and list every service that emits its ID.
3. Mark the hops where the ID disappears; record them as known gaps.
4. During an incident, collect every log line carrying the ID from every service.
5. Order the lines by timestamp, noting clock differences between hosts.
6. Write the request's reconstructed path with the gaps named.

## Anti-patterns

- Assuming every service propagates because one does.
- Searching by user identifier when IP or session could collide for other requests.
- Reconstructing cause from log ordering while ignoring clock skew.
- Trusting a correlated-looking trail from an unverified propagation path.
- Dropping the ID in fire-and-forget message sends.

## Done checklist

- [ ] ID generation points and format recorded.
- [ ] Propagation paths enumerated.
- [ ] Known gaps recorded.
- [ ] Synthetic request verified end to end.
- [ ] ID present in crash and dead-letter paths.
- [ ] Incident reconstruction lists gaps.

## Sources

- Distributed tracing concepts: <https://opentelemetry.io/docs/concepts/signals/traces/>
- Patterns of distributed systems: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
- W3C trace context propagation: <https://www.w3.org/TR/trace-context/>
