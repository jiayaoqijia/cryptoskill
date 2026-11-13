---
name: synthesize-findings
domain: research-operations/synthesize-findings
trigger: "\"pull this together\", \"what does the evidence say overall\", \"merge the notes into findings\"."
anti_trigger: "Publishing-shape rendering of findings for the reader (subskills/write-report.md); checking a specific claim's source trail (subskills/verify-claims.md)."
scope: "Merging verified evidence into findings: per-hypothesis verdicts, visible disagreement, deterministic arithmetic kept out of prose judgment"
status: "seedling"
---

# Synthesize findings

## Standard

- Read widely, write narrowly. Retrieval fans out; synthesis stays
 single-threaded so one mind owns the merge.
- Split the deterministic layer from the judgment layer. Arithmetic, counts,
 dates and reconciliation are computed and shown, never narrated from
 impression. The judgment layer stays visible as judgment: in that literature
 the pooled estimate was the least reproducible LLM output, matching at only
 60%.
- Every summary claim links back to study-level evidence. Traceability, not
 elegance, is what separates a synthesis from an essay (SWiM item 8).
- Guard the consensus illusion. When sources disagree, the finding is the
 disagreement with both sides cited, never a smoothed midpoint nobody holds
 (the failure mode: here it stays a rule rather than a measurement).

## Decision rules

- Numbers on the same population merge; numbers on different populations stay
 side by side with both populations named.
- A refuted hypothesis gets a finding that says refuted, with the refuting
 evidence cited. Not a quiet deletion.
- Under-determined is a valid terminal state. Write it when the corpus cannot
 settle the hypothesis.

## Procedure

1. Group the verified claims under their hypotheses.
2. Mark agreement lines and disagreement lines inside each group.
3. Compute every deterministic quantity with a script or by hand, and keep
 the inputs next to the output.
4. Write one finding per hypothesis: verdict, confidence capped by rung,
 the two or three sources that carry it.
5. Write the structural-uncertainty note for what more searching cannot
 settle.

## Anti-patterns

- Averaging away a real disagreement into a confident middle.
- A synthesis sentence with no hop back to a source span.
- Findings that introduce facts present in no source file.
- Losing ⚠️ single-source flags in the merge.

## Done checklist

- Every claim in every finding resolves to a source span in one hop.
- Every hypothesis carries its disposition.
- Disagreements appear as disagreements, with rival sources named.
- The confidence labels never exceed the best rung (source-triage ladder).

The synthesis should state which findings rest on a single lineage and which on several, because a document that presents both with equal weight has flattened the difference between a corroborated result and one source's assertion. That distinction is the synthesis, not a caveat appended to it.

## Sources

- SWiM reporting guideline: Campbell et al., BMJ 2020, https://doi.org/10.1136/bmj.l6890 (item 8 is the reporting standard for synthesis links).
- PRISMA 2020: Page et al., BMJ 2021, https://doi.org/10.1136/bmj.n71.
- Cochrane Handbook, chapter on synthesising results, https://training.cochrane.org/handbook.
