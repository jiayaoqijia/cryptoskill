---
name: literature-search
description: Use when conducting citation-sensitive cryptography, ZKP, or lattice literature discovery, prior-art mapping, closest-work comparison, or a bounded novelty search.
---

# Literature Search

Build a reproducible, version-aware evidence set and bounded conclusions. Discovery breadth and citation verification are separate stages.

## Scope

In scope: question decomposition, query design, multi-source discovery when available, screening, version deduplication, citation chaining, bibliographic verification, claim extraction, and closest-work comparison.

Out of scope: claiming exhaustive global coverage, guaranteeing novelty, fabricating inaccessible metadata, or treating search snippets and generated summaries as paper evidence.

## Required Inputs

- research question or candidate contribution;
- domain boundaries, date/language constraints, and relevant security/model distinctions;
- required deliverable: bibliography, map, related-work synthesis, or bounded novelty assessment;
- available source-access capabilities.

Clarify only boundaries that materially change inclusion or the novelty comparison. Record all other assumptions.

## Success Criteria

- Queries, sources, dates, filters, inclusion/exclusion decisions, and coverage limits are reproducible.
- Duplicate versions are linked while material differences remain visible.
- Each included citation has verified identity or an explicit unverified status.
- Claims are extracted from inspected documents, with source locations and model/parameter context.
- Closest prior art is compared claim by claim.
- Any negative/novelty conclusion is bounded by the actual search coverage.

## Failure Modes

- No network/database access: design the search strategy and process supplied sources, but label discovery and novelty coverage not executed.
- Inaccessible full text: keep bibliographic discovery separate from claim support; do not infer theorem content from title/abstract/snippet.
- Conflicting versions: retain each record, reconcile differences, and cite the version supporting the statement.
- Ambiguous research claim: decompose it into alternative interpretations and avoid a universal novelty conclusion.
- Saturation not reached within budget: report cutoff, remaining query/frontier, and partial coverage.

## Workflow

1. Decompose the question into objects, properties, models, assumptions, constructions, and claimed improvements.
2. Generate synonyms, historical terminology, notation variants, and neighboring problem names.
3. Apply [search-protocol.md](references/search-protocol.md), recording exact queries, sources, dates, and filters.
4. Deduplicate by work/version relationships, not title similarity alone.
5. Screen against explicit criteria and retain exclusion reasons.
6. Verify identity and inspect the exact documents used for claim extraction.
7. Perform backward/forward citation and key-author/venue searches when supported.
8. Compare closest works by formal claim, model, assumption, parameter regime, security notion, and cost.
9. Return the corpus, evidence table, coverage limits, and bounded conclusion.

## Output Contract

```text
Question and decomposed claims:
Sources/queries/dates:
Inclusion and exclusion criteria:
Verified corpus and version map:
Claim-evidence table:
Closest-work comparison:
Coverage gaps and inaccessible sources:
Bounded conclusion (including novelty limitations):
```

