---
name: circuit-breaking
domain: software-engineering/circuit-breaking
trigger: "Isolating a failing dependency with a breaker."
anti_trigger: "Not for timeout configuration alone, and not for load shedding."
scope: "Open, half-open, closed, and the recovery that must be proven."
status: seedling
---

# Circuit breaking

## Standard

A circuit breaker stops calling a dependency after a threshold of failures, which prevents callers from spending their own resources waiting on something that is not going to answer. The closed state passes traffic, the open state fails immediately, and the half-open state admits a limited probe to test whether recovery has occurred.

The half-open state is the mechanism that matters and the one most often misconfigured. A breaker that returns to closed on any success can oscillate between open and closed as a flaky dependency alternates; one that returns only after a sustained success rate avoids that but takes longer to recover. The record should state the transition conditions rather than the states alone, because the conditions are what the breaker actually does.

Primary sources: <https://aws.amazon.com/builders-library/> and <https://sre.google/>.

## Decision rules

- Record the failure threshold that opens the breaker and the window over which it is counted.
- Record what counts as a failure, since a client error is not a dependency failure.
- Record the half-open probe size and the condition for returning to closed.
- Record the time spent in open before a probe is admitted.
- Record whether the breaker is per instance, per host, or per client, since that changes its behaviour.
- Record the fallback path returned while open.

## Procedure

1. Record the failure classes that count toward opening.
2. Record the threshold and window.
3. Record the open duration and probe size.
4. Record the condition for closing again.
5. Record the fallback returned while open.
6. Write the state machine with its transitions.

## Anti-patterns

- Counting client errors as dependency failures, which opens the breaker for a bug.
- Returning to closed on a single success.
- A probe size large enough to re-overwhelm a fragile dependency.
- A per-instance breaker that leaves other instances hammering the dependency.
- An open breaker with no fallback, which turns a dependency failure into a hard error.

## Done checklist

- [ ] Failure classes recorded.
- [ ] Threshold and window recorded.
- [ ] Open duration and probe size recorded.
- [ ] Close condition recorded.
- [ ] Scope recorded.
- [ ] Fallback recorded.

The breaker's scope also decides whether it helps: a per-instance breaker protects one caller but leaves every other instance sending traffic to the same failing dependency, so the dependency stays loaded while the breaker reports that it is not. Shared state, at whatever level the topology allows, is what makes the open state mean anything.


## Sources

- Circuit breaker guidance: <https://aws.amazon.com/builders-library/>
- Reliability engineering practice: <https://sre.google/>
- Failure isolation context: <https://sre.google/workbook/table-of-contents/>
