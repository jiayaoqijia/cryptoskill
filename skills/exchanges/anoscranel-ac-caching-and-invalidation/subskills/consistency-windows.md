---
name: consistency-windows
domain: software-engineering/consistency-windows
trigger: "Stating the staleness bound a reader can observe."
anti_trigger: "Not for distributed consensus design, and not for query tuning."
scope: "What a reader can observe, and how to state the bound in a contract."
status: seedling
---

# Consistency windows

## Standard

A cached system does not deliver consistency; it delivers a bound, and the bound has to be stated in terms a reader can act on. "Eventually consistent" is not a bound — it is an admission that no bound is known. The useful form is a maximum staleness in time plus a description of the cases where it can be exceeded, such as a lost invalidation event.

The distinction that matters to consumers is read-your-own-writes. A user who updates a record and immediately reloads it expects to see their change, and a cache that can serve a value older than the user's own write breaks that expectation even when the staleness is within the global bound. Handling it usually means bypassing the cache for a short window after a write, or versioning the read so the user's own version is carried forward.

Primary sources: <https://www.rfc-editor.org/rfc/rfc9111.html> and <https://aws.amazon.com/caching/best-practices/>.

## Decision rules

- Record the maximum staleness in time, as a number.
- Record the cases where the bound can be exceeded, such as a dropped invalidation.
- Record whether read-your-own-writes is guaranteed and by what mechanism.
- Record which consumers can observe staleness and which cannot.
- Record the behaviour at the boundary, such as a read racing a write.
- Record what the system does when it cannot honour the bound, rather than silently exceeding it.

## Procedure

1. State the staleness bound as a number.
2. List the cases that exceed it.
3. Record the read-your-own-writes mechanism.
4. Record the consumer-visible effects.
5. Record the boundary behaviour.
6. Write the bound into the interface contract.

## Anti-patterns

- Describing the system as eventually consistent with no number.
- Guaranteeing a bound that a lost invalidation can exceed.
- Ignoring read-your-own-writes and surprising the user who just wrote.
- Stating the bound in internal documents and not in the interface contract.
- Treating a cache's clock skew as a rounding error.

## Done checklist

- [ ] Bound stated as a number.
- [ ] Exceeding cases listed.
- [ ] Read-your-own-writes mechanism recorded.
- [ ] Consumer effects recorded.
- [ ] Boundary behaviour recorded.
- [ ] Bound in the interface contract.

A further subtlety is that the bound is per consumer, not global: an internal admin tool reading a replica may tolerate minutes while a customer-facing page tolerates seconds, and a single stated bound applied to both will either be too strict for one or too loose for the other. The contract belongs per interface rather than per cache.


## Sources

- HTTP caching semantics: <https://www.rfc-editor.org/rfc/rfc9111.html>
- Caching best practices: <https://aws.amazon.com/caching/best-practices/>
- Consistency models reference: <https://jepsen.io/consistency>
