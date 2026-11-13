---
name: membership-changes
domain: software-engineering/membership-changes
trigger: "Adding or removing voting members without breaking the quorum invariant."
anti_trigger: "Not for learner seeding alone, and not for configuration management."
scope: "Joint configurations, the invariant during transition, and learner seeding."
status: seedling
---

# Membership changes

## Standard

Changing the voter set is the most delicate operation in a consensus deployment. The quorum intersection invariant holds within one configuration; between two it can silently fail. If members switch from a three-voter configuration to a five-voter configuration at different moments, there can be an instant where two disjoint groups each believe they hold a majority — one in the old configuration, one in the new — and both accept writes.

The joint-configuration pattern closes the gap. The change is committed as a special log entry describing both old and new configurations, and every member votes under both during the transition. No quorum can form without members from the old majority, so the invariant survives the switch, and the configuration change itself becomes a committed, ordered event rather than a race.

Primary sources: <https://raft.github.io/raft.pdf> and <https://dataintensive.net/>.

## Decision rules

- Record the exact sequence of a membership change and the committed entry that drives it.
- Record whether the deployment uses joint configurations, single-server changes, or something else.
- Record the worst-case transition where two disjoint majorities could coexist, and the mechanism preventing it.
- Record the learner seeding step: a new voter catches up before being granted a vote.
- Record the rollback path for a change that stalls mid-transition.
- Record the operator's safety rule for changing one member at a time.

## Procedure

1. Write the membership-change sequence with the committed entry in it.
2. Test the boundary: what happens when old and new configurations disagree on a quorum.
3. Verify learner seeding requires catch-up before a vote.
4. Find the stall detection and rollback path.
5. Write the operator's rule for how many members may change at once.
6. Trace a full change: propose, seed, commit, switch, catch-up.

## Anti-patterns

- Restarting members into a new configuration without committing the change.
- Granting votes before a new member has caught up.
- Changing two members concurrently in a small cluster.
- Treating a stalled transition as a failure without a rollback.
- Assuming single-server changes are automatically safe without seeing them traced.

## Done checklist

- [ ] Change sequence written.
- [ ] Boundary case tested.
- [ ] Learner seeding verified.
- [ ] Rollback path found.
- [ ] Operator rule written.
- [ ] Full change traced.

The operator's rule also deserves a stated worst case: in a three-voter cluster, two concurrent single-server changes can each be safe alone while jointly removing the quorum, so even single-server changes need to be sequenced explicitly and the record should name the sequence.

## Sources

- Raft membership section: <https://raft.github.io/raft.pdf>
- Consensus in production systems: <https://dataintensive.net/>
- Paxos membership background: <https://en.wikipedia.org/wiki/Paxos_(computer_science)>
