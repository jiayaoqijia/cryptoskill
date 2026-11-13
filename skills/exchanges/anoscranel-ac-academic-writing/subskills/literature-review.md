---
name: literature-review
domain: writing/literature-review
trigger: "\"write a lit review\", \"systematic review\", \"PRISMA\", \"screening criteria\", \"synthesise these studies\", \"protocol registration\"."
anti_trigger: "Reporting an original study (subskills/academic-papers.md); finding and judging sources before drafting; binding claims to checkable sources."
scope: "Narrative vs systematic reviews; search, screen, synthesise, PRISMA"
status: "seedling"
---

# Literature review

## Standard

- **Narrative and systematic are different instruments.** A systematic review needs a pre-registered protocol, an exhaustive search, dual independent screening and a structured synthesis. A narrative review organises a topic by argument.
- **PRISMA 2020 is the reporting standard.** It has 27 items in seven sections plus a 12-item abstract checklist (Page et al., *BMJ* 2021; 372:n71, https://doi.org/10.1136/bmj.n71). Items 8, 9 and 11 require "details of automation tools used".
- **Registration is the record-irreversible act.** PROSPERO requires a full protocol before registering, and "submissions must be made before data extraction commences (from October 2019)". Once processed, it locks.
- **Dual independent review is a conduct requirement about people.** Cochrane requires at least two people working independently on full-text selection. A review can be PRISMA-compliant while violating this.
- **Certainty is a judgement with eight named domains.** GRADE rates each critical outcome high, moderate, low or very low across five downgrade and three upgrade domains.
- **Automation belongs on the mechanical side.** Flow-diagram arithmetic, per-source search completeness and registration timestamps are checkable. Eligibility adequacy, synthesis choice and every rating are judgement.

## Decision rules

1. State the review type at the top; a systematic claim demands the systematic machinery.
2. Full search strategies are reported per source, with the date last searched.
3. Screening logs record reviewer counts per record and whether selection was independent.
4. Synthesis without meta-analysis follows SWiM's nine items: grouping, metric, method, presentation, summary, limitations.
5. Every inclusion and exclusion carries a reason.
6. Agent output is labelled `missing`, `present`, `unverifiable` or `inconsistent` — never a verdict.
7. Registration happens before extraction; a human holds the registry write access.

## Procedure

1. Write the question with explicit eligibility criteria and the grouping for syntheses.
2. Draft the protocol and register it before any extraction; record registry and number.
3. Run the search across databases, registers and websites; log strategy and date per source.
4. Screen by title and abstract, then full text in duplicate; record counts and disagreements.
5. Extract data in duplicate; log assumptions about missing data.
6. Appraise risk of bias per study with the design-matched tool.
7. Synthesise: state the metric and method, present per-study results.
8. Rate certainty per outcome across all eight domains.
9. Report the flow diagram and check the arithmetic: identified = included + excluded + not retrieved + duplicates removed.
10. Hand the human the draft, check log and flag list. **The human registers and publishes.**

## Anti-patterns

- Calling a narrative review systematic.
- A flow diagram whose numbers do not sum.
- Registration dated after extraction began.
- An agent-completed checklist presented as a verified one.
- A certainty rating with no domain-by-domain reasoning.

## Done checklist

- [ ] Review type stated; protocol registered before extraction.
- [ ] Search strategy and last-searched date reported per source.
- [ ] Dual independent screening recorded.
- [ ] Every inclusion and exclusion carries a reason.
- [ ] Flow-diagram arithmetic verified.
- [ ] Certainty rated per outcome across all eight domains.
- [ ] **Human-gated:** registered and published by a named person.

## Sources

- https://doi.org/10.1136/bmj.n71 · https://crd.york.ac.uk/prospero/
