---
name: provenance-and-vendor-claims
domain: investing/provenance-and-vendor-claims
trigger: "Establishing where a dataset came from before using it."
anti_trigger: "Not for predicting returns, and not for pipeline design."
scope: "Where the data came from, and how to test a vendor's assertions."
status: seedling
---

# Provenance and vendor claims

## Standard

Provenance is the chain from the original observation to the delivered file: who collected it, how, with what consent, and what transformations were applied. Each link is a place where the data can change in ways that matter, and a vendor that describes the output without the chain has described a product rather than a dataset.

Vendor claims should be tested rather than accepted. The testable ones are the specific assertions: that the panel covers a stated number of entities over a stated period, that the history is what was available at the time, that the mapping to securities is stable. Each can be checked against a sample, and a vendor that will not supply the sample for checking has answered the question.

Primary sources: <https://www.sec.gov/investor> and <https://www.nber.org/>.

## Decision rules

- Record the original source and the collection method.
- Record the transformations applied and whether any are irreversible.
- Record the entity mapping to securities and how it is maintained.
- Test a sample against the vendor's stated coverage and period.
- Record which claims were tested and which were accepted on assertion.
- Record the vendor's willingness to supply audit samples.

## Procedure

1. Document the chain from observation to file.
2. List the vendor's specific claims.
3. Design a sample test for each testable claim.
4. Run the tests and record the results.
5. Note claims accepted without testing and why.
6. Write the provenance summary.

## Anti-patterns

- Accepting a coverage claim without a sample check.
- Ignoring irreversible transformations that prevent verification.
- Assuming the entity mapping is stable across time.
- Treating a vendor's backtest as evidence about the data.
- Failing to record which claims were never tested.

## Done checklist

- [ ] Source and method recorded.
- [ ] Transformations recorded.
- [ ] Entity mapping recorded.
- [ ] Sample tests run.
- [ ] Untested claims noted.
- [ ] Provenance summary written.

The audit sample request is also the cheapest filter available: a vendor confident in its pipeline will supply one, and a refusal or a delay is information about the dataset rather than about the procurement process.


A useful habit is to record the vendor's own description verbatim alongside the tested findings, so that a later reader can see where the marketing ended and the verification began and can tell which claims were never checked.


## Sources

- Disclosure and data-handling context: <https://www.sec.gov/investor>
- Research methods on data quality: <https://www.nber.org/>
- Investor education on data use: <https://www.investor.gov/introduction-investing>
