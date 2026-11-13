---
name: single-decree-and-epochs
domain: software-engineering/single-decree-and-epochs
trigger: "Reading a protocol that agrees on one value at a time."
anti_trigger: "Not for full log replication, and not for distributed locks as a service pitch."
scope: "One value at a time, the epoch pattern, and when it is enough."
status: seedling
---

# Single-decree and epochs

## Standard

The earliest consensus protocols agreed on one value, not a log. The pattern is the epoch dance: a proposer requests permission to attempt a value from a quorum, receives the highest previously-accepted value it must respect, and then pushes its value through. Each epoch supersedes the last, and the requirement that a proposer adopt the highest accepted value rather than inventing its own is what makes agreement stable.

Single-decree lives on wherever a system needs one agreed fact rather than a sequence — the current primary in a sharded store, the identity of an epoch's coordinator, a slot in a lock sequence. The practical failure is assuming single-decree inherits the log's guarantees: each agreement is independent, and there is no commit index ordering them. The record should say which kind of agreement a system relies on, because the failure investigation differs.

Primary sources: <https://en.wikipedia.org/wiki/Paxos_(computer_science)> and <https://martinfowler.com/articles/patterns-of-distributed-systems/>.

## Decision rules

- Record whether the system's agreement object is a log of entries or discrete decided values.
- Record the epoch or ballot numbering and its persistence across restarts.
- Record the adopt-highest rule and where it is enforced in sequence.
- Read paths for a decided value: through the deciding quorum, through a lease, or unverified.
- Record what a proposer does after losing an epoch, and when to retry.
- Record what invariants the application layer must preserve around single-decree agreements.

## Procedure

1. Identify the agreement object: log or single values.
2. Write the epoch lifecycle with persistence.
3. Locate the adopt-highest rule in the message exchange.
4. Classify read paths for a decided value.
5. Determine the retry backoff for a losing proposer.
6. Write what the application must provide, such as fencing, to make single agreements useful.

## Anti-patterns

- Assuming an agreed value implies an order over separate agreements.
- Numbering epochs from volatile state and repeating them after restart.
- Letting a proposer invent its value when the quorum has accepted a higher one.
- Treating a decided value as durable without a quorum write behind it.
- Using single-decree where the query path requires ordered history.

## Done checklist

- [ ] Agreement object identified.
- [ ] Epoch lifecycle with persistence written.
- [ ] Adopt-highest rule located.
- [ ] Read paths classified.
- [ ] Retry rule recorded.
- [ ] Application duties stated.

## Sources

- Paxos single-decree reference: <https://en.wikipedia.org/wiki/Paxos_(computer_science)>
- Epoch and generation patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
- Consensus comparison: <https://dataintensive.net/>
