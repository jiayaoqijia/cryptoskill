---
name: recommender-record
domain: software-engineering/recommender-record
trigger: "Writing the record that makes the recommender's choices auditable."
anti_trigger: "Not for the log itself, and not for experiment documentation."
scope: "The written recommender record: signals, stages, rules, and their reasons."
status: seedling
---

# Recommender record

## Standard

The recommender record gathers the system's deliberately chosen, easily-misremembered facts: which signals count, what mixture each is treated as, the candidate sources and their quotas, the loss and its rationale, the bias corrections and their inputs, the final-ranking rules with parameters, the exploration budget and its allocation, and the current thresholds that end cold-start regimes. It is written for two readers: the engineer shipping the next change, who needs to know what was decided; and the analyst reading an outcome, who needs to know what the system was even doing when the outcome happened.

Its value is continuity in the face of change. Interaction semantics drift — what counted as a signal on one surface changes when the surface redesigns; loss decisions are revisited; rules tighten; the exploration budget falls out of the deployment as an oversight. Every one of those changes is recorded or the record ages into fiction; the discipline is an amendment per change, dated, with a link to what it changed in the running system, and a mirror of the shipped values so the gap between the record and the deployment is knowable.

Primary sources: <https://en.wikipedia.org/wiki/Recommender_system> and <https://en.wikipedia.org/wiki/Learning_to_rank>.

## Decision rules

- The record lists each leaf's decision points: signal weights, candidate quotas, loss class, correction methods, final-rule parameters, exploration sizes, cold-start thresholds.
- Every change to any of these is a dated amendment referencing the deployment version; the record never silently diverges from the system.
- The record names the offline evaluation definition per surface, its window, and the current primary metric.
- Regime labels — cold start vs full personalization, exploration vs organic — are listed with where they are stored so an outcome can be read in the context in which it was served.
- The record names each rule that ships on behalf of a product argument — diversity goal type, repetition window — with its owner.
- A review compares the record's stated values against the deployed configuration on a schedule; drift is a finding, not a routine.

## Procedure

1. Build the record from each leaf's decision points at design time.
2. Store a pointer to the feature and rule configuration repository alongside the record.
3. On every ship, amend the relevant sections; note the version the change rode out with.
4. Cross-reference the experiment documentation: each model or rule change links to its experiment.
5. Update the offline evaluation snapshot whenever the primary metric or window changes.
6. Schedule a record-versus-deployment diff; run it; file the mismatches.

## Anti-patterns

- A design document frozen at the system's initial launch, quietly outpaced by relate changes.
- Signal weights changed in config with no record entry; the model history becomes noise.
- No labels in the record for regimes; the analyst guesses what the system did.
- Record entries without the shipped version reference, so the gap between paper and deployed is unknowable.
- Amendments dated long after the change shipped into production.

## Done checklist

- [ ] All leaf decision points recorded.
- [ ] Amendments dated with deployment references.
- [ ] Offline evaluation snapshot current.
- [ ] Regime and exploration labels in the record's data map.
- [ ] Each rule's goal type and owner named.
- [ ] Record-versus-deployment diff scheduled and run.

## Sources

- Recommender overview: <https://en.wikipedia.org/wiki/Recommender_system>
- Learning to rank: <https://en.wikipedia.org/wiki/Learning_to_rank>
- Collaborative filtering: <https://en.wikipedia.org/wiki/Collaborative_filtering>
