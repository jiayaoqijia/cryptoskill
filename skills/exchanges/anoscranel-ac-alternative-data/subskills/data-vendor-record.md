---
name: data-vendor-record
domain: investing/data-vendor-record
trigger: "Writing the record of a dataset evaluation and its limits."
anti_trigger: "Not for certifying a dataset, and not for procurement approval."
scope: "The written record: source, tests passed, limits, and review dates."
status: seedling
---

# Data vendor record

## Standard

The vendor record states the dataset, its provenance, which integrity tests it passed and which it failed, the coverage limitations, the licensing constraints, and the review dates. It is written so that a decision made with the data can be reconstructed later, and so that a dataset's suitability is a recorded finding rather than a recollection.

The record also carries the known failure modes and their consequences. A dataset that is reconstructed rather than point-in-time can still be used for description, just not for backtesting; one whose licence forbids redistribution can support internal research but not external reporting. Stating the permitted uses beside the limitations is what prevents a dataset from being quietly reused in a context it does not support.

Primary sources: <https://www.sec.gov/investor> and <https://osf.io/prereg/>.

## Decision rules

- The record states the dataset, the vendor, and the acquisition date.
- Provenance and point-in-time findings are recorded separately.
- Coverage limitations are recorded with the comparison used.
- Licensing constraints are recorded with the permitted uses.
- The review date is set, since coverage and licensing change.
- Uses for which the dataset is not suitable are stated explicitly.

## Procedure

1. Record the dataset and acquisition.
2. Record provenance and integrity findings.
3. Record coverage limitations.
4. Record licensing and permitted uses.
5. State the unsuitable uses.
6. Set the review date.

## Anti-patterns

- Recording a verdict without the tests behind it.
- Omitting the unsuitable uses, which is the field that prevents misuse.
- Treating the licence as settled at acquisition.
- No review date, so a changed dataset is used under an old assessment.
- Recording coverage without the comparison that established it.

## Done checklist

- [ ] Dataset and acquisition recorded.
- [ ] Integrity findings recorded.
- [ ] Coverage limitations recorded.
- [ ] Licensing recorded with permitted uses.
- [ ] Unsuitable uses stated.
- [ ] Review date set.

The record should also name the person who performed the evaluation and the date, because dataset assessments age quickly and a later reader needs to know whether the finding reflects the current vendor terms and coverage or an earlier version of them.


The record should also distinguish the tests that were run from the tests that exist, since a dataset that passed the four checks performed is not the same as one that passed the twelve that could have been performed, and the difference is invisible unless the untested list is kept.


## Sources

- Data and disclosure context: <https://www.sec.gov/investor>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Investor education on data use: <https://www.investor.gov/introduction-investing>
