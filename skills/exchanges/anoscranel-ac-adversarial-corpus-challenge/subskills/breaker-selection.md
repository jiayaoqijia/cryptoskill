---
name: breaker-selection
domain: research-operations/breaker-selection
trigger: "\"who should run the adversarial round\", \"the reviewer keeps agreeing with the corpus\", \"make the review independent\", \"pick a red team\"."
anti_trigger: "Writing the mandate itself; scoring returned breaks; repairing the corpus after a break lands."
scope: "Selecting the breaker: independence from authorship, fresh context, lineage distance, tool access, time box, and the confirming-review failure mode"
status: "seedling"
---

# Breaker selection

## Standard

- Separation of duties is the base control: the party that approves is not the party that produced (NIST SP 800-53 Rev. 5, AC-5).
- A red team is authorised to attack a plan and is judged on findings that survive re-check, not on agreement with its authors (U.S. Army Red Team Handbook, ⚠️ edition unverified).
- Lineage matters. A breaker built by the same producers, on the same model family, shares their training priors and their framing. The blind spot is in the framing.
- Fresh context matters. The breaker reads the corpus and the charter, not the build history, the author's defence, or the earlier review threads.

## Decision rules

1. No authorship stake. The breaker did not write, plan, or repair the corpus.
2. Prefer a different model and provider lineage from the producers. If impossible, record shared lineage as a limit.
3. Give read access to the full corpus and write access to nothing.
4. Fix the time box before the round. At the box, partial dispositions ship with the untested claims named.
5. One breaker per round is normal. Split claims only when they are disjoint, and give each breaker the same charter.
6. Tool access must reach primary sources. A breaker limited to the corpus's citations can only check internal consistency.
7. Replace a breaker whose return reads as a summary or an endorsement.

## Procedure

1. Inventory candidates by model, provider, context window, and tools.
2. Exclude anyone who touched the corpus, including planning and repair.
3. Measure lineage distance. A different provider beats a different model version, which beats a new prompt.
4. Hand over the frozen corpus and the charter. Withhold author notes and prior review conclusions.
5. Set the time box, return format, and partial-return rule.
6. Ask the breaker to state, for each claim, what evidence would have broken it.
7. Check the return for the confirming-review signature before scoring.
8. Record the selection, lineage distance, and limits in the round record.

The confirming-review failure mode: the reviewer praises the corpus, restates its claims in new words, finds only typos, cites the corpus's own sources, and never names what would have broken a claim. That is not a weak round. It is not a round. Change the mandate and the breaker; do not ask the same reviewer to try harder.

## Anti-patterns

- **Author as breaker.** The producer cannot see the framing that produced the corpus.
- **Same lineage, new prompt.** A fresh prompt does not create a fresh prior.
- **Breaker with edit rights.** The first silent fix ends independence.
- **Defence brief attached.** Sending the author's rebuttal first anchors the attack.
- **Several breakers, one shared thread.** They converge; independence is lost.
- **Breaker who already reviewed the corpus.** Prior conclusions anchor the new round.

## Done checklist

- [ ] Breaker has no authorship stake.
- [ ] Lineage distance stated; shared lineage recorded as a limit.
- [ ] Read-only access confirmed.
- [ ] Time box and partial-return rule fixed before start.
- [ ] Charter sent without author notes.
- [ ] Return inspected for the confirming-review signature.
- [ ] Selection and limits written into the round record.

## Sources

- NIST SP 800-53 Rev. 5, AC-5 Separation of Duties, https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- U.S. Army, University of Foreign Military and Cultural Studies, "The Red Team Handbook" (⚠️ edition unverified; cite the copy you read).
- Stanford Encyclopedia of Philosophy, "Karl Popper", https://plato.stanford.edu/entries/popper/
