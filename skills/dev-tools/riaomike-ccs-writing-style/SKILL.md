---
name: ccs-writing-style
description: Use when revising an ACM CCS paper for a precise threat model, calibrated attack/defense claims, the CCS page budget, double-blind wording, adaptive-evaluation honesty, abstract and contribution-list condensation, technical-overview and scheme-section expansion, and the security house style expected by an adversarial SIGSAC program committee; also covers IEEE S&P and NDSS submissions, which share the same security-venue register and corpus-calibrated rules and have no dedicated skill of their own.
---

# CCS Writing Style

A CCS paper must let an adversarial reviewer locate every claim against a named adversary and checked evidence. Adapted from the CCS writing-style guidance in the Awesome-Journal-Skills collection (MIT).

## Evidence base for the numeric gates

Every number in the condensation gates and the expansion gates below is measured, not chosen. Two corpora back them:

- Security four-venue corpus: 35 papers (IEEE S&P 4 / ACM CCS 5 / USENIX Security 18 / NDSS 8), full texts on disk, 25 read in full. Quantified tables Q1–Q9 with sample sizes, extraction basis, and re-computation commands: `skills-work/corpus/security/statistics.md`.
- Cryptography three-venue corpus: 62 tier-A papers plus 135 full LaTeX sources. `skills-work/corpus/crypto/statistics.md`, whose `§Bases` section defines every unit used here.
- Evidence-apparatus census: **35 anchored rows** over both corpora — the float, cross-reference, label, citation-key and formal-content rows this skill's last three gates use. `skills-work/audit/evidence-structure-census.md`, whose §Appendix F table is the artefact: rows `A1`–`A20` (crypto), `B1`–`B6` (security four venues) and `G-E1`–`G-E9` (the registered gaps). Its §Bases defines the units and its §Appendix E states what it does not license.

**Provenance of the citations in this skill.** Every `file:line` citation below is a provenance annotation rather than a link: it points at the corpus snapshot inside the authoring workspace (`skills-work/`), and it is not expected to resolve beside an installed copy. The snapshots are the security four-venue corpus, the cryptography tier-A corpus, and the evidence-apparatus census built over both.

Rule this skill follows: a threshold is quoted with its source file, its line, its sample size `n`, and its unit — and the criterion that states a rule says which instrument row carries its value, so this file states the rule and its anchor and points at the row. Where a value is written here at all, it is written beside its anchor, so a reader can check it against the corpus rather than trust a copy: **the bounds that are written in this file are the counts and caps of the condensation and expansion gates, plus the two presence floors of the evidence-apparatus gates (one caption block on the figure-plus-table total; one citation key in the related-work region)**, and **what the instrument prints is the draft's own measured counts — not the bounds**. Each bound is read from the anchor line its own registry row names, which is why the counting step of `## Workflow` re-reports the measured numbers and compares them against those anchors, rather than reading a bound out of the instrument's output. Where the two corpora disagree, the corpus governs and the manuscript in front of you is not a constant. Where neither corpus measures the quantity, the rule is written qualitatively with no number — an invented number is a defect, not a default. The quotas a gate prints are its calibration, not its rule: the rule is the same for S&P and NDSS as for CCS, and it is the row the anchor names that decides which corpus calibrates it.

**Running the instrument: state the root, or the command does not run.** The shipped instrument resolves from the skill-suite root `skills-work/crypto-research-agent-skills`, which is the normative working directory for every command below, so each is written with the `skills/` prefix that makes it resolve there; `skills-work/tools/rule-trace-check.py` is by contrast a **workspace** instrument, cited below only where the text says so, and it does not resolve beside an installed copy.

```bash
# abstract-contributions prints abstract.words/.sentences/.mean_sentence_words,
#   contributions.items/.words_per_item_max/.items_over_72_words/.items_over_150_words, and
#   duplication.abstract_vs_contributions_{word,trigram}_jaccard
python3 skills/ccs-writing-style/scripts/count_prose_gates.py abstract-contributions PAPER.md
# evidence prints binding_thresholds, floats.{floor,floor_basis,scope,figure_outlier_note,breach,breach_reason}, cross_references, citations, appendix, math, exit_contract
python3 skills/ccs-writing-style/scripts/count_prose_gates.py evidence PAPER.md --related-work-heading "Related Work"
python3 skills/ccs-writing-style/scripts/count_prose_gates.py --self-test   # proves both directions of every gate
```

The quartiles and samples behind a bound are in `references/compression-and-expansion-gates.md` and `skills-work/corpus/security/statistics.md`.

Each corpus row a boundary is read from, with the quantity it measures and its sample size. As elsewhere in this file, `corpus/security/statistics.md` is `skills-work/corpus/security/statistics.md`, `corpus/crypto/statistics.md` is `skills-work/corpus/crypto/statistics.md`, and the census is `skills-work/audit/evidence-structure-census.md`.

| Quantity | Anchor |
|---|---|
| Abstract words / sentences / mean sentence length | `corpus/security/statistics.md:31`, `:32`, `:33` (n=35) |
| Venue split of abstract length; four-venue medians — both a null finding, so no per-venue cap | `corpus/security/statistics.md:50`, `:213` (n=35) |
| Contribution items; words per item; items carrying a number | `corpus/security/statistics.md:58`, `:59`, `:60` (n=22) |
| Contributions ↔ abstract, word-bag and trigram Jaccard | `corpus/security/statistics.md:61`, `:62` (n=22) |
| Why two overlap indices: word-bag catches a rewritten abstract, trigrams catch reused sentences | `corpus/security/statistics.md:67` (n=22) |
| Abstract process narration | `corpus/security/statistics.md:48` (n=35) |
| Technical overview presence; overview size; CCS-only overview size | `corpus/security/statistics.md:85` (n=35), `:92` (n=20), `:219` (n=5) |
| Overview internal components | `corpus/security/statistics.md:104` |
| Scheme/construction section size; its required constituents | `corpus/security/statistics.md:119` (n=35, and n=5 CCS-only), `:131` (n=25) |
| Threat/security-model section size when standalone; CCS-only standalone share | `corpus/security/statistics.md:157` (n=16), `:152` (n=5) |
| Standalone overview / threat-model section share, four venues | `corpus/security/statistics.md:216`, `:217` (n=35) |
| Body page limits, official CFP — policy, per cycle | `corpus/security/statistics.md:220` |
| Construction/analysis floor of a thin design; design word share of body | `corpus/crypto/statistics.md:285` (n=10, direct basis), `corpus/security/statistics.md:121` (n=32) |
| Overview size, crypto venues — a comparison, not a CCS target | `C:239` (n=18) |
| Largest child subsection's share of its parent | `C:330` (n=561) |
| Figure caption blocks; table caption blocks (no floor: the venue habits differ); lettered appendix (reachability is judged, never presence) | `E:` rows B1, B2, B4 (n=35) |
| Cross-references and labels, cryptography tier-A — whole-paper, non-binding here | `E:` rows A10, A11 (n=62) |
| Inline-math density, cryptography tier-A — whole-paper; another family's population, reported for a security-venue draft and never a security-venue floor | `E:` row A1 (n=62) |

## Scope

In scope: threat-model-first structure and wording; first-page security contribution framing; claim-to-evidence pairing (proof, measurement, exploit, or cost); abstract and contribution-list condensation to the measured bounds above; technical-overview and scheme-section expansion against the constituent checklists; page-budget compression for the current limit of the venue in hand (CCS, IEEE S&P, or NDSS); double-blind anonymization of self-citations, tool names, acknowledgments, and artifacts; adaptive-evaluation honesty for defenses; sentence-level rewrites that remove overclaiming, marketing adjectives, and research-process narration; concrete-value placement; and an output diagnosis format for revision.

Out of scope: inventing attacks, defenses, measurements, or citations; deciding novelty or authorship; guaranteeing acceptance; or submitting without human authorization. Writing-style rules for the cryptography venues (CRYPTO, EUROCRYPT, ASIACRYPT, LNCS) are owned by the `crypto-venue-paper-writing` skill; this skill owns the security-venue (CCS, USENIX Security, NDSS, IEEE S&P) form of them. Where the two would state the same rule, this skill states it once and points there.

### Venue mapping — what is shared across the four security venues, and what is CCS-only

This skill triggers for **ACM CCS, IEEE S&P, and NDSS**. The `usenixsec-writing-style` skill owns the USENIX Security form, including the two sections that venue mandates. IEEE S&P and NDSS have no dedicated skill, so this one carries their shared form — and that makes the split below load-bearing rather than cosmetic: a triggered S&P or NDSS run must not silently inherit a rule that was calibrated for CCS.

| Applies to every security venue this skill covers | CCS-only |
|---|---|
| The counted condensation gates (abstract, contribution list, contributions-versus-threat-model duplication, deletion list) | The CCS body-page limit excluding bibliography, appendices, and supplementary material |
| The counted expansion gates (overview components, design constituents, design-versus-analysis ratio, value placement) | The IRB / responsible-disclosure compliance statement obligation |
| The evidence-apparatus gates (float floor, cross-reference integrity, citation density) — floors calibrated on the security four-venue corpus, never on the cryptography family | The standalone-section default, which follows CCS's own standalone-section share (`corpus/security/statistics.md:217`); the S&P and NDSS shares are lower and higher respectively, so for those venues the placement is the author's call under the same precision requirement |
| Threat-model precision: explicit and locatable, capability list in prose, one statement of the adversary (four-venue standalone shares, `corpus/security/statistics.md:217`) | The CCS page-budget snapshot procedure; S&P and NDSS have their own limits, so read their own current call |
| Adaptive-attack honesty, caption discipline, de-identification, the deletion lists, and the register | A table-caption floor, which no corpus supports across the four venues: the NDSS table habit and the CCS one diverge (census B2), so tables are reported and never floored |

The page budget and the ethics/disclosure obligation for each venue are read from that venue's own official call — archived per venue under `skills-work/corpus/security/raw/` (digest at `corpus/security/statistics.md:220`). Never carry one venue's number to another, and never measure an ePrint author version against any of them (`corpus/security/statistics.md:21`).

## Required Inputs

- current official call for papers and template of the venue in hand — CCS, IEEE S&P, or NDSS here; page limit, anonymity, ethics, AI-disclosure, artifact policy;
- manuscript draft or section under revision;
- stated threat model, or the raw security claims to be given one;
- evaluation data or attack demonstrations that claims must be calibrated against.

## Success Criteria

- The security contribution is on the first page: problem, attacker, gap, mechanism, evidence.
- The abstract passes every condensation gate: at most **220 words**, at most **9 sentences**, mean sentence length at most the corpus median **24.1 words**, one paragraph that names the built artifact or mechanism, no research-process narration, no marketing adjective from the checklist, and no contribution sentence reused verbatim.
- The contributions list passes its own gates: the **per-item cap** and the **absolute item ceiling** are corpus values, read from the anchors on this line — the per-item cap is the security-family value (security four venues, **n=22**, `skills-work/corpus/security/statistics.md:59`) and the item ceiling is the same row's maximum, with the corpus median as the target. **The instrument prints neither bound:** what it prints is the draft's own `contributions.items`, `words_per_item`, `words_per_item_max`, and the counters `items_over_72_words` / `items_over_150_words`, which are *word*-threshold counters and are **not** the item ceiling; compare the printed counts against the caps taken from the anchors. The list total is at most **250 words**, word-bag Jaccard against the abstract is at most **0.20** and trigram Jaccard at most **0.019** (`duplication.abstract_vs_contributions_word_jaccard` / `..._trigram_jaccard` — these two the instrument does print, as the draft's measured values), and no duplicated span is left with the disposition unstated. The cryptography family publishes a different per-item cap — **29.5 words per bullet**, median over 214 bullets (`skills-work/corpus/crypto/statistics.md:198`) — derived from a different corpus (CRYPTO/EUROCRYPT/ASIACRYPT and TCC bullets, not security-venue contribution items) and it **does not govern a security-venue draft**. The two caps are about 2.4× apart because the two populations are different: a security contribution item is a paragraph-length claim with its evidence, a cryptography bullet is a one-line result statement. Neither skill may apply the other family's cap; the value follows the venue family of the paper in hand.
- The contributions list and the threat model are not the same text: their word-bag Jaccard is at most 0.20 — **no corpus row measures this pair**, so the number is the sibling bound carried over from the contributions-vs-abstract row rather than a second measurement (`references/compression-and-expansion-gates.md` §Contributions, which carries the caveat in full) — and conversely every security goal the paper promises appears in the threat model as a statement of what the adversary may do.
- The technical overview is a named subsection at or above the corpus minimum for a standalone overview (the instrument's `section-mass` report carries the words; the anchor is `corpus/security/statistics.md:92`, n=20) and carries all five required components; the scheme section carries at least **five** required components and is not thinner than **0.44** of the analysis section by word count.
- The threat model is explicit and early, names attacker capabilities, knowledge, position, and goal once in prose, and every attack/defense step stays inside those capabilities.
- The body follows the venue's section order (`references/section-order.md`): the threat model is locatable, there is no Roadmap subsection, no standalone numbered Open Problems section, the central result is named Theorem/Proposition, and assumptions are cited by environment rather than by work-plan label.
- Every security claim is paired with proof, measurement, exploit demonstration, or a cost number; nothing reads as marketing.
- The draft carries evidence apparatus, not prose alone: at least one figure or table caption block (the instrument's `floats.floor`, licensed by census B1/B2), every LaTeX reference target declared by a `\label` in the same file, and at least one citation key in the section that places the work against prior art (census A10/A11/A12). The float counts are reported against the census quartiles the instrument prints beside them, and a zero figure count is stated as an outlier rather than failed, because the corpus holds such papers.
- The formal-content question is a **manual self-check item, not a gate**: a draft whose design and analysis sections carry no formula at all gets a recorded reason, and the instrument prints the count plus the cryptography-corpus reference distribution without emitting a verdict (see the boundary note in `references/compression-and-expansion-gates.md`).
- Concrete measured values appear only in the sections allowed to carry them; theory and construction text carries symbolic or asymptotic expressions.
- Claims survive an adversarial pass: no overstated exploitability, no "practical" claims beyond the tested environment and versions, adaptive defenses state the attacker they were tested against.
- Double-blind wording holds in self-citations, tool names, acknowledgments, and artifact descriptions.
- The body fits the current page budget of the venue in hand, read from that venue's own call and recorded as a dated snapshot, with the core argument readable without the appendix.
- No AI-flavor prose remains (see the `crypto-venue-paper-writing` skill's de-AI checklist for the grep-level rules).

## Condensation and expansion gates

These gates are procedural, not advisory. Every threshold cites its corpus anchor, sample size, and basis. Run them as counts; a verdict adjective is not a result.

The gate set covers three families: **condensation** (abstract, contributions, duplication, deletion list), **expansion** (overview, scheme, value placement), and the **evidence apparatus** (float floor, cross-reference integrity, citation density). The expansion and evidence gates are the ones that answer "is there anything in this paper besides prose"; the condensation gates are the ones that answer "is the prose doing its job".

### Compression gates

**Gate-Condense-Abstract — Abstract cap and allocation.**
Text: the abstract; the cap is the corpus median abstract length in words (security four venues, n=35, `corpus/security/statistics.md:31`; the corpus's own long tail reaches well past it, so the cap is a target, and an abstract only slightly over it needs a recorded reason rather than a rewrite). **The instrument does not print the cap** — `abstract.words` is the *draft's* own count, and the `abstract` block's other fields (`sentences`, `longest_sentence_words`, `mean_sentence_words`, `paragraphs`, `allocation`) are measurements of the draft, not bounds. The value is the corpus line above; the instrument prints what the draft measured, and the comparison against the cap is this gate's step, performed by the reader.
Check: count words, sentences, and the words in the longest sentence; label each paragraph by the move it performs (context / gap / build / result); report the four numbers plus the per-paragraph allocation.
Pass: words at or under the cap, sentences at or under the corpus median in `corpus/security/statistics.md:32`, longest sentence at or under the crypto-corpus median (`corpus/crypto/statistics.md:124`), mean sentence length at or under the corpus median in `corpus/security/statistics.md:33`, and at least one paragraph performs the build move by naming the artifact, protocol, or mechanism this paper contributes.
Fail: any count over the bound with no recorded reason; an abstract whose every paragraph reports analysis outcomes while the construction this venue expects gets no naming paragraph — the reported defect was exactly this shape (an over-length abstract whose analysis paragraphs held most of its words) and such an abstract passes a bare length cap, so the length cap alone never closes this gate.

**Gate-Condense-Contributions — Contributions cap and duplication metric.**
Text: the contribution block in the introduction.
Check: count items; count words per item and in total; compute two metrics against the abstract — the Jaccard index over the deduplicated word sets of the two texts, and the Jaccard index over the sets of adjacent word trigrams — and list every shared trigram with the two line numbers it appears on.
Pass: items at or under the corpus median, with the absolute ceiling at twice it; words per item at or under the per-item cap with at most one item above the corpus third quartile; list ≤ 250 words; word-bag Jaccard ≤ 0.20 and trigram Jaccard ≤ 0.019 (both corpus medians, n=22, `corpus/security/statistics.md:61-62`, with the two-index rationale at `:67`). The item count, the per-item counts and the over-long-item flags are the instrument rows listed at the top of this file; the caps themselves are the corpus medians at `corpus/security/statistics.md:58-59`.
Fail: an item that only restates an abstract sentence with the words rearranged; a total over the cap with no reported number; a list left at its own corpus-maximum Jaccard against the abstract (`corpus/security/statistics.md:61`); two items over the corpus third quartile with the rest far below the first — the measured distribution's quartiles are far apart, so the item lengths must be deliberate, not accidental.

**Gate-Condense-Contributions-vs-Threat-Model — Contribution list versus threat model.**
Text: the contribution block and the threat/security-model section.
Check: compute the same word-bag Jaccard between the two spans; then list, for each promised security goal in the contributions, the threat-model sentence that states what the adversary may do.
Pass: Jaccard ≤ 0.20 (**no corpus row measures this pair** — the bound is the sibling value carried over from the contributions-vs-abstract row, not a second measurement); each promised goal has a threat-model counterpart; the threat model adds at least one capability, assumption, or explicit non-goal that the contributions do not state.
Fail: a threat model that is the contributions list with a heading — the corpus instance is a threat-model paragraph that opens by re-listing the parties the contributions already listed, so the two texts do the same work in two places. Restating the adversary is not the failure; restating it *only* there, with no capability the reader did not already have, is.

**Gate-Condense-Deletion-List — Marketing adjectives and process narration.**
Text: the abstract, contributions, introduction, and every claim sentence.
Check: grep for the marketing adjectives (`highly effective`, `trivial`, `negligible`, `completely`, `significantly`, `practical`, `efficient`, `robust`, `scalable`, `guarantees`, `breakthrough`, `seamless`, `powerful`, `state-of-the-art` without a companion number) and for research-process narration (stage identifiers, round labels, letter-number identifiers such as a `C`-prefixed contribution tag, `ref`-prefixed citation keys, attempt counts, abandoned-design inventories, "we first tried … then").
Pass: every surviving adjective carries a measurement, a scope, or is deleted; zero process-narration matches outside a sentence that quotes the anti-pattern in order to forbid it (n=35, `corpus/security/statistics.md:48` — the corpus holds no instance of process narration in abstracts, so this is a zero-tolerance row rather than a quantile).
Fail: one adjective left with no number and no recorded waiver; one identifier from an internal planning register left as if it were a paper concept. The plan's labels are not the paper's names.

### Expansion gates

**Gate-Expand-Overview — Technical overview floor and components.**
Text: the technical-overview subsection.
Check: count its words and lines; report whether it is a standalone top-level section or a named subsection of the introduction; check the checklist below, component by component, and report each as present with its line, or absent.
Checklist (each item anchored in the corpus):
1. one or two sentences of intuition stating the goal in plain terms;
2. a mechanism sentence explaining *why* the construction or attack works, not only what it is;
3. one named sub-block per subproblem, its title naming the subproblem it solves (the corpus median number of named components is anchored at `corpus/security/statistics.md:104`);
4. a forward reference from each sub-block to the section that gives the formal detail;
5. an early statement of the cost, leakage, or assumption the mechanism buys its result with.

Pass: at or above the corpus minimum word count for a standalone overview (n=20, `corpus/security/statistics.md:92`; the instrument's `section-mass` report prints the matched heading, the word count and the direct count for each named section, and the schemes' ratios — **it does not print a quartile**, so the corpus minimum and the first quartile you compare against come from the anchor line, not from its output; overview presence across the four venues is at `:85` and the CCS-only size at `corpus/security/statistics.md:219`), all five components present, and at least three named sub-blocks.
Fail: a component list that answers four of five; an overview that is only a table of contents ("Section 3 presents X, Section 4 proves Y") with no mechanism sentence; a long overview carrying one block — length without components does not pass. Note the venue contrast: CCS papers in the corpus present an overview function in every sampled case, so for CCS this gate always applies and never resolves to "this venue does not use overviews".

**Gate-Expand-Scheme — Scheme-section floor and components.**
Text: the design/construction/protocol section — the section that describes what is built, whatever its title, since most tier-A papers have no section whose title contains the word "Construction" (`corpus/crypto/statistics.md:112`) and fewer than half have any construction-role body section at all (`corpus/crypto/statistics.md:291`); a title-keyed rule misses the rest.
Check: count its words on a declared basis; check the constituents below; report each as present with its line or absent.
Required constituents (regular-expression-counted classes, n=25 deep reads, `corpus/security/statistics.md:131-138`, with the crypto-venue confirmation at `corpus/crypto/statistics.md:300`):
1. a step ordering that says in what order the protocol or attack proceeds (the single highest-hit constituent);
2. a named object, relation, or function defined once and reused, instead of re-deriving the same condition inline;
3. a complexity, communication, or cost expression;
4. the reason for the parameter, size, or field choice;
5. a protocol or algorithm box, or a figure that carries the message flow (the least frequent of the five, more frequent once figures carrying flow are counted).

Pass: all five present, and at least one mechanism-explanation sentence per mechanism (the causal sentence class the corpus has in the deep reads but which a phrase-level count under-counts — do not use the phrase count as the floor).
Fail: a scheme section whose description is a single synthesis sentence plus parameters; a section with the boxes but no step ordering. Where a required constituent genuinely does not apply, the report must name the component and the reason; silence is a fail. The per-constituent hit counts — the corpus row these five classes come from — are recorded in `references/compression-and-expansion-gates.md` and at `corpus/security/statistics.md:131-138`.

**Reading the numbers inside this gate — a diagnosis, not a second gate.** The pass/fail decision for the scheme section is the one above; the mass figures are reported alongside it. Count the scheme section, the security-analysis section and the evaluation section on one declared basis, then read:
Text: the scheme section, the security-analysis section, and the evaluation section.
Check: count words of each on one declared basis; compute scheme/analysis; compute the scheme section's share of the body.
Reading: a scheme/analysis ratio at or above the corpus first quartile of the construction/analysis word ratio (direct basis, n=10, `corpus/crypto/statistics.md:285`) and a scheme section at or above the corpus first quartile of design-section words (`corpus/security/statistics.md:119`; the implied share of the body is at `:121`) are within the corpus distribution; below either, the section is described as thin and the missing constituents are named. The crypto-venue overview size (median 3423 words, n=18, `corpus/crypto/statistics.md:239`) is a comparison for that family's drafts, not a CCS target. The reported defect shape was a protocol/construction pair of sections an order of magnitude shorter in lines than the analysis section, and this reading is the instrument that measures it — the ratio and the constituent checklist remain independent, so a ratio above the floor with three constituents missing still fails the gate above.
Fail (as a reading of the gate above, not a separate verdict): a scheme section clearly thinner than the sections about it, under either floor, with the missing scheme-section constituents named.

**Gate-Expand-Value-Placement — Concrete-value placement.**
Text: every section; specifically the design and proof regions versus the evaluation, parameters, and implementation regions.
Check: scan the design and analysis regions for numeric literals in the class of measured quantities (long decimal expansions, exact success or failure probabilities, bit counts and timings), and scan the evaluation region for symbolic-only statements that should carry the measured value.
Pass: measured values live in the evaluation, parameter, and implementation sections; the design and proof regions carry symbolic or asymptotic expressions; any measured value that belongs elsewhere is *relocated with its digits and its provenance*, never rounded away, never deleted, and the receiving section states where it came from.
Fail: a concrete success probability sitting in a construction paragraph with no location statement; a value deleted or replaced by an adjective "in the interest of style". The cheapest way to look detailed is to pour measured numbers into a construction — that recreates a known defect class, and this gate exists to stop it.

### Evidence-apparatus gates

The gates below close the dimension the prose counts cannot see. A draft can pass every word-count gate while carrying no float, no resolvable cross-reference, and no citation; these three are what stop that, and their measured distributions are census rows B1/B2/B4 and A10/A11/A12 of `skills-work/audit/evidence-structure-census.md`, row A1 and row C2.

**Gate-Expand-Float-Floor — Figure and table caption blocks.**
Text: the whole draft. Check: count the figure caption blocks, the table caption blocks, and their total, on the basis that belongs to the twin being read — LaTeX: `figure`/`table` environments; markdown: `Figure N`/`Fig. N`/`Table N` label lines plus pipe-table blocks, explicitly labelled a **proxy** and not interchangeable with the LaTeX count (R-24.1, R-32 F-3). The census basis for the security rows is a line-opening caption block (an optional number, then `Figure`/`Fig.`/`Table`, then the number and a separator; census B1/B2, security four venues n=35) and is a lower bound on the rendered float count.
Pass: the draft clears the floor the instrument prints as `floats.floor` — one caption block on the figure-plus-table total, licensed because nearly every corpus paper clears it — and the counts are reported beside the quartiles the same record prints in `floats.floor_basis` and the per-venue medians it prints under `floats.context_non_binding.per_venue_medians`, with a zero count on one of the two kinds reported through the instrument's own outlier bucket (`floats.figure_outlier_note`) rather than failed.
Fail: zero caption blocks of both kinds (the instrument's `floats.breach`, with its reason in `floats.breach_reason`). A **table** floor is not part of this gate: the NDSS table-caption median and the CCS one diverge (census B2), so a table floor would be a venue rule rather than a corpus rule, and the outlier bucket is reported instead. This floor is calibrated on the security four venues; the cryptography family is measured on a different float basis and is not failed by it (census A6/A7).

**Gate-Expand-CrossReference-Integrity — Every reference target resolves.**
Text: the LaTeX twin (no `n`: this is a draft property, licensed by census `skills-work/audit/evidence-structure-census.md:1`, not by a corpus quantile). Check: collect every `\ref`, `\eqref`, `\autoref`, `\cref` and `\pageref` target and every `\label`, then report the targets with no declaration; the instrument prints the unresolved set and exits non-zero.
Pass: the unresolved set is empty, including for material relocated to an appendix — the appendix's label must exist, and in a markdown draft the appendix must be called from the body, so the moved material stays reachable.
Fail: any `\ref` whose label is declared nowhere; the rendered draft ships `??`. A markdown twin has no resolvable targets, so this row reports **not-applicable** and exits **4** — a distinct code from the measurement failure **2**, so a pipeline does not read a healthy markdown draft as broken (R-32 F-7) — and it is never a pass either. The gate itself carries **no numeric threshold, and its thresholds carry no sample size because the requirement is a draft property rather than a corpus quantile**: there is no `n` to quote and no `statistics.md` row that licenses a bound here, which is why the cryptography tier-A figures sometimes quoted beside it (census A10/A11, whole-paper, per 1000 words and per paper) are **non-binding context** printed by the instrument as such under `cross_references` — not a security-venue floor, and not applicable to a section span (R-27).

**Gate-Expand-Citation-Density — The related-work region cites something.**
Text: the section that places the work against prior art (no `n` and no quantile: presence, licensed by the whole-paper key row at census `skills-work/audit/evidence-structure-census.md:1`). Check: its word count and its citation-key count.
Pass: at least one citation key. Fail: a related-work section with **zero** citation keys — a word-count floor on related work is satisfied by a section that cites nothing, and the requirement is a **presence** test over the named region rather than a density, so it binds no corpus quantile and carries no sample size either: the requirement is a draft property, and no `statistics.md` row licenses a bound for it. The density figures themselves (cryptography tier-A citation keys per 1000 words, census A12) are **whole-paper, non-binding context** from another family: they are not restated here as a security threshold, and no section-scoped density figure may be added without a security-side, section-scoped corpus measurement (R-27).

**Manual self-check item, not a gate: formal content.** Inline-math density is **reported, never verdicted**, at the security venues. The security corpus is PDF-extracted text with no LaTeX source, so this quantity was never measured on that population; the only measured distribution is the cryptography tier-A one, on a **whole-paper** basis (census A1), and it prints as **non-binding context** — neither a security-venue floor nor a section-scoped threshold (R-27). The instrument prints the draft's count and that distribution side by side and emits no verdict. What the author owes the report is a **recorded reason** when the design and analysis sections carry no formula, notation, or definition at all — the reviewer will ask, and "we did not think about it" is not a reason. The numeric floor for the cryptography family is owned by `crypto-venue-paper-writing`, on its own corpus.

### Venue-specific gates

**Gate-Venue-Threat-Model — Threat-model placement and size.** The requirement is that the adversary statement is **explicit and locatable** — stated once, in one place, in prose — not that it owns a heading. Standalone-section share is venue-dependent (`corpus/security/statistics.md:217`; the corpus's own CCS pair rows are at `:152`, and the CCS-only standalone count at `corpus/security/statistics.md:152`). A standalone section is the CCS default, so the gate is: a standalone section unless a recorded reason says why the adversary statement lives inside the system overview, and a draft that satisfies every requirement below from inside the system overview has not failed. When standalone, its size target is the corpus median threat-model section length (`corpus/security/statistics.md:157`, n=16; the quartiles are in `references/compression-and-expansion-gates.md`). The internal order is fixed by the corpus: parties and trust assumptions (who may collude) → adversary capabilities (what it sees, changes, and when it decides) → security goals and explicit non-goals. Capability lists are written as assumption-plus-decidable-statement prose, not as a table (`corpus/security/statistics.md:165`). Fail: a threat model that is a bulleted capability table with no trust assumptions, or one that drifts between model and evaluation.

**Gate-Venue-Disclosure-Ethics — Disclosure and ethics statement.** ACM CCS '24 requires that authors convince reviewers that proper procedures such as IRB approval or responsible disclosure have been followed (`corpus/security/statistics.md:177`). Gate: the paper states IRB status and the responsible-disclosure action, or says explicitly that neither applies and why, at the point the reader needs it. This is a policy obligation, not a corpus-derived rule — the corpus's own ethics and disclosure counts are close to zero (`corpus/security/statistics.md:182-183`), so the corpus cannot set its size. Fail: an ethics or disclosure statement added as a detached closing sentence with no relation to the experiment it covers.

**Gate-Venue-Page-Budget — Page budget and policy snapshot.** The CCS '24 limit is a body-page limit excluding bibliography, marked appendices, and supplementary material (`corpus/security/statistics.md:177`; the four-venue policy table is at `:220`). Gate: record a dated policy snapshot quoting the current call — the snapshot, not this file, is where the page number lives — check the body against it, and route overflow to appendices with forward references rather than by tightening spacing or margins. Never assert the limit from memory: the call for the submission cycle in hand governs. Fail: a budget report without a dated snapshot; a compression plan that shrinks section mass by template tricks.

**Gate-Venue-Adaptive-Attack — Adaptive-attack honesty.** Adaptive-attack discussion is among the rarest postures the corpus measures (`corpus/security/statistics.md:185`), and reviewers look for the absence. Gate: a defense evaluated against the attack it was designed to stop is reported as a standing limitation, and any adaptive evaluation names the adaptive attacker it used.

**Gate-Venue-Subsection-Share — Subsection share and move-not-delete relocation.** No child subsection should hold most of its parent section (the corpus median largest-child share and its third quartile are at `corpus/crypto/statistics.md:330`, n=561; treat the flag as diagnostic, not a hard gate — the median parent is already at half). Relocatable material is defined as verification records, review or process anecdotes, superseded metric tables, and measurement tables that no longer carry the argument. Relocation is *move, never delete*: every claim keeps its status wording and its provenance where it lands. Fail: "rebalance by deleting the extra subsection"; a relocation that drops a status label off a claim.

## Failure Modes

- No threat model or a shifting one: stop and draft the adversary statement before revising claims.
- Attack/defense claim without evidence anchor: expose it and scope the claim to what was measured or demonstrated.
- Abstract over the condensation caps, or under them while spending most of its words on analysis outcomes: run the abstract count instead of judging by feel.
- Contributions that restate the abstract, or a threat model that restates the contributions: run the contributions counts and report the two Jaccard values.
- Technical overview present but below the floor or missing components: run the overview gate and name each absent component with its line.
- Scheme section thinner than the sections around it, or missing scheme-section constituents: run both scheme gates together; a ratio inside the floor with constituents missing is still a fail.
- Measured values inside design or proof text, or symbolic-only evaluation numbers: run the value-placement gate and relocate rather than delete.
- No float anywhere: run the float-floor gate; zero caption blocks of both kinds is the breach, and a draft with a zero count on one kind is reported through the instrument's outlier bucket rather than failed.
- A `\ref` that resolves nowhere, or relocated material with no call from the body: run the cross-reference gate; the unfinished reference ships as `??`.
- Related work with no citation key: run the citation-density gate; the word-count floor does not catch it.
- Formal regions with no formula, notation, or definition at all: this is a **manual self-check item** — the instrument reports the count and the cryptography-corpus distribution without a verdict, and the report must carry the author's recorded reason.
- CCS page limit may have changed since training: verify the current official call before any compression claim.
- De-identification gap: fix author names, institution, and identifying repository references before the format pass.
- Evaluation only against the designed-for attack: report it as a standing limitation, not as strength.

## Workflow

1. Verify the current official call and template of the venue in hand (CCS, IEEE S&P, or NDSS); record a dated policy snapshot before any budget statement.
2. Read the draft and produce a diagnosis: clear / under-specified threat model / overclaimed / overloaded / verbose where it must be dense / thin where it must be dense. State the target venue first, because the page budget and the ethics obligation that follow are read from that venue's call and not from CCS by default.
3. Condensation count pass — run the counts over the abstract and the contributions and report the numbers: abstract words, sentences, longest sentence, per-paragraph move allocation; contribution item count, words per item, list total; contributions-versus-abstract word-bag and trigram Jaccard; contributions-versus-threat-model Jaccard. Report the before and after numbers together.
4. Fix the threat model and the first-page framing.
5. Expansion count pass — run the gates over the overview and the scheme section and report each component as present or absent: overview words and location, scheme words, scheme/analysis ratio, scheme share of body, and every overview and scheme component with its line.
6. Evidence-apparatus pass — run the three evidence gates and report each row with its basis: figure and table caption blocks against the census quartiles, the unresolved reference targets (empty or listed), the related-work citation-key count, and the formal-content count from the `math` row as a reported number with the author's recorded reason. From the skill-suite root: `python3 skills/ccs-writing-style/scripts/count_prose_gates.py evidence PAPER.md --related-work-heading "Related Work"` runs the whole pass; exit 1 carries the breach list on stderr, exit 2 means a row could not be measured and no verdict may be read. **The `--related-work-heading` and `section-mass --section` selectors read markdown headings (`#…`), which is why the command above names a `PAPER.md`; on a LaTeX twin they match nothing and the run reports `degenerate` with exit 2 rather than a verdict.** That is a limitation of the selector, not a defect in the draft, and it must never be reported as a prose failure: a LaTeX-side run needs the region map — the same shape of explicit input the venue instrument requires.
7. Rewrite claims against evidence: pair each claim with proof, measurement, exploit, or cost; strip the adjectives on the deletion list and the process narration.
8. Compress to the target venue's page budget — never to another venue's — moving transcripts, extra measurements, and full proofs to appendices with forward references, and re-run the cross-reference gate after the move so the relocated material stays reachable.
9. Run the double-blind scan and the de-AI grep checklist; fix every hit or record a waiver.
10. Run the structure conformance check in [references/section-order.md](references/section-order.md): section order, threat-model placement, banned forms (Roadmap subsection, standalone numbered Open Problems, Claim-named central result, bare work-plan labels); fix or record a reason.
11. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: writing diagnosis; the counted gate report set — abstract words/sentences/longest sentence/allocation, contribution items/words/Jaccard values, overview words and components, scheme words and components, scheme-versus-analysis ratio with its declared basis; the evidence-apparatus report — figure/table caption blocks against the census quartiles, unresolved reference targets, related-work citation keys, and the formal-content count with the author's recorded reason; first-page fix; claim-discipline table (claim mapped to proof/measurement/exploit/cost); compression cuts (move/delete/merge); anonymity edits; page-budget report; dated policy snapshot; unresolved items for the human author.

## Reference Files

| File | Contents |
|------|----------|
| `references/compression-and-expansion-gates.md` | The condensation and expansion gates with corpus anchors, sample sizes, bases, the counting method, and the CCS-versus-USENIX rule differences |
| `references/section-order.md` | Default body order for CCS/S&P/NDSS, the banned structure forms (Roadmap subsection, standalone numbered Open Problems, a central result named Claim, bare work-plan labels), and the conformance check to record before freeze |
| `references/sentence-rewrites.md` | Draft-pattern to CCS-safe-rewrite table, the deletion lists, and the compression vignette |
| `references/evaluation-scenarios.md` | Test specifications for independent evaluation |
| `skills/ccs-writing-style/scripts/count_prose_gates.py` | The counting instrument for every gate above: the tokenizer it used is pinned and printed with its output, and a pattern that matches nothing is reported as degenerate rather than zeroed. Subcommands: `abstract-contributions`, `section-mass`, `span`, and the evidence rows `evidence`, `captions`, `crossrefs`, `math`. Its exit codes are the contract the rules above are read against — measured and unbreached, a breached gate with its reason on stderr, a measurement failure from which no verdict may be read, and a row not applicable to this twin (a markdown draft has no `\ref` targets) which is neither a pass nor a failure. **That list is printed by the `evidence` subcommand, whose report carries an `exit_contract` field naming the codes and their meanings**; `abstract-contributions`, `section-mass` and `span` print their counts, their `status`/`match_status` values and their own exit code, but not the code list, so a reader who wants the contract in the instrument's own words runs `evidence`. `--self-test` proves both directions of every gate in one pass — including the R-27 scope assertions and the R-32 F-3/F-7 twin-basis and exit-code assertions — and prints its own case count, which is the count to quote. Paths are relative to the skill-suite root `skills-work/crypto-research-agent-skills`; run `cd skills-work/crypto-research-agent-skills` first |
| `skills/ccs-writing-style/scripts/check_pointer_resolution.py` | The installable pointer resolver: ships with this skill so the check still exists after installation to `~/.dsh/skills`, where `skills-work/tools/` does not. Run `python3 skills/ccs-writing-style/scripts/check_pointer_resolution.py` from the skill-suite root after a gate is renamed or a pointer file changes the name it uses — expected a `RESULT: PASS (nn/nn gate names resolve)` line, exit 0, and a `skip` line for every mention it excluded (a run that excludes none prints none). `--self-test` proves both directions (a warning sentence is a mention; the same name on an instruction line still fails) and prints its own case count |
| Pointer resolvability in the repository | The shared checker `python3 skills-work/tools/rule-trace-check.py --fail-on-gap` (C15) enforces the same rule inside this workspace. **It is a workspace instrument, not a shipped one:** run it from the workspace root (the directory that contains `skills-work/`), and do not expect the path to resolve beside an installed copy. Expected: `RESULT: PASS [no FAIL]`, exit 0. The two instruments must agree on the historical defect; the cross-check is recorded in `skills-work/reports/author-style-notes.md` |
