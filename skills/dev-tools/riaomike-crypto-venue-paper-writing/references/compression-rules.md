# Compression Rules — The Abstract and the Contribution List

Executable rules for the two places that must be condensed. Every threshold carries its corpus `file:line`, sample size `n`, and measurement basis. The basis vocabulary is fixed by the corpus and must be quoted with any number taken from it:

- `words` — whitespace-separated alphanumeric tokens of the plain-text rendering of the LaTeX source.
- `lines` — physical source lines of the file the unit lives in, comments removed.
- A section's `words` include its subsections' words unless the number says `direct`; `direct` means the section's own text with its immediate children's spans subtracted.
- Quantiles are computed on the sorted sample with `round(p * (n-1))` indexing; `median` is measured.

Source: `skills-work/corpus/crypto/statistics.md:10-21` (bases), n=59 tier-A abstracts and n=50 tier-A contribution blocks.

## What this pass is for

A cap on length alone does not fix a wordy abstract. The corpus's own upper tail reaches 483 words and its third quartile is 253 (`skills-work/corpus/crypto/statistics.md:121`), so a 250-word cap sits at the corpus third quartile and licenses exactly the long tail the defect report describes. The reported failure mode is an **allocation** defect as much as a length defect: an abstract that reports proved bounds, conditional theorems, and an open problem across most of its paragraphs, while the construction the paper is named after receives one sentence.

Therefore this pass always reports four abstract numbers and five contribution-list numbers, and treats a cap breach and an allocation breach as separate findings.

## Thresholds

**The rule column names the gate that prints the bound, and the bound is the instrument's to print at run time.** Bounds *are* written in this file where a rule is unreadable without one, and they are written under the re-statement rule of `scripts/count_venue_gates.py`, which is a **licence test rather than a ban**: a bound may be stated on a line that carries the citation its own `--constants` registry row declares — or, on a line with no other citation, that row's sample size `n` — and `--restatement-check` flags the bounds written without one. So the true statement is "every bound here carries its licence, and the licence is checkable", not "this file recites no bound"; `--restatement-report` prints each written bound with the pointer that excused it. The
corpus-value column is distribution CONTEXT — a quantile, a maximum, a pooled share — which is why
it stays: it says what the cap costs, not what the cap is. Run `cd skills-work/crypto-research-agent-skills` then
`python3 skills/crypto-venue-paper-writing/scripts/count_venue_gates.py --constants` for every bound with its printing gate, or read the bound off
the gate's own output line.

### The abstract

| quantity | rule (printed by) | corpus distribution (context) | anchor | n |
|---|---|---|---|---|
| total words | **at most the corpus median** — gate `abstract-words` | median · q1 144 · q3 253 · max 483 | `skills-work/corpus/crypto/statistics.md:121` | 59 |
| build share | **at least the corpus pooled share** — gate `abstract-build-share` | the pooled value is the floor | `skills-work/corpus/crypto/statistics.md:165` | 15 |
| longest sentence | **at most the corpus median** — gate `abstract-longest-sentence` | median · q1 34 · q3 49 · max 98 | `skills-work/corpus/crypto/statistics.md:124` | 59 |
| sentences | report; target the median | median 8 · q1 6 · q3 10 | `skills-work/corpus/crypto/statistics.md:122` | 59 |
| paragraphs | **at least the corpus floor**, and every paragraph is labelled — gate `abstract-paragraphs` | q1 2 · min 1 · max 9 | `skills-work/corpus/crypto/statistics.md:123` | 59 |

**Build share is computed by hand-coding, not by keyword.** Label every abstract paragraph `context`, `gap`, `build`, or `result`, then divide the words of the `build` paragraphs by the abstract total. The corpus method is recorded at `skills-work/corpus/crypto/statistics.md:141-147`. Do not substitute a keyword classifier: the corpus's own keyword pass reports a share far below the hand-coded pass for the same population (the two values and their disagreement are on `skills-work/corpus/crypto/statistics.md:177-179`, and the gate prints the floor it uses), and the file names the hand-coded table as the authority.

Corpus build-share span for calibration, from `skills-work/corpus/crypto/statistics.md:148-165`: the sample runs from 0.00 to 1.00, and the papers that read as "related work first" are the ones in the low tail. A paper whose contribution is a construction should not sit below the pooled value.

### The contribution list

| quantity | rule (printed by) | corpus distribution (context) | anchor | n |
|---|---|---|---|---|
| bullets | **the corpus's own range** — gate `contributions-block` | median 4 · q1 2 · q3 5 · max 13 | `skills-work/corpus/crypto/statistics.md:196` | 50 |
| block words | **at most the corpus median** — gate `contributions-block` | median · q1 71 · q3 255 · max 858 | `skills-work/corpus/crypto/statistics.md:197` | 50 |
| words per bullet | **at most the corpus median (per item)** — gate `contributions-items` | median · q1 13 · q3 57 | `skills-work/corpus/crypto/statistics.md:198` | 214 |
| longest bullet | **at most the corpus median** — gate `contributions-items` | median · q1 31 · q3 106 · max 486 | `skills-work/corpus/crypto/statistics.md:199` | 50 |
| block / abstract ratio | **at most the corpus median ratio** — gate `contributions-block` | median · q1 0.36 · q3 1.07 · max 4.56 | `skills-work/corpus/crypto/statistics.md:200` | 50 |

A contribution list is a list of **objects**, not of activities: the corpus's median bullet opens by naming the object it introduces (`skills-work/corpus/crypto/craft-notes.md:148-171`). A bullet that narrates what the authors did, in what order, and what they tried first is a process narration and is deleted, not shortened.

### The duplication metric

Use the corpus metric exactly, so the number is comparable across papers:

- tokenise both texts to `[a-z0-9]+`, case-folded;
- form all 6-grams of each;
- count **shared 6-grams** (absolute) and divide by the abstract's 6-gram count (ratio).

Definition and both distributions: `skills-work/corpus/crypto/statistics.md:206-212`, n=50.

| measurement | corpus value | anchor |
|---|---|---|
| shared 6-grams | median 0 · q1 0 · q3 0 · max 6 | `skills-work/corpus/crypto/statistics.md:211` |
| share of papers with at least one shared 6-gram | 0.1 | `skills-work/corpus/crypto/statistics.md:212` |

**Rule: zero shared 6-grams.** At least one shared 6-gram is a finding that requires a disposition. The permitted disposition is narrow: the overlap is a **named object** — a scheme name, a theorem name, a protocol label — being introduced in both places, which the corpus itself does (`skills-work/corpus/crypto/craft-notes.md:172-186`). Re-description of the same result in both units is not a permitted disposition; delete it from one of them and record which.

The security-venue corpus confirms the same norm with an independent metric, so a paper may cite either: bag-of-words Jaccard median 0.201 and trigram Jaccard median 0.019 between the contribution block and the abstract (`skills-work/corpus/security/statistics.md:61-62`, definition at `skills-work/corpus/security/statistics.md:64-67`, n=22).

## Claim preservation

Condensation may delete, merge, rephrase at equal strength, or **downgrade** a claim; it may never
strengthen one. Modality (`proves` / `claims` / `supports`), quantifiers and degree (`all`, `never`,
`first`, `only`), scope limits (`under assumptions`, a named parameter range), and the claim's object
(committing to the message vs committing to the codeword) are preserved across the rewrite unless the
claim ledger already carries the stronger form with its evidence. The gate that judges this is
`Gate-Condense-Claim-Preservation` in `ccs-writing-style/references/compression-and-expansion-gates.md`;
the same rule governs this family's abstract and contribution passes.

## The deletion and migration list

Compression here means **relocation**. Every removed span gets a destination, and the destination is recorded in the return value. The following devices are the ones the corpus actually uses; each is anchored to a real instance.

| device | corpus instance | anchor |
|---|---|---|
| defer the proof, keep the statement inline | `"We defer the proof to~\cref{sec:distinguish-marginals}."` | `skills-work/corpus/crypto/craft-notes.md:389` |
| sketch in the body, full proof in the appendix, and say so | `"We provide here only a sketch of the proof, and we refer the reader to the ... full security proof"` | `skills-work/corpus/crypto/craft-notes.md:390` |
| point at a named paragraph of the overview instead of re-deriving | `"For a first intuitive proof of the correctness and security, we refer to the corresponding paragraph in \cref{subsec:overview}."` | `skills-work/corpus/crypto/craft-notes.md:391` |
| move a section's roadmap into the overview | `"In \Cref{section:overview-qlde}, we overview how list-decoding from erasures can be used to ..."` | `skills-work/corpus/crypto/craft-notes.md:392` |
| let a figure carry the communication pattern | `"This is Message 1b in Figure~\ref{fig:comm-model}."` | `skills-work/corpus/crypto/craft-notes.md:393` |
| one quantitative pair instead of an adjective | `"multiplication depth 193, which outperforms the 680 required"` | `skills-work/corpus/crypto/craft-notes.md:394` |
| name the symbol set once | `\subsection{Notation}` | `skills-work/corpus/crypto/craft-notes.md:395` |

The same devices appear independently in the security corpus, which is why they are not crypto-venue quirks: point the abstract at a section instead of expanding it, carry a flow in a protocol box, abstract a recurring condition into a named object, and replace an adjective with a number (`skills-work/corpus/security/statistics.md:195-202`).

**Destination choices, in order of preference:**

1. **A named body section that already owns the material.** Add a forward pointer; add no new text.
2. **A footnote** — for a qualification that is true but not load-bearing.
3. **A heading-marked evidence record or appendix** — for verification records, review narrative, superseded metrics, and measurement tables. The corpus's own appendix share of body-plus-appendix is a median 0.038 (`skills-work/corpus/crypto/statistics.md:386`, n=62), so an appendix is an ordinary destination, not an admission of failure.
4. **Nowhere.** This is available only for process narration, meta-narration, and re-description that carries no claim, no number, and no status label. Record it explicitly as `deleted: no claim carried`, with the removed text quoted, so a reviewer can disagree with the judgement.

**Never deleted, at any step:** a claim, a theorem statement, a status label (`proven`, `transcribed`, `conditional`, `provisional`, `open`, `empirical-conjectural`), a measured value, or a citation. These are relocated with their wording intact. The governing ruling requires relocation rather than deletion and requires every statement heading to keep its status wording (`research-work/paper/revision/CAPTAIN-DECISIONS.md:103-109`).

## Cut order

Apply the cuts in this order and stop when the thresholds are met. Earlier cuts are cheaper and safer than later ones.

1. **Process narration.** Any sentence reporting the research process rather than the result: attempt counts, stage names, internal ledger labels, "we first tried, then", review or audit history. The corpus contains none of this in the abstract, contributions, or overview of 35 security papers (`skills-work/corpus/security/statistics.md:48`, `skills-work/corpus/security/statistics.md:201`), and the same holds for the crypto corpus's abstract register (`skills-work/corpus/crypto/craft-notes.md:115-129`).
2. **Meta-narration.** "This section will discuss", "Below we present", "As we will see" — except a genuine roadmap sentence in the introduction.
3. **Abstract-to-list duplication.** Apply the 6-gram metric; delete the copy that is further from its natural home.
4. **Adjectives standing where a number belongs.** "significantly faster", "negligible overhead", "much smaller" — replace with the measured value, or delete the comparison.
5. **Re-narration of the same result in a second unit.** One statement per result; the second becomes a forward pointer.

## Pass output

The compression pass returns, and `## Output Contract` requires:

- **Abstract:** the paragraph count against its floor of 2, total words, sentences, per-paragraph move labels with their word counts, build share, longest sentence — before and after, each with the threshold it was compared against. A one-paragraph abstract is returned as `unmatched` on the build share and as a breach of the paragraph floor; it is never returned with a share.
- **Contribution list:** bullets, block words, words per bullet, longest bullet, block/abstract ratio, shared 6-grams (absolute and ratio) — before and after.
- **Migration ledger:** one row per removed span, with the removed text quoted, the destination, and the reason.
- **Residual cap breaches:** any threshold still exceeded, with the corpus line that would license the exception or the explicit statement that none does.

## Worked calibration

The pass must reproduce these verdicts on the frozen calibration manuscript. They are the calibration evidence for this file's rules; the numbers are the contract's measurements, not new ones.

**Measurement basis — declared, because this file and `SKILL.md` require every budget claim to name its tokenization basis, and this table is the one place where the calibration basis differs from the corpus basis.** The absolute counts below are **whitespace tokens (`\S+`)** over the markdown twin `research-work/paper/final-paper.md`, which is the basis of the frozen measurement harness `research-work/paper/revision/d1_manuscript_measures.py`. The corpus thresholds this file enforces are defined on a **different** basis: `skills-work/corpus/crypto/statistics.md:12` defines `words` as whitespace-separated **alphanumeric** tokens. The bases disagree on absolute size, so the counts below are labelled with theirs and must not be read as corpus-basis counts:

| span | whitespace tokens (this table) | alphanumeric tokens (corpus basis) | shipped counter's tokenizer |
|---|---|---|---|
| abstract `research-work/paper/final-paper.md:11-17` | **247** | **295** | **268** |
| §5.5 share of §5 | **0.5659** | **0.6183** | — |

**Every verdict in this table is unchanged under either basis**, which is what makes it usable as calibration evidence (frozen calibration manuscript, `research-work/paper/final-paper.md`, with its share recorded against `corpus/crypto/statistics.md:330-334`, including the outlier line `corpus/crypto/statistics.md:334`). The §5.5 share is the one place where the two bases land in different corpus bands while agreeing on the verdict: 0.5659 sits between the corpus median 0.491 and the third quartile 0.607, while 0.6183 passes 0.607 — but both are above the 0.50 majority ceiling, so both break it, and neither reaches the 0.65 outlier line.

| region | measured (whitespace tokens) | threshold | verdict |
|---|---|---|---|
| abstract `research-work/paper/final-paper.md:11-17` | 247 words (295 on the corpus basis) | at most 210 (`corpus/crypto/statistics.md:121`, n=59) | **breach** — the near-miss case: a 250-word cap would have passed it, and it still breaches on either basis |
| abstract build share, same span | **0.3401** = build-paragraph words / abstract-total words, both whitespace tokens (0.3194 only if a keywords-inclusive denominator is used) | at least 0.56 (`corpus/crypto/statistics.md:165`, n=15) | **breach** — allocation defect, the one a length cap cannot see; the denominator is stated because the value moves with it |
| contribution list `research-work/paper/final-paper.md:29-44` | 902 words | at most 146 (`corpus/crypto/statistics.md:197`, n=50) | **breach** |
| block / abstract ratio, same pair | 3.65 | at most 0.81 (`corpus/crypto/statistics.md:200`, n=50) | **breach** |
| shared 6-grams, abstract vs list | 30 | 0 | **breach** — corpus maximum is 6 |

A pass that reports "abstract OK" for these regions, or that reports the 902-word list as acceptable, has not run. A pass that prints any of these absolute counts without the basis they were measured on has also not run.

## The paragraph floor — a one-paragraph abstract is not measurable

The abstract table above states a floor of **at least 2 paragraphs**. This section is the reason, and the mechanical form of the rule. It is placed at the end so that the line numbers of every table above stay stable for the citations that point at them.

**Why a floor and not a count to report.** The four-move annotation and the build share are *per-paragraph* measurements. With one paragraph there is one move, so the share can only be `0.0` or `1.0` **by construction**: the number is not evidence about allocation, it is an artefact of the paragraph count. A criterion that asks for per-paragraph move labels therefore cannot be falsified on a single-block abstract, and a pass that prints a share for one is answering a different question than the one asked.

**The corpus says this is a minority structure, not a style preference.** The abstract-paragraph row reads `min 1`, first quartile `2`, median `2`, third quartile `3`, max `9` (`skills-work/corpus/crypto/statistics.md:123`, n=59), and **0.78** of tier-A abstracts carry more than one paragraph (`skills-work/corpus/crypto/statistics.md:128`, n=59). So a single-block abstract sits at or below the corpus's lower structure, and it is *also* the structure that makes a mandatory criterion unmeasurable. Both halves of that evidence are inlined here rather than cited by implication, because a threshold without its sample size is not a threshold.

**The rule, mechanically:**

1. count the abstract region's non-blank blocks. **A count below 2 is a breach of this rule**, is reported as a breach, and is not smoothed over with a share;
2. when the count is below 2, **no build share is reported at all** — not by the classifier and not from a supplied hand-coded value, because a hand-coded share over one block is still a single move. The gate returns `unmatched` for the share and states that any supplied value was withheld and why;
3. an abstract region with **no** non-blank block is `unmatched` on the paragraph count itself, never `0 paragraphs -> breach`, so a region-slice error cannot be mistaken for a paragraph-count defect;
4. the paragraph count is a count of **blocks**, not of words, and every other number in the same report stays on the run's declared tokenizer basis.

**What this rules out.** A reviewer, or an instrument, that prints a build share for a one-paragraph abstract has measured the wrong object; a pass that reports the paragraph count without saying whether it clears the floor has not applied the rule either. Neither is permitted to reach "abstract OK".

