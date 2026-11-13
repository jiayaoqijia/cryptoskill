---
name: reserve-judgment
domain: research-operations/reserve-judgment
trigger: "\"the breaker wants to re-scope the register\", \"who decides whether the claim changes\", \"record a disagreement about a break\", \"the reviewer overruled the corpus owner\"."
anti_trigger: "Selecting the breaker; scoring dispositions; applying an approved correction to files."
scope: "Reserving the re-scoping judgment: what the breaker may propose, what only the corpus owner may decide, and how disagreement is recorded"
status: "seedling"
---

# Reserve the judgment

## Standard

- Separation of duties: the party that proposes a change is not the party that approves it (NIST SP 800-53 Rev. 5, AC-5).
- Changing a criterion after seeing results is a disclosed deviation, not a repair. Pre-registration loses its meaning if the plan can be edited once the data arrive (Nosek et al. 2018).
- Rescuing a failing claim by changing the test is the evasion Popper called conventionalist. A claim saved by moving the goalposts has not survived the test (Stanford Encyclopedia of Philosophy, Popper).
- The owner holds context the breaker lacks: why the claim exists, what depends on it, and what the operation promised. The breaker holds evidence the owner may resist.

## Decision rules

The breaker may propose a disposition, supply evidence, recommend a narrowing, and flag an unrepairable row. The breaker must never decide these alone:

1. Re-scoping a pre-registered register, threshold, or criterion.
2. Deleting a claim, a row, or a file.
3. Changing the headline set or the thesis.
4. Declaring an unrepairable break repaired.
5. Accepting residual risk on the owner's behalf.
6. Editing the corpus.

The owner may accept, narrow, or overrule a break, but must record the reason. An overruled break stays visible in the record with its evidence. Silence is not a decision.

## Procedure

1. The breaker returns dispositions and evidence only.
2. The owner reads the full ledger before any file changes.
3. Classify each landed break: in scope for repair, a scope decision, or a disagreement.
4. For a scope decision, write the decision, the reason, and the residual risk accepted.
5. For a disagreement, record both positions with their evidence.
6. Publish the decision log against the corpus version.
7. Apply approved repairs; the breaker does not edit.
8. If a disagreement cannot close, hand both positions to a human and leave the claim flagged.

Disagreement record, three fields:

- Breaker's position and evidence.
- Owner's decision and reason.
- Residual risk accepted, and by whom.

Add the date and the claim id. Both parties receive the same record. A decision log without reasons is a veto list.

Illustration: when three register rows died by one signature, the breaker's job was to name the defect. Whether to narrow the rows and accept the residue was the owner's decision, recorded with its reason.

## Anti-patterns

- **Breaker re-scopes.** Evidence authority becomes decision authority.
- **Owner deletes the finding.** The break disappears and the corpus looks clean.
- **Overrule without reason.** The next round cannot tell judgment from convenience.
- **Silent acceptance.** A break is neither repaired nor recorded.
- **Repair used as scope change.** The criterion moves while the report says it held.
- **Escalation by exhaustion.** The owner waits until the breaker gives up.

## Done checklist

- [ ] Breaker returned evidence, not edits.
- [ ] Owner read the full ledger before changes.
- [ ] Each break classified as repair, scope decision, or disagreement.
- [ ] Every scope decision has a written reason.
- [ ] Every disagreement records both positions and the residual risk.
- [ ] Decision log published against the corpus version.
- [ ] Unresolved rows remain flagged for a human.

## Sources

- NIST SP 800-53 Rev. 5, AC-5 Separation of Duties, https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- Nosek, Ebersole, DeHaven, and Mellor, "The preregistration revolution", PNAS 115(11), 2018, https://doi.org/10.1073/pnas.1708274114
- Stanford Encyclopedia of Philosophy, "Karl Popper", https://plato.stanford.edu/entries/popper/
