---
name: resumption-check
domain: collaboration/resumption-check
trigger: "Resume from this handoff; pick this up; verify what I was told before acting; the handoff says done but it is not; the handoff looks stale"
anti_trigger: "Writing the handoff artifact (subskills/handoff-artifact.md); deciding what was passed (subskills/context-selection.md); closing a shift with an acknowledgment (subskills/person-handoff.md)"
scope: "Consumer side: verify state before acting, reconcile drift, confirm freshness, ask versus assume; never act on a stale handoff"
status: "seedling"
---

# Resumption Check

## Standard

- **Starmer et al., NEJM (2014) / I-PASS**: synthesis by receiver; the receiver restates the state in their own words before taking over, and the read-back is part of the handoff, not a courtesy. <https://www.ipasshandoffstudy.com/>; <https://www.nejm.org/doi/full/10.1056/NEJMsa1405556> ⚠️ paywalled.
- **IHI, "SBAR Tool"**: the recommendation step is only as good as the receiver's confirmed reading of the situation. <https://www.ihi.org/resources/tools/sbar-tool-situation-background-assessment-recommendation>
- **Sun et al. (2026), arXiv:2608.24569**: a successful endpoint can conceal a damaged handoff; verify the artifact, not just the result. <https://arxiv.org/abs/2608.24569>
- **Ganz et al. (2026), arXiv:2608.24358**: continuing a non-native trajectory is lossy; assume the record is incomplete and check it against ground truth. <https://arxiv.org/abs/2608.24358>

## Decision rules

1. Verify before acting: the first action is a check, never the handoff's first next step.
2. Reconcile every claim against ground truth; a done item is done when its artifact shows it.
3. Freshness first: compare the handoff's timestamp against the artifacts' latest changes.
4. Drift found, work stops: list the discrepancies; repair, ask, or proceed with the gap recorded, never silently fixed.
5. Omission is not permission: a rule missing from the handoff is unknown, not allowed.
6. When the handoff contradicts reality, reality wins; the correction is written down, not implied.
7. Ask versus assume: a question costs minutes; a wrong assumption re-does finished work.

## Procedure

1. Locate the handoff and every artifact it points to. A missing target is drift; note it.
2. Check freshness: handoff timestamp versus artifact modification times.
3. Walk the state capsule: verify each done claim, locate each doing item, confirm each next step's precondition still holds.
4. Re-read the constraint block: state in one line what each rule requires or forbids; any rule you cannot restate is a gap.
5. Read back: restate done, doing, next, and the constraints in your own words; hand the read-back to the sender or its owner, or file it if no sender remains.
6. List discrepancies and resolve each: repair with a record, ask the sender, or proceed with the gap visible in your own ledger.
7. Start work only from the first next action whose precondition verified.

## Anti-patterns

- **Trust-first resumption.** Acting on "done" without checking. Fix: verify first, act second.
- **Silent repair.** Fixing drift without recording it, so the sender never learns. Fix: discrepancy list.
- **Assumed freshness.** No timestamps compared; the handoff may describe last week. Fix: compare before acting.
- **Reading as agreement.** A skim, then "got it". Fix: read-back in your own words.
- **Proceeding on gaps.** An artifact is missing, so improvise. Fix: ask, or record the gap and choose with it visible.

## Done checklist

- [ ] Handoff and all pointed artifacts located; missing targets recorded.
- [ ] Freshness verified against artifact timestamps.
- [ ] State capsule verified item by item against ground truth.
- [ ] Constraints restated as a binding-state check.
- [ ] Read-back delivered or filed.
- [ ] Discrepancies resolved or explicitly carried.

## Sources

- I-PASS program: <https://www.ipasshandoffstudy.com/>; Starmer et al., NEJM 2014: <https://www.nejm.org/doi/full/10.1056/NEJMsa1405556> ⚠️ paywalled.
- IHI, "SBAR Tool": <https://www.ihi.org/resources/tools/sbar-tool-situation-background-assessment-recommendation>
- Sun et al. (2026), arXiv:2608.24569: <https://arxiv.org/abs/2608.24569>
- Ganz et al. (2026), arXiv:2608.24358: <https://arxiv.org/abs/2608.24358>

⚠️ Read-back is validated in clinical settings; evidence in software teams is thinner, and the procedure borrows the mechanism rather than a measured effect size.
