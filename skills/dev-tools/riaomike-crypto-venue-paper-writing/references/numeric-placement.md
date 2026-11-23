# Numeric Placement — Where Concrete Values Belong

The counterweight to the expansion rules. The cheapest way to make a construction section look detailed is to pour measured numbers into it, which recreates the reported defect of concrete measured values sitting in theory sections. This file states which sections may carry concrete values, which must stay symbolic, and what happens to a value that has to move.

**Scope note.** This file encodes a **rule shape**, not any manuscript's values. It never lists specific literals, and neither may any other file in this skill: a value list belongs to one manuscript and does not generalise. What generalises is the region rule and the reason classes below.

## The region rule

**Concrete measured values belong in evaluation, parameters, and implementation material. Construction and proof sections stay asymptotic or symbolic.**

The corpus audit is unambiguous on this point. Counting literals with at least three decimal places per section role across tier-A body sections:

| section role | literals found | papers contributing | anchor |
|---|---|---|---|
| construction | **0** | 0 | `skills-work/corpus/crypto/statistics.md:407` |
| analysis (proof) | **0** | 0 | `skills-work/corpus/crypto/statistics.md:408` |
| related work | **0** | 0 | `skills-work/corpus/crypto/statistics.md:413` |
| evaluation | 180 | 4 | `skills-work/corpus/crypto/statistics.md:409` |
| introduction | 44 | 7 | `skills-work/corpus/crypto/statistics.md:410` |
| conclusion | 15 | 4 | `skills-work/corpus/crypto/statistics.md:414` |
| preliminaries | 6 | 2 | `skills-work/corpus/crypto/statistics.md:412` |

Full table: `skills-work/corpus/crypto/statistics.md:405-415`; the reading and the re-runnable command are at `skills-work/corpus/crypto/statistics.md:417-421`. The two roles whose count is exactly zero are the construction and the proof — the roles the expansion pass is asked to deepen. That is why this file exists.

Note the introduction carries 44 such literals across 7 papers, so the introduction is a **legitimate** home for a headline number. The rule is not "no numbers outside evaluation"; it is "no **measured** values in construction or proof".

## Region boundaries must be stated

A numeric-placement rule is unusable without a boundary. State, before scanning:

- the `file:line` span of each theory region (construction and proof sections) and of each evidence region;
- which heading marks each evidence record, so a scan can exclude it;
- the twin being scanned (tex or md) and the unit.

Values inside a **heading-marked evidence record** are exempt: they are the record of how a number was obtained, which is exactly what the appendix is for. See `references/section-budget.md` for the marker requirement.

## Reason classes for a value in a theory section

A concrete value may sit in a theory section only if it carries a **filed reason** of one of these classes, recorded next to the value:

1. **Analytic, not measured.** The value is an evaluation of the paper's own bound or lemma at a stated parameter point. It is arithmetic on stated formulas, not an experiment.
2. **Design-point or defining arithmetic.** The value defines a parameter set — a table size, a row count, a bit width — and states that it is a design choice rather than an observation.
3. **Symbolic scale.** The value is a level ("the 128-bit field", "the 2^128 target") rather than a measurement.
4. **Superseded, retained once for verifiability.** An earlier value kept deliberately, **marked** superseded, with a pointer to the current value. Retention is required; body placement is not.
5. **Stated paper target.** A threshold the paper's construction is compared against, not a value the paper measured.

The class is recorded, not inferred from the digits. "It looks analytic" is not a filed reason; the sentence must say so.

## The relocation rule

A measured value found in a construction or proof section is **relocated with its digits and provenance intact**:

- the digits are unchanged — never rounded, truncated, or re-expressed in a different unit on the way out;
- the **provenance travels**: the field, the parameter point, the sample size, the environment, and the method that produced it;
- a **pointer** is left where the value was, or the surrounding sentence is rewritten to compare against a symbol instead;
- the value is **never deleted**. A relocation that loses a number has destroyed evidence, and a later audit that finds the value absent from *both* the theory region and the parameters region is looking at data loss, not at compliance.

Conversely, symbolic expressions **do not** migrate into the evaluation section: the analysis keeps its asymptotic statements, and the evaluation keeps its measurements. Both registers are legitimate; they are separated by section, not merged.

## The scan

Because a LaTeX source has no page model, the scan operates on text:

1. Mark the theory regions and the evidence records.
2. Extract the concrete-literal class from the theory regions — high-precision decimals are the clear case, and integers above a stated digit threshold are the second.
3. For each hit, require a filed reason of one of the five classes. A hit without a reason is a finding.
4. Print the hit, its `file:line`, its region, and either the filed reason or `unfiled`.
5. Report the count of `unfiled` hits per region; zero is the pass condition for construction and proof.

Two false-positive classes a scan must expect, both of which the corpus records: a **derived** parameter can appear to be a measurement when it is defining arithmetic (class 2), and a bare integer can match inside a decimal or a symbolic exponent if the scan does not blank decimals and exponents before the integer pass. Report both as notes rather than findings when the reason class is filed.

## Pass output

The numeric-placement pass returns, and `## Output Contract` requires:

- **Region map:** the theory regions, the evidence records with their heading markers, and the twin and unit scanned.
- **Hit table:** one row per concrete literal in a theory region, with its `file:line`, its region, and its filed reason class or `unfiled`.
- **Relocation ledger:** for each relocated value, the old and new `file:line`, the digits before and after (which must be equal), the provenance that travelled, and the pointer left behind.
- **Preservation check:** the count of relocated values equals the count of values that appeared in the body scan, and no value is present in neither region.
- **Unfiled hits remaining,** as unresolved items for the human author.

## Worked calibration

The pass must reproduce this verdict on the frozen calibration manuscript; it is the contract's record, and the class names are the rule shape rather than the manuscript's contents.

| region | expected finding | basis |
|---|---|---|
| construction and proof sections before revision | measured values present in theory sections, with no filed reason class | the reported defect, closed in revision by relocation with the exemption classes above |
| the same regions after revision | the measurement class is empty; the retained superseded pair is marked and pointed at | `research-work/paper/revision/review-final-r2.md:223` |

A pass that reports "numbers look fine" for the pre-revision state has not run. A pass that recommends **deleting** a relocated value has failed, because retention is what makes the relocation auditable.
