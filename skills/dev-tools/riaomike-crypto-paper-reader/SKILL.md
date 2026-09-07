---
name: crypto-paper-reader
description: Use when deeply reading one cryptography, ZKP, or lattice paper to extract its claims, definitions, proof structure, assumptions, parameters, evidence, costs, limitations, and research implications.
---

# Crypto Paper Reader

Produce a version-specific research record, not a generic summary. Keep the authors' claims separate from what was independently checked.

## Scope

In scope: one focal work and its versions/supplements/artifacts; claim and definition extraction; proof/reduction map; security model; ZKP/lattice details; parameter/cost evidence; limitations; dependency and follow-up map.

Out of scope: exhaustive literature search, global novelty, full independent proof certification, or paper rewriting.

## Required Inputs

- exact paper or accessible identifier/version;
- desired depth and research purpose;
- supplements/artifacts when claims depend on them;
- target questions, if any.

## Success Criteria

- Exact version and accessible components are recorded.
- Contributions become atomic claims with evidence locations/status.
- Definitions, assumptions, security notions/models, parameters, failure terms, and cost models are explicit.
- Proof dependency/implication structure and omitted obligations are visible.
- ZKP/lattice-specific distinctions are extracted when applicable.
- Limitations, unresolved questions, closest cited dependencies, and reusable insights are separated from speculation.

## Failure Modes

- Abstract/snippet only: return an abstract-level map and mark technical claims unverified.
- Inaccessible supplement/artifact: mark dependent claims unverified.
- Version conflict: preserve both and identify which supports each extracted item.
- Undefined notation: reconstruct only when derivable; label reconstruction.
- Overloaded request covering many papers: ask to choose a focal paper or route to literature/related-work skills.

Never invent bibliographic details, theorem content, proof steps, parameters, experiments, or citations.

## Workflow

1. Freeze exact source/version and accessible components.
2. Apply [protocol.md](references/protocol.md) from problem framing through claim/evidence/proof/parameter extraction.
3. Distinguish author claim, source evidence, reviewer check, and residual uncertainty.
4. Build follow-up questions and citations that require separate verification.
5. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: citation/version record; one-paragraph problem/contribution orientation; terminology/definition table; claim-evidence matrix; proof/reduction dependency map; security/ZKP/lattice model; parameter and cost ledger; experiment/artifact map; limitations/gaps; related dependencies; research takeaways and follow-up questions.

