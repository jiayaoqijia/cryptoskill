---
name: developer-experience-metrics
domain: software-engineering/developer-experience-metrics
trigger: "Choosing metrics that describe developer experience honestly."
anti_trigger: "Not for individual performance review, and not for cost metrics."
scope: "What the metrics measure, and where they mislead."
status: seedling
---

# Developer experience metrics

## Standard

Delivery metrics describe a pipeline's behaviour: lead time for changes, deployment frequency, change failure rate, and time to restore. They were derived from research on organisational performance, and they are useful at that level. Applied to an individual or a small team they become targets, and a target that measures a pipeline invites improving the pipeline's numbers rather than the work.

The metrics that describe experience rather than delivery are different: the proportion of a week spent on unplanned work, the time to get a first change deployed in a new repository, the friction reported in a survey. Those are closer to what a platform is trying to improve, and they are harder to game because they depend on the person's account rather than on a system's log.

Primary sources: <https://dora.dev/> and <https://sre.google/>.

## Decision rules

- Record which question each metric answers, since a metric without a question becomes a target.
- Record the aggregation level: organisation, team, or individual, and never the third for delivery metrics.
- Record the metric's gaming route, since every metric has one.
- Record the survey or qualitative input alongside the quantitative, since the numbers describe systems rather than people.
- Record the baseline before any change, so improvement can be attributed.
- Record what the metric deliberately does not measure.

## Procedure

1. Record the questions the metrics should answer.
2. Choose metrics that answer them, and record the aggregation level.
3. Record the gaming route for each.
4. Pair quantitative metrics with a qualitative input.
5. Record the baseline.
6. Write the measurement plan with its limits.

## Anti-patterns

- Deploying DORA metrics at individual level, which converts them into pressure.
- A metric with no baseline, so improvement is unverifiable.
- Survey data used alone, which describes perception without behaviour.
- Optimising a lead-time number by splitting work into smaller deploys without changing the work.
- Reporting a metric without saying what it cannot show.

## Done checklist

- [ ] Question per metric recorded.
- [ ] Aggregation level recorded.
- [ ] Gaming route recorded.
- [ ] Qualitative input paired.
- [ ] Baseline recorded.
- [ ] Limits recorded.

The strongest guard against misreading a delivery metric is to name the system behaviour it actually records: deployment frequency counts pipeline events, so a team that splits a release into five deploys improves the number without changing what ships. Stating that in the definition prevents the metric from being quoted as evidence of something it never measured.


## Sources

- Software delivery performance research: <https://dora.dev/>
- Reliability and measurement practice: <https://sre.google/>
- Research context: <https://dora.dev/research/>
