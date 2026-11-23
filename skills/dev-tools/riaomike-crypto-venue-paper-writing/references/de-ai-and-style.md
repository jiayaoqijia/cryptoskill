# De-AI, Process-Register Naming, and Sentence-Level Style Rules

Derived from revision feedback on real manuscripts: reviewers increasingly reject prose that reads as AI-generated, and a paper that leaks its own production process reads as unreviewed. Treat this as an executable checklist, not a flavor guide. The rule groups below are referenced from the main `SKILL.md` workflow's de-identification and de-naming pass.

Two rule groups carry corpus evidence and are stated with it: the **process-register anti-pattern list** (§Process-register anti-patterns), which exists to stop this skill from teaching the very pattern a manuscript revision had to remove, and the **de-naming scan**. The vocabulary and structure groups are register guidance and are graded by the grep checklist at the end.

## Vocabulary red flags

Replace or delete; do not merely reduce frequency when the word itself signals the register:

- Sentence-openers used as filler: "Additionally, ...", "Moreover, ...", "Furthermore, ..." (at most a couple per paper, and only with real content), "In order to ..." (always "To ...").
- Emphatic adjectives with no measured referent: crucial, pivotal, paramount, comprehensive, groundbreaking, cutting-edge, remarkable, substantial (without a number), significant (without a number).
- Abstract nouns and metaphors: landscape, tapestry, testament, vibrant, intricate, interplay, realm, delve, foster, showcase, underscore, leverage (commercial register), synergy, holistic.
- Vague attribution: "Studies have shown ...", "It is widely believed ...", "As is well known ..." — replace with a citation or delete.
- Self-evaluative novelty: "novel", "first", "optimal" used as self-praise — keep only when scoped and defensible ("the first X with property P under assumption A"), never bare "novel technique".
- Hedging stacks: "may", "might", "could potentially" — quantify or condition ("if premise A holds"), do not stack.

## Structure red flags

- Forced parallelisms: "Not only X, but also Y" used repeatedly; rule-of-three lists everywhere; binary contrasts ("It is not about X — it is about Y").
- Meta-narrative: "This section will discuss ...", "Below we present ...", "As we will see ..." — state the content, not the plan (a roadmap sentence in the introduction is the exception, and a roadmap constituent in the overview is required by `expansion-rules.md`).
- Synonym cycling for one object (scheme/protocol/system/construction used interchangeably for the same thing): pick one term per object and stay consistent.
- Uniform paragraph lengths and uniform sentence lengths: vary them; break long parenthetical insertions out of the subject-verb path.

## Content red flags

- Significance inflation without evidence; promotional language in evaluation sections ("remarkable improvement"); generic conclusions ("this opens exciting new directions") — be specific about what opens and why.
- Every strong claim should carry its scope: "resists the adaptive attacker of the security section at C% overhead", not "is secure".
- Failure cases appear in the same paragraph as success rates; negative results are not hidden in footnotes.
- "No attack found" must not be written as "secure": pair it with "this is not a proof of security" once, and once only, in each relevant section.

## Sentence-level register

- Stress position: put the most important information (numbers, bounds) at the end of the sentence. "The prover achieves the optimal running time O(C)" rather than "The prover time is O(C), which is optimal".
- Topic position: start from what the reader already knows, then attach the new claim; do not bury the subject under long clauses.
- Voice: active for your contributions ("We present ...", "We prove the theorem under the stated assumptions"), passive or attributed for prior work ("It was shown in [ref] that ..."), past tense for experiments run, present tense for protocol and system properties.
- "We" refers to the authors' actions, not the protocol's behaviour ("the prover sends" rather than "we send").
- Numbers beat adverbs: replace "significantly", "negligible", "trivially" with the measured value or bound wherever one exists. In the abstract this is bounded by the sparse-number norm: median 1 numeric token (`skills-work/corpus/crypto/statistics.md:125`).

## Process-register anti-patterns

**This section is one of the marked places in this skill where a process-register pattern may appear, and every pattern named here is forbidden in a manuscript.** The others are enumerated in the self-scan bullet of §Stage 4; each must be able to write a literal down in order to be usable, and the self-scan excludes exactly those blocks and nothing else. Each entry states the class, why it is forbidden, and what to write instead. The classes are written as character classes rather than as literal tokens on purpose, so that the de-naming scan below returns zero hits against this skill's own text: a skill that quoted a real identifier would teach it.

The evidence that this matters is that such identifiers do reach manuscripts. The corpus's own LaTeX sources contain working-note registers, and the corpus scan finds them in a third of its tier-A papers while their published PDFs contain none (`skills-work/corpus/crypto/statistics.md:423-435`). The detection classes the corpus uses are a placeholder class and a process-naming class (internal identifiers, working-note blocks), run by the corpus's scan tool and recorded at `skills-work/corpus/crypto/craft-notes.md:561-566`. The corpus's own reading is decisive: the rule is "remove every marker before submission", **not** "never write it down" (`skills-work/corpus/crypto/statistics.md:432-435`).

| # | forbidden class (as a character class, not a pattern to copy) | why it is forbidden | write instead |
|---|---|---|---|
| 1 | a capital letter followed by optional hyphen and a digit, used as a **construct label** (`[A-Z]-?[0-9]`) | it names a construct after the work plan's item, not after its content; a reader cannot resolve it without a file outside the paper | a descriptive name for the object, and a normal LaTeX environment or `\paragraph{}` heading |
| 2 | a capital-letter-and-digit group with a hyphenated sub-label (`[A-Z][0-9]-[A-Z][0-9]`) | doubles the sin: two plan coordinates in one name | one descriptive name; if two objects are distinct, say how they differ |
| 3 | a prime- or suffix-marked round or stage label (`[A-Z]'*-[A-Z]+` or `[A-Z]+/[A-Z]+`) | it encodes the revision history of the idea, which is not part of the result | name the variant by what it changes, not by when it appeared |
| 4 | a bibliography-key-like token of the form `ref` plus two digits (`ref[0-9][0-9]`) | a hand-rolled citation key is not a citation; the bibliography generates keys | a real `\cite{}`, or remove the reference |
| 5 | a process-comment token of the form `frag` or `t` plus a digit (`frag[0-9]`, `\(t[0-9]+\)`) | it marks which fragment or task produced the sentence | delete the comment; the sentence must stand without it |
| 6 | row, sample, or configuration labels used as if they were paper constructs (`[A-Z][0-9]+` in prose) | a table's internal row labels are not objects a reader can cite across sections | name the configuration by its parameters, and let the table caption carry the labels |
| 7 | unresolved working-note macros and conditional-false blocks in the source | they are the author's own scratch space; the corpus finds them in the sources of accepted papers and never in the published PDFs | remove every marker before submission; the full inventory and counts are at `skills-work/corpus/crypto/statistics.md:426-431` |

**An anti-pattern entry is only valid if a forbidding sentence surrounds it.** A list entry with no prohibition — an example that models the identifier positively, or a heading with no rule — re-induces the defect it documents. The de-naming scan below checks exactly this: a match that is not inside this table's forbidding context is a finding.

**Zero is the corpus norm in the paper itself.** Across 35 security-venue papers, **none** narrate the research process in the abstract, the contributions, or the overview (`skills-work/corpus/security/statistics.md:48`), and the corpus lists "delete the research process" with zero counterexamples (`skills-work/corpus/security/statistics.md:201`). The same holds in the crypto corpus's abstract register, where numbers and process markers appear as outcomes only (`skills-work/corpus/crypto/craft-notes.md:115-129`).

## The de-naming scan

**A pattern hit is not a violation.** The classes above are deliberately over-broad, because they must catch a label that was named after a work-plan item without knowing in advance what that label will look like. The price of that breadth is that the same pattern also matches mathematics, LaTeX options, and substrings of ordinary words. So the scan collects **candidates** and then **adjudicates every one of them against the manuscript**, writing the verdict down. A scan that reports a raw class count as its result is a false-positive generator, and it must not be used as a gate.

Measured on the frozen calibration manuscript, the over-breadth is not marginal: class 1 matches **23** times in the markdown twin and **28** in the tex twin, class 3 matches **9** and **10**, class 6 matches **20** and **25**. Adjudicated, exactly **two of each twin are real leaks**. The counts are kept in this file only as a diagnostic of the instrument's breadth — never as a verdict.

### Stage 1 — collect candidates

Scan the manuscript source and its markdown twin for the classes above, plus the working-note macro classes. Record `file:line`, the matched text, the class, and a fixed character window of context (the window size is the scanner's own constant, printed by the tool). Record the per-class counts **for diagnostics only**.

### Stage 2 — the definition test (mandatory, per candidate)

Ask one question of every candidate: **can the reader resolve this token from the paper alone?** A candidate is **legitimate** if and only if it satisfies (a), (b), or (c).

| | legitimate when | the verdict carries |
|---|---|---|
| **(a) the manuscript defines it** | at or near first use: a label definition, a table or figure caption that carries it, or a numbered object the paper itself introduces. In practice this is the label column of a table row, in either syntax — markdown `\| Label \| … \|` or LaTeX `Label & … \\`. | the **definition anchor** as `file:line` |
| **(b) it is a domain-standard primitive, variant, or inherited notation** | resolvable by a reader of the field without consulting this paper's working records — `ROM/XOF` (random-oracle model; extendable output function), `A/B` (the variants this paper introduces), `P/Q` (the cited host's public equation) | the category and the reason |
| **(c) it sits inside a LaTeX package option, command argument, or math environment** | `\usepackage[T1]{fontenc}`, a bibliography key, or `$R-1$`. These are typesetting and notation contexts, not manuscript tokens. Detect a math span by **dollar-delimiter parity**, not by "sits between two `$`" — on a math-dense line the latter wrongly reports prose that merely sits next to two spans. | the context |

A candidate that satisfies none of the three is **an identifier the reader cannot resolve**, and its verdict is **`violation`** carrying `no definition found`.

**One further outcome, which is not a verdict about a token.** If the match is *not a token at all* — a substring of a longer alphanumeric word, or a fragment of a longer identifier — record `not-a-token` with the enclosing word. Nothing is being silenced: there is no token to resolve.

### Stage 3 — verdicts, and what each one costs

| verdict | meaning | required output |
|---|---|---|
| `violation` | an identifier the reader cannot resolve | `file:line`, matched text, class, `no definition found`, and the replacement written |
| `legitimate(a)` | defined by the manuscript | `file:line`, matched text, class, and the **definition anchor** `file:line` |
| `legitimate(b)` | domain-standard primitive / variant / inherited notation | `file:line`, matched text, the category, and the reason |
| `legitimate(c)` | inside a LaTeX package option, command, or math span | `file:line`, matched text, and which of the three contexts |
| `not-a-token` | the match is a substring or fragment | `file:line`, matched text, and the enclosing word |

### Class 6 has two owners, and the output must say which one fired

Row, sample, and configuration labels sit on a boundary, and reporting them without distinguishing the cases is itself a defect. **A label the manuscript defines is not process-register naming — it raises no `D-C1` finding.** What it can raise is a different thing:

- **`D-C1` finding (process-register naming)** — only for a label the manuscript does *not* define and a reader cannot resolve. Verdict `violation`, `no definition found`. This is the only case that is a naming leak.
- **class-6 style finding** — for a manuscript-defined label **cited outside its own table or caption**, e.g. prose that calls a configuration by its table-row label. This is a *style* finding, not a leak: the label is legitimate and its anchor proves it, but the fix is the one in the class-6 row above — name the configuration by its parameters and let the table caption carry the label. The verdict is `legitimate(a)` **plus** the style flag.
- **no finding** — a defined label used only inside its own table or caption. On the calibration manuscript `H1`–`H3` are in this category, while `F1`, `F3` and `F5` are additionally cited in prose and therefore also carry the style flag.

Every output line must state which of the three it is reporting. Collapsing them is how a style nit gets filed as a naming leak.

### This is not a waiver

The definition test is the **category's own criterion**, not an exemption bolted onto it, and the difference is not cosmetic:

- A **waiver** silences a token that has already failed the test. That remains forbidden: **no waiver is available for an undefined class 1–6 token**, and the earlier prohibition is unchanged.
- The **definition test** decides what the class *is*. A table-row label the paper defines was never a process-register leak. Calling it one and then waiving it would report a defect that does not exist — which is exactly how this rule came to produce a non-zero, largely false-positive count on a clean manuscript.

So the pass condition changed below; the obligation did not. An undefined identifier is still a violation, with no waiver route.

### Stage 4 — output contract

- **Every** candidate receives exactly one verdict from stage 3, with that verdict's required fields. An unadjudicated hit is itself a failure.
- **Pass condition: no unadjudicated hits, and zero unresolvable identifiers.** The raw per-class counts are printed as diagnostics and **must not be presented as the verdict** — a non-zero raw count on a clean manuscript says nothing about the manuscript and everything about the pattern.
- **Waivers must be a named category plus a reason**, drawn from this closed list: (i) manuscript-defined label, (ii) domain-standard primitive / variant / inherited notation, (iii) LaTeX package option, command argument, or math span, (iv) a legitimate venue name, (v) a bibliography-generated citation key, (vi) a term inside a quoted title. An ad-hoc waiver — "looks fine", "probably a label" — is not a waiver and must be recorded as a violation instead.
- **This skill's own files are scanned with the same pattern, and there the requirement is zero hits that are not accounted for**, because a skill that quoted a real identifier would teach it. The adjudication stage is pointed at the skill too, and it must return nothing. A hit is accounted for when any of these holds:

  1. **it is a substring artefact** — the same rule as stage 2 above;
  2. **it lies in one of the five blocks that must name literals to be usable** — the anti-pattern table (§Process-register anti-patterns), the definition test's example row in §Stage 2, the class-6 discussion, the worked adjudication, and the reproducible command in §Reproducible form;
  3. **it is legitimate under a named category** — in practice a **venue name**, which is why class 3 (`[A-Z]+/[A-Z]+`) fires on this skill's own `CRYPTO/LNCS` and `CRYPTO/EUROCRYPT`. That is the self-scan's version of the manuscript's own `CRYPTO/LNCS` hit, and it is adjudicated the same way, by category rather than by convenience.

  Anything else is a finding: the skill is teaching a pattern it forbids.

  **The self-scan must apply the same `not-a-token` rule as the manuscript scan, and this is not a formality: the pattern fires on this skill's own vocabulary.** Class 1 matches inside the contract's defect id `D-C1` and inside `D12`, which are exactly the identifiers this file exists to discuss. A self-scan that ignored that would demand that this file stop naming the defects it is about. So a match is excluded as a substring when the character before it is alphanumeric, or when it is preceded by `-` or `_` that is itself preceded by an alphanumeric, or when the character after it is a digit.

  Runnable self-scan. **Its residual is not zero on the shipped skill, and this file does not claim it is.** The command exits 2 with a non-zero residual, and at the revision this file was written against **every hit in it is a token the skill is *citing* rather than teaching**: census row ids from the R-3-exception list, the contract's rule ids, and the ids of the measurement rows in the structural comparison. None of them is an unadjudicated *identifier*, which is the thing the accounting rule above actually forbids, and each is dispositioned by category in the paragraph above — it is cited vocabulary, not adopted vocabulary. **The honest reading of this command is therefore: no hit may be an unadjudicated identifier, and every hit the residual does print must be dispositioned one by one.** Do not read the residual as a defect count, and do not quote a residual you have not just run: it moves with the number of rows the prose cites, so this file states the property rather than a number.

  ```bash
  cd skills-work/crypto-research-agent-skills
  python3 skills/crypto-venue-paper-writing/scripts/count_venue_gates.py --self-scan
  ```

### Reproducible form

The command below performs stage 1 and the mechanical part of stage 2 (label-column anchors in both markdown and LaTeX syntax, package options, math spans by delimiter parity, substrings) and prints the tally. Verdicts that need a judgement about the manuscript — category (b), and category (a) for objects that are not table rows — live in the `NAMED` table inside the command, so every adjudication is written down in one auditable place rather than applied silently.

```bash
cd skills-work/crypto-research-agent-skills
python3 skills/crypto-venue-paper-writing/scripts/count_venue_gates.py \
    --dename ../../research-work/paper/final-paper.md \
             ../../research-work/paper/latex/main.tex
```

### Worked adjudication on the frozen calibration manuscript

Every class-1/3/6 candidate on both twins, with its verdict. This table is the calibration evidence for stage 2; the verdicts are the ones the command above produces.

| raw class | hits (md / tex) | verdict group | tokens | representative anchors |
|---|---|---|---|---|
| 1 | 23 / 28 | `legitimate(a)` — manuscript-defined labels | `F1`–`F5` (field rows), `H1`–`H3` (host rows), `A/B` (the variants) | field-row table `research-work/paper/final-paper.md:417`; host-row table `:405`; variants `:160` |
| 1 | | `legitimate(c)` — math spans | `R-1`, `M-1` | `research-work/paper/final-paper.md:740`, `:576` |
| 1 | | `legitimate(c)` — **package option** | `T1` inside `\usepackage[T1]{fontenc}` | `research-work/paper/latex/main.tex:12` |
| 1 | | `not-a-token` — substring | `E2` inside `SHAKE256`; `D1` inside `D12` | `research-work/paper/final-paper.md:156`, `:696` |
| 3 | 9 / 10 | `legitimate(b)` — domain primitives / inherited notation | `ROM/XOF`, `P/Q` | `research-work/paper/final-paper.md:56`, `:143` |
| 3 | | `legitimate(venue)` | `CRYPTO/LNCS` | `research-work/paper/latex/main.tex:3` |
| 6 | 20 / 25 | `legitimate(a)` + **class-6 style flag** — defined labels cited in prose | `F1`, `F3`, `F5` outside their own table | `research-work/paper/final-paper.md:266`, `:425`, `:568`, `:570` |
| 6 | | **`violation` + `no definition found`** | `D12`, `D19` — internal decision identifiers in a comment | `research-work/paper/final-paper.md:696`; `research-work/paper/latex/main.tex:973` |

Calibration outcome on the frozen manuscript: **2 violations per twin** (the `D12`/`D19` decision identifiers, a genuine leak that must be removed), **103 legitimate**, **8 not-a-token**. `\usepackage[T1]{fontenc}` is **not** reported as class 1 — it is adjudicated `legitimate(c)` with the LaTeX-option reason.

Two consequences a pass must reproduce, because they are where the old rule went wrong:

1. **The old rule failed a clean manuscript.** Under the previous zero-hit pass condition all 23 md class-1 candidates were findings, including a font encoding and two mathematical expressions. An instrument with a near-total false-positive rate on its calibration instance cannot be a gate, and the fix is the adjudication stage — not a narrower class, which would have missed the real leak in `D12`/`D19`.
2. **The real leak survived the fix.** Narrowing the classes would have silenced `A/B` and `P/Q` *and* `D12`/`D19` alike. The definition test clears the false positives while keeping the two unresolvable internal identifiers as violations — the property to re-check whenever this rule is next revised.

## Executable grep checklist

Run these patterns after revision; each hit is either fixed or explicitly waived with a reason in the diff:

```text
^(Additionally|Moreover|Furthermore|In addition|However|Notably|Importantly)[, ]
delve|pivotal|showcase|underscore|tapestry|testament|landscape|vibrant|intricate|interplay|realm|foster|groundbreaking|cutting-edge
Not only .* but also
It (is|was) (important|worth|interesting|crucial) to (note|mention|stress)
In order to|aims to|aspires to|strives to
This (section|chapter|paper) (will|aims to|intends to)
dramatically|remarkably                   # unless a number follows in the same sentence
```

The process-register classes are deliberately **not** in this block, because a checklist that contains a live identifier cannot be run against itself; they are run by the de-naming scan above, which uses the character classes from the table.

## Section-specific attention

| Section | Primary risk |
|---|---|
| Abstract | all patterns; highest scrutiny, and the allocation rule in `compression-rules.md` |
| Introduction | significance inflation, vague attribution, meta-narrative |
| Technical overview | filler phrases, formula dumping, falling below the floors in `expansion-rules.md` |
| Construction | missing constituents, and measured values leaking in (see `numeric-placement.md`) |
| Security analysis | hedging, sketch-as-proof wording, ledger material left in the body (see `section-budget.md`) |
| Evaluation | promotional language, missing failure cases |
| Conclusion | generic positive statements, abstract repetition |
