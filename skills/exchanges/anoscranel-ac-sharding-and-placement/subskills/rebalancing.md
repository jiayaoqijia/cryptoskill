---
name: rebalancing
domain: software-engineering/rebalancing
trigger: "Moving data between shards without stopping the writes."
anti_trigger: "Not for the initial placement, and not for backup restore."
scope: "Movement cost, split-by-key, directory re-pointing, and doing it live."
status: seedling
---

# Rebalancing

## Standard

Rebalancing is the operation every placement design eventually owes. It moves a subset of the key space to new owners while traffic continues, and its cost is measurable in advance: in the size of the data moved, the duration of any ownership ambiguity, and the state a failure can leave behind. With consistent hashing the fraction is bounded by the scheme; with fixed ranges the split is by explicit keys; with a directory the move is an update to a mapping rather than to the data.

Doing it live means the system tolerates two owners briefly or none. The two designs in practice are dual-write — send to both old and new owner, verify, then cut reads over — and ownership transfer — the new owner catches up from the old, the mapping flips atomically, and the old owner demotes. Each has a failure state, and rehearsing that state before the first rebalance is the difference between an operation and an outage.

Primary sources: <https://dataintensive.net/> and <https://martinfowler.com/articles/patterns-of-distributed-systems/>.

## Decision rules

- Record the movement volume for a planned rebalance, and its time estimate at transfer rates.
- Record the ownership model during the move: dual-write, catch-up-then-flip, or freeze.
- Record the verification step that proves the new owner complete before reads move.
- Record what a failure mid-move leaves behind and the recovery action for each state.
- Record throttling that protects live traffic during movement.
- Record the rollback: what moves back, and what the window for that decision is.

## Procedure

1. Compute moved volume and time at realistic rates.
2. Choose the ownership model for the move.
3. Define the completeness check on the destination.
4. Rehearse the failure states and name the recovery action.
5. Set movement throttling and its live-traffic priority.
6. Write the runbook with the abort criteria stated before starting.

## Anti-patterns

- Estimating movement time at network line rate rather than demonstrated throughput.
- Cutting reads before verifying destination completeness.
- No rehearsed failure state, discovering recovery during production.
- Moving everything when the scheme bounds movement at a fraction.
- No throttle, starving live requests behind the migration.

## Done checklist

- [ ] Movement volume and duration estimated.
- [ ] Ownership model chosen.
- [ ] Completeness check defined.
- [ ] Failure states rehearsed.
- [ ] Throttling set.
- [ ] Abort criteria written in advance.

## Sources

- Rebalancing and resharding: <https://dataintensive.net/>
- Distributed systems patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
- Shard architecture: <https://en.wikipedia.org/wiki/Shard_(database_architecture)>
