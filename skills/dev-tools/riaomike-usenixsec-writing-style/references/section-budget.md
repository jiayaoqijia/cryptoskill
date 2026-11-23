# Section Budget, Calibration, Register

Adapted from the USENIX writing-style guidance in the Awesome-Journal-Skills collection (MIT, Copyright (c) 2026 Bryce Wang). Budget numbers are anchors for a 13-page body; verify the current cycle's official limit and template at execution time. The counted condensation and expansion gates, with their corpus anchors and sample sizes, are in [compression-and-expansion-gates.md](compression-and-expansion-gates.md).

## Per-section budget (13-page anchor)

| Section | Budget | Job | Anchor (file:line, n, basis) |
|---|---|---|---|
| Abstract + intro | 1-1.25 pp | Problem, adversary, what is built, contribution bullets with numbers | USENIX abstract **212 words median on the USENIX subsample, n=18** — four-venue table at `skills-work/corpus/security/statistics.md:213`, its per-venue header at `:211`; the same four medians are quoted at `:50` for the pooled 35-paper corpus, so the per-venue figure must never be labelled n=35 |
| Background + threat model | 1.5-2 pp | Just enough context; the adversary, stated once in prose | standalone threat-model section 843 words median (q1 769, q3 1041), n=16, words — `:157`; four-venue standalone share S&P 25% / CCS 60% / USENIX 28% / NDSS 88% — `:217` |
| Technical overview | 0.75-1.5 pp | The intuition and the mechanism, before the formal detail | 2 pages and 1535.5 words median (q1 854, min 596), n=20, pages and words — `:91-92`; USENIX standalone-section share 56% — `:216` |
| Design / attack technique | 3-4 pp | The mechanism, end to end; the design-section constituents | USENIX median 4063.5 words (n=18); all-venue median 3481 words (n=35) — `:127`, `:119` |
| Evaluation | 3.5-4.5 pp | Setup, headline results, adaptive/robustness analysis | 1291 words median, n=32, words — `:122` |
| Discussion + limitations | 0.75-1 pp | What breaks, what it costs, what is unknown | not measured per section by the corpus; report the actual share instead of borrowing a figure |
| Related work | 0.75-1 pp | Positioning | not measured per section by the corpus; report the actual share instead of borrowing a figure |
| Ethics considerations | main body, immediately before References | Policy-mandated section, not an appendix | policy: `skills-work/corpus/security/raw/usenix25-submission-policies.html`, digest at `:175` |
| Open science | main body, immediately before References | Policy-mandated section, not an appendix | policy: `skills-work/corpus/security/raw/usenix25-submission-policies.html`, digest at `:175` |

The two rows marked "not measured per section" say so deliberately: the corpus measured the argument-bearing sections, not discussion and related work, and a budget row without an anchor may not borrow one from another section. The policy-anchored rows and the corpus-anchored rows are separate kinds of evidence and are labelled as such.

**Page limit is policy; the other numbers are corpus.** "13 pages plus one page for the ethics and open-science sections" is a policy figure read from the current official call, archived at `skills-work/corpus/security/raw/usenix25-submission-policies.html` and digested at `skills-work/corpus/security/statistics.md:175`, with the four-venue comparison at `:220`. Re-read the call for the cycle in hand and date the snapshot before quoting it. Every other number in the table above is a corpus statistic with its own `file:line`, `n`, and basis; the full set, including the counting method, is in [compression-and-expansion-gates.md](compression-and-expansion-gates.md).

**An IACR ePrint author version is a different layout from the proceedings version.** Nine CCS and S&P corpus papers were read from the ePrint version, and the corpus says so at the top of its basis section (`skills-work/corpus/security/statistics.md:21`). Its page intervals must never be measured against an ACM, IEEE, USENIX, or NDSS page limit; only a PDF compiled under the cycle's own template may be checked against a limit.

**Compression is an action list, not a length knob.** Cut re-narration of tables, consolidate examples, delete research-process narration (0 of 35 corpus papers narrate it), delete abstract-versus-contributions duplication, and replace adjectives with numbers or a scope. Never reach the limit by spacing, margin, or template tricks — those are forbidden by the call.

Then the mandatory sections and references. The two mandatory sections sit in the main body immediately before the references, and they may occupy the extra page the policy provides.

## The ethics and open-science sections are not optional and not appendices

USENIX Security mandates two sections, by title, in the main body: a section titled "Ethics considerations" and a section titled "Open science", each immediately preceding the references section, with an additional page beyond the body limit available for them. Papers may instead place them in the extra page the policy provides; what they may not do is omit them or bury them in an appendix.

Two consequences for revision work:

1. **Wording.** Do not carry a previous cycle's clause wording forward. Read the current call, quote it, and date the snapshot. The 2025 cycle's clauses are recorded in the security corpus's policy table with the official CFP text archived alongside it.
2. **Content.** The ethics section states what was reviewed (IRB status or an explicit "no human subjects, and here is why"), how vulnerable parties were handled, and — where the work reports a live vulnerability — the disclosure plan or its outcome. The open-science section states what artifact is released, under what terms, and what cannot be released and why. Compliance is a policy requirement; the corpus cannot set its size, because only 2 of 35 corpus papers mention ethics at all and none carries a disclosure narrative.

## Claim calibration, the house dialect

Security prose fails in two symmetric ways: marketing ("we completely prevent...") and false modesty that buries a real result. The venue's fix is quantified hedging — every strong verb carries its measurement:

```text
Weak:    Our defense stops code-reuse attacks with negligible overhead.
Better:  Against the 412 ROP chains in our corpus, the defense blocks all
         chains that pivot through heap pointers (387/412; the remaining 25
         use stack-only gadgets, Section 6.3) at a 2.1% median CPU overhead
         (max 4.8%) on SPEC CPU 2017.

Weak:    Attackers can trivially bypass existing scanners.
Better:  Eight of the eleven scanners we tested miss payloads transformed by
         our encoder; the three that detect it do so through one signature rule, which
         also flags 4% of benign traffic in our enterprise trace.
```

Rules of thumb: numbers beat adverbs; populations beat anecdotes ("all 412" not "attacks"); every "first" gets a scope ("first automated analysis of X at ISP scale"); failure cases appear in the same paragraph as the success rate. The condensed counterpart of these rows — what to cut rather than how to phrase — is the condensation gate's deletion list, including the adjectives that must not survive without a number.

## The disclosure narrative belongs in the prose

Papers here often describe live harm potential. Beyond the mandated ethics section, weave the responsible-conduct thread into the body where the reader needs it: the scan methodology paragraph states the rate limits and opt-out handling; the vulnerability section states "reported to the vendor on <date>; patched in version Y" at the moment the flaw is introduced. Reviewers should never wonder, mid-section, whether the experiment was run responsibly. The corpus's own rate of explicit disclosure narrative is 0 of 35 papers, which is why this is a rule rather than an imitation of the literature: the papers that need the narrative are the papers that harm-measuring work produces, and the policy cycle now asks for it in writing.

## Register and mechanics

- Plain systems English. Define acronyms once; this community tolerates jargon density but punishes ambiguity about which TEE/DOM/EL2 you mean.
- Present tense for the system and its properties; past tense for experiments run.
- Figures carry the argument in evaluation sections — a reviewer flipping pages should reconstruct the results story from captions alone.
- Name the system early and use the name consistently; anonymize any name publicly attached to the group at submission time.
- Use the unaltered official USENIX LaTeX template; check the current call for AI-writing disclosure and reporting mandates before submission.

## Revision passes that pay at this venue

1. **Condensation pass**: count the abstract and the contribution list against their gates and report the numbers, including the abstract-to-contributions overlap metrics. A pass without counts is not a pass.
2. **Expansion pass**: count the overview and the design section, mark each required component present or absent with its line, and report the design-versus-analysis ratio with its basis.
3. **Adversary-consistency pass**: every evaluation claim re-checked against the stated threat model, whether the model is a standalone section or embedded.
4. **Calibration pass**: hunt the adjective list and attach numbers or delete.
5. **Cold-reader pass**: someone outside the subfield reads intro + threat model only, then writes down what they think the paper claims — mismatch means the framing leaks.
6. **Caption pass**: figures/tables self-contained, units and populations stated.
7. **Policy pass**: ethics and open-science sections present, titled as required, immediately before the references; page budget checked against a dated snapshot.

## Reverify each cycle

- Page budget and template version in the current official call.
- The ethics and open-science section requirements and their exact placement.
- Any new style-adjacent mandates (AI-writing disclosure, reporting checklists).
