---
name: venue-calibration
description: Use when choosing a target venue, adapting a draft to a venue's format, or calibrating a mock review. Summarises per-venue formats, what reviewers weigh, typical rejection reasons and scoring rubrics for IACR venues (CRYPTO, EUROCRYPT, ASIACRYPT, TCC, PKC, TCHES, ToSC/FSE) and security venues (CCS, S&P, USENIX Security, NDSS, PoPETs).
---

# Venue calibration

> **Everything numeric in this file (page limits, word limits, cycles, dates) changes
> between years. Treat it as orientation only and CHECK THE CURRENT CFP.** Record the
> CFP URL, the date you read it, and the exact quoted rules in `SUBMISSION.md` before
> you rely on them. Desk rejection "without consideration of merits" is common for
> format violations.

## 1. Format and process at a glance

| venue | template | body length (check the current CFP) | what counts | review process notes |
|---|---|---|---|---|
| CRYPTO | Springer LNCS | ~25–30 pp. at submission; camera-ready limit may differ | usually excludes references; supplementary material allowed but reviewers need not read it | anonymous; rebuttal/interactive phase in recent years; possible early reject round |
| EUROCRYPT | Springer LNCS | ~25–30 pp. | as above; body must be self-contained | two-stage process with early rejects before rebuttal in recent years (so first impression must come from the body alone) |
| ASIACRYPT | Springer LNCS | ~30 pp. | read carefully: some years count *everything before the references* (incl. appendices) toward the camera-ready limit | rebuttal + interactive phase with the meta-reviewer in recent years |
| TCC | Springer LNCS | check CFP | usually excludes references | theory audience; no experiments expected |
| PKC | Springer LNCS | check CFP | usually excludes references | public-key focus; implementation welcome but not required |
| TCHES (CHES) | IACR journal class (`iacrj`; older `iacrtrans`) | check CFP (roughly 20–25 pp. excl. references in recent years) | appendices may or may not count | several submission deadlines per year; journal-style decisions incl. major revision; artifact evaluation encouraged |
| ToSC (FSE) | IACR journal class (`iacrj`; older `iacrtrans`) | regular papers ~20 pp. excl. references; longer = "long paper" | material that must be carefully reviewed (e.g. proofs) counts even in appendices | four rounds per year; accept / minor / major revision / reject-and-resubmit / reject; artifact badges after acceptance |
| ACM CCS | ACM `sigconf` two-column | ~12 pp. excl. references and well-marked appendices (check) | appendices limited in some years | anonymous; multiple cycles; rebuttal and/or major revision in recent years |
| IEEE S&P | IEEE two-column | ~13 pp. excl. references and appendices (check) | total-length cap may apply | multiple cycles; major revision outcome common |
| USENIX Security | USENIX two-column | ~13 pp. excl. references and appendices (check) | ethics / open-science sections required in recent years | multiple cycles; major revision; artifact evaluation |
| NDSS | IEEE-like two-column | ~13 pp. excl. references and appendices (check) | | two cycles; rebuttal/revision |
| PoPETs | PETS template | check CFP (roughly 12–15 pp. excl. references/appendices recommended) | | four issues per year; major revision common; artifact badges |

Class files: never modify margins, fonts or spacing. LNCS: `llncs.cls` +
`splncs04.bst`. IACR journals: follow the current class instructions; the submission
option usually anonymises and adds line numbers (`$$...$$` can break line numbering;
use `\[...\]`).

## 2. What reviewers weigh (heuristic weights for mock review)

| venue group | dimension weights (sum 100) |
|---|---|
| CRYPTO / EUROCRYPT / ASIACRYPT | correctness 30, novelty of technique 25, significance 20, presentation 15, fit 10 |
| TCC | conceptual contribution 35, technical depth 30, novelty of technique 25, presentation 10 |
| PKC | correctness 30, novelty 25, significance 20, presentation 15, fit 10 |
| TCHES | implementation quality 25, security/side-channel or correctness analysis 25, performance data and fair comparison 20, novelty 15, presentation 15 |
| ToSC / FSE | security argument soundness 30, structural (not parametric) novelty 20, fair comparison 15, reproducibility 15, specification self-containedness 10, impact/invites analysis 10 |
| CCS / S&P / USENIX / NDSS | technical soundness 25, practical impact 25, threat model 20, novelty 15, presentation/evaluation 15 |
| PoPETs | privacy contribution 30, soundness 25, evaluation 20, usability/deployability 15, presentation 10 |

Venue-specific extra attention:

- **CRYPTO/EUROCRYPT:** proof tightness, standard vs idealised models, assumption
  minimality, a genuinely new technique. Pure constant-factor engineering is rarely
  enough.
- **ASIACRYPT/PKC:** slightly more tolerant of solid incremental improvements with a
  clear technique; implementation is a plus.
- **TCC:** new definitions/paradigms, broad applicability, connections to complexity.
- **TCHES:** real hardware/software measurements, fair comparison with best existing
  implementations, open source, side-channel considerations where relevant.
- **ToSC/FSE:** complete, conservative security analysis; design rationale backed by
  search evidence; test vectors; comparisons at equal failure probability and threads.
- **Security conferences:** threat model clarity, deployment realism, ethics and
  responsible disclosure, artifact availability, end-to-end evaluation.

## 3. Typical rejection reasons (and the pre-emptive fix)

| reason | venues where it bites | fix in the paper |
|---|---|---|
| "Incremental / just parameter tuning" | all IACR | name the structural mechanism; parameterised family; cost model theorem; "neither observation is a parameter tweak" paragraph |
| "Unfair or weak baseline" | TCHES, security venues, all with experiments | strongest configuration of the strongest library; same machine; measured vs claimed both reported |
| "Claims stronger than theorems" | CRYPTO/EC/TCC | scope every claim; conditional vs unconditional stated; weakened CLAIMS wording |
| "Counterexample to a lemma" | all | falsifier exhaustive search on small parameters before submission |
| "Key content only in the appendix" | EC/CRYPTO/AC | move the new technical core into the body, compress background instead |
| "Security level unclear / below claim" | FHE, lattice, symmetric | per-instance estimator table; binding attack; recent-attack check |
| "Overlap with prior/concurrent work" | all | explicit delta paragraph; "what this paper is not" sentence |
| "Not self-contained / hard to follow" | all | technique overview passes the goal test; notation table |
| "Missing threat model or ethics" | CCS/S&P/USENIX/NDSS/PoPETs | dedicated sections as the CFP requires |
| Format violation | all | camera-ready/submission checklists (`skills/camera-ready`, `templates/handoff/SUBMISSION.md`) |

## 4. Contribution type vs venue (observed heuristics, not rules)

From tracing publication lineages in several subfields:

- A new *named* algebraic structure (group action, module structure, known
  mathematical object) + measured gain → EUROCRYPT/ASIACRYPT/TCC-level.
- New assumption + reductions + attacks considered + measured gain + cross-scheme
  applicability → CRYPTO-level.
- Pure engineering (SIMD, memory layout, hardware) with real hardware numbers →
  TCHES.
- New key distribution with self-built security analysis → often security venues;
  the self-built analysis rarely convinces both crypto and performance reviewers.
- Porting a known trick to a neighbouring setting with a small gain → second-tier
  venues.
- "We organised the field" without a new result → workshop/SoK unless framed as SoK
  with a methodology.
- Speedup size correlates weakly with venue tier; the structure used to obtain it
  correlates strongly. Roughly ≥1.3× is a minimum for a performance claim to matter.

## 5. Scoring rubric used by `mock-review`

Normalised six-point scale (map to the venue form when known):
1 strong reject · 2 reject · 3 weak reject · 4 weak accept · 5 accept · 6 strong accept.
Confidence 1–4. A paper that gets one champion (≥5, confidence ≥3) and no strong
detractor usually survives discussion at IACR venues; one well-argued technical
reject (e.g. a counterexample) usually sinks it.

Calibration anchors:

- 6: new technique that will be reused; clean proofs; convincing evaluation.
- 5: clear technical contribution, minor presentation issues.
- 4: useful result, some doubts (baseline fairness, scope) that a rebuttal can fix.
- 3: interesting but claims exceed evidence, or novelty unclear vs a named prior work.
- 2: a correctness problem, or contribution judged incremental.
- 1: wrong, out of scope, or format violation.

Never report a probability of acceptance as if it were statistical; if asked, give a
subjective band with the conditions that move it.

## 6. Procedure

1. Fetch and quote the current CFP (WebFetch) into `SUBMISSION.md` §Venue.
2. Fill the table rows for the target venue with the quoted values.
3. Choose the mock-review personas and weights from §2.
4. Adjust the playbook budget (section shares, page limit, two-column vs LNCS).
5. Re-check the CFP one week before the deadline (rules and deadlines do change).
