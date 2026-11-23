---
name: usenixsec-writing-style
description: Use when drafting or revising prose for a USENIX Security Symposium paper — threat-model-first structure, calibrated security claims, a disclosure narrative woven into the text, the current USENIX page budget and its ethics and open-science sections, abstract and contribution-list condensation, technical-overview and design-section expansion (the family condensation and expansion gates), and the plain systems-security register this program committee rewards.
---

# USENIX Security Writing Style

A USENIX Security paper argues like an engineer under oath: state what the adversary can do, show what you built or broke, measure it honestly, and say plainly what does not follow. Adapted from the USENIX writing-style guidance in the Awesome-Journal-Skills collection (MIT).

## Evidence base, and where the shared gates live

Every `file:line` citation here is a **provenance annotation, not a link**: the paths point at the corpus snapshot inside the authoring workspace (`skills-work/`) and are not expected to resolve beside an installed copy. The snapshot is the security four-venue corpus — 35 papers, 25 read in full — plus, for a cross-family comparison, the 62 tier-A cryptography papers.

Three quantities this skill's own rules rest on are quoted below, because nothing else prints them; the shared gates' bounds are not.

| USENIX-specific quantity | Value (basis, sample) | Anchor |
|---|---|---|
| Standalone overview section | **USENIX 56%** (10 of 18 papers, section audit) — the embedded form is permitted here | `corpus/security/statistics.md:84`, `:216` |
| Standalone threat-model section | **USENIX 28%** (5 of 18 papers, section audit) — second-lowest of the four venues | `corpus/security/statistics.md:153`, `:217` |
| Adaptive-attack posture in the literature | **3 of 35** papers discuss it — the absence is what reviewers notice | `corpus/security/statistics.md:185` |

Two more quantities this skill used to quote are deliberately **not** here: the threat-model section size and the page budget. They live where they are measured or read — `corpus/security/statistics.md:157` (n=16), and the dated policy snapshot the workflow requires (`:220`, `references/section-budget.md`).

**The shared gates are owned elsewhere.** The family-wide security-venue gates — the abstract and contribution counts with their bounds, the two overlap indices, the deletion lists, the threat-model precision requirement, the overview and design constituent checklists, the design-versus-analysis mass ratio, the value-placement rule, and the three evidence-apparatus gates — are owned by **`ccs-writing-style`**, in `skills/ccs-writing-style/references/compression-and-expansion-gates.md`, and are invoked from there by name. This skill holds no second copy of them or of their bounds: the rewrite tables are in `skills/ccs-writing-style/references/sentence-rewrites.md`, and the counting instrument is `skills/ccs-writing-style/scripts/count_prose_gates.py`, run from the skill-suite root `skills-work/crypto-research-agent-skills`. **What that instrument prints per row is the draft's own measurement and the row's declared basis** — in `evidence` mode also a `binding_thresholds` block and the exit-code contract, and in the condensation modes the counts alone, with no bound field, so a bound printed in the family file is read from its anchor and never from this instrument's output.

**The evidence-apparatus rows are a named delegation, not a dropped citation.** Three gates carry this venue too, and this skill invokes them by name rather than re-tabulating them: `Gate-Expand-Float-Floor`, `Gate-Expand-CrossReference-Integrity`, `Gate-Expand-Citation-Density` — all three owned by `ccs-writing-style/references/compression-and-expansion-gates.md`, which is also where their corpus rows are stated with their sample sizes and basis. The census rows behind them are **`B1`/`B2`** (figure and table caption blocks, **per paper**), **`B4`** (lettered appendix), and **`A10`/`A11`/`A12`** (reference calls and labels, citation keys — cryptography tier-A and **whole-paper**, reported as non-binding context only), all of them in `skills-work/audit/evidence-structure-census.md` and all of them restated in that ccs file. They are deliberately not re-listed here: a second copy of a rule input is how two skills start answering the same check differently. A reader who needs the row behind a printed count follows the ccs file, not this one.

The doctrine both skills publish: a rule is stated once and pointed at. Measurements may be quoted on both sides — facts are shared, rule sentences are not.

**Scope (R-27).** The only **bound** value among the shared evidence rows is the float floor, and its scope matches its row's: both are **per paper**. The cross-reference and citation rows bind **no** number — they are draft properties — while every cryptography per-1000-words quartile printed beside them is whole-paper context that may not be applied to a section span, on this venue or any other.


## Scope

In scope: adversary-first structure and wording; quantified calibration of every strong claim; the two policy-mandated sections and their placement; page-budget planning against the current call; the permitted embedded overview form; the disclosure thread woven into the methodology and the vulnerability discussion; plain systems-English register; caption discipline; self-anonymization at submission time; and the revision passes that check adversary consistency and calibration.

Out of scope: inventing systems, attacks, measurements, or citations; deciding novelty or authorship; guaranteeing acceptance; or submitting without human authorization. The family-wide security-venue gates belong to `ccs-writing-style` and are invoked from there, not restated here. The cryptography and LNCS family belongs to `crypto-venue-paper-writing`.

## Required Inputs

- the current USENIX Security official call for papers and template (page budget, appendices, ethics, AI-disclosure, artifact policy);
- manuscript draft or section under revision;
- the stated adversary or the raw security claims to be given one;
- measurement data or attack demonstrations that claims must be calibrated against.

## Success Criteria

- Every claim sits relative to a named adversary, and the evaluation never assumes a stronger or weaker attacker than the stated model grants.
- The abstract, contribution list, overview and design sections pass the family gates invoked from `ccs-writing-style/references/compression-and-expansion-gates.md`, with the counts the instrument prints reported rather than judged.
- The evidence apparatus is present, not presumed: the draft clears the three family evidence gates invoked from `ccs-writing-style/references/compression-and-expansion-gates.md` — the caption-block floor, reference-target resolvability, and at least one citation key in the related-work region. The float count is taken on the basis that belongs to the twin being read: float environments on LaTeX, the markdown proxy (`Figure N`/`Fig. N`/`Table N` label lines plus pipe-table blocks) on a markdown draft, labelled a proxy and not interchangeable with the LaTeX count (R-24.1, R-32 F-3). Relocated material stays reachable — the appendix's label must exist and, in markdown, the body must call it. A markdown draft's reference row reports **not-applicable** rather than a pass or a failure, on a code the instrument distinguishes from measurement failure (R-32 F-7) and prints with the report.
- **Formal content is a manual self-check item here, not a gate.** The security four-venue corpus has no LaTeX source, so formula density was never measured on this population; the instrument prints the draft's count beside the cryptography-corpus distribution and emits no verdict. When the design or analysis sections carry no formula, notation, or definition at all, the report says so and the author records the reason.
- The body carries a section titled "Ethics considerations" and a section titled "Open science", each immediately preceding the References, and neither was carried over from a previous cycle's wording.
- The body fits the current USENIX limit — the call's body page count plus the one extra page the policy allows for those two sections — under the unaltered template, with no spacing or margin tricks. The number comes from the dated snapshot, never from this file.
- The overview function is present in one of the two permitted forms and carries the full constituent checklist.
- The disclosure thread states rate limits and opt-out handling in the methodology, and when and how each flaw was reported at the point it is introduced.
- Strong verbs carry their measurement, non-goals are named as concretely as goals, and figures read on their own.
- No AI-flavor prose remains (the de-AI checklist is owned by `crypto-venue-paper-writing`).

## USENIX-specific checks

The shared gates are invoked from `ccs-writing-style/references/compression-and-expansion-gates.md`; what follows are the checks this skill owns, each USENIX-only. Their evidence is in the table above, and their detail sections are in [compression-and-expansion-gates.md](references/compression-and-expansion-gates.md) and [section-budget.md](references/section-budget.md).

- **Adversary statement.** Stated once, in one place, in prose — parties and trust assumptions, then capabilities, then what is not guaranteed. Placement is the author's choice; this venue's standalone-section share is the lowest but one of the four. A draft that states it inside the system overview and grants every capability the evaluation uses has not failed; a draft whose model drifts from the evaluation has, wherever the heading sits.
- **Two mandated sections.** A section titled "Ethics considerations" and a section titled "Open science", each immediately preceding the References, in the main body or in the extra page the policy provides — a policy obligation verified against the current call, never sized from the literature.
- **Budget.** Read the current call, date the snapshot, and take the body page count and the extra page for those two sections from it. Never compress to a sibling venue's limit and never measure an author's ePrint copy against any limit.
- **Overview form.** Either an independent section or an overview subsection or named paragraph inside the introduction — this venue's corpus share of the independent form is why the embedded form is permitted here, and the constituent checklist still binds wherever the overview lives.
- **Disclosure narrative.** Rate limits and opt-out handling in the scan methodology paragraph; when and how a flaw was reported at the point the flaw is introduced.
- **Adaptive posture.** A defense measured only against the attack it was designed to stop is a standing limitation, and adaptive-attacker discussion is rare in the literature — the absence is what a reviewer notices.
- **Subsection share.** The family gate's diagnostic flag, owned by `ccs-writing-style`, with relocation that moves material and its claim-status wording rather than deleting it.

## Failure Modes

- Threat model missing or shifting between model and evaluation: stop and reconcile before revising prose.
- Abstract or contributions over their measured bounds, or under them while most words report analysis: run the condensation counts instead of judging by feel.
- Contributions restating the abstract, or a threat model restating the contributions: report the two Jaccard values and the shared spans with their lines.
- Technical overview missing components at USENIX: the embedded form is allowed, the components are not — run the overview gate and name each absent component.
- Design section thinner than its analysis section, or missing required constituents: run both expansion gates; passing one does not excuse the other.
- No float anywhere, an unresolvable `\ref`, or a related-work region with no citation key: run the three evidence gates the family owner declares — `Gate-Expand-Float-Floor`, `Gate-Expand-CrossReference-Integrity`, `Gate-Expand-Citation-Density` — because a paper whose only apparatus is prose passes every word-count gate and still fails these.
- Formal regions with no formula, notation, or definition at all: **manual self-check item** — record the count and the reason in the report; do not import the cryptography family's density number.
- Marketing or false modesty: rewrite with quantified hedging; a real result buried in modesty is as damaging as an overclaim.
- Live harm potential described without a responsible-conduct thread: add the disclosure narrative at the point of need.
- Ethics or open-science section missing, misplaced before the references, or carried over from a previous cycle's wording: read the current call and fix the placement.
- USENIX page budget or template may have changed since training: verify the current official call before any budget claim.
- De-identification gap: anonymize names publicly attached to the group at submission time.

## Workflow

1. Verify the current call and template; record a dated policy snapshot carrying the ethics and open-science requirements and the page budget, and take the budget numbers from that snapshot rather than from this skill.
2. Fix the threat model and non-goals early (a standalone section, the system overview, or the background, as the draft allows); state the measurement vantage and validity.
3. Condensation count pass — invoke the family condensation gates from `ccs-writing-style/references/compression-and-expansion-gates.md` and report the counts the instrument prints, before and after together.
4. Expansion count pass — invoke the family expansion gates over the overview and the design section and report each component present with its line or absent, plus the mass ratio with its declared basis.
5. Evidence-apparatus pass — from the skill-suite root (`cd skills-work/crypto-research-agent-skills`, the root every command in this skill assumes), `python3 skills/ccs-writing-style/scripts/count_prose_gates.py evidence PAPER.md --related-work-heading "Related Work"`, reporting each row with the basis it prints. The instrument prints its exit-code contract with the report, and a measurement failure means no verdict may be read. **That selector reads markdown headings, so the command above is run on the markdown twin; on a LaTeX file it matches nothing and the run reports `degenerate` rather than a verdict — a limitation of the selector, never a prose failure.**
6. Revise against a per-section budget; move overflow to appendices with forward references, never by template tricks, and re-run the cross-reference gate afterwards so the relocated material stays reachable.
7. Calibrate every strong claim: hunt the adjective list and attach numbers or delete; strip process narration and planning-register identifiers.
8. Weave the disclosure narrative into the methodology and the vulnerability discussion.
9. Check the ethics and open-science sections exist, are titled as the policy requires, and sit immediately before the references.
10. Run the adversary-consistency, calibration, cold-reader and caption passes.
11. Run the de-AI grep checklist; fix every hit or record a waiver.
12. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: threat-model precision verdict and evaluation-consistency check; the family gate report with the instrument's printed counts and bases (condensation, expansion, evidence apparatus, formal content with the author's recorded reason); calibrated claim table with rewrites; disclosure-thread report (present at point of need, or gaps); ethics and open-science section placement check; per-section page usage versus budget with overflow routing; dated policy snapshot; unresolved items for the human author.

## Reference Files

| File | Contents |
|------|----------|
| `references/compression-and-expansion-gates.md` | The pointer table: which family gate to invoke from `ccs-writing-style`, and what USENIX adds to each |
| `references/section-budget.md` | Page budget table, calibration examples, register and revision-pass notes, the mandatory ethics and open-science sections |
| `references/evaluation-scenarios.md` | Test specifications for independent evaluation |
