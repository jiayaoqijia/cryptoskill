---
name: abstract-craft
description: Use when writing or tightening a paper abstract (and its plain-text submission-form twin). Applies the three-part paradigm (state of the art, our technique, results and artifact) with a sentence-level function table and an overclaim filter.
---

# Abstract craft

## Inputs

`CLAIMS.md` (survived/weakened claims), `EVIDENCE.md` (numbers), the contribution
list (`paper/sections/intro.tex`), target venue (for length norms, see
[venue-calibration](../venue-calibration/SKILL.md)).

## Procedure

1. **Write a one-line viewpoint** of the paper: "We view X as Y." If this sentence
   cannot be written, the abstract is not ready; go back to the overview.
2. **Fill the sentence-function table** below in `paper/ABSTRACT_PLAN.md` (Chinese or
   English bullet map is fine; discuss it with the human author before prose).
3. **Draft three paragraphs** (see `paper-playbook/sections/02_abstract.md`).
4. **Overclaim filter** (automatic pass, then manual):
   - forbidden: novel, groundbreaking, rigorous guarantee, optimal (unless proven),
     significantly (without a number), first (unless a literature search in
     `LITERATURE.md` supports it, and even then prefer "to our knowledge, the first").
   - every number → EVIDENCE row id noted in a LaTeX comment `% EV:E12`.
   - every scope noun ("13 rings", "all primes p ≡ 1 mod 4") → matches the
     parameter/security tables.
5. **Consistency pass**: abstract ↔ contributions ↔ conclusion use the same numbers,
   the same order and the same framework name.
6. **Length**: IACR LNCS: fits page 1 with keywords (typically 200–300 words).
   ToSC/TCHES: usually 200–280 words. Security conferences: often ≤ 200–250 words in
   the submission form. Check the CFP.
7. **Plain-text twin** `paper/abstract_plain.txt` for the submission form.

## Sentence-function table (7–10 sentences)

| # | function | notes |
|---|---|---|
| S1 | field consensus + bottleneck | no citation needed |
| S2 | existing routes, grouped, venue'year | 1–2 representatives per route |
| S3 | open question | "However, ... has remained open." |
| S4 | our object and viewpoint | "We present/propose X, which views ... as ..." |
| S5–S6 | technical points, one each | "First, ... At the same time, ..." or structure → bound → construction |
| S7 | what we *prove* (property, not activity) | not "we analyse security" but "we prove that no attacker learns ... from three or fewer outputs" |
| S8 | scope → range → concrete points vs named baseline | measured on the same machine, if true, say so |
| S9 | artifact / formalisation / invitation for analysis | exact scope of formal verification |

## Upgrading weak sentences

| weak | strong |
|---|---|
| "We give a complete security analysis." | "Every considered attack needs more than 2^128 operations; the tightest margin comes from <attack> at 2^{x}." |
| "Our method is much faster." | "On N instances at ≥λ-bit security, <stage> is 2.1–3.4× faster than <baseline> in the same library." |
| "We formally verify our results in Lean." | "The algebraic core (Lemmas 2–5) is machine-checked in Lean 4; the noise analysis is not." |
| "We unify prior work." | "The methods of [A] and [B] are the cases w=1 and k=1 of our construction." |

## Headline-range hygiene

- Lower end = the most conservative **measured** number; if the upper end is an
  estimate, label it as an estimate in the table and say "up to ... (estimated)".
- Never mix instances below the claimed security level into the range.
- If a baseline number is reproduced rather than taken from the paper, the abstract
  compares against the reproduced number and the paper reports both.

## Output

`paper/sections/abstract.tex`, `paper/abstract_plain.txt`, and a short diff note in
`paper/CHANGELOG.md`.

See toy examples: `skills/paper-playbook/examples/toy_abstracts.md`.
