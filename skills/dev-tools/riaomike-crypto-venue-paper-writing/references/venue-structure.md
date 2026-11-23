# Venue Structure and Abstract Formula

Policies, page limits, and templates change every cycle. The tables here are starting anchors, not guarantees: verify the target venue's current official call and template at execution time, and record the snapshot date.

The **thresholds** live elsewhere, one file per subject: caps in `compression-rules.md`, floors and checklists in `expansion-rules.md`, ceilings and relocation in `section-budget.md`, and numeric placement in `numeric-placement.md`. This file gives the structure those rules are applied to.

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

**This skeleton is a default, not a requirement, and two of its cells are load-bearing.** The `1.3 Technical Overview` slot is where the overview *function* lives, but only 29% of tier-A crypto papers give the overview its own heading (`skills-work/corpus/crypto/statistics.md:229`, n=62). Do not require the titled section; require the content and the mass, and record which of the corpus's three placement forms you used (`skills-work/corpus/crypto/statistics.md:230-232`). Floors: `expansion-rules.md`.

Section **role** is likewise decided by content, not by the word "Construction": 69% of tier-A papers have no section whose title contains it (`skills-work/corpus/crypto/statistics.md:112`, n=62), so `Description ...`, `Parameters.`, and `Our scheme` blocks are construction material. The constituent checklist is in `expansion-rules.md`.

### Security venues — ACM CCS, IEEE S&P, NDSS, USENIX Security (all delegated)

Security venues want the threat model and the measured claim on the first page or two, but **this skill owns none of them**. The register and venue-specific rules of **ACM CCS**, **IEEE S&P**, **NDSS**, and **USENIX Security** all belong to the two security skills — page budgets, USENIX's mandated `Ethics considerations` and `Open science` sections, CCS's IRB and responsible-disclosure obligations, and each venue's overview and threat-model form — and are deliberately not restated here, because a duplicated rule is what the boundary exists to prevent. The authoritative boundary is `## Scope` in `SKILL.md`; for a security venue, read the security skill that owns it.

One cross-venue fact a crypto-venue author should not import by assumption: abstract length at the security venues does **not** differ significantly from crypto-venue abstract length — per-venue medians S&P 214, CCS 205, USENIX 212, NDSS 227.5, ranges fully overlapping (`skills-work/corpus/security/statistics.md:213`). That null finding is exactly why this skill sets **no per-venue word cap**, and it is the only abstract-length statement the security corpus licenses.

The remaining venue-specific shapes are owned per venue, not here: for instance the share of papers giving the overview its own section varies by venue (`skills-work/corpus/security/statistics.md:216-217`), so a rule about that placement belongs to the skill responsible for that venue, never to this one.

## Abstract Formula (four moves)

The abstract used by strong applied-crypto papers has four moves in sequence. The corpus's hand-coded calibration of that sequence is at `skills-work/corpus/crypto/statistics.md:141-165`, n=15, and the move shares over the whole tier-A sample are at `skills-work/corpus/crypto/statistics.md:167-179`.

1. **Problem or gap plus the strongest claim** (1-2 sentences): name the construction and its most defensible scoped superlative — "first X with property P under assumption A", "best concrete verifier time in family F".
2. **Parameters** (1-2 sentences): asymptotic complexity — prover time, verifier time, proof size — with the security assumption.
3. **Key technique** (1 sentence): the one technical insight that makes it work.
4. **Concrete numbers** (1-2 sentences): measured results and comparison, e.g. "runs in X seconds for Y, Zx faster than the state of the art on the same benchmark".

**The moves carry an allocation, not just a length.** Every paragraph is labelled `context`, `gap`, `build`, or `result` and the `build` share is measured; the corpus floor is 0.56 (`skills-work/corpus/crypto/statistics.md:165`). This is what stops a four-move abstract from being four moves of analysis. Method and caps: `compression-rules.md`.

Constraints, each with its rule:

- **The cap is the corpus median, not its third quartile** (corpus median, `skills-work/corpus/crypto/statistics.md:121`, n=59; `abstract-words` prints the draft's count against the cap it used — measured on the sample, `193 words vs cap 210 -> ok` — and it does **not** print the quartile, so the quartile being rejected is read from the anchor line rather than from the gate's output). The quartile licensed exactly the long tail that made the wordiness defect survive a review. Longer is possible only with the corpus line that licenses it quoted.
- **Longest sentence at most the corpus median** (median, `skills-work/corpus/crypto/statistics.md:124`, n=59).
- **Start with the contribution, not background.** Do not open with "X has attracted significant attention" or "in recent years".
- **Keep a concrete number in the abstract only if the body carries the same number with its methodology**, and only if it is an *outcome*. Numbers are sparse in the corpus: median 1 numeric token per abstract, and 0.576 of abstracts contain any (`skills-work/corpus/crypto/statistics.md:125`, `skills-work/corpus/crypto/statistics.md:129`). Placement rules: `numeric-placement.md`.
- **No process or workflow self-reference** in the abstract. See `de-ai-and-style.md`.
- **No AI-flavor vocabulary** and no vague "significantly improves" without numbers.

## Contribution List

A bulleted or enumerated list in the introduction area, one item per **object** rather than per activity, each opening by naming the object it introduces, and each optionally ending with a pointer to the section that delivers it (`skills-work/corpus/crypto/craft-notes.md:148-199`). Caps, the abstract-to-list duplication metric, and the migration list are in `compression-rules.md`.

## Section Budget

Per-section and per-subsection share ceilings, the move-not-delete relocation rule, and the relocatable classes are in `section-budget.md`. The measurement conventions a budget claim must use are quoted there.

One caveat that belongs with the structure table: **LaTeX sources have no page model**, so a budget stated in pages cannot be measured on a source file. The crypto corpus records every size in words or lines and says which (`skills-work/corpus/crypto/statistics.md:16-17`). Page figures come only from a compiled count or from a venue's official limit, and must be labelled as such.

## Venue Policy Anchors

The table lists only venues this skill owns. For a delegated venue, take the template, page limit, and register from the skill that owns it rather than from here.

| Venue | Owner | Template anchor | Notes |
|---|---|---|---|
| CRYPTO/EUROCRYPT/ASIACRYPT | this skill | Springer LNCS `llncs.cls` | double-blind; 30-page total practice; submit via IACR |
| ACM CCS, IEEE S&P, NDSS | `ccs-writing-style` | see that skill | delegated — page budget, template, register, IRB / responsible-disclosure obligations, reportable-vulnerability and ethics guidance are all owned there |
| USENIX Security | `usenixsec-writing-style` | see that skill | delegated — page budget, register, and the mandated `Ethics considerations` and `Open science` sections are owned there |

Anonymity: no author names, no identifying acknowledgments, no self-citation as "our previous work", no identifying repository URLs or full vulnerability identifiers, until the camera-ready phase per venue rules. Ethics, AI-disclosure, and artifact statements follow the current official call, not last year's.

## Recommended Writing Order

Write in dependency order rather than reading order: comparison table first (it forces the landscape and the delta), then the technical overview (if it cannot be explained intuitively, the construction is not ready), then preliminaries, construction, security, evaluation, and only then the abstract and introduction, with the title last.

Then run the passes in `## Workflow` order — diagnose, compress, expand, relocate, place numbers, de-name — because each pass reads the artefact the previous one produced.
