# Section Budget — Ceilings, Relocation, and the Move-Not-Delete Rule

The mirror half of the thinness defect. A skill that only pushes "write more" produces a paper that grows everywhere: the under-detailed section is repaired, the over-thick one is left alone, and the imbalance survives. This file supplies the ceiling and the relocation procedure.

Basis, quoted from `skills-work/corpus/crypto/statistics.md:10-21`: `words` are whitespace-separated alphanumeric tokens of the plain-text rendering; `lines` are physical source lines of the file the unit lives in, comments removed; a section's `words` include its subsections' words unless the number says `direct`, and `direct` means the section's own text with its immediate children's spans subtracted.

## The subsection share ceiling

**Rule: no subsection holds a majority of its parent section's words.**

| band | largest-child share of parent | meaning | anchor |
|---|---|---|---|
| **within budget** | at or below the majority boundary — gate `largest-child-ceiling` prints it | the parent is not monopolised by one child | `skills-work/corpus/crypto/statistics.md:330` |
| **relocation pass required** | above the majority boundary | the child holds a majority; the parent needs a move pass | `skills-work/corpus/crypto/statistics.md:333` |
| **outlier** | above the outlier boundary | only a minority tail of corpus parent-child pairs reach this | `skills-work/corpus/crypto/statistics.md:334` |

**The gate prints the share it judged and the band that share fell in; the two BOUNDARIES are not in its output** — measured on the four venue fixtures (t7, finding F-7; `skills-work/reports/venue/fixtures/demo-above-floor.tex` and its three siblings), e.g. `§'4. Our scheme' -> §'The core gadget' 0.5488 [relocation pass required]`, and the boundaries themselves occur zero times in the combined fixture JSON (`corpus/crypto/statistics.md:334` names theirs). Read the boundaries off `--constants` (`CEILING_MAJORITY`, `CEILING_OUTLIER`), which prints both with their anchors and `n`; do not go looking for them on a gate line.

**Is the `direct` degeneracy guard in scope here? No — and the reason is structural, not a convenience.** The guard in `references/expansion-rules.md` exists because the construction-to-analysis ratio is computed on **`direct` spans**, which subtract a section's children from its own text and can therefore collapse onto heading lines. The ceiling never does that: it compares a child's words against its **parent's** words under a **hierarchical** span — a section including its subsections — so **no `direct` count enters the figure on either side**, numerator or denominator, and the degeneracy cannot arise.

Consequently, for the ceiling pass a parent whose `direct` count would be degenerate is **exempt** rather than degraded. It does **not** drop the band, and it does **not** fall back to hierarchical-only reporting, because it is already on hierarchical counts. The only statuses the ceiling pass can return are:

- `measured` — the parent and its largest child were both located, and the share is computed on hierarchical words with the twin named;
- `unmatched` — the parent, or the child, could not be located in the named twin. This is reported, never passed, and it is the ceiling's only failure-to-measure status.

**Which region each pass owns — the two passes cannot contradict each other, and here is why.** `VENUE-R2-04` was raised because on one manuscript the ratio rule refused to print a §5 verdict while this file printed a §5.5 band. That is not a conflict between two opinions about the same quantity; they are two measurements of **different quantities over different regions**, and each owns its own:

| pass | owns | region it sums | basis | can it be `degenerate`? |
|---|---|---|---|---|
| construction-to-analysis ratio (`references/expansion-rules.md`) | the **cross-section mass** between two different sections | the `direct` spans of the construction sections (numerator) and of the analysis section (denominator) — `direct` **subtracts children**, which is why it can collapse | words, `direct` | **yes** — and it must refuse a band when it does |
| largest-child ceiling (this file) | the **within-section distribution** of one parent | the **hierarchical** span of a parent and of its largest child — no subtraction, so nothing collapses | words, hierarchical | **no** — `measured` or `unmatched` only |

So on the calibration manuscript both statements are true at once and neither overrides the other: the ratio pass reports **`degenerate`** for §3/§4/§5, because their `direct` spans are heading lines and the ratio is meaningless; the ceiling pass reports **`measured`, §5.5 = 0.5659, relocation pass required**, because that share is computed from §5's hierarchical words and its child's hierarchical words, where nothing degenerates. The ownership rule is:

- a `degenerate` status from the **ratio** pass never suppresses, downgrades, or invalidates a ceiling band — the ceiling does not read `direct` counts at all;
- a ceiling band never licenses a ratio band — the ratio still refuses if its own basis degenerates;
- the region a pass owns is exactly the region it sums, and an author reporting either verdict states that region, the twin, and the unit.

`D-B3`'s quantitative detector therefore survives the guard: the over-thick subsection is still detected on hierarchical counts, while the ratio declines to speak about the same section because its own basis cannot. One pass falling silent is not the other pass falling silent.

**Worked case, both passes on the same input** (calibration manuscript, markdown twin):

```
ratio  (words, direct)      construction §3+§4 vs analysis §5   12 / 4 = 3.00   -> degenerate, no band
ceiling (words, hierarchical) §5 -> §5.5                        0.5659          -> relocation pass required
```

Neither line contradicts the other, and a pass that prints the ratio's `3.00` as a band — or that withholds the ceiling band because the ratio went `degenerate` — has misread which region it owns.

The shared status vocabulary — `measured`, `degenerate`, `unmatched`, and what a non-zero exit means — is fixed by `SKILL.md` criterion 30, "Status contract for the two mass rules". (It is **not** criterion 21: that criterion is the whole-manuscript citation-key density floor, which has nothing to do with section statuses.)

Corpus distribution, n=561 parent-to-largest-child pairs: median share **0.491**, first quartile 0.367, third quartile 0.607, 90th percentile 0.774; 0.48 of pairs sit above the majority boundary and 0.205 above the outlier boundary (`skills-work/corpus/crypto/statistics.md:330-334`).

**State the ceiling's basis and its provenance honestly, because the number is not the corpus maximum.** 0.491 is the corpus *median* (`skills-work/corpus/crypto/statistics.md:330`), so the majority ceiling is deliberately stricter than the corpus's own practice: 48% of corpus pairs sit above it. It is a discipline line, not an outlier line, and it is justified only in combination with the move-not-delete rule below — a ceiling that cost content would be indefensible, and a ceiling paired with relocation costs nothing. Do not present 0.50 as "what top venues do"; present it as a median-anchored working ceiling whose cost is paid by relocation. The corpus's own tail is recorded at 0.774 (p90, `skills-work/corpus/crypto/statistics.md:332`) and, in the pathological cases, above 1.0 because a child can inherit a parent with no other content (`skills-work/corpus/crypto/statistics.md:336-344`).

A large appendix is normal and is not the defect this rule targets: heavy appendix material is ordinary (`skills-work/corpus/crypto/craft-notes.md:338-349`; appendix words median 644 and appendix share of body-plus-appendix median 0.038, `skills-work/corpus/crypto/statistics.md:385-386`, n=62). The defect is a **body** subsection that carries a parent's majority as prose, not an appendix that carries proofs.

## Move, never delete

Relocation is the whole mechanism. The governing ruling is explicit: relocate the over-thick section's ledger material to an appendix, **never delete a claim**, and keep every statement heading with its status wording intact (`research-work/paper/revision/CAPTAIN-DECISIONS.md:103-109`).

**Every relocation preserves, and the preservation is checkable:**

1. the **claim** and its statement wording, verbatim;
2. its **status label** — `proven`, `transcribed`, `conditional`, `provisional`, `open`, `empirical-conjectural` — which travels with the moved text and is never dropped or softened;
3. every **number** in the moved span, with its digits unchanged;
4. the **provenance** that makes the number auditable (the measurement's source, the environment, the field, the parameters it was taken at);
5. a **pointer** from the old location to the new one, so a reader who looked in the old place is routed;
6. a **deferral inventory** entry, so the pass can prove nothing was lost when material moved — count and list every deferral sentence in the body (`skills-work/corpus/crypto/craft-notes.md:370-372`).

A relocation that drops a status label, rounds a number, or leaves no forwarding pointer is a deletion wearing a move's clothing, and it fails this pass.

## What is relocatable, and what is not

**Relocatable classes** (at least these four; each is ledger material rather than a result):

1. **Verification and recomputation records.** Machine-check transcripts, hand-verification notes, phase checks, re-derivations that confirm a statement already made, and recount logs.
2. **Review and re-review narrative.** How a claim was checked, what a reviewer said, which pointer was repaired, and the history of the wording.
3. **Superseded or refuted metrics.** A value that has been replaced, retained once and **marked** superseded with a pointer to the current value. Retention is required for verifiability; living in the body is not.
4. **Measurement tables and enumeration listings.** Sample counts, enumeration sizes, band boundaries, seeds, resolutions, repetition counts, and flatness checks — everything that supports a number rather than being one.
5. **Tool and script output.** Logs, fixture results, and run records.

**Never relocatable, under any ceiling:**

- a claim, theorem, proposition, lemma, or corollary statement;
- a **status label** or the conditional wording a statement depends on;
- a limitation or open-obligation statement;
- a negative result;
- a value that *is* the paper's result rather than evidence for one;
- a counterexample or the evidence for a claimed *absence* (for example, the audit that shows a region contains no measured values).

The test is not "is this detail?" but "does anything depend on this being in the body?" If a statement's justification depends on it, it stays or it moves **with** a pointer that a reader can follow in one hop. Where the direction is genuinely ambiguous, keep it in the body and record the ambiguity as an unresolved item for the human author rather than resolving it silently.

## Heading-marked evidence records

Relocated material goes to a **heading-marked evidence record**: a section or appendix whose heading identifies it as an evidence or verification record. The marker matters mechanically, not cosmetically — a region scan can then exclude the record by its heading, so a later numeric-placement or region audit can distinguish "this value is in the body" from "this value is in the evidence record". Without the marker, everything moved into the appendix still counts against the body rule it was moved to satisfy.

A pass that moves material without marking the destination has not completed the relocation, because the next audit cannot tell what happened.

## The section-mass measurement step

Any budget claim must be produced by a reproducible measurement, and every printed number must carry its basis. The definitions are fixed and must be quoted rather than paraphrased (`research-work/paper/revision/t4-measure.py:8-17`):

- a section spans from its section heading line to the line before the next **section** heading — subsections never terminate a section;
- **raw** = every line in that span, including blank and comment lines;
- **comment** = a line whose first non-space character is `%`;
- **blank** = a whitespace-only line;
- **content** = neither blank nor comment;
- **words** = whitespace tokens after stripping LaTeX commands and brace/`&`/`#`/`$` characters.

Both conventions are reported, never one silently: the same file measures differently under raw lines, content lines, and words, and the largest-child share moves with the choice. The step prints, per section and per subsection: raw lines, content lines, words, the parent, and the largest-child share — for the tex twin and the md twin **separately**.

**A pass may not mix twins.** A comparison that puts an md figure in the numerator and a tex figure in the denominator is unusable, and so is one that compares raw lines against words. Name the twin, the unit, and the basis before the number.

## Pass output

The section-mass and relocation pass returns, and `## Output Contract` requires:

- **Mass table:** one row per section and per subsection, with raw lines, content lines, and words, the named twin, and the parent it belongs to.
- **Ceiling verdict:** for each parent, the largest-child share with its band (`within budget`, `relocation pass required`, `outlier`).
- **Relocation ledger:** one row per moved span, with the source `file:line`, the destination, the class from the relocatable list, and confirmation that the claim text, status label, numbers, and provenance travelled.
- **Preservation check:** the statement census and the status-label census before and after, which must be equal. A relocation that changes either has deleted something.
- **Pointers added:** the forwarding pointer written at each old location.
- **Residual over-thick regions:** any parent still above the ceiling, with the reason it could not be reduced without deleting a claim.

## Worked calibration

The pass must reproduce these verdicts on the frozen calibration manuscript; these are the contract's measurements, not new ones.

| parent | largest child | share | band | anchor |
|---|---|---|---|---|
| §5 Security analysis | §5.5 | 0.5659 (1880 of 3322 words) | **relocation pass required** — above the majority boundary, below the outlier line | `research-work/paper/final-paper.md:270-394`, child at `:308-367` |

The §5.5 case is the reason this file states its ceiling's provenance: at 56.6% it sits **between the corpus median and the third quartile** (0.491 and 0.607, corpus distributions over n=561 pairs, `skills-work/corpus/crypto/statistics.md:330`), so it is not a corpus outlier and does not by itself prove anything about the corpus. What makes it a defect in the manuscript is the ruler's own instruction to relocate the ledger material, and what makes the fix safe is move-not-delete. A pass that reports §5.5 as balanced has not run; a pass that recommends **deleting** any of its claims has failed, and the correct finding is relocation with the claim, status label, and numbers intact.

## The Related Work floor — the mirror of the ceiling

A ceiling cannot see a section that was never written. The whole file above is an apparatus for shrinking an over-thick section, and every rule in it is a cap; a paper can therefore satisfy all of them while a required section sits at a fraction of corpus practice. That is not hypothetical: the t35 sample's Related Work is **102 words** against the floor of **392** words, and it passed every gate the skill then shipped, because the skill had **no floor rule for it at all** — the registry contained zero rules mentioning "related" and the structural comparison records the gap as "no such rule — verified" (the M5 table of `skills-work/eval/structural-comparison.md`). This section closes it in the same two-sided spirit as the rest of the file. **The floor is not a corpus statistic:** it is an external measurement of n=3, and the next paragraph states that provenance rather than letting the word "corpus" imply otherwise.

**Rule: a located Related Work section carries a floor of 392 words, the median of the measured sample (`n=3`).** A located related-work section that measures fewer words than the floor is a finding and is reported as a breach; at or above the floor it is within corpus practice. The floor is the sample's **median**, not its minimum: the minimum (228) is reported as the sample's spread, and is deliberately **not** used as the rule, so that the threshold sits at corpus practice rather than at the weakest point of a three-paper sample.

`R-3-EXCEPTION: 392 words — external n=3 measurement, NOT corpus-derived.` This marker is here because the exception is real and must be greppable rather than hidden: R-3 requires every numeric threshold to be findable in `corpus/*/statistics.md`, and this one is not findable there, because the corpus contains no related-work size measurement at all. The exemption is claimed openly, the value is stated with its sample size and its provenance table, and the value is therefore **not** written as an inline bound inside a rule-shaped line: an inline `below 392 words` reads as a corpus-derived threshold and would be an R-3 violation in form as well as in substance. The rule is stated over **the floor**, and the floor's value and derivation live here and in the table below.

**Measurements the floor is anchored to, with their sample size stated rather than buried.** The crypto corpus records **no** related-work size distribution — its section census lists `related` with counts `0` and `0` (`skills-work/corpus/crypto/statistics.md:413`), and its per-paper table has no related-work column; the security corpus has no such row either. The only measurement that exists is the t36 structural comparison, in which **3 of 20** comparators expose a related-work section at all (the M5 table of `skills-work/eval/structural-comparison.md`), and those three measure:

| comparator | venue | year | related-work words | anchor |
|---|---|---|---|---|
| `usenix2023-bienstock` | USENIX Security | 2023 | 228 (sample minimum, context only) | `skills-work/eval/metrics.json` → `comparators[14].M5`, `n=3` |
| `ndss2023-real-threshold-ecdsa` | NDSS | 2023 | **392 — the floor (sample median)** | `skills-work/eval/metrics.json` → `percentiles["M5.related_work_words"]`, `n=3` |
| `ndss2023-trellis-robust-and-scalable-metadata-private-anonymo` | NDSS | 2023 | 1067 (sample maximum, context only) | `skills-work/eval/metrics.json` → `comparators[19].M5`, `n=3` |

The raw values are anchored to `skills-work/eval/metrics.json`, a machine-generated data file, by key rather than by line — a line anchor into a file that an active task owns and edits is a clock ticking down (R-23), and the structural comparison itself is cited by name and by its M5 table.

**The two honest weaknesses, stated rather than smoothed over.** First, `n=3` is a small sample and this floor is weaker evidence than every other threshold in the skill; the sample size therefore travels with the number wherever it is printed, and the floor is never quoted without it. Second — and this is a deliberate choice, recorded as such — a floor set at the sample **median** is a *discipline line*, not an outlier line: roughly half of any distribution sits below its own median, so this rule is expected to bite about half the time among papers that have a related-work section, and it must not be presented as "what top venues require". It is the same posture this file already takes for the majority ceiling, which is the corpus median and is likewise stricter than corpus practice. The cost of the rule is bounded by the fact that the fix is cheap and additive — unlike the ceiling, a floor asks for writing that the section should contain anyway, and adds no deletion risk.

**Absence of the section is not a defect.** 17 of 20 comparators fold related work into the introduction, so a paper without a related-work heading is in the corpus majority and is not in breach. When the material lives in a named introduction block, the floor applies to **that block**, and the caller names it with `--related A-B`; the gate then measures it.

**What the instrument does with it.** `count_venue_gates.py` evaluates this as the `related-work-floor` gate, in the same status vocabulary as the rest of the file:

- `measured`, `ok` — a region was located and it clears the floor;
- `measured`, `BREACH` — a region was located and it falls below the floor. The gate prints how many words short it is, the floor with its `n=3`, and the sample's minimum and maximum for context;
- `unmatched` — **no** region was supplied and no heading matches `related work|prior work|related literature`. This is reported as a measurement failure (non-zero exit) and implies **no floor verdict in either direction**; it is never a silent pass. This is also why a located region is what the floor is stated over, not the absence of a section.

The region resolution rules, so the number is comparable with the anchor: the gate takes a span supplied with `--related A-B` when the caller gives one; otherwise it selects the section by heading, using the *same* heading test as the instrument that produced the corpus figures (`skills-work/eval/measure-structure.py`, its related-work heading pattern, cited by name and not by line under R-23), and it measures the section **body with the heading line excluded** — the convention of that same instrument. A gate that included the heading would overstate the section by the heading's own words and stop being comparable with the 228/392/1067 measurements.

**Worked calibration, on the frozen manuscript and on the sample.** Both lines below are measurements of this rule, not new ones, and both name their basis:

| paper | region | measured (whitespace tokens, heading excluded) | verdict |
|---|---|---|---|
| frozen calibration manuscript §1.4 Related work | `research-work/paper/final-paper.md:69-75`, heading at `:68` | **292 words** | **breach** — 100 words below the 392 floor |
| t35 sample §3 Related work | `skills-work/eval/sample-paper/paper.md:69-76`, heading at `:68` | **102 words** | **breach** — 290 words below the floor, and below the sample minimum as well |

The contrast is the point of this section: the sample that passed every other gate sits at 102 words, and the frozen calibration manuscript — a document about to be argued for at a top venue — sits at 292, also below the floor. A pass that reports either as acceptable has not run this rule.

