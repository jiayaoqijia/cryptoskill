---
name: leader-and-terms
domain: software-engineering/leader-and-terms
trigger: "Reading term numbers and the leader's claim to authority."
anti_trigger: "Not for split-brain outcomes alone, and not for protocol recommendations."
scope: "Term numbers, election restrictions, and the two-leaders impossibility."
status: seedling
---

# Leader and terms

## Standard

The term is the protocol's clock. Elections increment it, and every message carries the term of its sender. A member that sees a higher term steps down immediately; a leader that sees a higher term demotes itself without negotiation. The term makes authority testable: a leader's right to decide is not innate but current, and any member can prove it stale by naming a newer number.

Election restrictions close the last gap. A candidate may only win with a log at least as up to date as a quorum's, so a member that lacks committed entries cannot bury them by winning an election. This single restriction — vote only for candidates whose log is at least as long and at least as new — turns the majority vote into a statement about data completeness rather than mere liveness.

Primary sources: <https://raft.github.io/raft.pdf> and <https://dataintensive.net/>.

## Decision rules

- Record how terms are numbered and persisted across restarts.
- Record the election timeout and its relation to message round trip and clock assumptions.
- Record the log currency restriction on voting rights.
- Record what a member does on seeing a higher term, and a leader on losing majority contact.
- Record pre-vote or similar steps that prevent a temporarily-partitioned member from disrupting a healthy leader.
- Record the observable state of a leadership change, from an operator's view.

## Procedure

1. Write the term lifecycle: creation, persistence, and use in every message.
2. Derive the election timeout from the deployment's network and disk figures.
3. Locate the log currency restriction in the protocol.
4. Test the down-level-term behaviour: a member that sees a higher term steps down.
5. Test the disruption case: a rejoining member with a stale term must not force elections.
6. Write the authority model with the two-leader impossibility stated.

## Anti-patterns

- Treating the term as a counter without persistence, resetting on restart.
- An election timeout shorter than the worst legitimate heartbeat interval.
- Voting for a candidate whose log could be missing committed entries.
- Reading a leader's address as fixed state; leadership is per-term.
- Allowing a bounced member to disrupt a healthy quorum with forced elections.

## Done checklist

- [ ] Term lifecycle written.
- [ ] Timeout derived and recorded.
- [ ] Log currency restriction located.
- [ ] Step-down behaviour tested.
- [ ] Pre-vote or disruption guard verified.
- [ ] Authority model stated.

## Sources

- Raft paper and leadership: <https://raft.github.io/raft.pdf>
- Consensus background: <https://dataintensive.net/>
- Paxos comparison and roles: <https://en.wikipedia.org/wiki/Paxos_(computer_science)>
