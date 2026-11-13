---
name: source-triage
domain: research-operations/source-triage
trigger: "\"how good is this source\", \"can I trust this number\", \"which sources should I use\", \"is this claim solid\"."
anti_trigger: "Executing the retrieval order across engines and APIs (subskills/retrieval-cascade.md); verifying one specific claim against indexes (subskills/verify-claims.md)."
scope: "Grading every source on the trust ladder and capping each claim's confidence by rung and lineage count"
status: "seedling"
---

# Source triage and the trust ladder

## Standard

- The source-trust ladder: primary docs and source
 code, then peer-reviewed, then reputable outlets and benchmarks, then vendor
 claims, then community anecdotes, then unverified. A claim's confidence
 label may never exceed the rung of its best source.
- Independence is counted by index lineage, not engine count.
 Bing, Yahoo and DuckDuckGo share the Bing lineage and count as one source.
 Independent web indexes are the Bing lineage, Brave, Mojeek and Marginalia.
- Every number carries its population. Never cite a benchmark without naming
 what it measured: BrowseComp spans 20-31% on bare-model boards to ~92% on
 vendor model-plus-deep-research clusters, a 60-point gap under one name.
- Vendor claims enter tagged, never blended with measured numbers. A vendor's
 own benchmark is the vendor's claim about itself; treat every headline number
 as its author's own.

## Decision rules

- If only one lineage supports a claim, state it as single-source with the ⚠️
 flag and the source named.
- If the best source is a vendor claim, the confidence cap is vendor rung.
 Dress it up and the ladder is void.
- If a claim is contested (two lineages disagree), the disagreement is the
 finding, exactly as found.

## Procedure

1. Rung-tag every source at ingestion: primary, peer-reviewed, reputable,
 vendor, anecdote, unverified.
2. Population-label every number at ingestion: what was measured, on whom,
 when.
3. Count lineages per claim before assigning confidence.
4. Cap each claim's stated confidence at its best rung.
5. Mark contested claims contested. Mark single-source claims ⚠️ with the
 lineage named.

## Anti-patterns

- Three pages sharing one index presented as three independent sources.
- A vendor benchmark quoted without its population or its lineage.
- Confidence assigned by writing quality instead of source rung.
- Dropping the ⚠️ flag when a single-source number reads well.

## Done checklist

- Every source in the study carries a rung tag.
- Every number carries a population label.
- Every load-bearing claim names its lineage count.
- Every single-source claim carries ⚠️ plus the source name.

The triage decision should record what would change the rung, because a vendor claim becomes a primary source the moment the underlying data is published and a peer-reviewed paper drops a rung when its sample is shown to be unrepresentative. A rung assigned once and never revisited is a label rather than an assessment.

## Sources

- <https://training.cochrane.org>
- <https://www.cisa.gov>
