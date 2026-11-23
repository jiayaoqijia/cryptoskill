# Compression and Expansion Gates — CCS

Numeric gates for the security-venue prose this skill covers, with the corpus anchor, sample size, and measurement basis of every number. The skill triggers for **ACM CCS, IEEE S&P, and NDSS**; the USENIX Security form lives in the `usenixsec-writing-style` skill and the cryptography-venue (CRYPTO/LNCS) form in the `crypto-venue-paper-writing` skill, and this file restates neither. The gates below are shared across the four security venues because the corpora measure no significant difference between them in the quantities they gate; the venue-specific rows are marked as such, and the page budget and ethics obligations are read per venue from that venue's own official call.

**Which corpus supplies which number.** The security four-venue corpus (IEEE S&P 4 / ACM CCS 5 / USENIX Security 18 / NDSS 8, 35 papers) supplies the abstract, contribution, overview, threat-model, and scheme-section distributions, because those are shapes the security venues share. The cryptography three-venue corpus (62 tier-A papers, 135 full LaTeX sources) supplies the cross-section mass floor and the subsection-share distribution, because it is the only corpus that measured them with a declared basis. Where a rule could be misread as a CCS-specific constant, the adjacent sentence says so.

## Counting method — reproduce these numbers yourself

Every gate below is a count. The counts are only comparable if the basis is declared, so state it in the report.

- **words** — whitespace-separated alphanumeric tokens of the plain-text rendering; the security corpus counts `[A-Za-z][A-Za-z'\-]*` over PDF-extracted text, the cryptography corpus counts whitespace-separated tokens of the plain-text rendering of the LaTeX source. A word count is always reported with which of the two it is.
- **sentences** — split on `.`/`!`/`?` followed by whitespace or end of text, after protecting common abbreviations and reference numbers from splitting.
- **section words** — a section's words include its subsections unless the report says `direct`; `direct` means the section's own text without its subsections.
- **body words** — all sections before the first appendix section or appendix marker.
- **pages** — measured on the compiled PDF under the venue template of the cycle in hand. The security corpus's page-interval numbers carry a plus/minus one page error because a section boundary was taken at the heading page; treat page-level conclusions as plus/minus one page.
- **an IACR ePrint author version is a different layout from the ACM or IEEE proceedings version.** Nine CCS and S&P corpus papers were read from the author's ePrint version, and the corpus records this at the top of its basis section (`skills-work/corpus/security/statistics.md:21`). Its page numbers must never be compared against an ACM, IEEE, USENIX, or NDSS page limit. Only a compiled PDF under the cycle's own template may be checked against a limit.
- **word-bag Jaccard** — over two texts A and B: |set(words(A)) ∩ set(words(B))| / |set(words(A)) ∪ set(words(B))|, case-folded, punctuation stripped, deduplicated.
- **trigram Jaccard** — the same index over the sets of adjacent word trigrams, which is more sensitive to reused phrasing than the word bag.
- **numeric-literal class** — measured quantities: multi-digit exact decimals, exact success or failure probabilities, bit counts, byte counts, and timings. Small structural integers (a number of parties, a number of protocol rounds, a party index) are not in the class.

- **caption block** — a line that opens a float caption: an optional number, then `Figure`/`Fig.`/`Table`, then the caption number and its separator. This is the unit of census rows B1/B2 and a **lower bound** on the rendered float count (a caption the extraction merged into a paragraph line is not counted). It is not the LaTeX-environment basis and the two are never averaged.
- **reference call** — a LaTeX `\ref`/`\eqref`/`\autoref`/`\cref`/`\pageref` target, resolved against the `\label` declarations in the same file.

`skills/ccs-writing-style/scripts/count_prose_gates.py` in this repository prints these counts for a manuscript or for one extracted span: `abstract-contributions`, `section-mass`, `span`, and the evidence rows `evidence`, `captions`, `crossrefs`, `math`. Run it from the skill-suite root (`cd skills-work/crypto-research-agent-skills`) before rewriting and after; a gate report without before-and-after numbers is incomplete. `--self-test` runs **47 cases** that prove both directions of every gate in one pass — including the R-27 scope assertions and the twin-basis and exit-code assertions of R-32 F-3/F-7, so a later edit cannot silently turn a whole-paper cryptography quartile into a section- or security-scoped threshold, read a markdown draft with the LaTeX float basis, or collapse "not applicable" into "failed". **The instrument prints that count itself** (`self-test: 47/47 as expected`) and the printed count is authoritative: if this file and the instrument disagree, the instrument is right and this file is stale. A gate that cannot be shown to fire is not a gate. Its exit codes are part of the contract: **0** measured with no breach, **1** a breached gate whose reason is printed on stderr, **2** a measurement failure (missing or empty input, no `--section`, a heading pattern that matched nothing) from which no verdict may be read, **4** a row that does not apply to this twin (a markdown draft has no `\ref` targets), which is neither a pass nor a failure.

### Checking that a pointer still points at something

Pointer resolvability is enforced by **two instruments that must agree**, because they have different reach:

- **In the repository:** the shared checker, `python3 skills-work/tools/rule-trace-check.py --fail-on-gap` (its C15 check). **A workspace instrument, not a shipped one** — run it from the workspace root (the directory containing `skills-work/`), and do not expect that path to resolve beside an installed copy. Expected `RESULT: PASS [no FAIL]`, exit 0.
- **Wherever this skill is installed:** `python3 skills/ccs-writing-style/scripts/check_pointer_resolution.py` **from the skill-suite root** (`cd skills-work/crypto-research-agent-skills`), which ships with the skill and therefore travels to `~/.dsh/skills`, where `skills-work/tools/` does not exist (R-20a). Expected `RESULT: PASS (n/n gate names resolve)`, exit 0; it prints one `OK`/`FAIL` line per pointer/owner pair, and a `skip` line for each name it excluded — a run that excludes no name prints no `skip` line.

Both use the same contextual criterion: a gate name that is backticked, or introduced by *invoke / call / apply / run / use / check / grep*, is a **use** and must resolve in the owning file; a name the text warns about is a **mention** and is left alone. That distinction is what lets a pointer file warn "a reader may expect a gate named after the design section; no such gate exists — the owner declares `Gate-Expand-Scheme`" without failing: the warning is excluded as a mention, and the canonical gate the sentence sends the reader to is still checked. Run either instrument after a gate is renamed, after a pointer file changes the name it uses, and before a submission. `skills/ccs-writing-style/scripts/check_pointer_resolution.py --self-test` proves both directions at once — **14 cases** at the revision this file was written against, and it prints that count itself, which is the one to quote — if you want to see the guard rather than trust it.

### The instrument's contract — three rules a measuring device must obey

An instrument that reports a clean zero where it matched nothing is worse than no instrument, so the script is bound by three rules and states them in its own output.

1. **The tokenizer is pinned and printed.** The script prints the exact pattern it used in a `tokenizer` field, and the printed `basis` describes that same pattern rather than a basis it never applied. Counts from this script are comparable only to counts from the same pattern on the same text form; a different tokenizer shifts word counts by a few percent, so re-run rather than rescale. Expected agreement between two honest tokenizations is about 4% on a 250-word span.
2. **An unmatched pattern is reported as unmatched.** The contribution list may be written as bullet lines, as bold run-in labels (the form this manuscript uses), or as plain paragraphs. `--items any` finds all three; the report names the mode and, when nothing matched, returns `match_status: "unmatched"` with every per-item field set to null and a `degenerate` note. A null per-item gate is never a pass — the script exits non-zero so a caller cannot read a clean result out of a failed match.
3. **A missing structural input is refused, not defaulted.** `section-mass` with no `--section`, or with a pattern that matches no heading, prints `status: "degenerate"`, leaves `sections` and `ratios` null, names the remedy, and exits non-zero. An empty report is not evidence that a section is well proportioned.

## Thresholds, with anchors

The Corpus column says which file an anchor resolves in: **Security** is `skills-work/corpus/security/statistics.md` (35 papers, PDF-extracted text), **Crypto** is `skills-work/corpus/crypto/statistics.md` (62 tier-A papers, LaTeX plain-text rendering). The two corpora count different textual bases, so a number is only comparable to another number from the same corpus; the full paths are used here so every anchor resolves from the workspace root.

**The bound is stated once, in the gate below; the sample and the row it came from are here.** The distributions themselves are printed by `skills/ccs-writing-style/scripts/count_prose_gates.py`, but **not in the `basis` field**: that field describes the unit measured — the tokenizer, the twin, the proxy warning. The quartiles, medians and extremes print in the **context** records beside each row: `citations.context_non_binding.citation_keys_per_1000w` and `cross_references.context_non_binding.reference_calls_per_1000w` for the cryptography rows, `floats.floor_basis` and `floats.context_non_binding.per_venue_medians` for the float rows, and `math.reference_distribution` for the formal-content row. **Correction recorded (t3): an earlier version of this paragraph said those numbers were printed "as that row's `basis`", and that the table below therefore does not copy a bound — both statements were false.** The instrument has no `basis` field of that kind, and the table does state each bound as a number. What the table adds is the unit and the sample size — the two things a reader needs to check that a bound's scope matches the row that licenses it (R-27) — plus the anchor to recompute the distribution from, and every bound it states carries that anchor on its own row.

| Gate quantity | Threshold | n | Basis | Anchor | Corpus |
|---|---|---|---|---|---|
| Abstract words | at most **220** | 35 | words, PDF-extracted text | `skills-work/corpus/security/statistics.md:31` | Security |
| Abstract sentences | at most **9** | 35 | sentences | `skills-work/corpus/security/statistics.md:32` | Security |
| Mean words per abstract sentence | at most **24.1** — the corpus median, and the **pass threshold the gate applies is the 1.25× tolerance band on it, i.e. 30 words**; the two numbers are reconciled at `Gate-Condense-Abstract` below, so the table and the gate never state different bounds | 35 | words/sentence | `skills-work/corpus/security/statistics.md:33` | Security |
| Longest abstract sentence | at most **40** | 59 | words | `skills-work/corpus/crypto/statistics.md:124` | Crypto |
| Contribution items | at most **5**, absolute **10** | 22 | items | `skills-work/corpus/security/statistics.md:58` | Security |
| Words per contribution item | at most **72** | 22 | words | `skills-work/corpus/security/statistics.md:59` | Security |
| Contribution items carrying a number | median **66.7%** — a target, not a floor | 22 | share | `skills-work/corpus/security/statistics.md:60` | Security |
| Contributions vs abstract, word-bag Jaccard | at most **0.20** | 22 | word sets | `skills-work/corpus/security/statistics.md:61` | Security |
| Contributions vs abstract, trigram Jaccard | at most **0.019** | 22 | trigram sets | `skills-work/corpus/security/statistics.md:62` | Security |
| Abstract process narration | **0** instances tolerated | 35 | manual + lexical scan | `skills-work/corpus/security/statistics.md:48` | Security |
| Contributions vs threat model, word-bag Jaccard | at most **0.20**, the same index as the contributions-vs-abstract row but computed between two different spans; no separate corpus row measures this pair, so the number is the sibling bound carried over rather than a second measurement | — (no corpus row; scope is the draft) | word sets | prose-declared, licensed by `skills-work/corpus/security/statistics.md:61` only for the index definition | Security |
| Technical overview, minimum size | at least **596** words | 20 | words | `skills-work/corpus/security/statistics.md:92` | Security |
| Technical overview, expected size | median **1535.5** words; CCS-only median **1058** | 20 / 5 | words | `skills-work/corpus/security/statistics.md:92`, `:219` | Security |
| Technical overview, presence | **5 of 5** CCS papers present an overview function | 5 | manual section audit | `skills-work/corpus/security/statistics.md:82` | Security |
| Overview components | **5** required components, each with a corpus instance | 5 named / 20–25 deep reads | manual deep read of the overview sections | `skills-work/corpus/security/statistics.md:104` | Security |
| Scheme section, expected size | median **3481** words (corpus and CCS-only coincide) | 35 / 5 | words | `skills-work/corpus/security/statistics.md:119`, `:127` | Security |
| Scheme section, required constituents | **5** constituents, each a regular-expression-counted class | 25 | regex count over deep reads | `skills-work/corpus/security/statistics.md:131` | Security |
| Scheme/analysis word ratio | at least **0.44** (the corpus first quartile) | 10 | words, direct basis | `skills-work/corpus/crypto/statistics.md:285` | Crypto |
| Abstract length, four-venue medians | fully overlapping — the null finding that forbids per-venue caps | 35 | words | `skills-work/corpus/security/statistics.md:213` | Security |
| Standalone overview section share | venue-dependent; this venue's value is in the `usenixsec-writing-style` skill | 35 | section audit | `skills-work/corpus/security/statistics.md:216` | Security |
| Standalone threat-model section share | venue-dependent; CCS's own value is the default this skill reads | 35 | section audit | `skills-work/corpus/security/statistics.md:217` | Security |
| Body page limits, official CFP | one numbered limit per venue, per cycle | — | official calls | `skills-work/corpus/security/statistics.md:220` | Security |
| Scheme/design section words | at least **2663** words (the corpus first quartile of the design-section word count) | 35 | words | `skills-work/corpus/security/statistics.md:119` | Security |
| Threat-model section size | median **843** words | 16 | words | `skills-work/corpus/security/statistics.md:157` | Security |
| Largest child subsection share | flag above the corpus third quartile | 561 | words | `skills-work/corpus/crypto/statistics.md:330` | Crypto |
| CCS body page limit | **12** pages, excluding bibliography, marked appendices, supplementary material — policy, verify at execution time | — | official call | `skills-work/corpus/security/statistics.md:177` | Security |

## Condensation gates

### Compression is an action list, not a length knob

The measured lengths are ceilings to check, not the instrument that produces the cut. A draft is compressed by doing these three things and re-measuring, in this order:

1. **Delete research-process narration.** The corpus contains 0 of 35 papers narrating process in the abstract, the contributions, or the overview (`skills-work/corpus/security/statistics.md:48`), so every stage name, round label, attempt count, and abandoned-design inventory is a deletion candidate rather than a judgement call.
2. **Delete abstract-versus-contributions duplication.** Measure the two overlap indices (gate above) and give each shared span a disposition — delete, merge into one statement, or move into the body with a forward reference. This is the mechanical half of the condensation, and it is where over-length abstracts actually lose their words.
3. **Replace adjectives with numbers, or delete them.** A claim that cannot carry a number carries a scope instead ("on this platform, at this version"); one that can carry neither is deleted.

Length caps do not enter this list because the corpus does not support a per-venue one: the four security venues' abstract medians are 205 to 227.5 words with fully overlapping ranges (`skills-work/corpus/security/statistics.md:213`), and the crypto venues sit at a median of 210 (`skills-work/corpus/crypto/statistics.md:121`). Setting a different hard cap per venue would encode a difference the corpora do not contain.


### Gate-Condense-Abstract

**Input** the abstract. **Output** words, sentences, longest sentence, per-paragraph move labels (context / gap / build / result), and the share of words in each move.

**Pass:** words ≤ 220 unless a recorded reason names why the venue's own distribution supports more; sentences ≤ 9; mean sentence length ≤ 30 words — **that 30 is the corpus median of 24.1 with the 1.25× tolerance band applied, and it is the bound this gate passes on**, exactly as the threshold table above states it, so the row and the gate cannot disagree; longest sentence ≤ 40 words; at least one paragraph performs the build move by naming the artifact, protocol, or mechanism the paper contributes; zero process-narration spans; no sentence shared verbatim with the contributions list.

**Fail:** every number inside the caps but no paragraph naming what is built; a 220-word abstract whose analysis paragraphs hold over half the words and whose build paragraph is a single clause. The reported defect has exactly this shape — a 247-word abstract in four paragraphs, three of which report analysis outcomes — and it passes a bare length cap, so a length cap alone never closes this gate.

**Near-miss to catch:** an abstract at 219 words achieved by deleting the construction sentence.

### Gate-Condense-Contributions

**Input** the contribution block and the abstract. **Output** item count, words per item, list total, word-bag Jaccard, trigram Jaccard, and the list of shared trigrams with the two line numbers of each.

**Pass:** items ≤ 5 (≤ 10 absolute); words per item ≤ 72 with at most one item above 150; list ≤ 250 words; word-bag Jaccard ≤ 0.20; trigram Jaccard ≤ 0.019; each duplicated span given a disposition (delete, merge, or move into the body with a forward reference).

**The per-item cap is a security-family value, and the other family's number is named here so neither can be
transplanted (R-11(a), t8 T8-01).** The 72-word cap comes from the security four-venue corpus, **n=22**,
`skills-work/corpus/security/statistics.md:59`. The cryptography family's cap is **29.5 words per bullet**,
median over 214 bullets, longest bullet 57.5 (`skills-work/corpus/crypto/statistics.md:198-199`), and it is
**not** the rule at this venue: it is measured on bullet lists in CRYPTO/EUROCRYPT/ASIACRYPT/TCC papers, and it
does not govern a security-venue contribution item. The 2.4× gap is a measured population difference, not a
tolerance — before applying either number, name the venue family of the paper, and apply only that family's
cap. `crypto-venue-paper-writing` carries the mirror statement for the other family.


### Gate-Condense-Contributions-vs-Threat-Model

**Placement rule first.** The requirement is that the adversary statement is **explicit and locatable** — stated once, in one place, in prose — not that it occupies its own section. Standalone-section share measured across the four venues: S&P 25% / **CCS 60%** / USENIX 28% / NDSS 88% (`skills-work/corpus/security/statistics.md:217`). CCS is the venue where the standalone form is the majority habit, which is why this gate states a default rather than a universal rule: a draft that states the model in the system-overview subsection and satisfies every requirement below has not failed. A model that is scattered across the design and evaluation sections has failed regardless of where the headings are.

**Input** the contribution block and the threat or security model section. **Output** word-bag Jaccard between them, a table mapping each promised security goal in the contributions to the threat-model sentence stating what the adversary may do, and the list of capabilities, assumptions, or non-goals the threat model adds.

**Pass:** Jaccard ≤ 0.20; every promised goal has a threat-model counterpart; the threat model contributes at least one element the contributions do not state.

**Fail:** a threat-model section that opens by re-listing the parties the contributions already listed and adds nothing; a threat model consisting only of the security goals restated from the contributions, with no statement of what the adversary can do. In the corpus the capability list is written as assumption-plus-decidable-statement prose, not as a table (`skills-work/corpus/security/statistics.md:165`), and a threat-model paragraph that begins by re-enumerating the parties is the observed near-miss (`skills-work/corpus/security/statistics.md:162`).

### Gate-Condense-Deletion-List

**Input** abstract, contributions, introduction, and every claim sentence. **Output** two lists: surviving adjectives with their supporting number or scope, and surviving process-narration spans with a decision per span.

**Marketing adjectives to hunt:** highly effective, trivial, negligible, completely, significantly, practical, efficient, robust, scalable, guarantees, breakthrough, seamless, powerful, state-of-the-art (the last one only fails when no companion number or scope follows it).

**Research-process narration to hunt:** stage or phase names, round labels, attempt counts, abandoned-design inventories, letter-number identifiers from a planning register, citation-key placeholders, and "we first tried … then" narratives. The corpus contains 0 of 35 abstracts narrating process (`skills-work/corpus/security/statistics.md:48`), across all four venues.

**Pass:** every adjective carries a measurement or a scope, or is deleted; zero process-narration spans outside a sentence that quotes the pattern in order to forbid it.

**Fail:** one adjective left bare, one internal identifier left standing as though it were a paper concept. A planning register's labels are not the paper's names, and readers outside the project cannot resolve them.

## Expansion gates

### Gate-Expand-Overview

**Input** the overview span. **Output** word count, line count, whether it is standalone or nested, and each of the five components marked present with a line number or absent.

**Required components, each with its corpus anchor:**

1. an intuition statement naming the goal in plain terms;
2. a mechanism sentence explaining why the approach works, not only what it is;
3. one named sub-block per subproblem, its title naming the subproblem it solves;
4. a forward reference from each sub-block to the section that carries the formal detail;
5. an early statement of the cost, leakage, or assumption the mechanism pays for its result.

All five appear in the required shape in the corpus deep reads (`skills-work/corpus/security/statistics.md:104`), and the named sub-block pattern is confirmed in the cryptography corpus, where an overview carries 5 named blocks at the median and 11 at the third quartile (`skills-work/corpus/crypto/statistics.md:269`).

**Pass:** at least 596 words — the corpus minimum, the floor a draft must clear to be comparable to the thinnest overview in the sample (the first quartile is 854) — plus all five components and at least three named sub-blocks.

**Fail:** four of five components; a table-of-contents overview ("Section 3 presents X, Section 4 proves Y") with no mechanism sentence; a 1100-word overview with a single block — length without components does not pass. The reverse also fails: all five components in 400 words means the mechanism is asserted, not explained — 400 is below the 596-word corpus minimum, so the word floor catches that case too.

**CCS-specific note.** All five CCS corpus papers present an overview function, so this gate always applies at CCS and cannot be resolved by arguing that the venue skips overviews. Where the overview is a subsection of the introduction rather than a top-level section, the word floor still applies to that subsection; where it is a short named paragraph rather than a subsection, the component checklist still applies and the floor is reported as a ratio to the introduction instead of an absolute.

### Gate-Expand-Scheme

**Input** the scheme section — the section describing what is built, whatever its title. **Output** word count on a declared basis, the scheme/analysis ratio, the scheme share of body words, and each required constituent marked present with a line or absent.

**Why the title cannot be the key.** 69% of tier-A papers (43 of 62) have no section whose title contains the word "Construction" (`skills-work/corpus/crypto/statistics.md:112`), and only 46.8% of tier-A papers have any construction-role body section (`skills-work/corpus/crypto/statistics.md:291`). A rule keyed on the title "Construction" misses most of the literature.

**Required constituents, counted over 25 deep reads** (`skills-work/corpus/security/statistics.md:131`):

1. step ordering — in what order the protocol or attack proceeds (20 of 25);
2. a named object, relation, or function defined once and reused (19 of 25);
3. a complexity, communication, or cost expression (17 of 25);
4. the reason for a parameter, size, or field choice (15 of 25);
5. a protocol or algorithm box, or a figure carrying the message flow (10 of 25 for a box, more when flow figures are counted).

Plus the mechanism-explanation sentence class: the corpus holds it in the deep reads but the phrase-level count under-counts it (`skills-work/corpus/security/statistics.md:137`), so it is required per mechanism and is never validated by the phrase count alone.

**Pass:** all five constituents present; at least one mechanism sentence per mechanism; design/analysis word ratio ≥ 0.44; design-section words ≥ 2663 on the same basis.

**Fail:** a scheme section that is a synthesis sentence plus a parameter table; boxes with no step ordering; a ratio inside the floor while three constituents are missing — the ratio and the checklist are independent, and passing one does not excuse the other. A constituent that genuinely does not apply must be named with its reason in the report; silence fails.

**Reading the numbers — a diagnosis, not a second gate.** This gate has one pass/fail decision, and it is the one above. The mass figures are read as a diagnosis and reported alongside it: a scheme section whose ratio to the analysis section falls under 0.44, or whose word count falls under 2663 on the same basis, is described as thin, with the missing constituents named. That reading is the instrument for the reported imbalance between a thin protocol-and-construction pair and a thick analysis section, and it is deliberately expressed as a judgement about proportion rather than as a separate numerical gate — a second gate with the same thresholds would fail the same drafts twice and suggest a distinction that does not exist. Report the ratio with its basis every time; the same manuscript measures differently in lines and in words, so a ratio without its basis is not a result.

**What must not be written into this rule.** Not "the scheme must be longer than the analysis": the measured ratio has a median of 0.89 and only 40% of pairs above 1 (`skills-work/corpus/crypto/statistics.md:285`), so a floor above the median contradicts the corpus. Also not a target taken from a manuscript: a manuscript's post-fix ratio is not a constant, and the corpus distribution governs.

### Gate-Expand-Value-Placement

**Input** every section, split into a design-and-analysis region and an evaluation-and-parameters region. **Output** the numeric literals of the measured-quantity class found in each region, with line numbers, and the disposition of each relocated value.

**Pass:** measured values live in the evaluation, parameters, and implementation sections; the design and proof regions carry symbolic or asymptotic expressions; a measured value that must move is moved *with its digits and its provenance*, is never rounded away and never deleted, and the receiving section says where it came from.

**Fail:** an exact success probability or a long decimal expansion sitting in a construction paragraph with no location statement; a value replaced by an adjective in the name of style. The cheapest way to make a construction look detailed is to pour measured numbers into it, and that recreates a known defect class. Precision in the design section belongs to definitions, not to measurements.

## Evidence-apparatus gates

These three gates close the dimension the prose gates above cannot see: a draft can pass every word-count gate while carrying no float, no resolvable cross-reference, and no citation. The measured distributions are census rows `B1`/`B2`/`B4` and `A10`/`A11`/`A12` of `skills-work/audit/evidence-structure-census.md`, whose §Appendix F table now runs to `A1`–`A20` with `B1`–`B6` and `G-E1`–`G-E9` beside them; its §Bases defines the units. The instrument is `skills/ccs-writing-style/scripts/count_prose_gates.py evidence`, with `captions`, `crossrefs` and `math` for one row at a time.

**Scope rule (R-27), which these gates obey and the reader must not bend.** A threshold's scope must equal the scope of the corpus row that licenses it, because scope is part of the basis. The corpus rows cited here come in exactly two scopes, and they are not interchangeable:

- **per paper** — B1, B2 (figure / table caption blocks per paper) and A10/A11's label count;
- **whole paper, per 1000 words** — A1, A10, A12 (each measured over a paper's entire source, not over a section).

So the only **bound** values the three gates below carry are: the float floor of **1** (B1/B2, per paper — same scope as its row), and the structural requirement of **no unresolved reference target** and **no zero-citation related-work region**, which are properties of the draft and are derived from no corpus quantile at all. Every other number printed beside them — the cryptography per-1000-words quartiles, the label medians, the per-venue caption medians — is **context, whole-paper scoped, and non-binding**, and the instrument says so in its own output (R-24a.2). A section-scoped density breach is **not licensed for the security venues**, and the reason is the population rather than an absence: the security four-venue corpus is PDF-extracted text with no LaTeX source and no role decomposition, so **no security-venue section-scoped row exists** and a security-venue section cannot be judged on a scope that was never measured for it. **This file does not claim the wider statement that "no section-scoped corpus row exists" — that claim was withdrawn as FALSE (R-32 F-4).** The cryptography corpus's own per-role table does carry section-scoped rows (`corpus/crypto/statistics.md` §FORMAL.2: construction, analysis, overview, preliminaries, introduction, evaluation, related, conclusion, each with its own n and quantiles), `crypto-venue-paper-writing` binds a floor on them at criterion 20a, and the same statement is made in the USENIX sibling so the two cannot drift. What a security-venue draft may not do is borrow that role row: the role would have to be a security-venue role, and none was measured.

### Gate-Expand-Float-Floor

**Input** the whole draft. **Output** the count of figure caption blocks, of table caption blocks, and of their total, on the basis the instrument prints.

**Basis — the count belongs to the twin being read, and the two bases are never mixed (R-24.1, R-32 F-3).**

- **LaTeX twin**: `\begin{figure}` and `\begin{table|longtable|sidewaystable}` environments.
- **markdown twin**: the **markdown proxy** — `Figure N` / `Fig. N` / `Table N` label lines, plus **pipe-table blocks** (two or more consecutive `|` lines) standing in for the table body. A markdown draft has no float environments, so judging it with the LaTeX basis reports 0 for a draft that plainly carries tables and fires the floor on a healthy paper. That was the reported defect (t6 F-3): one input, two sibling instruments, opposite verdicts.

The markdown classes are **proxies**: they are not interchangeable with a LaTeX float count and must never be summed with or compared to one; the instrument prints `"proxy": true` and the warning beside them. What is comparable across twins is the **verdict on the same manuscript**, and after this change the three instruments that read a draft agree on it.

The census basis for the security rows is a caption block that starts a line (an optional number, then `Figure`/`Fig.`/`Table`, then the number and a separator) — census rows B1/B2, security four venues, n=35 — which is what the LaTeX branch counts; the markdown branch is the proxy described above. Both are **lower bounds** on the rendered float count, because a caption the text extraction merged into a paragraph is not counted. Never lift `corpus/security/metrics.raw.json`'s `floats.figure_captions` row as a float count: it counts every in-text mention, and its median for these same 35 papers is 23 against the 10 caption blocks measured here (census B6).

**Pass:** at least one figure or table caption block. That is the whole floor, and it is a floor because **34 of 35** corpus papers clear it: figures per paper min **0**, first quartile **5**, median **10**, third quartile **13**, max **20**, with **2 of 35** at zero; tables per paper min **0**, first quartile **0**, median **2**, third quartile **5**, max **12**, with **12 of 35** at zero (census B1/B2). The one paper with neither is `usenix2024-angel`.

**Why the floor is 1 and not the median.** A table floor would be a **venue** rule rather than a corpus rule: NDSS's table-caption median is **0 of 8** while CCS's is **5 of 5** (census B2), so no table value is shared across the four venues. Figures are counted and reported for the same reason — two of 35 papers have none, so a zero figure count is an outlier to state in the report, not a breach to fail. Report the counts against the quartiles above; only the figure-plus-table total of zero is a breach.

**Fail:** zero figure caption blocks and zero table caption blocks. Report the counts and the quartiles with the verdict — a bare "add figures" is not a result.

**Family boundary.** This floor is calibrated on the **security four venues** and is applied to them only. A cryptography-family draft (CRYPTO/EUROCRYPT/ASIACRYPT/LNCS) is measured on a different float basis (LaTeX `figure`/`table` environments: **55 of 62** tier-A papers carry some float form, census A6/A7) and is never failed on this security floor; the instrument's `--venue crypto` switch reports the counts and withholds the verdict.

### Gate-Expand-CrossReference-Integrity

**Input** the LaTeX twin of the draft. **Output** every `\ref`, `\eqref`, `\autoref`, `\cref` and `\pageref` target, every `\label`, and the target set that resolves nowhere.

**Basis and why it carries no threshold.** The security four-venue corpus is PDF-extracted text with no LaTeX sources on disk, so reference-call density was never measured on it. What the cryptography corpus measured (census A10/A11, tier-A n=62) is **whole-paper** scoped — reference calls per 1000 words min **0.000**, first quartile **2.778**, median **3.468**, third quartile **5.687**, with 61 of 62 papers above zero; labels per paper min **2**, median **49.5**, with **0 of 62** papers carrying zero labels — and every one of those numbers is **context only, printed as non-binding** in the instrument's output. Two reasons they may not bind here: they are whole-paper statistics while this gate reads the whole draft's reference commands (a count, not a density), and they belong to another family whose scope and population both differ. This gate therefore states the **resolvability** requirement, which is a property of the draft rather than of a population, and it leaves any density floor to the cryptography-family skill that owns that corpus.

**Pass:** every reference target has a `\label` declaration in the same file. The list of unresolved targets is printed and the instrument exits non-zero on a breach; a broken pointer is a measurement failure, not a silent pass.

**Fail:** a `\ref` whose target is declared nowhere — the rendered draft ships `??`. The clause includes the relocation case: if a span was moved to an appendix, the appendix's label must exist, and a markdown draft's appendix must be called from the body, otherwise the reader cannot reach the material that was moved out of the body.

**Not-applicable state, and its own exit code (R-32 F-7).** A markdown twin has no `\ref`/`\label` targets, so this row does not apply to it. The instrument reports `status: "not_applicable"` and exits **4**, which is deliberately *not* the measurement-failure code **2**: a pipeline that reads every non-zero exit as a failure would otherwise call a healthy markdown draft broken. The row is neither a pass nor a failure, and silence is still not evidence — the run prints the skipped row and its reason.

### Gate-Expand-Citation-Density

**Input** the related-work section (or whatever section places the work against prior art). **Output** its word count and its citation-key count.

**Pass:** at least one citation key. **Fail:** a related-work section with **zero** citation keys. That is a **presence** requirement over the named region and it is derived from no corpus quantile — a word-count floor on related work is satisfied by a section that cites nothing, which is the hole this gate exists to catch. The density distribution itself is measured only in the cryptography corpus and is **whole-paper** scoped: citation keys per 1000 words min **1.108**, first quartile **3.736**, median **4.798**, third quartile **6.199**, median **100.5** keys per paper (census A12). Those figures are **non-binding context** — section-scoped density for this region has no corpus row, and another family's whole-paper quantiles may not be transplanted onto a security-venue section (R-27) — so no security-venue density figure is claimed here and none may be added without a security-side, section-scoped measurement.

**Reported, never a verdict:** inline-math density. The security corpus cannot be measured for it — the papers are PDFs with no LaTeX source — while the cryptography corpus can: tier-A n=62, inline math per 1000 words min **4.700**, first quartile **46.082**, median **54.940**, third quartile **64.373**, with 0 of 62 papers at zero (census A1). Those are **another family's** numbers on a **whole-paper** basis, and they are printed as non-binding context in the instrument's output: quoting them at a security-venue draft would be calibrated on a population the threshold was not measured on, and applying them to a section span would additionally be a scope mismatch (§Scope rule above). The instrument's `math` row prints the count and the reference distribution and **emits no verdict**; a security-venue draft whose formal regions carry no formula at all is a **manual self-check item** — the author records why — never an automatic breach. `crypto-venue-paper-writing` owns the numeric floor for its own family.

## Policy anchors per venue — verify at execution time

Policy numbers are cycle-specific. Record a dated policy snapshot before writing any budget claim, and quote the current call **of the venue in hand**; this skill covers three of them, and the three limits differ.

| Venue this skill covers | Body limit | Ethics / disclosure obligation | Source |
|---|---|---|---|
| ACM CCS | 12 pages, excluding bibliography, well-marked appendices, and supplementary material | Authors are expected to convince reviewers that proper procedures such as IRB approval or responsible disclosure have been followed; optional artifact evaluation | `skills-work/corpus/security/statistics.md:177`; `skills-work/corpus/security/raw/ccs2024-cfp.html` |
| IEEE S&P | up to 13 pages of text and up to 5 pages for references and appendices, 18 in total | Research Ethics Committee; ethical considerations for vulnerability disclosure; IRB disclosure for human subjects | `skills-work/corpus/security/statistics.md:176`; `skills-work/corpus/security/raw/sp2025-cfp.html` |
| NDSS | 15 pages in total, including references and appendices; double-blind | Disclose ethics review where the work has ethical or legal impact and discuss the plan for responsible disclosure of a high-impact vulnerability; artifact evaluation | `skills-work/corpus/security/statistics.md:178`; `skills-work/corpus/security/raw/ndss2025-cfp.html` |
| USENIX Security (owned by the other skill) | 13 pages plus one page for the mandated Ethics considerations and Open science sections | Two titled sections immediately preceding References | `skills-work/corpus/security/statistics.md:175`; `skills-work/corpus/security/raw/usenix25-submission-policies.html` |

An S&P or NDSS draft must not be compressed to the CCS row, and a CCS draft must not adopt the NDSS all-inclusive limit. State which venue the draft targets before any budget statement.

- **Body limit.** ACM CCS '24: no more than **12** pages excluding the bibliography, well-marked appendices, and supplementary material (`skills-work/corpus/security/statistics.md:177`).
- **Anonymity.** Anonymous review; papers not properly anonymized may be rejected without review (`skills-work/corpus/security/statistics.md:177`).
- **Ethics and disclosure.** Authors are expected to convince reviewers that proper procedures such as IRB approval or responsible disclosure have been followed (`skills-work/corpus/security/statistics.md:177`).
- **Artifact evaluation.** Optional, separate from the paper limit (`skills-work/corpus/security/statistics.md:177`).
- **Adaptive posture.** Only 3 of 35 corpus papers discuss adaptive attacks (`skills-work/corpus/security/statistics.md:185`); the corpus cannot set a size, but the absence is what reviewers notice.
- **Official originals for the numbers above.** The page limits are read from the calls archived at `skills-work/corpus/security/raw/ccs2024-cfp.html`, `sp2025-cfp.html`, `ndss2025-cfp.html`, and `usenix25-submission-policies.html` (digest also recorded at `skills-work/corpus/security/statistics.md:220`). Quote the current cycle's page, not the archived one, and date the snapshot.
- **ePrint is a different layout.** Nine CCS and S&P corpus papers were read from the author's IACR ePrint version (`skills-work/corpus/security/statistics.md:21`). Never measure an ePrint PDF against an ACM, IEEE, USENIX, or NDSS page limit.

## Division of labour with the neighbouring skills

- **`crypto-venue-paper-writing`** owns venue structure for the cryptography venues (CRYPTO, EUROCRYPT, ASIACRYPT, LNCS), its abstract formula, its section budget, and the de-AI grep checklist. This skill points there for the de-AI list rather than duplicating it, and states only what differs at CCS: 12 pages excluding bibliography and appendices, the IRB and disclosure statement, the standalone threat-model default, and the overview and scheme gates above.
- **`usenixsec-writing-style`** owns the USENIX Security form: the mandatory Ethics considerations and Open science sections, their placement, and the 13-page-plus-one budget. The shared numeric gates (abstract, contributions, overview floor, scheme constituents, ratio floor) are identical, and the corpus says why: the four security venues show no significant difference in abstract length (`skills-work/corpus/security/statistics.md:50`) or a CCS-specific contribution-item threshold (the CCS subsample is 3 papers, `skills-work/corpus/security/statistics.md:70`), so inventing a per-venue abstract cap would be a fabricated difference. What differs between CCS and USENIX is measured at `skills-work/corpus/security/statistics.md:216-221`: overview presence (100% CCS against 56% USENIX), threat-model section presence (60% against 28%), and the policy budget and ethics obligations.
- **`crypto-paper-writing`** owns drafting workflow. It is not restated here.
