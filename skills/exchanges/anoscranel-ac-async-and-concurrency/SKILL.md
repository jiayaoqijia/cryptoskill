---
name: ac-async-and-concurrency
description: "Designing code that does more than one thing at a time without races: shared mutable state and the primitives that protect it, async runtimes and the executor model, cancellation checkpoints and what never runs, structured concurrency and scope lifetime, ordering guarantees and happens-before, message passing and actor ownership as the alternative to locks, testing concurrency deterministically, and the written concurrency record. It explains how concurrent code behaves and fails; it never recommends a runtime and never promises a speedup. Use when asking \"race condition\", \"deadlock\", \"async await\", \"callback\", \"coroutine\", \"cancellation\", \"structured concurrency\", \"happens before\", \"atomicity\", \"lock ordering\", \"why does it fail only sometimes\", \"shared mutable state\". Not for distributed state and replication (ac-distributed-state-and-replication), not for resilience budgets around calls (ac-resilience-budgets), not for workflow orchestration (ac-durable-execution)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Async and concurrency

## Overview

Concurrency bugs are distinguished from other bugs by their reproducibility: a race fails once in ten thousand runs, on the machine with the different core count, during the demo. The cause is rarely exotic — two threads of execution touching shared mutable state without an agreed ordering — and the cure is rarely cleverness: it is making the sharing and the ordering explicit, then testing both under pressure.

This skill is the single-machine craft: what shared state is, what the synchronisation primitives actually guarantee, how async runtimes schedule and what that implies, what cancellation means and what it silently skips, how to test nondeterministic code, and how to write down a concurrency design so a reviewer can reason about it. Distributed agreement and retry budgets are other skills.

Primary sources: <https://martinfowler.com/> and <https://dl.acm.org/>.

## When to use

- When code runs tasks concurrently and shares state or resources.
- When a failure is intermittent, timing-dependent, or load-dependent.
- When designing or reviewing an async API, a cancellation path, or pooled resources.

## When NOT to use

- For replicated data and quorum consistency (use ac-distributed-state-and-replication).
- For timeouts, retries, and circuit breakers around calls (use ac-resilience-budgets).
- For durable workflows and saga orchestration (use ac-durable-execution).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/shared-state-and-primitives.md` | `software-engineering/shared-state-and-primitives` | What shared mutable state is, and what locks and atomics actually provide. |
| `subskills/async-runtimes.md` | `software-engineering/async-runtimes` | Executors, scheduling, and the assumptions async breaks. |
| `subskills/cancellation.md` | `software-engineering/cancellation` | What cancellation means, what it skips, and designing to be cancelled. |
| `subskills/lock-ordering-and-deadlock.md` | `software-engineering/lock-ordering-and-deadlock` | Acquiring in order, timing out, and why deadlock is a design error. |
| `subskills/concurrency-testing.md` | `software-engineering/concurrency-testing` | Making races reproducible: stress, interleaving injection, and model checks. |
| `subskills/async-api-design.md` | `software-engineering/async-api-design` | Futures, callbacks, and the semantics an async interface must state. |
| `subskills/message-passing-and-actors.md` | `software-engineering/message-passing-and-actors` | Actors, mailboxes, ownership by isolation, and where message passing beats locks. |
| `subskills/concurrency-record.md` | `software-engineering/concurrency-record` | The written record: shared state, orderings, cancellation, and blast radius. |

## Status and honest limits

Concurrency correctness is a proof about all interleavings, and tests exercise a vanishing subset of them; a stress run that passes a million iterations has not examined the one interleaving that deadlocks. The mitigations — explicit state ownership, documented orderings, bounded pools, and cancellation semantics — reduce the space rather than close it, and nothing here recommends a runtime or promises a speedup, because most parallelism gains are bought by waiting, not by racing.
