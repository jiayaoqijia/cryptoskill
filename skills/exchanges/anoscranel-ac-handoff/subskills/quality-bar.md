---
name: quality-bar
domain: collaboration/quality-bar
trigger: "Is this handoff good enough; check this handoff before I send it; audit the handoff; the receiver keeps asking questions the document should answer"
anti_trigger: "Writing the artifact's content (subskills/handoff-artifact.md); verifying received work before acting (subskills/resumption-check.md); choosing what to pass (subskills/context-selection.md)"
scope: "The acceptance test: a stranger resumes on one read; the completeness checklist; the living-handoff update protocol; anti-patterns"
status: "seedling"
---

# Quality Bar

## Standard

- **Gawande, The Checklist Manifesto (2009)**: a checklist holds a complex transfer to a standard when attention is thin; the completeness checklist below is that list. ⚠️ cited without URL.
- **Starmer et al., NEJM (2014) / I-PASS**: the acceptance moment is the receiver's synthesis; if the receiver cannot synthesize, the handoff failed regardless of how it reads. <https://www.ipasshandoffstudy.com/>; <https://www.nejm.org/doi/full/10.1056/NEJMsa1405556> ⚠️ paywalled.
- **Ganz et al. (2026), arXiv:2608.24358**: every ambiguity the receiver must resolve is paid downstream; completeness up front is cheaper than re-verification after. <https://arxiv.org/abs/2608.24358>
- **Sun et al. (2026), arXiv:2608.24569**: a clean ending does not prove a clean handoff; the artifact is checked separately from the outcome. <https://arxiv.org/abs/2608.24569>
- House line: the test is resumption, not readability.

## Decision rules

1. Pass means a stranger, one read, no questions: they state done, doing, next, the constraints, and their first action.
2. Any question the artifact could have answered is a defect in the artifact, not in the reader.
3. A paraphrased constraint fails the bar; verbatim is a gate, not a bonus.
4. A dead pointer fails the bar at the moment of handover.
5. The handoff stays current until acknowledged: updates go to the artifact, never to chat alone.
6. Ownership transfers at acknowledgment, and only after the receiver's read-back.
7. Length is not completeness; the one-read budget holds.

## Procedure

1. Cold-read test: a person without context reads the artifact once, then restates done, doing, next, and the constraints, pointing to the lines that carry them.
2. Question audit: every question they ask that the artifact could have answered is a defect; fix and retest.
3. Completeness pass: run the checklist below.
4. Freshness pass: timestamps current, every pointer live.
5. Constraint gate: verbatim block present; binding-state check passed.
6. Send, then keep updating the artifact as facts change until the receiver acknowledges.
7. At acknowledgment: record it, freeze the handoff, transfer ownership.

## Anti-patterns

- **Transcript dump.** History instead of state. Fix: capsule first, history behind a pointer.
- **"LGTM".** An acknowledgment that verified nothing. Fix: read-back before acknowledgment.
- **Dropped constraints.** Compression ate a must. Fix: verbatim block and a binding-state check.
- **Stale handoff.** Reads well, describes last week. Fix: timestamp, freshness pass, update protocol until acknowledgment.
- **Resume-style status.** Achievements with no state. Fix: done, doing, next with evidence.
- **Length as virtue.** A long handoff that fails one read. Fix: cut to the budget; move bulk behind pointers.

## Done checklist

- [ ] Cold-read test passed: a stranger resumes on one read.
- [ ] No question asked that the artifact could have answered.
- [ ] Done / doing / next present with evidence and first steps.
- [ ] Constraints verbatim; binding-state check passed.
- [ ] Pointers live; timestamps current.
- [ ] Update protocol running until acknowledgment.
- [ ] Acknowledgment recorded; ownership transferred.

## Sources

- Gawande, The Checklist Manifesto (2009). ⚠️ cited without URL.
- I-PASS program: <https://www.ipasshandoffstudy.com/>; Starmer et al., NEJM 2014: <https://www.nejm.org/doi/full/10.1056/NEJMsa1405556> ⚠️ paywalled.
- Ganz et al. (2026), arXiv:2608.24358: <https://arxiv.org/abs/2608.24358>
- Sun et al. (2026), arXiv:2608.24569: <https://arxiv.org/abs/2608.24569>

⚠️ The one-read test is a house acceptance test derived from clinical read-back; no public study measures its error rate for document-style handoffs.
