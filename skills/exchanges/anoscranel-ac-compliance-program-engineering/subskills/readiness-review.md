---
name: readiness-review
domain: security-hardening/readiness-review
trigger: "Reproducing the audit internally before the auditor arrives."
anti_trigger: "Not for the real audit, and not for the findings response."
scope: "Reproducing the audit internally before the auditor arrives."
status: seedling
---

# Readiness review

## Standard

A readiness review is the audit rehearsed internally: pick the controls, sample the period exactly as an auditor would, request the same evidence, and score the findings honestly. Its value is measured by what it surfaces early: the control that stopped running in March, the manual record nobody filed, the policy sentence whose system drifted. Every finding here is cheap; the same finding during the real audit is expensive, and in an attestation report it is public to customers.

The review is adversarial by design. A readiness review that passes everything it samples has either sampled nothing hard or scored generously, and the real audit will find what the rehearsal chose not to. The honest readiness review samples the controls with known fragility first, records every failure at finding severity without smoothing, and produces a remediation queue with owners and dates — it is the diff between the compliance program you believe you have and the one the evidence supports.

Primary sources: <https://www.isaca.org/resources/isaca-journal/issues/2020/volume-1> and <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2>.

## Decision rules

- Sample as an auditor would: random dates across the period, requested evidence sight-unseen.
- Score at audit severity; generous scoring only defers findings to the public report.
- Prioritise sampling the controls with known fragility over a random tour.
- Include the freshly built and recently changed controls; newness is a risk factor.
- Each finding gets an owner, a remediation date, and a re-test commitment.
- Run the review far enough before the audit window that remediation can actually complete.

## Procedure

1. Choose the control sample from the mapping, weighted toward fragile and new.
2. Pull evidence for random dates without pre-checking.
3. Score each against the policy sentence and the framework's expectation.
4. Write findings at audit severity, with the gap described factually.
5. Assign owners and dates; commit remediation as engineering work.
6. Re-test remediated controls in a follow-up pass before the real audit.

## Anti-patterns

- The readiness review as celebration rather than rehearsal.
- Sampling dates known to have good evidence.
- Findings softened to "observations" for internal comfort.
- Running the review two weeks before the audit, making remediation impossible.
- Discovering at the real audit a control the readiness review never sampled.

## Done checklist

- [ ] Sample weighted for fragility, includes new controls.
- [ ] Random-date pulls, sight-unseen.
- [ ] Findings scored at audit severity.
- [ ] Owner and date per finding.
- [ ] Timing allows remediation.
- [ ] Re-test pass completed.

## Sources

- Attestation readiness practice: <https://www.isaca.org/resources/isaca-journal/issues/2020/volume-1>
- SOC 2 process: <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2>
- Control families: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
