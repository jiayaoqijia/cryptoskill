---
name: propagate-breaks
domain: research-operations/propagate-breaks
trigger: "\"a break landed and the corpus still says the old thing\", \"propagate a corrected number\", \"the same wrong figure appears in four files\", \"record an amendment\"."
anti_trigger: "Scoring the round; deciding whether a claim should be re-scoped; running the breaker."
scope: "Propagating landed breaks: dated amendments, root-fix-then-propagate, the dependency sweep, register versus corpus defects, and unrepairable claims"
status: "seedling"
---

# Propagating breaks

## Standard

- Amend beside the claim; never rewrite the base body. The old claim stays visible beside the correction. A silent rewrite destroys the audit trail and hides whether the claim was salvageable.
- Fix at the root, then propagate. A wrong input moves through every derived quantity (JCGM 100:2008).
- Keep provenance traceable: each corrected figure names its source and owning file (W3C PROV-O).
- Re-verify the shipped state, not the reviewed one. Corrections can contradict a line nearby.

## Decision rules

1. Never rewrite the base body. Add a dated amendment block: claim id, old claim, new fact, source, and fix location.
2. Correct the owning file first, then each dependent, with recomputation shown.
3. Search the old value, claim wording, metric name, and derivatives: rates, costs, totals, rankings.
4. Put `base_body_superseded:` in the frontmatter, naming the old value and the correction's location.
5. When two files disagree, fix the shared root. Do not pick a winner and edit the loser.
6. Name a register defect as a plan defect. Apply the finite residue once by narrowing rows in place; never re-sample until the criterion passes.
7. A repair needing new measurement is unrepairable: keep the ⚠️ flag, name the open thread, attach no unsupported citation.
8. Re-verify after wording fixes as well as numeric ones.

## Procedure

1. Collect landed breaks and ids.
2. Find the file that owns each claim or calculation.
3. Correct the root; show old value, new value, arithmetic.
4. Run the sweep with every rule-3 key.
5. Recompute each dependent and mark it changed.
6. Write the amendment block in every affected file.
7. Re-verify the shipping artifact, fix wording, verify again.
8. Log what changed, what remains, what is unrepairable.

Illustrations:

- A flat per-pass cost of fourteen requests became eleven core calls plus an age-scaled term, nineteen to twenty-eight on old items; four files needed recomputation.
- A ten-row register returned seven survivors against a threshold of eight; three rows died by one signature because no task was assigned to source them. That is a plan defect: narrow once, file the decision, do not re-sample.
- An actor count returned two, six, and eight across routes. It reconciled to six but was not verified, so the claim stayed flagged and a frozen account list became the open thread.

## Anti-patterns

- **Silent rewrite.** The corpus looks clean and the audit trail is gone.
- **Local patch.** One file is fixed; four others still state the old figure.
- **Re-sample until it passes.** Manufactures a pass and corrupts the criterion.
- **Citation padding.** A source is attached that does not support the claim.
- **Skipping the shipped state.** The reviewed version is verified, the released one is not.

## Done checklist

- [ ] Every landed break has an amendment block.
- [ ] The owning file was corrected first.
- [ ] Sweep covered values, wording, metric names, derivatives.
- [ ] Dependent figures were recomputed visibly.
- [ ] Superseded base bodies are flagged in frontmatter.
- [ ] Register defects are named and not re-sampled.
- [ ] Unrepairable claims keep a ⚠️ flag and an open thread.
- [ ] The shipped state was re-verified after all fixes.

## Sources

- JCGM 100:2008, "Evaluation of measurement data — Guide to the expression of uncertainty in measurement", https://www.bipm.org/en/publications/guides
- W3C, "PROV-O: The PROV Ontology", https://www.w3.org/TR/prov-o/
- Nosek, Ebersole, DeHaven, and Mellor, "The preregistration revolution", PNAS 115(11), 2018, https://doi.org/10.1073/pnas.1708274114
