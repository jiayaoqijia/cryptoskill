---
name: extraction-forms
domain: research-operations/extraction-forms
trigger: "Designing and piloting the form that turns studies into data."
anti_trigger: "Not for the analysis of extracted data, and not for the report."
scope: "Designing, piloting, and versioning the data extraction form."
status: seedling
---

# Extraction forms

## Standard

Extraction converts each included study into the raw material of the synthesis, and the form is that conversion's contract. Fields are defined before extraction begins; a pilot on a handful of studies proves the form captures what the question needs and no more; and every change after piloting is a version with a reason. A form designed after reading the studies measures whatever the studies happened to report.

The piloting catches the errors that otherwise surface at synthesis time: a field that no study actually populates, an outcome recorded in a unit nobody uses, a definition of the population that three papers read three ways. Ten studies piloted in duplicate expose nearly all of that; the form is then frozen, or versioned if the protocol allows, and the extraction proceeds with the same dual discipline as screening.

Primary sources: <https://training.cochrane.org/handbook> and <https://community.cochrane.org>.

## Decision rules

- Define every field before extraction, sourced from the protocol's outcomes and population.
- Pilot the form on a representative sample in duplicate; reconcile and revise.
- Version the form and record what changed between versions and why.
- Extract in duplicate for the first studies and whenever a field is judgment-heavy.
- Record the data source for each field: table, text, registry, or correspondence with the authors.
- Record when a field is not reported, separately from when it is zero.

## Procedure

1. Derive fields from the protocol: population, intervention, comparison, outcomes, design, and funding.
2. Pilot in duplicate on a sample of studies; note every field that forces a judgment call.
3. Revise, version, and re-pilot only if fields changed materially.
4. Extract all studies with the frozen form.
5. Resolve discrepancies by reference to the source text or author contact.
6. Archive the completed forms per study, with field-level provenance.

## Anti-patterns

- A form built from whatever the first study reports.
- Blank cells meaning both unreported and zero.
- One extractor for judgment-heavy fields like adverse events.
- Changing a field definition without a version bump.
- Extraction from the abstract rather than the full text.

## Done checklist

- [ ] Fields defined from the protocol before extraction.
- [ ] Pilot in duplicate completed and reconciled.
- [ ] Form versioned with changes recorded.
- [ ] Duplicate extraction for judgment-heavy fields.
- [ ] Field-level source recorded.
- [ ] Not-reported distinguished from zero.

## Sources

- Cochrane Handbook, data collection: <https://training.cochrane.org/handbook>
- Cochrane community resources: <https://community.cochrane.org/>
- PROSPERO registry: <https://www.crd.york.ac.uk/prospero/>
