---
name: fund-reporting-record
domain: investing/fund-reporting-record
trigger: "Writing the record of a private-fund performance reading."
anti_trigger: "Not for recommending a fund, and not for the manager's report itself."
scope: "The written record: metrics, dates, definitions, and the comparison used."
status: seedling
---

# Fund reporting record

## Standard

The reporting record states the metrics, their as-of date, whether they are gross or net, the valuation basis behind the residual value, the vintage, and the peer comparison with its provenance. Those fields are what allow a later reader to know whether two reports are comparable, and most private-fund misreadings come from comparing figures that were never measuring the same thing.

The record also carries the arithmetic that produced each metric where it can be reconstructed. A TVPI built from a marked-up residual is a different claim from one built from realised distributions, and the difference is invisible unless the components are written down beside the ratio. Stating the components is what makes the multiple auditable rather than assertive.

Primary sources: <https://www.cfainstitute.org/> and <https://osf.io/prereg/>.

## Decision rules

- Record each metric with its definition, date, and gross or net basis.
- Record paid-in, distributed, and residual value as components.
- Record the valuation source and the date of the latest mark.
- Record the vintage and the peer universe with its provider.
- Record the fund's age and deployment percentage.
- Record the unfunded commitment and its share of the portfolio.

## Procedure

1. Record the metrics with dates and definitions.
2. Record the components behind each ratio.
3. Record the valuation source and mark date.
4. Record vintage, universe, and percentile.
5. Record age, deployment, and unfunded.
6. File the record and reference it from any allocation decision.

## Anti-patterns

- Recording a metric without its definition.
- Omitting the gross versus net distinction.
- Leaving the valuation source unstated.
- Recording a percentile without the universe.
- Treating the manager's own report as the record.

## Done checklist

- [ ] Metrics recorded with definitions and dates.
- [ ] Components recorded.
- [ ] Valuation source recorded.
- [ ] Vintage and universe recorded.
- [ ] Age and deployment recorded.
- [ ] Unfunded recorded.

Keeping the record in one place across funds also makes the aggregate visible: a portfolio of ten funds each reporting a strong multiple can still be a portfolio whose combined DPI is low and whose unfunded commitments exceed its liquid assets, and that finding only appears when the records are read together rather than one report at a time.

Finally, the record should state which figures were audited and which were produced by the manager alone. An annual audited net asset value and a quarterly internal mark carry very different weight, and a reader who does not know which is which will treat both as equally firm when only one of them has been examined by anyone outside the firm.

## Sources

- Investment performance standards: <https://www.cfainstitute.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Fund disclosure context: <https://www.sec.gov/investor>
