---
name: factor-record
domain: investing/factor-record
trigger: "Writing the record of a factor definition and its implementation."
anti_trigger: "Not for recommending a factor, and not for backtest validation."
scope: "The written record: definition, construction, and capacity assumption."
status: seedling
---

# Factor record

## Standard

The factor record states the definition, every construction choice, the neutralisation applied, the capacity estimate, and the evidence the exposure rests on. It is written so that the definition can be reproduced and so that a later review measures the factor that was actually built rather than a idea of it.

The record also carries the falsifier. A factor whose premium is expected to persist should state what would constitute evidence that it has stopped: a sustained drawdown beyond the historical range, a documented change in the mechanism, or a crowding measure that has reached an extreme. Without that, every disappointment can be explained as temporary, and the position becomes unfalsifiable.

Primary sources: <https://www.nber.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the characteristic, the denominator, and the universe.
- Every construction choice is recorded, including outlier treatment and rebalancing.
- The neutralisation specification is recorded.
- Capacity, turnover, and impact assumptions are recorded.
- The evidence is recorded with its sample structure.
- The falsifier is stated as an observable condition.

## Procedure

1. Record the definition and construction choices.
2. Record the neutralisation.
3. Record capacity and turnover.
4. Record the evidence and its samples.
5. State the falsifier.
6. File and date the record; amend rather than rewrite.

## Anti-patterns

- A record that states the idea without the construction.
- Omitting the neutralisation, which changes what is measured.
- Recording evidence without its sample structure.
- No falsifier, so the position cannot be wrong.
- Rewriting the record after a change of definition.

## Done checklist

- [ ] Definition and construction recorded.
- [ ] Neutralisation recorded.
- [ ] Capacity and turnover recorded.
- [ ] Evidence and samples recorded.
- [ ] Falsifier stated.
- [ ] Record dated and append-only.

The record's final use is across factors rather than within one: comparing definitions side by side shows whether two exposures overlap substantially, and a portfolio that believes it holds three factors but whose records show correlated construction choices may be holding one exposure under three names.


Recording the implementation vehicle matters as much as the definition: a factor held through a fund carries the fund's own tracking, fees, and securities lending, and a review that compares the factor's documented premium with the fund's return is comparing two different objects unless the vehicle's contribution is separated out.


## Sources

- Factor research methods: <https://www.nber.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Market data for capacity estimation: <https://fred.stlouisfed.org/>
