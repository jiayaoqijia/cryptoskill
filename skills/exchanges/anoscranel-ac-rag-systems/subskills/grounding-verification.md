---
name: grounding-verification
domain: prompt-engineering/grounding-verification
trigger: "Checking the generated answer against the retrieved passages."
anti_trigger: "Not for prompt writing, and not for model evaluation."
scope: "Checking the answer against retrieved text after generation."
status: seedling
---

# Grounding verification

## Standard

The generation stage is asked to answer only from retrieved text, and it will usually comply — but not always, and the failure is invisible without a check. Verification reads the generated answer against the passages actually retrieved and asks a narrow question: is each claim supported by the passages, and did anything in the answer appear from nowhere? The check is mechanical in spirit — a second pass over text that both exists — even where the judge of "supported by" is itself a model.

The narrowness is what makes it affordable. Verifying every answer with a second model pass doubles the cost; verifying a sample, or all high-stakes answers, or answers whose generation showed the markers of drift (specific numbers not in passages, entity names absent from text) catches the bulk at a fraction of the price. The design decision is what triggers a verification, and the record states it because every trigger catches false positives too.

Primary sources: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview> and <https://docs.anthropic.com/en/docs/build-with-claude/citations>.

## Decision rules

- State the verification trigger before deciding the checker: sample rate, stakes, or drift markers.
- Check support at the claim level against the retrieved passages actually in the prompt.
- Unsupported claims are flagged, corrected, or the answer is refused — the response path is designed, not improvised.
- Verification results join the failure taxonomy: misbinding, fabrication, and conflation are different failures with different fixes.
- When a "supported by" check is a model, its own false-positive rate is measured.
- Verify the verifier periodically against a labelled set; a checker that passes everything is the failure mode.

## Procedure

1. Choose the trigger: what fraction of answers, and on what marker.
2. Run the support check at claim level against the prompt's passages.
3. Route failures by class: fabrication, conflation of two passages, and out-of-passage knowledge have different causes.
4. Measure and log the failure classes with sampled false positives.
5. Fix at the stage that failed: retrieval, prompt citation binding, or generation.
6. Re-run the labelled set periodically to keep the verifier honest.

## Anti-patterns

- Treating verification as too expensive and skipping it on high-stakes answers because they are costly.
- Verifying whole answers instead of claims; detail hides in whole-answer judgments.
- A verifier with no false-positive measurement.
- Sending the checker the passages with no identifiers; misbinding cannot be caught.
- Improvised failure handling — the response path is part of the design.

## Done checklist

- [ ] Trigger determined and stated.
- [ ] Claim-level check against prompt passages.
- [ ] Failure classes routed with designed responses.
- [ ] Misbinding included in the taxonomy.
- [ ] Verifier false-positive rate measured.
- [ ] Verifier re-checked on a labelled set periodically.

## Sources

- RAG architecture and verification stages: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview>
- Citation-enabled answering: <https://docs.anthropic.com/en/docs/build-with-claude/citations>
- Original RAG paper: <https://arxiv.org/abs/2005.11401>
