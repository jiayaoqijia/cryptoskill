---
name: quality-checks-at-the-boundary
domain: software-engineering/quality-checks-at-the-boundary
trigger: "Validating a dataset when it arrives rather than after it propagates."
anti_trigger: "Not for profiling an unfamiliar dataset, and not for model evaluation."
scope: "Validating on ingest rather than discovering defects downstream."
status: seedling
---

# Quality checks at the boundary

## Standard

A defect discovered downstream has already propagated: it sits in a table, a dashboard, a model, and possibly a decision. A defect caught at the boundary stops at the point of arrival, which is why the checks belong there even though the same check is cheaper to write later.

The checks worth writing are the ones that correspond to a stated guarantee. A null check corresponds to a nullability promise; a range check corresponds to a domain constraint; a row-count comparison corresponds to completeness; a referential check corresponds to a stated relationship. Checks written without a guarantee behind them accumulate as noise, and a suite that fires false positives is one that gets muted.

Primary sources: <https://csrc.nist.gov/> and <https://www.w3.org/>.

## Decision rules

- Record each check and the contract term it enforces.
- Record the check's severity: block the load, quarantine the row, or alert.
- Record the quarantine path, since a blocked row must go somewhere.
- Record the false-positive history, since a check that fires wrongly is muted.
- Record the check's cost, because a full scan on every batch may not be affordable.
- Record who is notified and what they can do, since an alert without an action is noise.

## Procedure

1. List the contract's guarantees.
2. Write one check per guarantee, recording what it enforces.
3. Assign severity and record the quarantine path.
4. Record the check's cost and how it scales with volume.
5. Record notification and available actions.
6. Review false positives after the first month and record adjustments.

## Anti-patterns

- Checks that enforce no stated guarantee.
- Blocking a load with no quarantine, which discards data.
- Alerts without an action the recipient can take.
- A check whose false positives were never measured.
- Validating only samples when the defect is rare and consequential.

## Done checklist

- [ ] Checks mapped to guarantees.
- [ ] Severity recorded.
- [ ] Quarantine path recorded.
- [ ] Cost recorded.
- [ ] Notification and actions recorded.
- [ ] False positives reviewed.

The check's placement also decides its cost: validating a batch as it arrives is proportional to volume, while validating a table before a query is proportional to the query's scope, and mixing the two produces a system where the expensive check runs on every request and the cheap one runs once.


## Sources

- Data quality and control guidance: <https://csrc.nist.gov/>
- Data standards: <https://www.w3.org/>
- Quality management context: <https://csrc.nist.gov/publications>
