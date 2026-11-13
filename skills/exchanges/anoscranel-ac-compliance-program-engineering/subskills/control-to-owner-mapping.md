---
name: control-to-owner-mapping
domain: security-hardening/control-to-owner-mapping
trigger: "Mapping every framework control to a named owner and pipeline."
anti_trigger: "Not for implementing the control, and not for the audit itself."
scope: "Every control mapped to a named engineer and its pipeline."
status: seedling
---

# Control-to-owner mapping

## Standard

A framework's control list is a spreadsheet that ends up orphaned unless each row acquires two artefacts: a named human owner who is accountable for the control operating, and a place in the engineering pipeline where the control actually lives. "Access is reviewed periodically" maps to a named owner, and to the specific review job, its frequency, its record location, and its output. A control with an owner but no pipeline address is an intention; with a pipeline address but no owner it decays at the first reorganisation.

The mapping also drives evidence: when the control has a pipeline home, the evidence of operation is the job's own records, and collection is a matter of pointing at them. When a control cannot be given a pipeline home — executive sign-off, annual policy acknowledgement — the mapping names the manual step, where its record lands, and who substitutes when the named owner is on leave. The audit samples controls; the mapping is why a sample finds an operating control instead of a discovered gap.

Primary sources: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final> and <https://www.isaca.org/resources/isaca-journal/issues/2020/volume-1>.

## Decision rules

- Each control row acquires: owner, pipeline address (or the recorded manual step), and evidence location.
- Owner is a named engineer, not a team alias; aliases orphan at reorganisation.
- Controls without pipeline homes are explicitly marked manual, with the record path named.
- The mapping is reviewed when the org chart changes, not at audit time.
- Different frameworks' overlapping controls map once, with cross-references, not twice.
- Gap rows — control required but not operating — are visible findings, not hidden.

## Procedure

1. Export the framework's control list from the current edition.
2. For each control, locate the pipeline artefact that implements it, or record manual.
3. Name an owner per control; check against the org chart for real names.
4. Record the evidence each pipeline artefact produces and where it lives.
5. Cross-reference controls shared across frameworks.
6. Flag gap rows and drive remediation before the audit samples them.

## Anti-patterns

- Owner set to a team name or a departed founder's email.
- Control list kept in a spreadsheet that no CI change ever touches.
- Mapping done during the audit window, discovering gaps live.
- The same control mapped twice under different wording across frameworks.
- Gap rows softened to look compliant in the mapping document.

## Done checklist

- [ ] Every control has an owner and address.
- [ ] Manual controls branded and record-pathed.
- [ ] Org-chart review scheduled.
- [ ] Cross-framework duplicates referenced.
- [ ] Gaps flagged rather than reworded.
- [ ] Evidence locations named per control.

## Sources

- Control catalogue for mapping: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- Governance practice commentary: <https://www.isaca.org/resources/isaca-journal/issues/2020/volume-1>
- SOC 2 framework: <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2>
