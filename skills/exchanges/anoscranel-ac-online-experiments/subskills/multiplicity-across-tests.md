---
name: multiplicity-across-tests
domain: software-engineering/multiplicity-across-tests
trigger: "Keeping a fleet of experiments and metrics from manufacturing findings."
anti_trigger: "Not for a single experiment's power, and not for prompt eval sweeps."
scope: "Many tests, many metrics, and the corrections that keep a fleet honest."
status: seedling
---

# Multiplicity across tests

## Standard

A platform running a dozen concurrent experiments, each reading twenty metrics on ten segments, performs thousands of implicit comparisons per day. At a five percent false-positive rate, uncorrected noise will produce "wins" on schedule; the more places a team looks, the more it will find, and the finding is a property of the looking. The standard defences are structural: hierarchy — guardrails and the OEC carry decision rights; everything else is exploratory and labelled as such — and correction, where a family of comparisons is tested together with an adjusted threshold.

The correction decision starts with defining the family. Correcting across everything destroys power; correcting across nothing publishes noise. A defensible line is: correct inside an experiment, label across the fleet, and require replication for any exploratory finding that a team wants to promote to a decision. The promotion rule matters more than any specific correction formula.

Primary sources: <https://en.wikipedia.org/wiki/Multiple_comparisons_problem> and <https://experimentguide.com/>.

## Decision rules

- Pre-declare the metric hierarchy at platform level: OEC, guardrails, then exploratory.
- Limit decision rights to the pre-declared hierarchy; exploratory movers generate hypotheses, not launches.
- Within an experiment, correct for the number of metrics the team will jointly assess.
- Record every metric examined, including the ones nobody reported.
- Require an independent replication before an exploratory finding drives a decision.
- Watch for overlapping experiments on shared surfaces; interaction conflicts are multiplicity too.

## Procedure

1. Classify all metrics into OEC, guardrail, and exploratory tiers.
2. Choose the correction family inside each experiment (all jointly-read metrics).
3. Apply the correction to the family; leave tiered labels visible in reports.
4. Log every lookup of a metric from the experiment's data, not only reported results.
5. Replicate the exploratory findings that matter before promoting them.
6. Record the multiplicity policy and any promotion decisions.

## Anti-patterns

- Running many metrics and reporting the single significant one as the result.
- A platform "winner's page" that feeds off uncorrected exploratory movers.
- Treating any significant segment as a discovery without replication.
- Ignoring hidden multiplicity from many experiments hitting the same metric.
- Applying a blanket correction that destroys the power of the OEC itself — the family was drawn too wide.

## Done checklist

- [ ] Metric hierarchy pre-declared.
- [ ] Correction family chosen per experiment.
- [ ] Exploratory findings labelled as hypotheses.
- [ ] All metric lookups logged.
- [ ] Replication before promotion.
- [ ] Policy and decisions recorded.

## Sources

- Multiple comparisons problem: <https://en.wikipedia.org/wiki/Multiple_comparisons_problem>
- Fleet-scale experimentation: <https://experimentguide.com/>
- Sample size context: <https://en.wikipedia.org/wiki/Sample_size_determination>
