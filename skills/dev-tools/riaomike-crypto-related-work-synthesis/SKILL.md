---
name: crypto-related-work-synthesis
description: Use when synthesizing a verified cryptography, ZKP, or lattice paper corpus into a taxonomy, historical development, claim comparison, tradeoff map, research gaps, or related-work section evidence base.
---

# Crypto Related Work Synthesis

Synthesize relations among verified works. Do not substitute topical similarity for claim-level evidence or turn a corpus gap into global novelty.

## Scope

In scope: corpus normalization, taxonomy, chronological/intellectual lineage, compatible comparison, assumption/model/parameter tradeoffs, contradictions, limitations, and evidence-linked gap statements.

Out of scope: broad discovery without a corpus, one-paper deep reading, proof verification, universal novelty, or prose polishing detached from evidence.

## Required Inputs

- screened corpus with exact versions and verification status;
- synthesis question and intended contribution/section;
- inclusion/exclusion and coverage boundaries;
- claim-evidence records or access to inspected papers.

## Success Criteria

- Work/version identity and claim-support status remain visible.
- Taxonomy axes are technically meaningful, mutually explained, and evidence-backed.
- Comparisons align security model, assumptions, parameters, functionality, and cost model.
- Historical influence/citation claims are verified rather than inferred from dates.
- Contradictions and non-comparable results remain explicit.
- Gap statements are bounded by corpus/search coverage and distinguish missing study from impossible/unknown result.

## Failure Modes

- Abstract-only corpus: produce a provisional topic map, not technical synthesis.
- Mixed/unknown versions: stop affected comparisons until reconciled.
- Incompatible metrics: qualify rather than rank.
- Sparse corpus: return coverage gaps and next-search needs.
- Advocacy request: preserve adverse closest work and counterevidence.

Never fabricate citations, relationships, priorities, theorem content, or comparative superiority.

## Workflow

1. Apply [protocol.md](references/protocol.md) to normalize the corpus and build claim-level comparison axes.
2. Construct taxonomy, lineage, tradeoff/contradiction matrix, and bounded research gaps.
3. Trace every synthesis sentence to verified corpus entries or label it interpretation.
4. Return an evidence map usable for writing, plus unresolved search/verification needs.
5. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: corpus/version summary; synthesis question; taxonomy with rationale; chronology/influence map; claim-comparison matrix; assumption/model/parameter/cost tradeoffs; contradictions; bounded gaps; evidence-linked outline; excluded/unverified items; next searches.

