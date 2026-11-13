---
name: placement-record
domain: software-engineering/placement-record
trigger: "Writing the record for a sharding or placement decision."
anti_trigger: "Not for recommending a scheme, and not for the engine's own docs."
scope: "The written record of key, scheme, measured skew, and rebalance history."
status: seedling
---

# Placement record

## Standard

The placement record states the key, the scheme, the measured load that resulted, and the rebalances performed. Its purpose is to make the placement falsifiable: the next reader can compare the measured distribution against the design's claim, and can see whether the rebalance runbook matched the plan. Without the record, a placement scheme is a belief.

The entries that earn their space are the measured ones. The key's value distribution as measured — not assumed — the top-key share over a representative window, the hottest-shard ratio, and the movement fraction of the most recent rebalance. Together they say what the scheme produced; the design rationale says what it intended; and the gap between them is the finding.

Primary sources: <https://dataintensive.net/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the shard key, the served query shapes, and the losses accepted.
- The scheme is written executably: a reader could route a key with the text alone.
- Measured distribution is recorded with its window: top-key share and hottest-ratio.
- Rebalance events are logged with volume, duration, and abort criteria encountered.
- The mitigation in force for hot keys is recorded with its trade.
- Review triggers are dated: scale milestones, new largest tenant, scheme news.

## Procedure

1. Record the key and query shapes with accepted losses.
2. Write the routing rule in executable form.
3. Record the measured distribution and its window.
4. Log each rebalance with volume, duration, and anomalies.
5. Record hot-key mitigation and its cost.
6. Set review triggers and amend at each.

## Anti-patterns

- Recording the scheme with no measurements to confront it.
- Writing the rule in prose too vague to execute.
- Omitting rebalance history, leaving the runbook untested on paper.
- Stating mitigation with no statement of what it costs elsewhere.
- No triggers, so the record decays silently.

## Done checklist

- [ ] Key and query shapes recorded.
- [ ] Routing rule executable.
- [ ] Measured distribution recorded.
- [ ] Rebalance history logged.
- [ ] Mitigation and cost recorded.
- [ ] Triggers dated.

The record should also state what the scheme cannot express, because that is the boundary a future design will hit: if the placement is computed, the exceptions it cannot hold are the next directory service's requirement, and if it is a directory, the mappings that merely duplicate the formula are the next simplification. Writing both boundaries turns the record from a snapshot into the input to the next decision.

## Sources

- Partitioning and rebalancing: <https://dataintensive.net/>
- Stated conditions practice: <https://osf.io/prereg/>
- Distributed patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
