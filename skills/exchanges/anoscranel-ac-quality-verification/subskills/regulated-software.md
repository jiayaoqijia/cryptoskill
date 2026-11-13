---
name: regulated-software
domain: software-engineering/regulated-software
trigger: "\"medical device software\", \"write the design history file\", \"IEC 62304 evidence\", \"DO-178C objectives\", \"auditor wants the trace matrix\"."
anti_trigger: "General quality attributes and the V&V plan (subskills/quality-vv.md); security controls and threat models; delivery metrics and SLOs; general release governance."
scope: "Lifecycle evidence for regulated domains: IEC 62304, DO-178C, regulated agile"
status: "seedling"
---

# Regulated Software

## Standard

- **IEC 62304:2006+AMD1:2015** (edition 1.1, 2015-06-26) is current, stability date 2028. Edition 2 is NOT published: the IEC webstore shows stage ACD (see Sources). ⚠️ Sites claiming a 2026 publication are wrong.
- **Safety classes A/B/C** (edition 1.1): Class A documents requirements and release; Class B adds architecture and traced verification; Class C adds detailed design and full verification. Classification is risk-based.
- **DO-178C** is objectives-based: 71 objectives at DAL A, 30 needing independence. Verification independence is personal, not phasic: the verifier may not be the author.
- **AAMI TIR45:2023** is the FDA-recognized consensus guide for agile device software (no. 13-143): agile operates inside the QMS, never around it.
- **Standards demand evidence, not sequence.** Neither names a process model; 62304 Annex B allows iteration.

## Decision rules

1. Agile is permitted. The Definition of Done carries the evidence, or compliance debt accrues.
2. The audit answer is the requirement, the test, the result, the reviewer.
3. Independence is enforced per artifact: an approver never authored their own record.
4. The audit answer is a pipeline artifact, never a screenshot assembled that week. SOUP needs a register entry, in-context verification, change control per bump, and advisory monitoring; the release SBOM doubles as the inventory.
5. Any compliance or certification claim is **human-gated**. The agent drafts evidence; a human attests.
7. ⚠️ Lightweight-agile-efficacy claims are community/vendor rung; TIR45, ZVEI and DoD patterns lift them to reputable practice, but no head-to-head outcome data exists.

## Procedure

1. Identify the standard, edition and classification. Record all three.
2. Set the rigor level: Class A/B/C or the DAL, and write the objective list.
3. Map each artifact to a pipeline output: build log, test report, review record, SBOM, and write the trace matrix: requirement → design → test → result (subskills/quality-vv.md).
4. Put evidence capture in the Definition of Done: test cases link to requirement ids; results retained and dated; runner config versioned; failures route through problem resolution. Enforce reviewer ≠ author in the review gate (out of scope for this leaf: review-gate rules).
5. Register SOUP: component, version, verification basis, change-control rule per bump, and qualify tools that carry verification credit.
6. Rehearse the audit: pull one requirement end to end — spec, commit, test, result, reviewer. Route retro actions to CAPA tracking.

## Anti-patterns

- Evidence reconciled in audit week instead of produced per build.
- An author signing their own verification record.
- SOUP upgraded with no register change.
- An audit package with no requirement-to-test chain.
- Citing an edition that is not published.

## Done checklist

- [ ] Standard, edition and classification recorded.
- [ ] Objective list written with independence requirements.
- [ ] Trace matrix current and bidirectional.
- [ ] Reviewer ≠ author enforced per artifact.
- [ ] SOUP register, change control, and tool qualification evidence.
- [ ] Human attested any compliance claim.

## Sources

- <https://meddeviceguide.com/blog/agile-vs-waterfall-medical-device-software-iec-62304-design-controls-guide>
- <https://www.iec.ch/functionalsafety>
- <https://webstore.iec.ch/en/publication/22794> (IEC 62304 status)
