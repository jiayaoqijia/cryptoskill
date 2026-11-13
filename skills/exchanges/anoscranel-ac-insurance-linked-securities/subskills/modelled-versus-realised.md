---
name: modelled-versus-realised
domain: investing/modelled-versus-realised
trigger: "Comparing a loss model's estimates with what has actually happened."
anti_trigger: "Not for predicting an event, and not for model selection."
scope: "Model assumptions, their revisions, and the realised record."
status: seedling
---

# Modelled versus realised

## Standard

Catastrophe models estimate the frequency and severity of events from a combination of historical data, physical modelling, and expert judgement. They are the best available tool and they have been wrong in identifiable ways: underestimating losses from events outside the historical record, mis-specifying the vulnerability of newer construction, and revising estimates substantially after a large event revealed an assumption.

Comparing model to realisation is therefore a review discipline rather than a validation. The record should state the model version, the date of the last revision, and any published comparison of modelled against realised losses for comparable perils. Where the model has been revised after an event, the revision itself is information about how the next estimate should be discounted.

Primary sources: <https://www.artemis.bm/> and <https://www.nber.org/>.

## Decision rules

- Record the model vendor, version, and revision date.
- Record the peril and region coverage of the model.
- Record any published modelled-versus-realised comparison for the peril.
- Record revisions after significant events and their direction.
- Record the assumptions the model is most sensitive to.
- Where the model has no history for a peril, record that and lower the confidence.

## Procedure

1. Record vendor, version, and revision date.
2. Record coverage and the peril's treatment.
3. Collect published comparisons where available.
4. Record past revisions and their direction.
5. Identify the sensitive assumptions.
6. Write the comparison with its confidence.

## Anti-patterns

- Treating a model output as an observed frequency.
- Using a model version without its revision date.
- Ignoring a history of upward revisions after events.
- Assuming coverage implies accuracy in a region.
- Comparing models from different vendors without disclosure.

## Done checklist

- [ ] Vendor, version, date recorded.
- [ ] Coverage recorded.
- [ ] Comparisons collected.
- [ ] Revisions recorded.
- [ ] Sensitive assumptions identified.
- [ ] Confidence stated.

The discipline that follows is to treat every expected loss figure as provisional: recording it with its version and its revision history makes the provisional nature visible, while recording a bare percentage presents a model output as if it were a property of the bond, which is exactly the misreading that produces surprise when an event behaves differently from the estimate.

A useful habit is to record the expected loss both as reported and adjusted for the model's own revision history: if a vendor has raised its loss estimates after each of the last three major events, the current figure is likely to be revised upward again, and a record that shows only the reported number treats the most recent estimate as the settled one.

## Sources

- ILS market and model information: <https://www.artemis.bm/>
- Research on catastrophic risk: <https://www.nber.org/>
- Securities disclosure context: <https://www.sec.gov/investor>
