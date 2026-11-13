---
name: graceful-shutdown
domain: software-engineering/graceful-shutdown
trigger: "Stopping a service without abandoning work in flight."
anti_trigger: "Not for deployment strategy, and not for runtime tuning."
scope: "Signal handling, drain sequences, and deadline-driven termination."
status: seedling
---

# Graceful shutdown

## Standard

Termination arrives as a signal, and the service's behaviour in the next few seconds decides whether the stop is clean. The drain sequence is fixed: stop accepting new work first — close the listener, or signal the load balancer to withdraw — then finish the work in progress under a deadline, then close outward connections in a deliberate order, then exit. A service that skips the first step keeps accepting work it will then kill; a service without a deadline hangs on a stuck request and is killed by an external timeout it did not choose.

The deadline is the design decision. The graceful window must be shorter than the external kill timeout, with margin, so the service controls its own ending; and the work that cannot finish in the window needs an explicit disposition — complete it after restart, hand it to a durable queue, or fail it with a retriable error. The shutdown path is the one code path that runs at most a few times a month, which is exactly why it is the least tested and the most often wrong.

Primary sources: <https://sre.google/> and <https://martinfowler.com/>.

## Decision rules

- Record the signal expected and its handler: stop accepting, then drain.
- Record the graceful deadline and the external kill timeout, and verify the deadline is shorter with margin.
- Record the drain order: listener close, in-flight completion, connection close, exit.
- Record the disposition for work that cannot finish in the deadline.
- Record idempotency or checkpointing for any work resumed after restart.
- Test the shutdown under production-shaped load at least once per release.

## Procedure

1. Write the signal handler and the drain sequence.
2. Set the graceful deadline below the external kill timeout with margin.
3. Define the in-flight disposition at deadline expiry.
4. Add resume-or-checkpoint for unfinished work.
5. Load-test the shutdown: full traffic, then signal, then observe the drain.
6. Record the measured drain duration at peak load.

## Anti-patterns

- An immediate exit on signal, killing every request in flight.
- The graceful deadline equal to or longer than the external kill, so the external one wins.
- A drain that waits forever on one hung request.
- Connections closed in arbitrary order, breaking in-flight work mid-drain.
- A shutdown path that exists only in code review, never under load.

## Done checklist

- [ ] Signal and handler recorded.
- [ ] Deadline below kill timeout with margin.
- [ ] Drain order recorded.
- [ ] Expiry disposition defined.
- [ ] Resume path defined for unfinished work.
- [ ] Load-tested and measured.

## Sources

- Shutdown and lifecycle practice: <https://sre.google/>
- Deployment patterns: <https://martinfowler.com/>
- Distributed systems references: <https://www.distributed-systems.net/>
