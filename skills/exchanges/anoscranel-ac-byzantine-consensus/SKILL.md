---
name: ac-byzantine-consensus
description: "Agreement when some participants may be malicious or arbitrarily broken: the Byzantine failure model and how it differs from crash faults, the 3f+1 replica arithmetic that makes it survivable, three-phase commit and the prepare and commit rounds PBFT runs, view changes when the primary itself is the fault, client quorums and how a reply is trusted, signed versus MAC-based message authentication, and the written Byzantine record. It explains the model and its arithmetic; it never recommends a protocol. Use when asking \"byzantine fault\", \"byzantine agreement\", \"PBFT\", \"3f plus 1\", \"view change\", \"byzantine generals\", \"malicious replica\", \"signed messages versus MACs\", \"why do byzantine systems need more replicas\". Not for crash-fault consensus of the Raft or Paxos family (ac-consensus-protocols), not for quorum intersection in majority systems (ac-consensus-protocols), not for security hardening of the endpoints themselves (ac-security-engineer)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Byzantine consensus

## Overview

Crash-fault consensus assumes a failed node stops and says nothing false. Byzantine consensus makes no such assumption: a faulty node may send different messages to different peers, lie about what it received, and actively work against the outcome. The consequence is arithmetic — tolerating f Byzantine faults requires 3f+1 replicas rather than 2f+1, and every guarantee must hold against an adversary choosing the worst messages at the worst moments.

This skill covers that model and the machinery built on it: why 3f+1 is the minimum, how the three-phase prepare-commit structure lets replicas converge on one order despite equivocation, how view change replaces a primary that may itself be the fault, and how a client decides a reply is trustworthy without trusting any single node. It ends at the boundary of the crash-fault family, which belongs to another skill.

Primary sources: <https://pmg.csail.mit.edu/papers/osdi99.pdf> and <https://en.wikipedia.org/wiki/Byzantine_fault>.

## When to use

- Reading or evaluating a system that claims Byzantine fault tolerance.
- Reasoning about why a deployment needs 3f+1 replicas and what f it buys.
- Following a view change when the primary is suspected faulty.
- Deciding between signed messages and MACs for message authentication.

## When NOT to use

- For crash-fault protocols of the Raft or Paxos family (use ac-consensus-protocols).
- For quorum intersection in majority systems (use ac-consensus-protocols).
- For hardening the endpoints themselves (use ac-security-engineer).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/byzantine-versus-crash.md` | `software-engineering/byzantine-versus-crash` | The failure model: what a Byzantine node may do that a crashed one cannot. |
| `subskills/replica-arithmetic.md` | `software-engineering/replica-arithmetic` | Why 3f+1 is the minimum, and the quorum sizes it produces. |
| `subskills/three-phase-commit.md` | `software-engineering/three-phase-commit` | Pre-prepare, prepare, and commit, and what each round eliminates. |
| `subskills/view-changes.md` | `software-engineering/view-changes` | Replacing a suspected primary without losing committed work. |
| `subskills/client-quorums.md` | `software-engineering/client-quorums` | How a client trusts a reply without trusting any single node. |
| `subskills/signatures-versus-macs.md` | `software-engineering/signatures-versus-macs` | Authentication cost, message counts, and the recovery post-surgery. |
| `subskills/byzantine-record.md` | `software-engineering/byzantine-record` | The written record of f, quorums, authentication, and evidence. |

## Status and honest limits

Byzantine tolerance is expensive: more replicas, more message rounds, more cryptographic work, and a threat model that must be stated to mean anything. A deployment that never names its f has not chosen a fault tolerance, and a system that mixes the crash-fault vocabulary with Byzantine claims is usually one or the other. Nothing here recommends a protocol, and no Byzantine system tolerates faults in the clients or in the code every replica shares — the model covers the replicas, not the software's own correctness.
