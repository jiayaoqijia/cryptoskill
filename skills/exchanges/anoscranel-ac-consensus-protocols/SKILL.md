---
name: ac-consensus-protocols
description: "How a distributed system agrees on one order of events: the replicated log as the agreement object, leaders and term-and-index structure, quorum intersection and what a commit proves, leader leases and fencing tokens, membership changes and joint configurations, single-decree epochs, learner and witness roles, and the written record. It explains what a consensus commits and what it costs; it never recommends a protocol library and never promises a fault-free cluster. Use when asking \"consensus protocol\", \"raft\", \"paxos\", \"replicated log\", \"commit index\", \"leader lease\", \"fencing token\", \"membership change\", \"joint consensus\", \"learner node\", \"why is my cluster stalled\", \"quorum intersection\", \"log compaction\". Not for leader election alone (ac-distributed-state-and-replication), not for client-side session guarantees (ac-distributed-state-and-replication), not for queue delivery semantics (ac-durable-execution)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Consensus protocols

## Overview

Consensus solves one problem: several machines, any of which may fail or lag, must agree on a single order of events. The agreement object is not a value but a log — an ordered sequence of entries — and the protocol's commitment is that once an entry is acknowledged, every future leader will see it in the same position. Everything else, from databases to lock services to configuration stores, is an interpretation built on that ordered log.

Reading a protocol means tracking three numbers and one invariant. The numbers are the term (who is the current legitimate leader), the index (a position in the log), and the commit point (the highest entry known to be durable on a quorum). The invariant is quorum intersection: any two majorities share a member, so a leader that has confirmed an entry on a quorum must find that entry reflected back by any successor's quorum. Membership change is where the invariant is at risk, and the joint-configuration pattern is how it is preserved during transition.

Primary sources: <https://raft.github.io/raft.pdf> and <https://martinfowler.com/articles/patterns-of-distributed-systems/>.

## When to use

- Reading, evaluating, or operating a system built on a consensus protocol.
- Diagnosing a stalled cluster, an uncommitted entry, or a leadership dispute.
- Reasoning about leases, fencing, and what a client may rely on.
- Planning a membership change without breaking the quorum invariant.

## When NOT to use

- For the election and split-brain outcome alone (use ac-distributed-state-and-replication).
- For read-your-writes and session guarantees on the client side (use ac-distributed-state-and-replication).
- For at-least-once job and workflow semantics (use ac-durable-execution).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/replicated-log.md` | `software-engineering/replicated-log` | The log as the agreement object, and what a commit index commits. |
| `subskills/leader-and-terms.md` | `software-engineering/leader-and-terms` | Term numbers, election restrictions, and the two-leaders impossibility. |
| `subskills/quorum-intersection.md` | `software-engineering/quorum-intersection` | Why majorities overlap, what a write quorum proves, and read quorum subtleties. |
| `subskills/leases-and-fencing.md` | `software-engineering/leases-and-fencing` | Leader leases versus fencing tokens, and the clock question. |
| `subskills/membership-changes.md` | `software-engineering/membership-changes` | Joint configurations, the invariant during transition, and learner seeding. |
| `subskills/single-decree-and-epochs.md` | `software-engineering/single-decree-and-epochs` | One value at a time, the epoch pattern, and when it is enough. |
| `subskills/learners-and-witnesses.md` | `software-engineering/learners-and-witnesses` | Non-voting members, cross-region learners, and the cost of full copies. |
| `subskills/consensus-record.md` | `software-engineering/consensus-record` | The written record of protocol, quorum, leases, and incident history. |

## Status and honest limits

A consensus protocol commits an order; it does not commit that the order was the one the client intended, that the applied state machine is correct, or that a slow minority is healthy. Clock-based leases carry an availability risk if clocks jump, and fencing tokens carry a latency cost if every read checks them. Nothing here recommends a protocol; the honest output is knowing exactly which guarantee the deployment relies on and where its next failure will come from.
