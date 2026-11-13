---
name: compliance-record
domain: security-hardening/compliance-record
trigger: "Writing the record of the whole compliance program."
anti_trigger: "Not for the audit report itself, and not for legal opinions."
scope: "The written record: scope, mappings, evidence index, findings, dates."
status: seedling
---

# Compliance record

## Standard

The compliance record holds the program's whole state: the scope statement with its framework edition, the control-to-owner mapping, the evidence index with each artefact's location, the policy version history, the readiness-review findings with their remediation status, and the dated trail of every audit, letter, and customer request. It exists so the program's continuity does not depend on the memory of whoever ran the last audit window — teams change, auditors change, and the record is what makes year three cheaper than year one.

Its second function is drift detection. Because scope, mapping, policies, and findings are all in one place with dates, the record shows the program's true direction: controls whose owners changed three times, evidence locations that moved, findings that recurred. The review that reads this record finds the weak rows before the auditor does, and the record's completeness is itself a control — an auditor who cannot trace the program's history writes a finding about the program, not about a single access review.

Primary sources: <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2> and <https://osf.io/prereg/>.

## Decision rules

- The record holds scope, mapping, evidence index, policy history, findings, and correspondence — with dates on everything.
- One evidence index entry per control, pointing at the pipeline artefact, not the copies.
- Findings tracked from discovery to closure with the re-test evidence attached.
- Every audit, readiness review, and customer request is a dated entry.
- Append-only; a corrected entry references the one it replaces.
- The record is reviewed on the same cadence as the readiness review, before the audit.

## Procedure

1. Assemble the six sections from the program's existing artefacts.
2. Date every entry that lacks one; undated entries are gaps.
3. Cross-check the evidence index against the mapping — every control, one index row.
4. Attach findings' closure evidence; close the loop per finding.
5. Review before audit windows; note owner changes and recurring findings.
6. Amend — never overwrite — when facts change.

## Anti-patterns

- The record as a folder of exports nobody can trace.
- Evidence index pointing at copies rather than the producing artefact.
- Findings without closure evidence attached.
- Owner changes invisible — three owners in two years reads as stable.
- The record assembled fresh for each audit rather than maintained between them.

## Done checklist

- [ ] Six sections assembled and dated.
- [ ] Evidence index mapped one-to-one to controls.
- [ ] Findings carry closure evidence.
- [ ] Correspondence and audits logged with dates.
- [ ] Record reviewed before each audit window.
- [ ] Append-only with reference-style amendments.

## Sources

- SOC 2 attestation: <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2>
- Stated-record discipline: <https://osf.io/prereg/>
- Control-families context: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
