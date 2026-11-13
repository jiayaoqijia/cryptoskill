---
name: scoring
domain: research-operations/scoring
trigger: "\"score the adversarial round\", \"how many claims did the review break\", \"the review returned findings but no verdicts\", \"count what the round actually changed\"."
anti_trigger: "Writing the attack mandate; selecting the breaker; editing the corpus after a break is confirmed."
scope: "Scoring a break round on overturned and narrowed claims, with a pre-registered rubric, failed-attack accounting, and false-positive re-checks"
status: "seedling"
---

# Scoring the round

## Standard

- The round's yield is claims overturned and claims narrowed, not findings produced. A long report that changes no claim has produced nothing.
- Publish the rubric with the charter. Pre-registration separates a test from a search for something to say (Nosek et al. 2018).
- A failed attack is a result. Corroboration means the claim survived a real attempt to break it, not that it is proven (Stanford Encyclopedia of Philosophy, Popper).
- False positives are expected. A break that dissolves under re-check is logged, never quietly dropped.
- Keep a ledger: mechanisms proposed, claims broken, narrowed, overturned, and whether the prior backlog was absorbed.

## Decision rules

1. OVERTURNED means the claim is false or unsupported as written, with primary-source evidence. The corrected statement is part of the score.
2. NARROWED means a narrower version survives. Write the narrower wording; a narrowing without wording is not scored.
3. UNCHANGED means the attack failed. The return must say what evidence would have broken the claim.
4. A secondary source can narrow a claim, not overturn it. An overturn on secondary evidence scores as a failed attack.
5. A reworded existing signal is not a new mechanism. Score it zero.
6. Material already absorbed by an integration pass scores zero when re-proposed.
7. Editing the corpus scores zero and voids the round's independence.
8. Re-check every landed break before propagation. If it dissolves, log it as a false positive and drop it from the change set.
9. Report zero as zero. A round that breaks nothing and says so is a pass.

## Procedure

1. Publish the rubric with the charter: three states, evidence tiers, and the re-check rule.
2. Normalise returns to one row per claim id.
3. Check each break's evidence tier. Secondary support narrows at most.
4. Re-check each landed break through a different reader or a different source route.
5. Log re-check failures as false positives with the reason.
6. Count broken, narrowed, unchanged, false positives, and absorbed backlog. Report counts, not only rates.
7. Write one line: what changed, what survived, what remains untested.
8. Pass the scored ledger to propagation. Keep the full return for the record.

Illustration: a round attacked eleven conclusions, broke four, narrowed five, and overturned none. That is nine changed claims and two survivors, not four findings and not a failure.

## Anti-patterns

- **Scoring by volume.** Pages and mechanisms are not yield.
- **Counting an overlap.** A reworded signal already in the corpus is not a break.
- **Secondary-source overturn.** The claim falls on evidence that cannot carry it.
- **Hiding a failed attack.** Silence makes the corpus look tested when it is not.
- **Treating zero as failure.** It pushes the next round to manufacture breaks.
- **Scoring after the returns arrive.** The rubric bends toward what was found.

## Done checklist

- [ ] Rubric published before the round.
- [ ] One row per claim id, each with a disposition.
- [ ] Every overturn carries primary-source evidence and corrected wording.
- [ ] Every narrowing carries the narrower statement.
- [ ] Every unchanged claim names what would have broken it.
- [ ] Every landed break re-checked; false positives logged.
- [ ] Counts reported with the round verdict.

## Sources

- Stanford Encyclopedia of Philosophy, "Karl Popper", https://plato.stanford.edu/entries/popper/
- Nosek, Ebersole, DeHaven, and Mellor, "The preregistration revolution", PNAS 115(11), 2018, https://doi.org/10.1073/pnas.1708274114
- Center for Open Science, "Preregistration", https://www.cos.io/initiatives/prereg
