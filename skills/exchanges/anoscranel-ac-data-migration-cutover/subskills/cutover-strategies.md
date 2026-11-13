---
name: cutover-strategies
domain: software-engineering/cutover-strategies
trigger: "Choosing how the move happens before doing any of it."
anti_trigger: "Not for schema migrations inside one store, and not for code rollout."
scope: "Big bang, dual write, and shadow-verify; what each risks."
status: seedling
---

# Cutover strategies

## Standard

Three strategies cover most cutovers, and each carries a distinct failure. The big bang stops writes, copies, and restarts on the new store: simple, auditable, and it buys its simplicity with an outage whose length is discovered during the outage. The dual write keeps both stores in step during a transition, backfills the old data behind it, then flips reads: no downtime, but two stores that must agree for the whole transition, and a partial write failure at either side creates divergence that compounds silently.

Shadow-verify is the honest middle: route a copy of real traffic to the new store, answer from the old, compare the two, and cut over only when the comparison has been quiet for a stated period. Its cost is building the comparison, and its risk is that the shadow only compares what it was built to compare — a path the shadow does not exercise ships unverified. The choice among the three is a bet on which failure you can afford, and the bet must be written down with the numbers.

Primary sources: <https://martinfowler.com/> and <https://www.postgresql.org/>.

## Decision rules

- Record the chosen strategy and the failure it accepts, in one sentence each.
- Record the write volume, the acceptable outage if any, and the divergence tolerance.
- For dual write: record which store is truth during the transition and how a disagreement is resolved.
- For shadow-verify: record the traffic share shadowed and the comparison coverage.
- For big bang: record the measured migration time on a full copy, not an estimate.
- Record the rollback trigger in numbers before the migration starts.

## Procedure

1. Measure the data size and the write rate.
2. Compare the three strategies against the outage tolerance and divergence tolerance.
3. Choose, and write the accepted failure in the record.
4. Design the phase gates: each phase ends at a stated criterion, not at a date.
5. Size the rollback path for the chosen strategy.
6. Rehearse on a production-shape copy before touching the real system.

## Anti-patterns

- Dual write chosen because it avoids downtime, without anyone assigned to the divergence question.
- Shadow-verify with a comparison that exercises only the happy masking path.
- A big bang whose outage estimate came from a fraction of the data.
- Phase gates written as dates rather than as measured criteria.
- No rehearsal on production volume.

## Done checklist

- [ ] Strategy chosen with accepted failure stated.
- [ ] Write volume and tolerances measured.
- [ ] Truth store and disagreement rule recorded for dual write.
- [ ] Shadow coverage recorded.
- [ ] Big-bang migration time measured on a copy.
- [ ] Rollback trigger set in numbers.

## Sources

- Migration patterns: <https://martinfowler.com/>
- Replication and copy mechanics: <https://www.postgresql.org/docs/>
- Data engineering references: <https://www.distributed-systems.net/>
