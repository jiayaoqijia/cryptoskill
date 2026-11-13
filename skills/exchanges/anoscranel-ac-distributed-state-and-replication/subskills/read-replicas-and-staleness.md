---
name: read-replicas-and-staleness
domain: software-engineering/read-replicas-and-staleness
trigger: "Bounding how far behind a replica read can be."
anti_trigger: "Not for cache TTL choices, and not for recommending a product."
scope: "Replica lag, its causes, and bounding how far behind a read can be."
status: seedling
---

# Read replicas and staleness

## Standard

A read replica serves reads from a copy that is behind the primary by some interval, and that interval is not a constant: it grows under write bursts, under long transactions on the primary, under network contention, and during a replica catch-up after a restart. Treating lag as a fixed number produces a system that is correct in the dashboard and wrong under load.

The bounding question is application-specific: how stale can this read be before it is wrong? A product listing tolerates seconds; a read-after-write confirmation does not tolerate any. The answer decides which reads go to the replica, which must be routed to the primary, and what fallback exists when lag exceeds the bound — route to primary, wait for the write, or show a staleness indicator.

Primary sources: <https://jepsen.io/> and <https://www.postgresql.org/docs/>.

## Decision rules

- State the staleness bound per operation, in time or in transaction count.
- Measure actual lag at peak write load, not at idle.
- Route reads that must see a just-made write to the primary or to a session-aware path.
- Record the replica's catch-up behaviour after a restart and its worst measured lag.
- Record what happens when lag exceeds the bound and who detects it.
- Never write to a replica designated for reads.

## Procedure

1. Classify reads by their staleness tolerance.
2. Measure lag under peak write load and under a replica restart.
3. Set the routing rule per read class.
4. Define the exceed-lag fallback and its detection.
5. Add lag monitoring with an alarm at a fraction of the bound.
6. Record the measured distribution, not only its average.

## Anti-patterns

- A single lag number quoted from quiet-hour monitoring.
- Read-your-own-writes expected from a replica that has not received the write.
- Writes to a read replica, splitting the point of truth.
- An average lag reported without its tail.
- No detection when lag silently exceeds the tolerance.

## Done checklist

- [ ] Staleness bound stated per operation.
- [ ] Peak-load lag measured.
- [ ] Restart catch-up measured.
- [ ] Routing rules per read class.
- [ ] Exceed-lag fallback defined.
- [ ] Lag tail monitored, not only its mean.

A subtle failure mode deserves a line of its own: replica lag does not queue evenly. A replica that falls behind by minutes and then catches up in a burst serves reads that are correct-by-lag-average and wrong-by-history, and a monitoring window that samples once a minute can miss the burst entirely. Measure the maximum observed lag, not the steady state, and test with the write pattern of a real weekday rather than a benchmark's uniform load.

## Sources

- Replication behaviour under faults: <https://jepsen.io/>
- Streaming replication mechanics: <https://www.postgresql.org/docs/>
- Distributed systems primer: <https://www.distributed-systems.net/>
