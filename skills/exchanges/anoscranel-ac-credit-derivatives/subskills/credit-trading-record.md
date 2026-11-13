---
name: credit-trading-record
domain: investing/credit-trading-record
trigger: "Writing the record of a credit derivatives position and its hedge."
anti_trigger: "Not for recommending a credit, and not for the trade blotter."
scope: "The written record: direction, spread, DV01, event exposure, and review."
status: seedling
---

# Credit trading record

## Standard

The credit record states what protection was bought or sold, at which spread and maturity, against which reference entity and documentation, with what spread DV01, and what the position pays or receives if a credit event occurs. Those facts are what make the position reviewable, and several of them — the spread, the DV01, the basis — change daily while the contract stays the same.

The event clause belongs in the record explicitly. A protection position is only as good as the definition it relies on, and a hedge that does not cover restructuring is a hedge with a gap that the record should name rather than leave to be discovered at the event. Recording the recovery assumption alongside the payout is what turns a notional into a risk.

Primary sources: <https://www.isda.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the reference entity, seniority, maturity, and documentation version.
- The direction is recorded with the spread and the upfront paid or received.
- Spread DV01 is recorded, with the hedge ratio if the position hedges something.
- The credit events covered and the restructuring clause are recorded.
- The payout at a range of recovery values is computed and recorded.
- Review entries record spread moves, basis moves, and roll or series changes.

## Procedure

1. Record the contract terms and direction.
2. Record spread, upfront, and DV01.
3. Record the event definitions and restructuring clause.
4. Compute payout across recovery values.
5. Record the hedge ratio where applicable.
6. Review at the stated cadence and record what changed.

## Anti-patterns

- Recording the notional and not the DV01.
- Omitting the restructuring clause.
- Recording one recovery assumption instead of a range.
- Leaving the counterparty out of a hedge record.
- Reviewing only the profit and loss.

## Done checklist

- [ ] Contract terms and direction recorded.
- [ ] Spread, upfront, and DV01 recorded.
- [ ] Event definitions and restructuring recorded.
- [ ] Payout across recoveries recorded.
- [ ] Hedge ratio recorded where applicable.
- [ ] Reviews record spread and basis changes.

The record should also note which side of the market the position sits on in a stress event: a protection buyer's position gains when spreads widen and pays out on an event, while a seller's gains are capped at the premium and its losses are not, and that asymmetry belongs at the top of the page rather than in a footnote.

## Sources

- Credit derivatives documentation standards: <https://www.isda.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Market and credit spread data: <https://www.federalreserve.gov/>
