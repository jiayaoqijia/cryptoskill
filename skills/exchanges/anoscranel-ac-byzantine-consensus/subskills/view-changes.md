---
name: view-changes
domain: software-engineering/view-changes
trigger: "Replacing a Byzantine primary suspected of being the faulty node."
anti_trigger: "Not for leader election in crash systems, and not for protocol selection."
scope: "Replacing a suspected primary without losing committed work."
status: seedling
---

# View changes

## Standard

In a Byzantine system the primary may itself be the fault: it can sign wrong sequence numbers, send different requests to different replicas, or simply stop. A view change replaces it while guaranteeing the one property everything else depends on — nothing committed in the old view is lost. That guarantee is the reason prepared values are exchanged during the change: a new primary is chosen only after enough replicas testify about what the old view had finalized, so the successor inherits the committed history rather than inventing one.

The subtle failure is timing. A replica that times out declares the primary suspect, but its peers may be running slightly behind and still processing the old view's messages. The protocol resolves this by requiring a view-change quorum before the new view is installed and by having replicas refuse messages from a view older than their own, so a half-completed change cannot fork the membership into two views that both believe they are current.

Primary sources: <https://pmg.csail.mit.edu/papers/osdi99.pdf> and <https://en.wikipedia.org/wiki/PBFT>.

## Decision rules

- Record the timeout that triggers suspicion and its relation to the protocol's steady-state latency.
- Record the view-change quorum and the new primary's selection rule.
- Record how prepared values survive the change and into the new view.
- Record how the system rejects stale-view messages after a change.
- Record what happens when two view changes occur back-to-back.
- Record the operator's visible signal that the deployment is changing views repeatedly.

## Procedure

1. Trace a view change from timeout to new-primary installed.
2. Follow one prepared value from the old view into the new.
3. Trace a delayed message from the old view meeting the new.
4. Trace a second change beginning before the first completes.
5. Record the threshold at which repeated view changes alarm.
6. Write the change protocol with the committed-work guarantee stated.

## Anti-patterns

- Timing out shorter than steady-state latency, thrashing view changes.
- Discarding prepared values at the change and losing committed work.
- Accepting old-view messages after installing a new view.
- Selecting the new primary without the quorum's testimony.
- Assuming a view change is rare in a faulty cluster; it is the common path.

## Done checklist

- [ ] Change traced end to end.
- [ ] Prepared value carried through.
- [ ] Stale-view rejection traced.
- [ ] Consecutive changes traced.
- [ ] Alarm threshold set.
- [ ] Committed-work guarantee stated.

## Sources

- PBFT view changes: <https://pmg.csail.mit.edu/papers/osdi99.pdf>
- View change reference: <https://en.wikipedia.org/wiki/PBFT>
- Leader-replacement patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
