---
name: timeout-budgets
domain: software-engineering/timeout-budgets
trigger: "Working out how a request's time is divided across the calls it makes."
anti_trigger: "Not for latency optimisation, and not for load testing."
scope: "How per-call timeouts compose, and the deadline that must propagate."
status: seedling
---

# Timeout budgets

## Standard

A request has a deadline, and every call it makes spends from that deadline. When each call has its own independent timeout, the sum can exceed the request's own deadline, so a handler that calls five dependencies at two seconds each can run for ten seconds against a client that gave up at three. The work continues after the client has gone, consuming resources for a response nobody will read.

Passing a deadline rather than a timeout composes correctly. The caller sends the time remaining, the callee sets its own timeout to the lesser of the remaining time and its own maximum, and each hop spends from the same budget rather than starting a new one. That requires the deadline to be part of the request context, which is a design decision the record should state.

Primary sources: <https://sre.google/> and <https://aws.amazon.com/builders-library/>.

## Decision rules

- Record the request's total deadline and where it originates.
- Record each downstream call's timeout and whether it derives from the remaining deadline.
- Record the sum of the per-call timeouts against the total, which must be less.
- Record the behaviour when the deadline is exhausted: abort, partial, or error.
- Record how the deadline propagates: header, context field, or library convention.
- Record the timeout for background work, which has a different budget from a request.

## Procedure

1. Record the end-to-end deadline.
2. List each downstream call and its timeout.
3. Check the sum against the deadline and record any overflow.
4. Convert timeouts to remaining-deadline derivation where they overflow.
5. Record the exhausted-deadline behaviour.
6. Write the budget with the arithmetic shown.

## Anti-patterns

- Independent per-call timeouts that sum to more than the request allows.
- A timeout longer than the client's own, which guarantees wasted work.
- Retrying after the deadline has passed.
- A background job inheriting a request timeout, which is either too short or too long.
- Assuming the framework sets deadlines when it sets only timeouts.

## Done checklist

- [ ] Total deadline recorded.
- [ ] Per-call timeouts recorded.
- [ ] Sum checked against the deadline.
- [ ] Deadline propagation recorded.
- [ ] Exhausted behaviour recorded.
- [ ] Background timeout recorded.

The deadline should also be visible to the caller's user: a request that will exceed its budget can be refused before the work starts, which is cheaper than starting work that will be abandoned. Admission by remaining budget is a small design change that removes a class of wasted work.


## Sources

- Site reliability engineering guidance: <https://sre.google/>
- Distributed systems patterns: <https://aws.amazon.com/builders-library/>
- Service level context: <https://sre.google/workbook/table-of-contents/>
