---
name: crypto-literature-search
description: Use when conducting cryptography, ZKP, or lattice literature discovery, prior-art mapping, citation verification, closest-work comparison, related-work evidence collection, or bounded novelty searches.
---

# Crypto Literature Search

Build a reproducible, version-aware evidence corpus. Discovery, bibliographic verification, claim support, coverage, and novelty are separate conclusions.

## Scope

In scope:

- targeted, exploratory, systematic, or update searches for cryptography/ZKP/lattice research;
- prior-art and closest-work mapping;
- citation identity, version, and claim-support verification;
- related-work evidence tables and bounded novelty assessments;
- query/source logs, screening, deduplication, citation chaining, and coverage reporting.

Out of scope:

- summarizing only one supplied paper when no discovery is requested;
- auditing whether a proof is valid;
- formatting an already verified bibliography without discovery/verification;
- guaranteeing exhaustive global coverage, global novelty, or absence of unpublished work;
- publishing, contacting authors, or changing an external bibliography unless separately requested.

## Required Inputs

- research question or candidate contribution decomposable into searchable claims;
- relevant primitives/problems, properties/security notions, setup/model, assumptions, parameter regime, and claimed differences;
- date, language, venue/source, publication-state, or corpus boundaries when required;
- desired deliverable: search log, verified bibliography, evidence map, related-work synthesis, or bounded novelty assessment;
- available source-access capabilities and search budget.

If the candidate claim is too vague to screen or compare, ask for the minimum contribution description. Otherwise state reasonable boundaries and continue.

## Success Criteria

- Sources, exact queries, dates, filters, result counts, screening decisions, and stopping rule are reproducible.
- Work identity is separated from version identity; ePrint/preprint, conference, journal, and revision relationships remain visible.
- Every included citation has a verification status; every extracted claim points to an inspected version/location or is marked unverified.
- Search snippets and secondary summaries are used only for discovery unless independently verified against the exact source.
- Closest prior work is compared claim by claim across model, assumptions, security notion, parameters, functionality, proof basis, and compatible cost measures.
- Coverage gaps, inaccessible sources, excluded populations, and unresolved conflicts are explicit.
- Any negative or novelty conclusion is bounded by documented sources, queries, dates, and stopping conditions.

## Failure Modes

- No search/network access: design the search plan and process supplied sources only; label discovery, citation chaining, and novelty coverage not executed.
- Inaccessible full text: retain bibliographic discovery status but do not treat title, abstract, snippet, or third-party summary as support for theorem/security details.
- Conflicting metadata/versions: preserve all records, reconcile authoritative identifiers when possible, and cite the exact version used.
- Over-broad or ambiguous question: decompose alternative interpretations and avoid one universal conclusion.
- Search budget exhausted before saturation: return the partial corpus, frontier, cutoff, and next queries/sources.
- Incompatible cost evidence: refuse a ranking until cost model, parameter regime, hardware/software, setup, and amortization are aligned or qualified.

Never invent an author, title, venue, year, identifier, quotation, theorem number, search result, query run, citation relationship, or novelty claim.

## Workflow

1. Freeze the question, contribution claims, boundaries, deliverable, available capabilities, and budget.
2. Apply [search-protocol.md](references/search-protocol.md) to decompose concepts, generate query families, discover broadly, screen, chain citations, and stop under a documented rule.
3. Record every query, work/version, screening decision, and claim using [corpus-schema.md](references/corpus-schema.md).
4. Apply [source-verification.md](references/source-verification.md) before treating bibliographic identity or a paper's content as verified evidence.
5. For prior-art or novelty work, apply [novelty-assessment.md](references/novelty-assessment.md) and compare closest work claim by claim.
6. Separate discovered, screened, identity-verified, full-text-inspected, claim-verified, and excluded records.
7. Return the corpus, evidence map, closest-work matrix, coverage limits, and bounded conclusion.
8. When evaluating this skill itself, use [evaluation-scenarios.md](references/evaluation-scenarios.md); do not claim those scenarios ran unless independent fresh-context outputs were inspected.

## Output Contract

Return, in order:

1. question, decomposed claims, and search boundaries;
2. sources, exact queries, dates, filters, and stopping rule;
3. inclusion/exclusion criteria and decision log;
4. verified corpus and version graph;
5. claim-evidence table with verification status;
6. closest-work comparison when applicable;
7. citation conflicts, inaccessible sources, and coverage gaps;
8. bounded conclusion and explicit novelty limitations;
9. reproducible next-search frontier when coverage is partial.

