---
name: session-guarantees
domain: software-engineering/session-guarantees
trigger: "Making a user see their own writes on a replicated store."
anti_trigger: "Not for authentication sessions, and not for cache coherence."
scope: "Monotonic reads, read-your-writes, and routing a session to the right replica."
status: seedling
---

# Session guarantees

## Standard

The guarantees that matter to a session are four: monotonic reads — a session never sees data go backwards; read-your-writes — a session sees its own writes; monotonic writes — a session's writes are applied in its own order; writes-follow-reads — a session's write lands after the state it read. None of them is global consistency, and each is cheaper than it: they bind only within a session, and a session is an application-defined thing.

The implementation is routing. Read-your-writes is delivered by sending the session's reads to the replica that has its writes, or by tagging writes with positions and making reads wait for them, or by pinning the session to the primary for the read-after-write operations only. Each mechanism has a cost — routing complexity, waiting, or primary load — and the choice must be explicit per operation class because the cheapest correct option is different for each.

Primary sources: <https://jepsen.io/> and <https://martinfowler.com/>.

## Decision rules

- State which of the four guarantees the session needs, per operation class.
- Record how a session is identified and how long it lasts.
- Record the routing mechanism per guarantee: replica pinning, position waiting, or primary routing.
- Record the staleness bound a read-your-writes read can still carry, if any.
- Record the guarantee's behaviour across a failover, when positions may reset.
- Test with a real session that reads immediately after writing.

## Procedure

1. Classify the session's operations by the guarantee each needs.
2. Define the session identifier and its lifetime.
3. Choose the routing mechanism per guarantee.
4. State any residual staleness and where it is visible.
5. Write the failover behaviour for the guarantees.
6. Test read-after-write across the routing path.

## Anti-patterns

- Expecting read-your-writes to be a property of the store rather than of the routing.
- Sticky sessions with no expiry, pinning users to one replica forever.
- A guarantee implemented for reads but not for the writes it reads.
- Guarantees silently lost at failover, with the reset undocumented.
- Testing with sequential single-client traffic, which never exercises the path.

## Done checklist

- [ ] Guarantees stated per operation class.
- [ ] Session identifier and lifetime recorded.
- [ ] Routing mechanism per guarantee recorded.
- [ ] Residual staleness stated.
- [ ] Failover behaviour recorded.
- [ ] Read-after-write tested on the routing path.

## Sources

- Session consistency under faults: <https://jepsen.io/>
- Data consistency patterns: <https://martinfowler.com/>
- Distributed systems primer: <https://www.distributed-systems.net/>
