---
name: network-meta-analysis
domain: research-operations/network-meta-analysis
trigger: "Comparing interventions that were never compared head-to-head."
anti_trigger: "Not for a simple pairwise meta-analysis, and not for deciding treatment."
scope: "Indirect comparison, transitivity, and incoherence checking."
status: seedling
---

# Network meta-analysis

## Standard

When trials compare A against B and other trials compare B against C, the network combines both to estimate A against C — an indirect comparison built on the assumption that the trials are similar in everything except the interventions being compared. That assumption is transitivity, and it is a substantive judgement about populations, co-interventions, and settings that no statistic can fully test. The geometry gives a check: where direct and indirect evidence about the same pair exist and disagree, that is incoherence, and it means at least one piece of the assumption is wrong somewhere.

The discipline follows from the assumption. Every node of the network is a different question about which trials can sit together. The proportion of the network connected by direct evidence limits what can be ranked. Ranking itself is where over-claiming lives: treatment rankings are sensitive to the model, unstable with few studies, and carry uncertainty that a league table's ordered appearance conceals.

Primary sources: <https://training.cochrane.org/handbook/current/chapter-11> and <https://handbook-5-1.cochrane.org/chapter_9>.

## Decision rules

- State the transitivity assumption as a judgement, with the characteristics compared across trials.
- Map the network geometry before estimating anything.
- Test incoherence where direct and indirect paths overlap; report the result either way.
- Treat rankings as uncertain; report rank probabilities, not a first-to-last table alone.
- Pre-specify the comparisons that matter; do not let the geometry enumerate the questions.
- Record the model, the reference treatment, and the variance structure.

## Procedure

1. Map all direct comparisons as a network graph.
2. Judge transitivity by comparing populations and designs across nodes.
3. Select the model and reference treatment; record both.
4. Estimate the network; extract the comparisons of interest.
5. Run the incoherence test where loops exist.
6. Report estimates, incoherence, and rank probabilities with uncertainty.

## Anti-patterns

- Presenting a ranking table without rank-probability uncertainty.
- Assuming transitivity because the trials share a topic.
- Testing incoherence only where it is convenient.
- Letting the network generate dozens of unplanned comparisons, all reported as findings.
- Reading a geometric node diagram as evidence that comparisons are valid.

## Done checklist

- [ ] Network geometry mapped first.
- [ ] Transitivity judged on stated characteristics.
- [ ] Model and reference recorded.
- [ ] Incoherence tested where loops exist, reported either way.
- [ ] Rankings reported with probabilities.
- [ ] Comparisons of interest pre-specified.

## Sources

- Cochrane Handbook, network meta-analysis: <https://training.cochrane.org/handbook/current/chapter-11>
- Cochrane Handbook 5.1, special topics: <https://handbook-5-1.cochrane.org/chapter_9>
- Methods articles: <https://www.biomedcentral.com/methods>
