---
name: harness-record
domain: software-engineering/harness-record
trigger: "Writing and reviewing the record of harness runs and ship decisions."
anti_trigger: "Not for the ship decision itself, and not for production incidents."
scope: "The written record: coverage, results, and the ship/no-ship decision."
status: seedling
---

# Harness record

## Standard

The harness record documents what was tested, what the run found, and what shipped despite: scenario-set version and its provenance, assertion map with invariants and tolerances, per-run results with failure classifications and variance annotations, flaky tolerances with defined pass thresholds, and finally the ship/no-ship decision with the reasoning attached.

The reasoning attachment is what the record is for. The binary proclaims a verdict, and the record shows the picture: failed scenarios at each priority, dismissed findings with links to evidence, the impact of nondeterministic tolerance on agent quality over time. A ship decision made without a record is no decision — the next engineer cannot tell what the harness run represented, and so cannot tell whether recurrence means the same defect.

Primary sources: <https://osf.io/prereg/> and <https://testing.googleblog.com/>.

## Decision rules

- Record scenario-set version and its trace provenance.
- Per-run: pass/fail/flaky per scenario with assertion-layer failures broken out.
- Every skip and drop carries its reason and re-entry condition.
- A variance tolerance applied must state the threshold and the observed stability.
- The ship/no-ship entry links its reasoning: failures dismissed need evidence links.
- A record that cannot say what was NOT covered is not a record.

## Procedure

1. Record the scenario-set version and provenance.
2. Run the suite; log per-scenario result and failure classification.
3. Attach variance annotations for flaky-classified scenarios.
4. Document coverage: scenario count by category, untested surfaces by name.
5. Write the ship/no-ship decision with dismissals linked to evidence.
6. Save to record; the next run's record starts fresh, never entering prior without link.

## Anti-patterns

- "All green" without scenario-class weights.
- A ship decision with no reasoning attached.
- Skipped scenarios without reason or re-entry date.
- Only the failures documented — passes matter for coverage weight too.
- Editing prior records to retroactively align with the current run.

## Done checklist

- [ ] Scenario-set version with provenance recorded.
- [ ] Per-scenario outcome and classification logged.
- [ ] Variance annotations attached.
- [ ] Coverage with untested surfaces named.
- [ ] Ship/no-ship reasoning linked to evidence.
- [ ] Next record fresh-linked, not edited.

One number belongs at the top of every record line: the ratio of scenarios exercised to production task volume since the last run. A suite of two hundred scenarios against three months of traffic is a statement about coverage that honest readers need, and hiding it behind a raw count is the reporting failure this record exists to prevent.

## Sources

- Preregistration discipline: <https://osf.io/prereg/>
- Google testing blog: <https://testing.googleblog.com/>
- Test record craft: <https://en.wikipedia.org/wiki/Software_testing>
