---
name: replication-record
domain: software-engineering/replication-record
trigger: "Writing down the replication design and its guarantees."
anti_trigger: "Not for recommending a store, and not for operations runbooks."
scope: "The written record: topology, guarantees chosen, failover plan, and measured lag."
status: seedling
---

# Replication record

## Standard

The replication record is the design's contract with its readers: the topology, the guarantee each operation class receives, the failover plan with timings, and the measured lag distribution. It exists because replication behaviour is invisible until it fails, and a design that is not written down is argued about from memory during an incident.

Its second function is honesty about residual risk. Every replicated design has windows — election, catch-up, dual-primary residual — and the record names them with their probability and their recovery path. A record that claims a guarantee without its window is marketing, and the failure will arrive in exactly the window the record omitted.

Primary sources: <https://jepsen.io/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the topology, the write set, and the ordering guarantee.
- Each operation class lists the consistency guarantee it receives and the mechanism that delivers it.
- The failover plan is written with detection time, promotion time, and the in-flight write outcome.
- Measured lag at peak load and its tail are recorded, not only the average.
- The residual windows — dual-primary, catch-up, guarantee loss at failover — are named with recovery paths.
- The record is reviewed at every topology or configuration change.

## Procedure

1. Record the topology and the write set.
2. Record the guarantee per operation class with its mechanism.
3. Record the failover plan with measured timings.
4. Record the lag distribution at peak load.
5. Name the residual windows and their recovery paths.
6. Re-verify the measurements at every configuration change.

## Anti-patterns

- A record of guarantees with no measurements behind them.
- Failover described in words, never timed.
- The average lag recorded and the tail omitted.
- Residual windows absent because they are uncomfortable.
- A record written once and never re-verified after changes.

## Done checklist

- [ ] Topology and write set recorded.
- [ ] Guarantee per operation class with mechanism.
- [ ] Failover timings measured.
- [ ] Lag distribution recorded with tail.
- [ ] Residual windows named with recovery.
- [ ] Re-verification scheduled on changes.

The record's most useful section is often the one nobody writes: what the design cannot do. A topology that cannot accept writes during a failover is honest about a thirty-second outage; a topology that silently continues on a stale majority is not. Stating both in advance lets a reader choose the failure they prefer rather than discover the one they got.

## Sources

- Consistency verification reports: <https://jepsen.io/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Distributed systems primer: <https://www.distributed-systems.net/>
