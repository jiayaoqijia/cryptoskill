---
name: subgroups-and-meta-regression
domain: research-operations/subgroups-and-meta-regression
trigger: "Testing whether a characteristic explains heterogeneity."
anti_trigger: "Not for narrative synthesis, and not for exploratory story-building."
scope: "Moderator analysis done as pre-specified test, not story."
status: seedling
---

# Subgroups and meta-regression

## Standard

A subgroup analysis splits the studies by a characteristic and pools within each split. Meta-regression models the effect as a function of one or more study-level characteristics. Both are justified only when the moderator was named in the protocol, when a plausible mechanism connects it to effect size, and when enough studies exist to give the test meaning. Between them, the protocol is the difference between a hypothesis test and a story assembled after seeing the forest plot.

The multiplicity trap is the standard failure. With ten candidate moderators and a handful of studies, something will reach a conventional threshold by chance; a cut at p less than 0.05 across many unadjusted tests manufactures findings. The ecological trap is subtler and worse: a moderator measured at study level can show an association that patient-level data would not, because the association rides on differences between studies rather than differences between people. Subgroup findings from few studies are hypotheses for the next review, not conclusions of this one.

Primary sources: <https://training.cochrane.org/handbook/current/chapter-10> and <https://training.cochrane.org/handbook/current/chapter-12>.

## Decision rules

- Perform only protocol-specified moderator analyses; exploratory runs are labelled exploratory.
- Require a stated mechanism linking the moderator to the effect.
- Test the difference between subgroups; separate significance within subgroups is not interaction.
- State the number of moderators examined and any multiplicity handling.
- Interpret study-level associations ecologically; never as patient-level claims.
- Treat few-study moderator findings as hypothesis-generating.

## Procedure

1. List the protocol-specified moderators and their mechanisms.
2. Compute the between-subgroup heterogeneity or the meta-regression slope.
3. Run each specified test once; record every run including non-significant ones.
4. Report the number of tests and how significance was evaluated.
5. Distinguish within-subgroup estimates from the between-subgroup test.
6. Ballot exploratory findings explicitly as hypotheses for future reviews.

## Anti-patterns

- Running every searchable moderator and presenting the significant one.
- Interpreting significance in both subgroups as a difference between them.
- Reporting a patient-level conclusion from study-level data.
- Splitting on characteristics defined after seeing the results.
- Claiming a mechanism after the test rather than before.

## Done checklist

- [ ] Moderators pre-specified with mechanisms.
- [ ] Between-subgroup test computed.
- [ ] Every run recorded, significant or not.
- [ ] Test count and multiplicity handling stated.
- [ ] Ecological interpretation maintained.
- [ ] Exploratory results labelled as hypotheses.

## Sources

- Cochrane Handbook, subgroup analyses: <https://training.cochrane.org/handbook/current/chapter-10>
- Cochrane Handbook 5.1, heterogeneity investigation: <https://handbook-5-1.cochrane.org/chapter_9>
- Special topics chapter: <https://training.cochrane.org/handbook/current/chapter-12>
