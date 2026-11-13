---
name: evidence-from-the-pipeline
domain: security-hardening/evidence-from-the-pipeline
trigger: "Making control evidence a by-product of the running system."
anti_trigger: "Not for log design, and not for the audit sampling plan."
scope: "Evidence as a by-product of normal operation, sampled not staged."
status: seedling
---

# Evidence from the pipeline

## Standard

An auditor asks: show me this control operating over the audit period. The strong answer is a query over records the system produced in the normal course of operation — access reviews logged when they ran, change tickets with approvals attached, onboarding records with the training completion timestamped. The weak answer is a document assembled for the audit, undated or dated last week, describing what the control would do. The first reads as an operating control; the second reads as a finding.

Making evidence automatic is therefore an engineering investment with a compliance return. A periodic access review whose results are written to a known location produces evidence as a side effect; a backup whose restore is tested on a schedule produces restore logs no one had to remember to save. Wherever a control's operation is a manual act, the record of that act belongs in the same place every time — a checklist is not evidence, but a signed, dated record stored at a known path is.

Primary sources: <https://www.isaca.org/resources/isaca-journal/issues/2020/volume-1> and <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>.

## Decision rules

- Evidence is produced continuously and stored centrally; audits sample it.
- Every control from the mapping names where its evidence lives before the audit needs it.
- Manual steps write their record at the moment they happen, not monthly in batch.
- Evidence retains timestamps and actor identity from the producing system.
- Evidence gaps over the audit period are surfaced early, not excused at review.
- Where a control cannot produce machine evidence, the manual record's format is fixed in advance.

## Procedure

1. Walk the control mapping; for each pipeline-located control, name the evidence artefact.
2. Confirm the artefact is already written by normal operation; if not, build that.
3. Centralise where audits will look, keeping original timestamps.
4. For manual controls, define the record format and storage path.
5. Run an evidence dry-run: pick random dates across the period and reconstruct.
6. Fix controls whose dry-run finds nothing, then re-run before the real audit.

## Anti-patterns

- Evidence assembled in the audit window with freshly minted dates.
- Screenshots of dashboards as evidence, with no underlying record references.
- Evidence kept in personal drives or inboxes that permissions changes will strand.
- Manual records backfilled monthly from memory.
- Controls whose evidence exists only for the sampled dates because production is inconsistent.

## Done checklist

- [ ] Each control's evidence artefact named in the mapping.
- [ ] Artefacts written by normal operation, not by audit prep.
- [ ] Central storage with original timestamps and actors.
- [ ] Manual record formats fixed.
- [ ] Random-date reconstruction dry-run passed.
- [ ] Fix loop completed before the real audit.

## Sources

- Evidence practice commentary: <https://www.isaca.org/resources/isaca-journal/issues/2020/volume-1>
- Control-families context: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- SOC 2 attestation model: <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2>
