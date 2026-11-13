---
name: replicated-log
domain: software-engineering/replicated-log
trigger: "Reading the log a consensus protocol agrees on."
anti_trigger: "Not for event sourcing as an application pattern, and not for queue semantics."
scope: "The log as the agreement object, and what a commit index commits."
status: seedling
---

# Replicated log

## Standard

The agreement object of a consensus protocol is a log: a totally ordered sequence of entries, each carrying the value to apply and the term in which it was appended. The protocol's job is to keep the prefixes identical across the voting members. The commit index marks the boundary: entries at or below it are durable on a quorum and will never be lost while a quorum survives; entries above it are tentative and may vanish.

The subtlety that causes most operational confusion is what a commit proves. A client acknowledgement means the entry is committed, not that every member has it; followers may lag indefinitely, and a system that reports the lagging tail as failure has misread the protocol. Retrieving that lag is the leader's job during a catch-up, and the design question is whether lagging followers slow the quorum or simply fall behind it gracefully.

Primary sources: <https://raft.github.io/raft.pdf> and <https://dataintensive.net/>.

## Decision rules

- Record the log entry structure: value, term, index, and checksum.
- Record how the commit index advances and what observation proves it.
- Record what an acknowledged write means: quorum-durable, all-durable, or applied.
- Record the policy for a follower that falls behind the leader's retention.
- Record the applied state machine's relationship to the log: applied-at-commit or batched.
- Record store size bounds and the compaction or snapshot escape, since the log cannot grow forever.

## Procedure

1. Write the entry structure with its fields and their meaning.
2. Trace one acknowledgement from submission to commit index advance.
3. State precisely what the client's ack guarantees.
4. Determine what happens to a follower with an unreachable gap.
5. Record how and when the applied index is persisted.
6. Find the snapshot and compaction path that bounds the log's growth.

## Anti-patterns

- Reporting a committed write as durable on all nodes.
- Assuming a follower's lag is a failure rather than a catch-up task.
- Letting the log grow without a snapshot, waiting for the disk to decide.
- Acknowledging at acceptance instead of at commit.
- Treating log replay as uniformly idempotent without testing it.

## Done checklist

- [ ] Entry structure recorded.
- [ ] Commit path traced end to end.
- [ ] Ack semantics stated.
- [ ] Follower gap policy recorded.
- [ ] Applied index persistence recorded.
- [ ] Snapshot path found and stated.

## Sources

- Raft paper: <https://raft.github.io/raft.pdf>
- Replication chapter and consensus: <https://dataintensive.net/>
- Distributed systems patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
