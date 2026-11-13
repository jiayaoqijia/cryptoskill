---
name: climate-record
domain: investing/climate-record
trigger: "Writing the record of a climate risk assessment and the assumptions behind it."
anti_trigger: "Not for recommending a security, and not for a compliance report."
scope: "The written record: emissions, scenario, exposure, and assumptions."
status: seedling
---

# Climate record

## Standard

The record states the emissions figure and what it counts, the scenario and its assumptions, the exposure by asset or sector, and the arithmetic that connects them to a valuation input. Its purpose is to make the assessment reproducible, because climate analysis is unusually dependent on assumptions that are invisible once the conclusion is written down.

It also states what was not assessed. Scope 3 coverage is often partial, physical risk is often assessed only for the largest sites, and the scenario used is often the one the company itself published. Naming those limits is what prevents a partial assessment from being read as a complete one, and it is the difference between an analysis and a summary of a disclosure.

Primary sources: <https://www.sec.gov/investor> and <https://osf.io/prereg/>.

## Decision rules

- The record states scopes covered, year, basis, and estimation method.
- The scenario is recorded with its source, horizon, and carbon price assumption.
- Transition exposure is recorded by sector with intensity and pass-through.
- Physical exposure is recorded by asset and location.
- The break-even carbon price is recorded where computed.
- Limits are stated: what was not assessed, and why.

## Procedure

1. Record the emissions data and its basis.
2. Record the scenario used and its assumptions.
3. Record transition exposure by sector.
4. Record physical exposure by asset.
5. Record the arithmetic and the break-even where relevant.
6. State the limits and file the record.

## Anti-patterns

- Recording a score instead of the underlying figures.
- Omitting the scenario's assumptions.
- Presenting a partial assessment as complete.
- Recording an emissions number without its basis.
- Leaving the valuation link implicit.

## Done checklist

- [ ] Emissions data and basis recorded.
- [ ] Scenario and assumptions recorded.
- [ ] Transition exposure recorded.
- [ ] Physical exposure recorded.
- [ ] Arithmetic and break-even recorded.
- [ ] Limits stated.

The record's most defensible feature is that it separates what was measured from what was modelled: an emissions figure from a reported filing, a carbon price from a published scenario, and a physical hazard from a public dataset are three different kinds of evidence, and a reader who cannot tell them apart cannot judge how much weight the conclusion deserves. Labelling each input by its source is the cheapest way to keep that distinction alive.


## Sources

- Climate disclosure requirements: <https://www.sec.gov/investor>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Climate risk frameworks: <https://www.bis.org/>
