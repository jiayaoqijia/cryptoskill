---
name: findings-and-remediation
domain: security-hardening/findings-and-remediation
trigger: "Closing an audit finding at the cause."
anti_trigger: "Not for disputing findings, and not for the re-audit contract."
scope: "Closing a finding at the cause, with the re-test to prove it."
status: seedling
---

# Findings and remediation

## Standard

A finding is a labelled gap between a control's claim and its operation. Closing it means changing the system so the gap cannot recur, which is different from making the finding disappear: a re-run access review closes nothing if the review job's defect is still there, and a policy edit softening the requirement moves the gap into next period's report. The remediation question is always: what in the pipeline, owner, or policy permitted this, and what change removes that permission?

Evidence of closure is the re-test. After the change lands, the same sampling that produced the finding is reproduced over a post-change window, and the clean result — with the artefact timestamps to prove the window — is the closure package. A finding closed without a re-test is an assertion; most frameworks require exceptions to show the control operating after remediation, and the assertion without evidence simply relabels the finding.

Primary sources: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final> and <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2>.

## Decision rules

- Root-cause before fix: pipeline defect, missing owner, or policy-system drift.
- Fix at the cause; the cosmetic fix reopens at the next period.
- Closure evidence = re-test window + artefacts; assertion-only closure is not closure.
- Policy edits as remediation must tighten the system or honest the sentence, never quietly lower the bar.
- Each finding dated from discovery to closure in the record; aging visible.
- Repeat findings escalate: a second occurrence is a program defect, not an accident.

## Procedure

1. Reproduce the finding from the evidence to confirm the gap is real, not a sampling artefact.
2. Classify the cause: pipeline defect, ownership gap, or policy drift.
3. Fix the cause; schedule the change like any other engineering work.
4. Define the re-test window and sampling mirroring the original.
5. Run the re-test and capture the artefacts with timestamps.
6. Record closure with cause, fix, and re-test evidence; escalate repeats.

## Anti-patterns

- Access review run 40 times in a week to paper one missed quarter.
- Policy softened where the system should have been fixed.
- Closure claimed at fix-merge, before any re-test evidence exists.
- Findings closed by the owner who failed the control, unchecked.
- Repeat findings treated as new incidents each time.

## Done checklist

- [ ] Finding reproduced before fixing.
- [ ] Cause classified.
- [ ] Fix at cause, scheduled as engineering work.
- [ ] Re-test window mirroring original sampling.
- [ ] Artefacts captured with timestamps.
- [ ] Repeat occurrence escalated as program defect.

## Sources

- Control remediation context: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- Attestation and exceptions: <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2>
- Findings practice: <https://www.isaca.org/resources/isaca-journal/issues/2020/volume-1>
