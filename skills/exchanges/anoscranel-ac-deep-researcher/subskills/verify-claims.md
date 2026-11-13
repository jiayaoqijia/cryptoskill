---
name: verify-claims
domain: research-operations/verify-claims
trigger: "\"verify this claim\", \"check these citations\", \"is this number real\", \"prove this before we use it\"."
anti_trigger: "Attacking already-supported conclusions with counter-evidence (subskills/adversarial-pass.md); deciding which claims need a permanent card (subskills/evidence-cards.md)."
scope: "Verifying load-bearing claims: two independent lineages, a verbatim span archived, citation resolution in two indexes, retraction status"
status: "seedling"
---

# Verify claims

## Standard

- No claim is stated as fact on one lineage. Two or more independent source
 lineages before a claim stands; otherwise it is ⚠️ single-source with the
 lineage named.
- Verification happens when a claim enters the record, not at the end. An
 injected misleading document lands hardest just before synthesis: false-
 conclusion adoption jumps to 85.0% at that seam, versus 34.5% at cold start
 (MisKnow, arXiv 2607.20891).
- Anchor claims in raw snippets, not in the researcher's notes. Raw snippets
 carried up the chain bought +5pp recall and +3-7pp precision on citation
 accuracy (arXiv 2608.24306).
- Every citation resolves in at least two independent indexes (this skill's own bar). Anything heading for a published artifact also gets a retraction
 check at publication time: 32.2% of contaminated-review citations post-date
 retraction (JAMA Network Open 2025).
- A verifier loop is judged on false-positive rate at the desk's real base
 rate, not recall (HALLMARK, arXiv 2607.18360).
- Unsupported claims are deleted, not softened.

## Decision rules

- A claim is load-bearing when the verdict, a number, a price, or a named
 entity depends on it. Load-bearing claims get the full loop; passing detail
 gets the lineage tag only.
- A cross-model recheck is not sufficient evidence on its own: it flagged
 every planted item as misleading and the conclusions were still adopted
 (MisKnow, 2025). Resolution and spans decide.

## Procedure

1. Extract the claim in one sentence.
2. Resolve its citation in two independent indexes (for example Crossref plus
 OpenAlex or PubMed). Record both identifiers.
3. Archive the verbatim span supporting it in the source's file on disk.
4. Tag rung, population, and lineage count.
5. Mark the outcome: verified, single-source ⚠️, contested, or unverified.
6. For anything publication-facing, run the retraction check before sign-off.

## Anti-patterns

- Trusting the citing page instead of resolving the primary (citation
 laundering).
- A fetch that returned nothing turned into a plausible citation anyway.
 Empty fetch means empty claim.
- Verification reported as a model's assertion instead of an artifact.

## Done checklist

- Every load-bearing claim has two-index resolution or an explicit flag.
- Every verified claim has a verbatim span on disk.
- No claim stands on a single lineage without the ⚠️ mark.

The verification should also record the version of the source, because a live document changes and a claim verified against last quarter's revision is unverified against this quarter's. For anything load-bearing, archiving the copy that was read is the difference between a citation and a memory.

## Sources

- <https://osf.io/prereg/>
- <https://training.cochrane.org>
