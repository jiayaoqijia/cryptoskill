---
name: handoff-artifact
domain: collaboration/handoff-artifact
trigger: "Write a handoff; hand this off; so someone else can pick this up; what should I pass on; write a shift report"
anti_trigger: "Resuming handed-off work and verifying it (subskills/resumption-check.md); deciding what to pass and what to leave out (subskills/context-selection.md); auditing a finished handoff (subskills/quality-bar.md)"
scope: "What a handoff document contains: state capsule (done / doing / next), decisions with rationale, open questions, artifact pointers; SBAR and I-PASS anchors; the one-read test"
status: "seedling"
---

# Handoff Artifact

## Standard

- **IHI, "SBAR Tool"**: Situation, Background, Assessment, Recommendation; the clinical structure for a transfer that must land on first contact. <https://www.ihi.org/resources/tools/sbar-tool-situation-background-assessment-recommendation> ⚠️ AHRQ's TeamSTEPPS page teaches the same structure but blocked automated fetch; cited without a URL.
- **Starmer et al., "Changes in Medical Errors after Implementation of a Handoff Program", NEJM (2014)**: the I-PASS program — illness severity, patient summary, action list, situation awareness and contingency planning, synthesis by receiver; the study reports roughly one quarter fewer medical errors after adoption. <https://www.nejm.org/doi/full/10.1056/NEJMsa1405556> ⚠️ paywalled; program site: <https://www.ipasshandoffstudy.com/>
- **Gawande, The Checklist Manifesto (2009)**: structure beats memory under load; a written artifact carries what a rushed mind drops. ⚠️ cited without URL.
- House line: the one-read test. A stranger reads the artifact once and can state done, doing, and next.

## Decision rules

1. Lead with state, not narrative: the first lines answer "where does this stand".
2. Every next item gets an owner and a first step; "continue as before" fails.
3. A decision carries a one-line rationale wherever a resumer could reasonably reverse it.
4. An open question carries the current best guess, so work continues while it is open.
5. Pointers, not pastes: name the artifact and its exact location.
6. Dead ends are recorded with one line of why; a resumer who repeats one pays twice.
7. Contingencies follow I-PASS: for each live risk, "if X, do Y".

## Procedure

1. Write the situation line: one sentence saying why this handoff exists and what is live.
2. Build the state capsule. Done: each item with its evidence. Doing: the exact state in flight. Next: ordered, each with a first step.
3. List decisions: the decision, one line of rationale, what it constrains downstream.
4. List open questions: question, best guess, who or what can unblock.
5. Point to artifacts: exact names and locations for plans, data, drafts, and logs.
6. Record dead ends: what was tried and ruled out.
7. Add contingencies for live risks: trigger, action, owner.
8. Read it once as a stranger. If done, doing, or next cannot be restated, fix the gap before sending.

## Anti-patterns

- **Transcript dump.** The resumer mines state from a wall of history. Fix: capsule first; history behind a pointer.
- **Resume-style status.** "Made great progress on X" names no state. Fix: done, doing, next with evidence.
- **Next with no first step.** "Finish the report" cannot be started. Fix: name the opening action and where it happens.
- **Pointer rot.** Artifacts named without locations. Fix: exact paths, verified live.
- **Decisions without rationale.** The resumer re-litigates or silently reverses them. Fix: one line of why.

## Done checklist

- [ ] Situation line present.
- [ ] Done / doing / next capsule written; done items carry evidence, next items carry first steps.
- [ ] Decisions listed with one-line rationale and constraints.
- [ ] Open questions carry best guess and unblocker.
- [ ] Artifact pointers exact and live.
- [ ] Dead ends and contingencies recorded.
- [ ] One-read test passed.

## Sources

- IHI, "SBAR Tool": <https://www.ihi.org/resources/tools/sbar-tool-situation-background-assessment-recommendation>
- Starmer et al., NEJM 2014: <https://www.nejm.org/doi/full/10.1056/NEJMsa1405556> ⚠️ paywalled; I-PASS program: <https://www.ipasshandoffstudy.com/>
- Gawande, The Checklist Manifesto (2009). ⚠️ cited without URL.

⚠️ The I-PASS error-reduction figure is single-study evidence from one clinical setting; treat it as support for structure, not a guaranteed effect size.
