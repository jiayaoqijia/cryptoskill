---
name: replay-and-rebuild
domain: software-engineering/replay-and-rebuild
trigger: "Replaying an event log to rebuild a projection."
anti_trigger: "Not for backup restoration, and not for broker configuration."
scope: "Replaying the log, rebuilding projections, and the cost of both."
status: seedling
---

# Replay and rebuild

## Standard

Replay is the property that justifies keeping a log: because events are facts, a projection can be discarded and rebuilt by reading them again. That capability is real and it is also constrained, because the log's retention may be finite, the projection's rebuild may take longer than the window available, and the replay may produce different results than the original run if any consumer is not deterministic.

The determinism requirement is the one most often missed. A projection that calls an external service, reads the current time, or depends on iteration order will produce a different result on replay, and the difference is usually discovered during the rebuild rather than before it. The record should state what the projection depends on and whether those dependencies are captured in the event.

Primary sources: <https://martinfowler.com/> and <https://www.cncf.io/>.

## Decision rules

- Record the log's retention and whether it covers the full history the projection needs.
- Record the rebuild's expected duration and the window available for it.
- Record the projection's dependencies: external calls, clocks, ordering, and randomness.
- Record whether those dependencies are captured in the event payload.
- Record the rebuild's parallelism and how ordering is preserved per key.
- Record the cutover: how the rebuilt projection replaces the old one without serving stale reads.

## Procedure

1. Record retention and compare with the history required.
2. Record the rebuild duration estimate and the available window.
3. Enumerate the projection's non-deterministic dependencies.
4. Capture each in the event or record the exclusion.
5. Record the rebuild's ordering guarantee.
6. Record the cutover procedure and its rollback.

## Anti-patterns

- Assuming the log is retained indefinitely.
- A projection that reads the current time during replay.
- Rebuilding in parallel without preserving per-key order.
- Cutting over without a way back.
- Discovering non-determinism during the rebuild rather than before it.

## Done checklist

- [ ] Retention recorded against history required.
- [ ] Rebuild duration and window recorded.
- [ ] Dependencies enumerated.
- [ ] Each dependency captured or excluded with reason.
- [ ] Ordering recorded.
- [ ] Cutover and rollback recorded.

The rebuild's cutover is where a correct rebuild can still produce an incident: serving from the new projection while some consumers still hold a reference to the old one produces inconsistent reads, and the cutover needs a switch that is atomic from the readers' perspective rather than a sequence of deployments.


## Sources

- Event sourcing and replay practice: <https://martinfowler.com/>
- Cloud native streaming guidance: <https://www.cncf.io/>
- Integration pattern reference: <https://www.enterpriseintegrationpatterns.com/>
