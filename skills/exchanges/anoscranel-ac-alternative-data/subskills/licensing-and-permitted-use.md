---
name: licensing-and-permitted-use
domain: investing/licensing-and-permitted-use
trigger: "Checking what a data licence permits before relying on the data."
anti_trigger: "Not for legal advice, and not for procurement."
scope: "Terms, redistribution, derived data, and the compliance constraint."
status: seedling
---

# Licensing and permitted use

## Standard

A data licence specifies what may be done with the data: whether it may be used internally only, whether derived outputs may be shared, whether the raw records can be stored beyond a term, and whether the data can be combined with other sources. Those terms are operational constraints rather than legal footnotes, because a strategy built on data that cannot be redistributed produces results that cannot be shown to anyone.

The derived-data question is the one that most often surprises. A model trained on licensed data, or a feature computed from it, may be treated as a derived work subject to the same restrictions, which can prevent a fund from describing its process. The record should state what the licence permits at each stage: ingest, storage, computation, and disclosure.

Primary sources: <https://www.sec.gov/investor> and <https://www.nber.org/>.

## Decision rules

- Record the permitted uses: internal, redistribution, derived outputs.
- Record the storage term and any deletion obligation.
- Record restrictions on combining with other sources.
- Record whether derived features or models are treated as covered.
- Record the disclosure constraints that follow for external reporting.
- Record the questions reserved for legal review rather than assumed.

## Procedure

1. Read the licence and list the permitted uses.
2. Map each stage of the process to a permission.
3. Identify the stages where permission is unclear.
4. Record the disclosure constraints.
5. Note the questions for counsel.
6. Write the permitted-use summary.

## Anti-patterns

- Assuming a licence permits redistribution because the data was purchased.
- Treating derived features as unencumbered.
- Ignoring a storage term that requires deletion.
- Overlooking restrictions on combining sources.
- Resolving an ambiguous term by assumption rather than by review.

## Done checklist

- [ ] Permitted uses listed.
- [ ] Storage term recorded.
- [ ] Combination restrictions recorded.
- [ ] Derived-data treatment recorded.
- [ ] Disclosure constraints recorded.
- [ ] Counsel questions listed.

A practical approach is to record the licence as a table of stages against permissions, since the terms are rarely uniform and a summary sentence loses the distinction between storing data for a year and holding a derived aggregate indefinitely.


The practical consequence is that licence terms should be read before the research is designed, since a restriction discovered after a year of work may make the entire result undisplayable and force the analysis to be redone on a different source.


## Sources

- Disclosure and market-participant context: <https://www.sec.gov/investor>
- Research practice on data governance: <https://www.nber.org/>
- Investor education on data and research: <https://www.investor.gov/introduction-investing>
