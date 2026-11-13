---
name: adversarial-pass
domain: research-operations/adversarial-pass
trigger: "\"stress-test this conclusion\", \"what would prove this wrong\", \"attack this report\", \"find the counter-evidence\"."
anti_trigger: "First-pass verification of claims and citations (subskills/verify-claims.md); the stop decision itself (subskills/stop-rules.md)."
scope: "Attacking the draft's conclusions: strongest counter-hypothesis per claim, opposition queries, hypothesis dispositions"
status: "seedling"
---

# The adversarial pass

## Standard

- The pass runs at the merge, because the merge is where errors concentrate:
 84.7% of final-report errors originate at the orchestrator, not in the
 retrieved leaves (arXiv 2608.24306, EMNLP 2026).
- Every hypothesis ends the pass with one of three dispositions: confirmed,
 refuted, or under-determined. "Read a lot" is not a disposition.
- Authority and polish are attack surfaces, not safety signals: high-authority
 injected documents drove 48.0% false-conclusion adoption versus 36.8% for
 low-authority, and paper-style prose beat post-style 48.0% to 29.7%
 (MisKnow benchmark, 2025).
 Inspect the convenient, authoritative citation hardest.
- The pass searches for disconfirming evidence with fresh lineages. Re-running
 the same engines that built the draft finds the same draft.

## Decision rules

- The deeper the stake, the harder the pass. A verdict memo for money gets the
 full loop; a literature map gets the loop on its three load-bearing claims.
- If counter-evidence and evidence balance, the report says so. A tie is a
 finding, not a verdict to force.
- If the disconfirmer named at scoping shows up, the hypothesis is refuted.
 Name it refuted.

## Procedure

1. List the claims the verdict depends on.
2. For each, write the strongest counter-hypothesis an informed opponent
 would hold.
3. Run opposition queries against fresh lineages for each counter.
4. Re-check populations: was the number measured on the population the draft
 claims.
5. Disposition every hypothesis: confirmed, refuted, under-determined.
6. Record what future evidence would change the verdict; those become the
 refresh targets.

## Anti-patterns

- A confirmation-only sweep called an adversarial pass.
- Counter-queries through the same lineage that produced the draft.
- Softening a refuted hypothesis into "mixed evidence" because a source was
 pleasant to read.
- Skipping the pass because the corpus feels big. The MisKnow result says a
 confident corpus is exactly where planted error wins.

## Done checklist

- Every hypothesis carries a written disposition.
- At least one genuine opposition query ran per load-bearing claim, or the
 reason it could not is stated.
- The refresh-target list exists, even if short.

The pass is more useful when it is aimed at the conclusion the author is most confident in rather than the one that feels weakest, since the confident conclusion is the one that received the least scrutiny on the way in. An attack that only finds faults in the hedged claims has found the hedging, not the error.

## Sources

- MisKnow benchmark, 2025 preprint, indexed at <https://arxiv.org> (cite the version you check).
- PRISMA 2020: Page et al., BMJ 2021, https://doi.org/10.1136/bmj.n71.
