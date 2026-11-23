# Expansion Rules — The Technical Overview and the Construction

Executable rules for the two places that must be **detailed**. Every floor and every checklist item carries its corpus `file:line`, sample size `n`, and basis.

Basis vocabulary, quoted from `skills-work/corpus/crypto/statistics.md:10-21`: `words` are whitespace-separated alphanumeric tokens of the plain-text rendering; `lines` are physical source lines of the file the unit lives in, comments removed; a section's `words` include its subsections' words unless the number says `direct`, and `direct` means the section's own text with its immediate children's spans subtracted. **Pages are not measurable in a LaTeX source** — the corpus records no page number, so a rule stated in pages is unusable.

## Why a floor is needed at all

Thinness is invisible without a distribution. The corpus's smallest technical overview is 379 words and its first quartile is already 1930 (`skills-work/corpus/crypto/statistics.md:239`, n=18), while its median is 3423. An overview of a few hundred words reads as complete to its own author and is below the corpus floor; the calibration manuscript's overview is 288 words, under the corpus minimum. A skill that never states the floor cannot flag it.

The same holds for the construction. But a **mass** rule alone does not catch the reported defect, and this file says so explicitly rather than pretending otherwise. The bands the rule applies are the row's first quartile and its median: gate `construction-analysis-ratio` prints the ratio it measured and the band that ratio fell in, while the two boundary values themselves are the registry rows `RATIO_FAIL_BELOW` / `RATIO_PASS_AT` in `--constants` (measured, t9: the gate's line carries no `0.44` and no `0.89`). The reported pre-revision construction-to-analysis ratio was 0.576 measured on tex lines and 0.667 on words, both on the **hierarchical** basis (calibration reading) (a section's span including its subsections); the corpus bands in §The construction-to-analysis mass ratio below are stated on the **words, `direct`** basis, and **that basis degenerates on this manuscript**. Sections 3, 4 and 5 carry no direct prose — nearly all their text sits in subsections — so their `direct` spans collapse onto heading lines and measure 8 / 4 / 4 words on the markdown twin and 9 / 5 / 5 on the tex twin, giving ratios of 3.00 and 2.80. Those are meaningless numbers, and they make the rule print **`pass` at or above the band's upper boundary** (`corpus/crypto/statistics.md:285`) for the very §3 that the constituent checklist below calls thin. An independently written counter agrees: t5's instrument computes `direct_words` design = 10 against analysis = 3, a ratio of 3.33. So the mass rule is not the detector for this defect, and it must not be used as one on any manuscript whose `direct` basis degenerates: **the guard in §Degenerate `direct` measurement — the mandatory guard is required**, and the instrument that actually discriminates thin from thick is the constituent checklist in §The construction below, where the thinnest quartile and the thickest quartile separate sharply. Treat the ratio as a guardrail only where its basis is sound, and the checklist as the detector.

## The technical overview

### Placement: content and mass are mandatory, a title is not

**Do not require a separately titled overview section.** Only 29% of tier-A papers have one (18 of 62, `skills-work/corpus/crypto/statistics.md:229`), and a rule keyed on the title misses the other 71%. The corpus's placement variants, with counts (`skills-work/corpus/crypto/statistics.md:230-232`):

- a separate top-level section — 16 papers;
- a named subsection inside the introduction — 4 to 5 papers;
- a named paragraph block inside the introduction — 2 or more papers, a lower bound because authors rename the heading macro.

What is mandatory is that the overview **function** be locatable and that it clear the floors below. Record which form was used and the `file:line` span.

### Floors

**The floor column names where the bound is printed, not the bound** (the re-statement rule of
`scripts/count_venue_gates.py`): gate `overview` prints each floor and the practical target it
builds on, and `--constants` prints the registry rows `OVERVIEW_WORDS_FLOOR`,
`OVERVIEW_LINES_FLOOR` and `OVERVIEW_SHARE_FLOOR`. The corpus VALUE column stays: it is the
distribution the floor was drawn from.

| quantity | floor (printed by) | practical target | corpus distribution (context) | anchor | n |
|---|---|---|---|---|---|
| overview words | **the corpus minimum** — gate `overview` | the first quartile | median 3423 · q3 4420 · max 6360 | `skills-work/corpus/crypto/statistics.md:239` | 18 |
| overview lines | **the corpus minimum** — gate `overview` | the first quartile | median 271.5 | `skills-work/corpus/crypto/statistics.md:240` | 18 |
| overview words / introduction words | **the corpus minimum** — gate `overview` | the first quartile | median 1.48 | `skills-work/corpus/crypto/statistics.md:241` | 18 |
| named sub-blocks inside the overview | **the first quartile** — diagnostic, no verdict | the median | q3 11 · max 23 | `skills-work/corpus/crypto/statistics.md:243` | 19 |
| named block inside the introduction, instead of a section | **the corpus minimum for that block** | its first quartile | median 558 | `skills-work/corpus/crypto/statistics.md:252` | 5 |

The corpus states the reading plainly: the minimum "is the number a draft has to clear before it is comparable to the thinnest overview in this sample; the first quartile is the practical target" (`skills-work/corpus/crypto/statistics.md:245-246`).

A cross-check from the security corpus, usable when the target venue is a security venue: the overview function is present in 27 of 35 papers (77%) and, when present,
it runs a median 2 pages and 1535.5 words (`skills-work/corpus/security/statistics.md:85`, `skills-work/corpus/security/statistics.md:89-92`). The two corpora agree that a paragraph is not an overview.

### Mandatory constituents

All five are required. Each is anchored to a corpus line carrying a real instance, and each is a *reader-necessity*, not a stylistic preference: the corpus's smallest overviews carry them and the thin-draft failure mode is their absence.

1. **The obstacle, stated as a failed first attempt.** Give the natural design and why it does not work, then the fix. Corpus instance: a block literally named `First Attempt.` whose next block is the optimization (`skills-work/corpus/crypto/statistics.md:270`). This is a first-class move, not filler.
2. **The idea, one named sub-block per mechanism.** At least four named sub-blocks, one per mechanism, each with the same shape. Corpus: median 5 named blocks (`skills-work/corpus/crypto/statistics.md:269`), and each block typically states the obstacle, the idea, why it works, and then points forward (`skills-work/corpus/crypto/craft-notes.md:222-249`).
3. **Why it works — a mechanism sentence, not a restatement.** State the property that makes the idea succeed. Corpus: informal statement environments placed next to the formal ones (`skills-work/corpus/crypto/statistics.md:272`); the security corpus records the stable structure as 「难点 → 我们的想法 → 为何可行」 and finds both an intuition sentence and a mechanism sentence in 24 of its 25 deep-read papers (`skills-work/corpus/security/statistics.md:96-102`).
4. **An explicit pointer to the formal statement or proof.** Name the section, theorem, or lemma label that delivers what the overview promised. Corpus: `skills-work/corpus/crypto/statistics.md:274`, instance `T:2608.06724/overview.tex:48`. The security corpus records the same device — for example "See Sec. VI for details." (`skills-work/corpus/security/statistics.md:107`).
5. **A labelled step list in the shape of the final object.** The overview should carry the object's steps in order, in prose or a description list, before the formal construction exists. Corpus: `skills-work/corpus/crypto/statistics.md:273`, instance `T:2608.06724/overview.tex:29`.

Two further devices are supported but optional: a roadmap of the overview's own subsections (`skills-work/corpus/crypto/statistics.md:275`) and an enumeration of challenges, each later answered by name (`skills-work/corpus/crypto/statistics.md:271`). The security corpus adds a sixth useful item — name a recurring condition as a **named object** so later sections can cite it (`skills-work/corpus/security/statistics.md:110`).

### What the overview must not become

- **A second contribution list.** The overview is not interchangeable with the contributions: it is the reader's route into the mechanisms, and the corpus's overviews are larger than the contribution blocks they make concrete (`skills-work/corpus/crypto/craft-notes.md:202-221`).
- **A formula dump.** Prose in the construction and overview carries the *reason* for each formal step, not the notation again (`skills-work/corpus/crypto/craft-notes.md:309-323`).
- **A place for concrete measured values.** See `references/numeric-placement.md`.

## The construction

### How to find the construction section

**Never key on the title.** 69% of tier-A papers have no section whose title contains "Construction" — 43 of 62 (`skills-work/corpus/crypto/statistics.md:112`). Classify by what a section *presents*, and count `Description ...`, `Parameters.`, `Our scheme`, and similar blocks as construction material. The corpus names the papers a title-keyed rule misses (`skills-work/corpus/crypto/statistics.md:293-296`).

### The constituent checklist — the discriminating instrument

Each item below shows its presence share in the **thinnest** and **thickest** quartiles of construction sections (n=7 each), from `skills-work/corpus/crypto/statistics.md:351-370`.

**The binding form of this checklist is the corpus's own DISJUNCTION, not a conjunction of every item (R-30).** At least **one** of `formal_object_box`, `labelled_parameter_list`, `correctness_claim` must be present. The corpus states it that way itself — "a construction section that contains **none** of the box / parameter-list / correctness group is below what this corpus does" (`skills-work/corpus/crypto/statistics.md:321-323`) — and the joint rates are measured, not assumed:

| shape | joint pass | source |
|---|---|---|
| the corpus's own disjunction (box ∨ parameter-list ∨ correctness) | **28 of 36 = 0.778** | `corpus/crypto/statistics.md:321-323`, n=36 construction-role sections |
| the SIX-item conjunction (the five the earlier revision required + `formal_object_box`) — derived: `skills-work/reports/formal-content-audit.md:1`; license: `corpus/crypto/statistics.md:321-323`, n=36 | **2 of 36 = 0.056**, reproduced **2/40 = 0.050** | **repealed by R-30.1** — it rejects 34 of 36 papers, and adding `formal_object_box` to the five-way conjunction rejects **no additional paper** |
| the pre-existing FIVE-item conjunction (`correctness_claim`, `labelled_parameter_list`, `reader_roadmap`, `step_ordering`, `intuition_sentence`) — derived, `skills-work/reports/formal-content-audit.md:1` | **2 of 36 = 0.056**, reproduced **3/40 = 0.075** | the severity was **not** introduced by the sixth item |
| adding `formal_object_box` to the conjunction — derived, `skills-work/reports/formal-content-audit.md:1` | **+0 sections** (2 of 36 either way; 2/40 vs 3/40 in the reproduction — still no gain) | its marginal discriminating power *inside a conjunction* is **zero**, so a longer conjunction is not a stricter floor, only a less honest one |

**Reproduction (three independent runs, all agreeing on the disjunction).** The corpus's own instrument (the values below are this file's own derived readings, declared in `skills-work/reports/formal-content-audit.md:1` §2d, over `corpus/crypto/tools/constituent_joint.py`; the corpus row that licenses them is `corpus/crypto/statistics.md:321-323`, n=36) `corpus/crypto/tools/constituent_joint.py` (t1's, with its own `--self-test`) reports on n=36: disjunction **28/36 = 0.778**, six-way conjunction **2/36 = 0.056** with the last item's marginal effect **+0 papers**, and the "any formal item" alternative (`formal_object_box` ∨ `protocol_diagram` ∨ `algorithm_box`) **17/36 = 0.472**; its per-paper distribution is `{0:5, 1:7, 2:5, 3:8, 4:6, 5:3, 6:2}`. Reading the same population from `corpus/crypto/analyze.jsonl`'s `construction_components` reproduces it exactly (**28/36 = 0.778**, six-way **2/36**, box-alone **17/36**). The joint rates below were then recomputed for this file with the corpus's own detector — `corpus/crypto/tools/analyze.py`'s `COMPONENT_PATTERNS` via `component_report(doc, start, end)` over each paper's largest non-appendix construction-role unit — on **n=40** papers, giving the disjunction **30/40 = 0.750**, the five-way conjunction **3/40 = 0.075**, the six-way **2/40 = 0.050**, `formal_object_box` alone **18/40 = 0.450**, and `step_ordering` ∧ `labelled_parameter_list` **19/40 = 0.475**. The published figures in the table are the t1 audit's (n=36); the two universes differ only in how "largest construction-role section" is bounded. **Every per-paper figure in this file must name its universe**, and a rule may not be justified by a joint rate computed on the other one.

**Every item below is therefore a DIAGNOSTIC with its incidence, and carries no verdict** (R-30.3, R-24a.2). A required-constituent list whose joint pass rate is 0.056 (`skills-work/reports/formal-content-audit.md:1`) is not a floor — it is a fiction, and it would tell an author to add a `reader_roadmap` to every construction section when only 0.241 of the corpus (`corpus/crypto/statistics.md:364`) has one. **The 0-formula defect is closed by two other instruments, and they are two, not one (R-30.4):** the whole-manuscript `formal-density` floor (46.082 inline-math pairs per 1000 alnum tokens, census row `A1`) and the construction disjunction above. They catch **disjoint** cases, which is why neither is redundant — the disjunction rejects a construction section that carries **none** of the three constituents (a section with no formal object), while the density floor rejects a manuscript whose formal content is **too sparse across the whole paper** even if one section happens to carry a box. A draft can pass either and fail the other, so a pass on one says nothing about the other.

**Name the population.** The published incidence of `formal_object_box` is **0.552 of n=29** construction sections (`corpus/crypto/statistics.md:307`) while the joint disjunction rate is measured on **n=36** (`:321-323`): two different universes, and a rule must say which one it is judged on (R-30.6). The row below is judged on the disjunction's n=36; the per-item incidences carry their own n=29.

| # | constituent | thin quartile | thick quartile | anchor | status |
|---|---|---|---|---|---|
| 1 | `correctness_claim` — a correctness or "why it works" statement | 0.0 | 0.857 | `skills-work/corpus/crypto/statistics.md:356` | **in the disjunction** |
| 2 | `labelled_parameter_list` — parameters, algorithms, or parties as a labelled list | 0.143 (thin) | 0.857 (thick) | `skills-work/corpus/crypto/statistics.md:361` | **in the disjunction** |
| 3 | `reader_roadmap` — a statement of how the section is organised | 0.0 | 0.571 | `skills-work/corpus/crypto/statistics.md:364` | diagnostic |
| 4 | `step_ordering` — the steps of the object in order | 0.429 | 1.0 | `skills-work/corpus/crypto/statistics.md:367` | diagnostic |
| 5 | `intuition_sentence` — an intuitive explanation beside the formalism | 0.0 | 0.429 | `skills-work/corpus/crypto/statistics.md:360` | diagnostic |
| 6 | `formal_object_box` — a displayed or labelled formal object: an equation, a definition, or a labelled box | 0.571 | 0.571 | baseline 0.552 of n=29, `skills-work/corpus/crypto/statistics.md:307`; thin/thick `:358` | **in the disjunction** |
| 7 | `security_notion_needed` — the construction names the notion the analysis will prove | 0.0 | 0.286 | `skills-work/corpus/crypto/statistics.md:366` | diagnostic |
| 8 | `why_necessary` — why each ingredient is needed | 0.0 | 0.286 | `skills-work/corpus/crypto/statistics.md:369` | diagnostic |
| 9 | `citation_to_prior_building_block` — build-up from named prior constructions | 0.0 | 0.286 | `skills-work/corpus/crypto/statistics.md:354` | diagnostic |
| 10 | `complexity_statement` — the cost or complexity of the object stated | 0.143 | 0.143 | baseline 0.241 of n=29, `skills-work/corpus/crypto/statistics.md:304`; thin/thick `:355` | diagnostic |

**`formal_object_box` is in the disjunction — and its justification is deliberately NOT a thin-versus-thick gap.** The prose-and-structure items are all satisfiable by a construction section that contains **no formula, no notation and no labelled object at all**; that is exactly how a draft with zero formulas passed every gate the skill shipped. The corpus row that licenses the requirement is the **baseline incidence**: `formal_object_box` is present in **0.552 of the 29 construction sections** (16 of 29, `skills-work/corpus/crypto/statistics.md:307`, n=29), the second-highest incidence among the construction constituents above after `labelled_parameter_list` 0.586 and `step_ordering` 0.69 — i.e. **above `correctness_claim` (0.414) and far above `reader_roadmap` (0.241) and `intuition_sentence` (0.207)** (`skills-work/corpus/crypto/statistics.md:305`, `:309`, `:313`; the same table's quartile columns are at `corpus/crypto/statistics.md:350-370`). The rule is therefore stated as a **floor on the section's content**, and this file does **not** claim that it discriminates thin from thick: the row reads 0.571 against 0.571 between the quartiles (`skills-work/corpus/crypto/statistics.md:358`), so it is a **presence** requirement. Stated that way it is still the instrument for the reported defect, because the defect is **absence**, not thinness.

**`complexity_statement` is deliberately NOT in the disjunction, and the same table (`corpus/crypto/statistics.md:350-370`) is the reason.** It appears in 0.241 of the 29 construction sections (7 of 29, `skills-work/corpus/crypto/statistics.md:304`) and in **0.143 of both quartiles** (`skills-work/corpus/crypto/statistics.md:355`): it separates nothing, and putting it in the disjunction would place the rule **below the practice of three quarters of the corpus** — a subfield preference dressed as corpus practice. It stays a **diagnostic**, as do `algorithm_box` (0.172) and `protocol_diagram` (0.379). The decision is recorded here rather than left implicit, because "which constituents are required" is the checklist's whole content.

Baseline shares over the whole construction sample (n=29), so a section can be compared against the corpus rather than against the thin quartile only: `step_ordering` 0.69, `labelled_parameter_list` 0.586, `formal_object_box` 0.552, `correctness_claim` 0.414, `protocol_diagram` 0.379, `complexity_statement` 0.241 (`skills-work/corpus/crypto/statistics.md:316`, `skills-work/corpus/crypto/statistics.md:310`, `skills-work/corpus/crypto/statistics.md:307`, `skills-work/corpus/crypto/statistics.md:305`, `skills-work/corpus/crypto/statistics.md:312`, `skills-work/corpus/crypto/statistics.md:304`). The two incidence rows that differ between the baseline and the quartile table are used here for **two different jobs and must not be conflated**: the thin/thick columns decide which items are *discriminating* (items 1–5), and the baseline incidence decides which items are *common enough to require* (item 6). A required constituent needs only the second; claiming the first for `formal_object_box` would contradict `:358`.

Two corpus warnings about the table. First, the automated counts are a **lower bound**: authors rename heading macros, so a named block may exist undetected. Second, two constituents are genuinely rare in the corpus (`parameter_choice_reason` 0.0, `worked_example` 0.0, `skills-work/corpus/crypto/statistics.md:311`, `skills-work/corpus/crypto/statistics.md:319`), so their absence is **not** a defect — do not add them just to tick the list.

The security corpus supplies an independent, compatible checklist for a concrete scheme section, usable as a cross-check: a named object or relation (19 of 25), a protocol or algorithm box (10 of 25), a parameter-choice justification (15 of 25), and a complexity or communication expression (17 of 25) (`skills-work/corpus/security/statistics.md:131-138`). It also records the cap: a named-object definition is what makes a recurring condition citable, and the mechanism explanation belongs in prose rather than in a regular expression (`skills-work/corpus/security/statistics.md:140-143`).

### The construction-to-analysis mass ratio

**Basis: words, `direct` measurement** — the section's own text with its immediate children's spans subtracted (`skills-work/corpus/crypto/statistics.md:18-19`). State the basis with every number you print.

**The two boundaries are the registry's to state, not this file's to recite** (the re-statement rule of
`scripts/count_venue_gates.py`): gate `construction-analysis-ratio` prints the ratio it measured
against the boundary it applied, and `--constants` carries the registry rows `RATIO_FAIL_BELOW`
and `RATIO_PASS_AT`. The band LABELS and their corpus meaning are this file's content.

| band (gate `construction-analysis-ratio`) | at, relative to the corpus distribution | corpus meaning | anchor |
|---|---|---|---|
| **fail** | below the **first quartile** | thinner than the corpus first quartile (n=10) | `skills-work/corpus/crypto/statistics.md:285` |
| **needs expansion** | from the first quartile to below the **median** | above the first quartile, below the median | `skills-work/corpus/crypto/statistics.md:285` |
| **pass** | at or above the **median** | at or above the corpus median | `skills-work/corpus/crypto/statistics.md:285` |

Corpus distribution on that basis: min 0.11 · q1 · median · q3 1.41 · max 2.88, n=10 — the two
boundaries are the first quartile and the median of that same row. Only two fifths of pairs exceed 1
and seven tenths exceed 0.5 (`skills-work/corpus/crypto/statistics.md:288`, which carries the two
shares), so **"the construction must exceed the analysis" is not supported by the corpus and must
not be written as a rule.**

A second figure exists on a different basis and must not be mixed with the first: on **words with appendix sections of the same role added** (construction n=36 · analysis n=40), n rises to 17 and the median ratio is 1.1, q1 0.39, q3 1.64 (`skills-work/corpus/crypto/statistics.md:290`). **The two rows are the SAME population measured on two bases** — the rule's own bars (the first quartile as the fail boundary, the median as the pass boundary, and the 40%/70% shares of pairs above 1 and above 0.5) all come off the `direct`-words row at `skills-work/corpus/crypto/statistics.md:283-288`, while `:290` is that population re-measured with same-role appendices included (t7 provenance audit, `skills-work/reports/venue/t7-provenance-audit.md`); the two may be quoted side by side and never substituted. A third, on **lines with hierarchical spans**, has median 1.21 and q1 0.36 (`skills-work/corpus/crypto/statistics.md:286`). Choose one, name it, and keep the comparison inside it.

The basis-dependence is not academic. The same manuscript measures 0.576 on tex lines and 0.667 on words before revision, and 0.9524 on tex lines against 1.3120 on md lines after — different bases, different verdicts at the same moment in the paper's history. Any printed ratio without its named basis is unusable, and md and tex measurements may not be mixed in one comparison.

Cross-venue check available for a security-venue paper: the security corpus reports a construction-to-proof page ratio with a median of 5 to 1 (construction median 5 pages, proof median 1 page, `skills-work/corpus/security/statistics.md:124`), on a page basis. Because the crypto corpus cannot measure pages at all, **do not transfer that figure into a LaTeX-source measurement** — use it only when the unit really is pages.

### Degenerate `direct` measurement — the mandatory guard

**This guard is mandatory, and it is carried by the registry row for R-VENUE-13 as well as by this file, because downstream execution follows the registry row rather than this prose.**

**What degeneracy is.** A section's `direct` count is the section's own text with its immediate children's spans subtracted (`skills-work/corpus/crypto/statistics.md:18-19`). When a section's prose lives almost entirely in its subsections, that subtraction leaves only the section heading and stray connective lines, and the `direct` number stops measuring text and starts measuring headings.

**Detection.** Treat the `direct` basis as **degenerate** for a section when either holds:

- the section's `direct` word count is **smaller than the word count of its own heading** plus a small allowance, or more plainly smaller than 20 words; **or**
- the section's `direct` span contains **no running prose** — every counted line is a heading, a label, or a fragment.

Report the detection as a named observation per section, with the `direct` count, the heading count, and the twin.

**Scope of the guard — which sections it covers, and on which side.** The guard is evaluated for **every section whose `direct` count enters the printed figure, numerator and denominator alike**. For the construction-to-analysis ratio that is:

- **the numerator** — each section classified as construction by content (see §How to find the construction section), summed;
- **the denominator** — the section classified as analysis, whose `direct` count forms the whole denominator.

A degenerate reading on *either* side makes the ratio meaningless, so both sides are tested. The ratio is printed **only when every contributing section returns `measured`**. If any contributing section returns `degenerate`, the ratio is reported as **not evaluated on the `direct` basis**, with the hierarchical numbers, the named twin and unit, and the offending section named — never as a band verdict. If a contributing section cannot be located at all, its status is `unmatched`, which has the same consequence.

The guard does **not** cover the overview floors of §Floors, which are absolute word and line counts on a named span rather than a `direct` ratio; those are reported against their floors with the twin and unit named, and a span that cannot be located is `unmatched`.

**Required behaviour when it fires.** The rule **must not** output a corpus band conclusion for that section:
- it **must not** print `pass`, `needs expansion`, or `fail`, and must not quote the ratio bands at all (neither the values nor the words), because the input to those bands is meaningless;
- it reports **only the hierarchical numbers** — the section spans with subsections included — together with the **named twin** (`tex` or `md`) and the **named unit** (`raw lines`, `content lines`, or `words`);
- it states which sections tripped the guard, and reports the ratio as **not evaluated on the `direct` basis**;
- for the thin/thick judgement it falls back to the constituent checklist in §The constituent checklist, which is the discriminating instrument anyway.

**Why this is not optional — the measured failure.** On the calibration manuscript the guard is the difference between a correct verdict and a false negative. Sections 3, 4 and 5 carry no direct prose, so:

| twin | §3 direct | §4 direct | §5 direct | printed ratio | verdict the unguarded rule printed |
|---|---|---|---|---|---|
| markdown | 8 words | 4 words | 4 words | 3.00 | `pass` at or above the median |
| tex | 9 words | 5 words | 5 words | 2.80 | `pass` at or above the median |

Those `direct` counts are heading lines, not content. The rule as written *without* the guard therefore prints **`pass` for §3**, a section the constituent checklist simultaneously calls thin. Two independently written counters produce the same degenerate reading — this file's tokenizer gives 8 / 4 / 4 and 9 / 5 / 5, and t5's instrument computes `direct_words` design = 10 against analysis = 3, a ratio of 3.33. A false-negative instrument is worse than a missing rule, which is why the guard is a hard requirement rather than advice.

### Deferral discipline

The construction is allowed to defer detail, but the deferral must be **named** and nothing may be lost. The corpus defers proofs and says where (`skills-work/corpus/crypto/craft-notes.md:324-337`), and the deferral count is small: forward references inside a construction section have a median of 0 and a maximum of 3 (`skills-work/corpus/crypto/statistics.md:387`, n=29). When material moves out of the construction, record it in the relocation ledger required by `references/section-budget.md` and keep its claim and status wording.

## The formal-content floors

Every floor above is a floor on **prose**. That is the whole shape of the skill's earlier rule set:
each gate of `scripts/count_venue_gates.py` counted words, allocated words between regions, or
capped words, so a paper with **no formula, no notation, no cross-reference and no label** was
indistinguishable from a compliant one: the t35 sample paper sits at zero on all of those rows and
passed every gate the skill then shipped, while the frozen calibration manuscript sits inside the
corpus distribution on them (§Appendix C of the census file named below).
The floors below close that dimension. **Their anchors are the census rows the criteria name** —
`A1` for the whole-manuscript inline-math floor, `A12` for citation keys, `A10` and `A11` for
reference calls and labels, `A18` for the statement/proof sum, `A17` for float forms, and `A14` and
`A15` for source composition — in `skills-work/audit/evidence-structure-census.md`, whose rows are
**append-only**: rows `A3`, `A4`, `A6`, `A7` and `A9` are the context printed beside those floors,
and they are not floors. A rule cites a row by its **anchor id**, and the id is the part that does
not move.

**Citations are by anchor id, never by line number.** The calibration file
`skills-work/audit/evidence-structure-census.md` is rewritten in place whenever rows are appended,
and its own §Appendix G records the consequence for a citation: census row `A1` has been at 51, then 55, then 57. A rule therefore cites the census **anchor id** (`row A1`) and the reader resolves it through
that file's §Appendix F table; the instrument resolves it at run time (`--validate-anchors` prints
every anchor it cites with its current line and exits 2 when one fails to resolve), so a stale
citation is a measurement failure rather than a silent drift.

**Basis for every row.** `words` = alphanumeric tokens (`[A-Za-z0-9]+`) over the comment-stripped
LaTeX source; on a markdown twin, the same regex over the file text. `per 1000 words` is
1000 x count / words. This is the tokenizer of the census, so a printed density is comparable with
the row it is judged against and not merely similar to it.

**Scope is part of the basis — one rule, applied to every row below.** The census rows are
**whole-paper** rows: each is measured over a paper's entire source. A threshold derived from such
a row may therefore only be applied to a **whole-paper** measurement. Two consequences, both
mandatory:

1. the **binding** form of every WHOLE-PAPER floor below is the whole-manuscript measurement;
2. a measurement restricted to a named span is judged on **that span's own corpus row where one
   exists**. Two cases, and they are not the same:
   * **construction / analysis spans have their own rows** (`corpus/crypto/statistics.md` §FORMAL.2,
     construction n=36 / analysis n=40) and the floor there is **BINDING** — see the role row in
     the table below. An earlier revision of this file and of R-27 claimed that "no region-scoped
     corpus row exists" and kept this axis non-binding on that ground. **The claim was false and is
     withdrawn (R-32 F-4)**; the axis is binding, and on the frozen calibration manuscript it fires
     (its §4 lands below the construction role's first quartile — the gate prints both numbers),
     which is the defect the user reported;
   * a span with **no** row of its own (ad-hoc spans, a span whose role the caller cannot name) is
     reported **without a verdict**, and the instrument says so in its own output rather than
     leaving the reader to infer it. The reason is now the honest one: the row does not exist for
     THAT span, not that region rows are absent in general.

### The floors

| # | row | floor (binding) | corpus value at the anchor | anchor | n | scope |
|---|---|---|---|---|---|---|
| census A1 | inline math per 1000 words, whole manuscript | **the tier-A first quartile** — gate `formal-density` prints it | median 54.940 · q3 64.373 · max 88.288 · min 4.700 · **0 of 62 at zero** | `skills-work/audit/evidence-structure-census.md` row `A1` | 62 | whole paper |
| census A12 | citation keys per 1000 words, whole manuscript | **the tier-A first quartile** — gate `citation-density` prints it | median 4.798 · q3 6.199 · min 1.108 · median 100.5 keys per paper | `skills-work/audit/evidence-structure-census.md` row `A12` | 62 | whole paper |
| census A10 | reference calls per 1000 words, whole manuscript | **the row's own per-1000-word first quartile** — gate `ref-density` prints it | q1 2.778 (context) · median 3.468 (context) · q3 5.687 | `skills-work/audit/evidence-structure-census.md` row `A10` | 62 | whole paper |
| census A11 | labels per manuscript | **at least one label** (0 of 62 papers have zero) — gate `ref-resolvability` | min 2 · median 49.5 · q3 79 · labels/refs median 0.601 (context) | `skills-work/audit/evidence-structure-census.md` row `A11` | 62 | whole paper |
| §FORMAL.2 role rows | inline math per 1000 words over the construction/analysis span | **the role's first quartile** (`corpus/crypto/statistics.md:650-660`, the §FORMAL.2 role table; construction n=36 · analysis n=40) — gate `formal-density-role` prints both | construction median 113.72 / 3 of 36 at zero · analysis median 114.83 / 1 of 40 at zero | `corpus/crypto/statistics.md` §FORMAL.2 (reproduce: `corpus/crypto/tools/formal_by_role.py`) | 36 / 40 | region (construction or analysis) |
| census A18 | statement apparatus = theorem-family + `proof` environments, per 1000 words | **the combined row's first quartile** — gate `statement-apparatus` prints it — **plus** the zero-rate rule (zero-rate 0.0484 = 3 of 62 < 0.20, so **zero combined apparatus breaches unless a `not-applicable` filing is recorded**) | median 1.778 · q3 2.373 · 4 of 62 have a theorem env but no proof, 1 of 62 the reverse | `skills-work/audit/evidence-structure-census.md` row `A18` | 62 | whole paper |
| census A17 | float forms (`figure` + `table` float + `tabular` body) per 1000 words | **the combined row's first quartile** — gate `float-presence` prints it — **plus** the zero-rate rule (zero-rate 0.1129 = 7 of 62 < 0.20, so **no float form at all breaches**) | median 0.347 per 1000 · median 9.0 per paper · q3 0.781 · max 2.579 | `skills-work/audit/evidence-structure-census.md` row `A17` | 62 | whole paper |
| census A11 (structural) | reference resolvability | **every `\ref`/`\eqref`/`\autoref`/`\cref` target has a `\label` in the same twin** | not a distribution but a structural invariant; the label floor above is what the corpus measures | `skills-work/audit/evidence-structure-census.md` row `A11` | 62 | whole manuscript |
| census A20 (evidence, **not bound by this skill**) | display-only combined basis = `\[ … \]` displays + equation-family environments (**inline excluded**), per 1000 words | **no floor** — the gate judges on the equation-family basis (criterion 17) and refuses any other basis; the row exists so that a caller may name it with `--combined-display-row A20`, and it is the **only** combined row whose numerator equals this gate's count | q1 **1.331** · median 2.381 · q3 3.038 · max 7.591 · **2 of 62 at zero** (zero-rate 0.0323) · 1 531 + 3 159 = 4 690 display objects | `skills-work/audit/evidence-structure-census.md` row `A20` (refused alternative: row `A19`, which counts inline) | 62 | whole paper |

**Why the float floor sits on the COMBINED row and not on the single-form rows.** This is the
general shape of a licensed floor, and the census measures it rather than asserting it: per-paper zero-rates are **0.258** for `figure` (`skills-work/audit/evidence-structure-census.md` row A6), **0.468** for `table` floats (census row A7) and **0.419** for `algorithm`/`protocol` boxes (census row A9) — a floor on any of them would misjudge a quarter to nearly half of the accepted corpus — while the combined row's zero-rate is **0.1129** (7 of 62, census row A17).
A floor may only be set on a quantity the corpus itself treats as near-universal, and the
selection is a measurement, not a preference. Both single-form rows, and the algorithm-box row, therefore print as
**context** in the instrument's output and never judge.

**Two rows are deliberately NOT stated as floors.**

- **Statement and proof environments — the floor is on their SUM (row A18), not on A3/A4.** The
  single axes are genre signals (`skills-work/audit/evidence-structure-census.md` row A3 / row A4): `theorem_envs` first quartile **0.488** (`skills-work/audit/evidence-structure-census.md` row A3) with **4 of 62** at zero,
  `proof_envs` first quartile **0.174** (`skills-work/audit/evidence-structure-census.md` row A4) with **7 of 62** at zero, and the census records **4 of 62**
  papers with a theorem environment but no proof and **1 of 62** the reverse. Their **sum** is
  near-universal (census row A18): per-paper zero-rate **0.0484** (3 of 62), first quartile **0.712** per 1000 words,
  median 1.778, third quartile 2.373 (census row `A18`). Consequently the **combined row carries the
  binding floor (`skills-work/audit/evidence-structure-census.md` row `A18`)**, **census rows `A3` and `A4` print as `context only`**, a draft with zero combined
  apparatus is judged leniently **only** with a recorded `not-applicable` filing (the genre caveat —
  a paper that proves no statement is not thereby defective), and that filing does **not** discharge
  the density floor. This skill's own recalculation of the combined row over the 62 tier-A papers
  gives first quartile **0.717** (context; its input row is `skills-work/audit/evidence-structure-census.md` row `A18`). **Population caveat:** over all 127 measured papers the
  same quantity has **40 at zero** (zero-rate 0.3150; census row A18 over all measured papers) and first quartile 0.000, so the floor is on
  the tier-A population and the instrument prints that caveat beside the number.
- **Source composition (census rows A14/A15).** Float line share first quartile **0.016** (`skills-work/audit/evidence-structure-census.md` row `A14`) and math line
  share first quartile **0.053** (`skills-work/audit/evidence-structure-census.md` row `A15`). The
  census proposes no floor and no ceiling for these; they are reported as diagnostics so that a
  draft at 0.000 on both rows is visibly an outlier on two rows at once.
- **The display-only combined basis (row `A20`) — evidence for a caller, not a floor this skill
  binds.** The census now carries **two** rows that combine display objects, and they are **not
  interchangeable**: row `A19` is inline `$…$` pairs **+** `\[ … \]` displays **+** equation-family
  environments (`skills-work/audit/evidence-structure-census.md` row A19, first quartile 48.452, n=62), row `A20` is the display-only basis that **excludes**
  inline (`\[ … \]` displays + equation-family environments; census row A20, first quartile **1.331**, median 2.381,
  **2 of 62 at zero**, zero-rate 0.0323, n=62; totals 1 531 bracketed + 3 159 environments = 4 690
  display objects). This skill's display gate reports the bracketed count and the combined count but
  **judges on the equation-family basis** (criterion 17), because the census's own worked case shows
  the frozen calibration manuscript at **0.634** on the A20 basis — **below A20's first quartile** —
  while carrying **1 244** inline mathematics and clearing census row `A1` comfortably, and of the **16 of
  62** papers below A20's first quartile the inline-only density has median **52.9** against the
  corpus inline median **54.5**. The axis separates **formatting, not mathematical content**. A
  caller who nonetheless wants the combined zero-rule must supply `--combined-display-row <ROW-ID>`,
  and the instrument then reads that row's **own heading** at run time: `A20` is accepted (it
  excludes inline), `A19` is **refused** as a basis substitution (it counts inline as a component),
  and a row whose heading says neither is refused as an unreadable basis. A refused row is
  `unmatched` **with a breach and a non-zero exit** — never a silent substitution and never a pass.

**Why the floors are quartiles and minima, and never medians.** A median floor fails half the
corpus. The inline-math median (54.940, `skills-work/audit/evidence-structure-census.md` row `A1`, n=62) is above the frozen calibration manuscript's own whole-paper
figure (53.196), so a median floor would have flagged a healthy paper — the floors here are the
first quartiles or the measured boundary, and each prints its population and its n beside the
number. For the same reason the **region-scoped** inline-math density of the calibration manuscript
(measured over its construction and analysis span) is **not** compared with the
whole-paper quantile: the two statistics have different scopes, and no corpus row licenses treating
them as one. It is judged on its own scope instead — the per-role table of §FORMAL.2, whose
construction and analysis first quartiles are the **binding** floors of criterion 20a — so "different
scope" here means a different row, never the absence of one.

### The reproducible command

The formal apparatus is a **metric of this skill**, printed by the same instrument as the other
gates, so no pass has to be assembled by hand:

```bash
cd skills-work/crypto-research-agent-skills
# the region map is required; --formal is the construction/analysis span, and the role floor of
# criterion 20a is judged on it, so supply it whenever the draft has a construction section
python3 skills/crypto-venue-paper-writing/scripts/count_venue_gates.py \
    --manuscript <your.md|your.tex> --twin md|tex \
    --regions '{"abstract":[a,b],"contributions":[c,d],"introduction":[e,f],"overview":[g,h]}' \
    --formal A-B --formal-role construction   # repeatable; the whole-paper rows do not need it
# the frozen calibration manuscript, sha256-pinned:
python3 skills/crypto-venue-paper-writing/scripts/count_venue_gates.py \
    --manuscript research-work/paper/final-paper.md --calibration-regions
```

Exit codes: **0** measured clean and unbreached · **3** a threshold breached · **2** a gate could
not be measured (degenerate/unmatched, a missing region map, an out-of-range span, or a
`--calibration-regions` sha256 mismatch) · **1** a verdict-path failure (`--dename`). A zero-formula
draft exits **3**; it is never a clean run with a note.

## Pass output

The expansion pass returns, and `## Output Contract` requires:

- **Overview:** the `file:line` span, its placement form, words, lines, and share of the introduction, each against floor and target; the present/absent mark for each of the five mandatory constituents; the named sub-block count.
- **Construction:** the sections classified as construction and the rule used to classify them (content, not title); words and the named basis; the ratio and its band; the present/absent mark for each checklist item **including the required `formal_object_box`**; the list of constituents absent relative to the thick quartile.
- **Formal apparatus:** one row per formal row of `scripts/count_venue_gates.py` — the measured value, its **scope** (whole manuscript for the whole-paper rows; the declared span for the role-scoped and overview rows, which are **binding** on their own corpus rows under R-32 F-4), its threshold or, where the row genuinely carries no bound, its explicit non-binding label, and its corpus anchor id. Inline math is reported three times — whole manuscript (criterion 20, row `A1`), the declared construction/analysis span under its declared role (criterion 20a, §FORMAL.2), and the declared overview span (`overview-formal-density`) — and no one of the three may be substituted for another. An `unmatched` formal row is a finding, not an omission and not a pass.
- **Additions ledger:** one row per added sentence, with the source it restates — the manuscript, the design record, or an artifact. An addition with no source is a new claim and is not permitted here.
- **Residual shortfalls:** any region still below its floor, with the reason, and the explicit statement of whether a corpus line licenses the exception.

## Worked calibration

The pass must reproduce these verdicts on the frozen calibration manuscript; they are the contract's measurements, not new ones.

| region | measured | floor / target | verdict |
|---|---|---|---|
| §1.3 technical overview `research-work/paper/final-paper.md:60-67` | 288 words / 8 lines | floor 379 words · 99 lines (`corpus/crypto/statistics.md:239-240`) | **breach** — below the corpus minimum |
| overview share of the introduction | **0.1567** (floor row `corpus/crypto/statistics.md:241`) = overview 288 words ÷ region **1838** words, region `research-work/paper/final-paper.md:29-75`, basis **whitespace tokens (`\S+`)** | floor 0.25 | **breach on allocation** — the overview is also smaller than the 902-word contribution list it exists to make concrete. The region is named because the figure moves with it: the region is the introduction's budgeted subsection block, from §1.1 at `:29` to the last line before §2 at `:75`. Widening it to `:23-75` — the §1 heading plus its two framing paragraphs, which are not budgeted subsections — gives 288 ÷ 2102 = **0.1370**, a different number, so the two are never mixed and neither is quoted without its region. |
| §3 host protocol `research-work/paper/final-paper.md:106-157` | 1089 words | 5-item checklist | **thin** — but read the corrected reason below: §3 has more than the earlier text claimed |
| §4 construction `research-work/paper/final-paper.md:158-269` | 2646 words | 5-item checklist | **passes the checklist 5 of 5** — the earlier text called it thin and was wrong on its stated grounds |
| §3/§4/§5 `direct` basis (the rule's mandated basis) | 8 / 4 / 4 words (md), 9 / 5 / 5 (tex) | ratios 3.00 (md) and 2.80 (tex) against the corpus band (`corpus/crypto/statistics.md:285`, n=10) | **guard fires** — the basis is degenerate, so **no band verdict is printed**; only the hierarchical numbers are reported, with the twin and unit named |
| construction/analysis ratio, tex lines, hierarchical basis | 0.9524 | instrument reproduction, not a corpus-band comparison | **within band** — recorded with its basis |
| construction/analysis ratio, md lines, hierarchical basis | 1.3120 | same | **within band** |
| construction/analysis ratio, md words, hierarchical basis | 1.1243 | same | **within band** |
| same ratio before revision, tex lines, hierarchical basis | 0.576 | below the corpus first quartile (`corpus/crypto/statistics.md:290`, n=17, a different basis) in spirit, but a different basis — see the note below | **needs expansion** — the band that the mass rule alone would have left alone |

Two notes that a pass must reproduce, because they are where a careless report goes wrong.

First, the corpus bands (whose two boundaries are the row's first quartile and median, read from `--constants` and NOT printed by the gate) are on **words, `direct`**; the manuscript figures above are on **hierarchical** spans. They may be **reported side by side but never substituted for one another**. The ratio's job on the manuscript is to reproduce the instrument's frozen reading, and its job against the corpus is a separate, explicitly cross-basis indication. On this manuscript the `direct` basis trips the degeneracy guard, so no band verdict is printed at all.

Second, the last-but-one row is the honesty check on this file: a rule that measured mass alone would have called the pre-revision §3/§4 acceptable, because 0.576 sits above the first quartile, and would now print `pass` for a thin §3 through a degenerate basis. **The five-item checklist is what names §3 as thin**, and a pass that reports only the ratio has not run.

### The corrected §3 and §4 verdicts (non-normative calibration record), and why the earlier text was wrong

**The caution criterion 15 delegates here.** The calibration manuscript's §3 *is* thin, but not for the reason an earlier draft of the rules gave — §3.4 (`research-work/paper/final-paper.md:131-151`) is an ordered round-by-round message flow, so §3 fails on its **parameter list** and **roadmap**, not on message ordering; and its §4 **passes the required checklist in full** (`research-work/paper/final-paper.md:174-181`, worked instance `:266`). This block is where the manuscript literals live, so the rule statements in `SKILL.md` can stay free of them (R-5).

The earlier version of this table stated that §3 had "no ordered message flow and no drawn instance" and that §4 had "no worked table layout and no per-round algorithm box". **Both reasons were false against the manuscript, and a calibration table whose stated reason does not match the text gets copied into reviews, so the corrections are recorded here rather than quietly edited.** A verdict is recorded with the text that produced it, not only with its conclusion.

| region | the superseded claim (withdrawn — nothing in this column is asserted by this file) | what the manuscript actually contains | corrected verdict |
|---|---|---|---|
| §3 host protocol | "no ordered message flow and no drawn instance" | an ordered round-by-round message flow at `research-work/paper/final-paper.md:131-151`, opening "One round of the host proceeds as follows. The prover commits …" and then answering in turn and ordering the two sumchecks over the same committed table | **`thin` stands; the stated reason was wrong.** §3 *has* the step-ordering constituent and fails instead on its **labelled parameter list** and its **reader roadmap** |
| §4 construction | "no worked table layout and no per-round algorithm box" | the row-band layout table at `research-work/paper/final-paper.md:174-181` (content / randomness / flood / padding bands, each with its row-index range) and a worked instance at `research-work/paper/final-paper.md:266` — one masking row at `u = mu + n + 1 = 2^13 + 1`, `R' = 2^14`, `M = 2^10 - 1 = 1023` | **`thin` is withdrawn.** §4 **passes the construction disjunction** (it carries a labelled layout table, i.e. a `labelled_parameter_list` and a `formal_object_box`); the per-round algorithm box is a *diagnostic* item whose absence does not make a section thin (R-30.3) |

So the verdicts this file now expects from a pass are: the §1.3 overview **thin** (under the corpus minimum gate `overview` prints), §3 **thin** on the parameter-list and roadmap constituents, §4 **passing** the required checklist, and the §5 subsection share **over the majority ceiling** (gate `largest-child-ceiling`) — see `references/section-budget.md`. A pass that copies "§4 is thin" into a review, or that justifies §3's thinness by message ordering, contradicts the manuscript and has not run.
