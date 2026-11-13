---
name: edge-record
domain: software-engineering/edge-record
trigger: "Writing down the delivery configuration someone will inherit."
anti_trigger: "Not for the vendor's console, and not for release notes."
scope: "The written record of the delivery configuration."
status: seedling
---

# Edge record

## Standard

The edge record states the DNS layout and TTLs, TLS termination points and certificate ownership, load balancer algorithms and health rules, CDN key schemes per route class, shield topology, and the edge rules layer with its order. It exists because the delivery layer is configured rarely and debugged rarely — long gaps between touches, different people each time, and a console that remembers what nobody wrote down.

Its second purpose is change safety. TTL lowering, certificate renewal, key scheme changes, and rule additions each have failure modes that a review can catch only against a record of what exists today. The change plan that lists current state, intended state, rollback, and expiry windows is a document this record feeds.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/HTTP> and <https://www.rfc-editor.org/>.

## Decision rules

- Record the DNS zone layout, each record's TTL, and the change procedure.
- Record every certificate with its scope, expiry, and renewal automation point.
- Record load balancer algorithm, health check, ejection, and draining per service.
- Record the CDN key scheme per route class and the purge authority.
- Record redirect and rewrite rules in evaluation order.
- Attach a change plan template: current, intended, rollback, expiry windows.

## Procedure

1. Assemble each layer's configuration into the record.
2. State TTLs and expiry windows explicitly.
3. Name the owner of each automated renewal and each purge authority.
4. Record the change template and attach one completed example.
5. Review at every edge change and re-date.
6. Audit quarterly against actual configuration, and reconcile drift.

## Anti-patterns

- A record of the last change only, with no current-state baseline.
- Certificates recorded without renewal automation owners.
- Key schemes documented as intent rather than as observed configuration.
- No reorder plan when rules are added.
- A record that never gets compared to the running configuration.

## Done checklist

- [ ] DNS layout and TTLs recorded.
- [ ] Certificates and renewals recorded.
- [ ] Balancer configuration recorded.
- [ ] Key schemes and purge recorded.
- [ ] Rules layer recorded in order.
- [ ] Change-plan template attached.

The record also serves incident response: when a route misbehaves, the responder needs to know within a minute whether a CDN, a balancer rule, or the origin stands in the path, and which cache keys could be serving the wrong thing for how long. A record organised by route class answers that; a record organised by vendor console does not.

## Sources

- HTTP semantics reference: <https://developer.mozilla.org/en-US/docs/Web/HTTP>
- RFC 9111, HTTP caching: <https://www.rfc-editor.org/rfc/rfc9111>
- Operational review practice: <https://sre.google/sre-book/>
