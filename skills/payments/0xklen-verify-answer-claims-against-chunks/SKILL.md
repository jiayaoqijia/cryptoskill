---
name: verify-answer-claims-against-chunks
description: Use when a generated answer may state things the retrieved chunks never said. Checks every claim sentence against its cited chunk and flags or drops unsupported ones before shipping.
---

# Verify Answer Claims Against Chunks

RAG does not guarantee faithfulness: the model can blend retrieved facts with memory. Verification is mechanical — each claim must be entailed by a chunk it cites, or it does not ship.

## Procedure

1. Split the answer into atomic claims (one fact per sentence or clause) so support can be checked per claim.
2. Require a citation marker per claim and map it to the chunk id (`attach-stable-citation-ids`).
3. For each claim, check entailment against its cited chunk: an NLI model (`facebook/bart-large-mnli`) or a strict judge prompt returning `supported` / `unsupported` / `contradicted`.
4. Drop or flag any `unsupported` claim; treat `contradicted` as a hard failure that blocks the answer.
5. Flag claims whose number, date or entity does not appear verbatim in the cited chunk — numeric drift is the common fabrication.
6. Distinguish `unsupported` (not in the chunk) from `contradicted` (chunk says otherwise); they need different fixes.
7. Sample the verifier's own decisions by hand — a lenient NLI model will pass fabrications.
8. Report the faithfulness rate (supported claims / total) as a metric that must not fall when generation changes.
9. Keep the claim-to-chunk map with the answer, so a reader can see the support for each line.
10. Re-run the check on any prompt or model change; faithfulness is a property of the pair, not the model alone.

11. Store the verifier output per claim with the answer, so a rejection can be reviewed rather than re-run.

## Pitfalls

- Checking the whole answer against the whole context instead of claim-by-claim, hiding one unsupported line in a supported paragraph.
- A verifier that reads the claim and the chunk in one prompt and defers to the claim's confidence.
- Treating a paraphrase with a wrong number as supported because the rest of the sentence matches.
- Dropping the citation and keeping the claim, so an unsupported fact ships unlabelled.
- Using the same model for generation and verification with no adversarial check on the verifier.
- Ignoring `contradicted` claims because they are rarer than `unsupported` ones.

- A verifier prompt that asks 'is this consistent' and accepts topical overlap as entailment.
- Checking only claims that carry a citation, missing uncited claims added by the model.

## Verification

    python3 faithfulness.py --answer answer.md --context chunks.jsonl
    # passes when every claim resolves to a chunk and the contradicted count is 0

Report to the user: claims checked, supported/unsupported/contradicted counts, faithfulness rate, and every dropped claim with its reason.
