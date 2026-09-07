# Venue Structure and Abstract Formula

Policies, page limits, and templates change every cycle. The tables here are starting anchors, not guarantees: verify the target venue's current official call and template at execution time, and record the snapshot date.

## Structure Families

### CRYPTO / EUROCRYPT / ASIACRYPT (Springer LNCS)

LNCS single-column proceedings; `llncs.cls`; bibliography `splncs04.bst`. IACR conferences typically allow up to 30 pages total including references and appendices; reviewers commonly read the first roughly 25 pages, so keep construction and the main theorems early.

Crypto papers are not IMRAD. The working skeleton:

```text
Abstract
1. Introduction
   1.1 Our Contributions (bullet list with formal claims)
   1.2 Comparison Table (asymptotic + concrete numbers)
   1.3 Technical Overview (intuitive explanation of the key ideas)
   1.4 Related Work (organized by technique family)
2. Preliminaries (notation, definitions, building blocks)
3. Construction / Protocol
4. Security / Correctness Analysis
   (theorem statements in the body; full proofs in the appendix when space-constrained)
5. Implementation and Evaluation
6. Conclusion
Appendix A. Deferred Proofs
Appendix B. Additional Benchmarks
```

For theory-heavy papers Section 4 dominates and Section 5 may be brief or absent; for systems-oriented papers (zkVM, zkEVM) Section 5 dominates. Contributions, comparison table, and technical overview should all appear even when subsections are reordered.

### IEEE S&P, ACM CCS, USENIX Security, NDSS

Security venues want the threat model and the measured claim on the first page or two. See `ccs-writing-style` and `usenixsec-writing-style` for venue-specific registers; page limits (for example S&P and USENIX around 13 pages plus references, CCS around 12-15 depending on the cycle) must be checked against the current call.

## Abstract Formula (four parts)

The abstract used by strong applied-crypto papers (for example the SNARK/ZKP line) has four moves:

1. **Problem plus strongest claim** (1-2 sentences): name the construction and its most defensible superlative, scoped — "first X with property P under assumption A", "best concrete verifier time in family F".
2. **Parameters** (1-2 sentences): asymptotic complexity — prover time, verifier time, proof size — with the security assumption.
3. **Key technique** (1 sentence): the one technical insight that makes it work.
4. **Concrete numbers** (1-2 sentences): measured results and comparison, e.g. "runs in X seconds for Y, Zx faster than the state of the art on the same benchmark".

Constraints learned from revision cycles:

- Hard cap: at most 250 words for CRYPTO/LNCS practice; verify any stricter venue cap. Count carefully; math that collapses to one token should still be reported honestly.
- Start with the contribution, not background. Do not open with "X has attracted significant attention" or "in recent years". Do not spend words on motivation.
- Keep concrete numbers in the abstract only if the body contains the same numbers with methodology.
- No workflow or tooling self-reference (round numbers, internal paths, audit trail naming) in the abstract; move that to the body or a footnote.
- No AI-flavor vocabulary (see de-ai-and-style.md) and no vague "significantly improves" without numbers.

## Venue Policy Anchors

| Venue | Template anchor | Notes |
|---|---|---|
| CRYPTO/EUROCRYPT/ASIACRYPT | Springer LNCS `llncs.cls` | double-blind; 30-page total practice; submit via IACR |
| IEEE S&P | IEEE conference template | double-blind; check current call for page limit and annex policy |
| ACM CCS | `acmart.cls` sigconf | double-blind; check current call |
| USENIX Security | USENIX template | double-blind; check current call |
| NDSS | NDSS template | double-blind; check current call |

Anonymity: no author names, no identifying acknowledgments, no self-citation as "our previous work", no identifying repository URLs, until the camera-ready phase per venue rules. Ethics, AI-disclosure, and artifact statements follow the current official call, not last year's.

## Recommended Writing Order

Write in dependency order rather than reading order: comparison table first (it forces the landscape and the delta), then technical overview (if it cannot be explained intuitively, the construction is not ready), then preliminaries, construction, security, evaluation, and only then the abstract and introduction, with the title last.
