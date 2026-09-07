---
name: crypto-venue-paper-writing
description: Use when drafting, restructuring, or polishing a cryptography paper for a specific top venue (CRYPTO, EUROCRYPT, ASIACRYPT, IEEE S&P, ACM CCS, USENIX Security, NDSS) or for CRYPTO/LNCS-style submission, including venue structure, abstract compression, de-AI rewriting, double-blind compliance, and format checks.
---

# Crypto Venue Paper Writing

Write for the venue, not in the abstract: every structural and stylistic decision is made against one named conference's current official call, template, page limit, and reviewing culture.

## Scope

In scope: choosing a venue-specific structure and section budget; writing or compressing an abstract (four-part formula, hard word cap); drafting contribution bullets, comparison tables, and technical overviews; organizing related work by technique family; writing preliminaries, construction, security, experiments, and conclusion in venue register; applying a concrete de-AI rewriting checklist; verifying double-blind anonymity; checking LNCS/ACM/IEEE/USENIX formatting and citation style; and running a pre-submission quality pass.

Out of scope: inventing results, proofs, citations, or experiments; upgrading claim tiers; deciding novelty or authorship; guaranteeing acceptance; or submitting without human authorization.

## Required Inputs

- target venue and its current official call for papers (page limit, template, anonymity, ethics, AI-disclosure, artifact policy);
- manuscript draft or outline to revise, or verified claims/evidence to write from;
- comparison corpus for the related-work and comparison-table positioning;
- LaTeX/Markdown sources and bibliography, or the venue template to set up.

## Success Criteria

- Abstract follows the four-part formula (strongest defensible claim first, parameters, key technique, concrete numbers) and stays within the venue word cap (CRYPTO/LNCS practice: at most 250 words; fewer when the venue says so).
- Structure matches the named venue's convention, not generic IMRAD: contributions bullets, comparison table, and technical overview appear in the introduction area for crypto venues.
- Every contribution bullet and every concrete number in the abstract/table has an addressable body section; wording is calibrated (proven vs claimed vs estimated vs open).
- De-AI checklist passes: no vocabulary flags, no forced structures, no meta-narrative, no workflow self-reference, no synonym cycling, no unbounded superlatives.
- Double-blind wording holds everywhere, including self-citations, acknowledgments, artifact links, and code identifiers.
- Page limit, template, bibliography style, and current CFP requirements are verified against the venue's official site at execution time, not assumed from memory.

## Failure Modes

- Draft with no target venue or no verified CFP snapshot: return structure-neutral guidance and require the official call before format claims.
- Claim or number without a body address or evidence anchor: expose it and block the affected sentence rather than smoothing it over.
- AI-flavor prose that survives a first pass: run the grep-level checklist in [de-ai-and-style.md](references/de-ai-and-style.md) and rewrite, do not just flag.
- Venue template/page rules may have changed since training: verify the current official template and CFP; never rely on remembered page limits or style files.
- De-identification gap (author names, institution, identifying repo): fix before any format pass.

## Workflow

1. Freeze the target venue and fetch its current official CFP and template (see [venue-structure.md](references/venue-structure.md) for per-venue anchors).
2. Decide the venue structure and section budget; map existing content onto it.
3. Write or rewrite in dependency order: comparison table first, then technical overview, then abstract, then introduction framing, then body sections.
4. Apply the de-AI and register rules from [de-ai-and-style.md](references/de-ai-and-style.md) to every section, including the abstract and conclusion.
5. Run the pre-submission pass: number/body consistency, claim tiers, citation integrity, double-blind scan, page budget, template compile.
6. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: target-venue policy snapshot with date; structure and section budget; revised manuscript or section diffs; abstract word count and four-part coverage; de-AI checklist results; double-blind and format compliance report; unresolved items requiring the human author.

## Reference Files

| File | Contents |
|------|----------|
| `references/venue-structure.md` | Venue-specific structure, abstract formula, page limits, template anchors |
| `references/de-ai-and-style.md` | De-AI vocabulary/structure/content red flags and sentence-level register rules |
| `references/evaluation-scenarios.md` | Test specifications for independent evaluation |
