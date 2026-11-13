---
name: fx-option-record
domain: investing/fx-option-record
trigger: "Writing the record of an FX option position and its conventions."
anti_trigger: "Not for recommending a position, and not for the confirmation itself."
scope: "The written record: pair, strike or delta, vol, premium, and barrier terms."
status: seedling
---

# FX option record

## Standard

The FX option record states the conventions the position was quoted and settled under, because those conventions are where the arithmetic goes wrong. The pair, the strike in both price and delta terms, the volatility, the premium and its currency, the delta convention used, the expiry cut, and the settlement method are the fields that make the position reproducible.

For structures with conditions, the record adds the barrier or trigger terms and the monitoring convention. Those terms determine whether the position exists at all in a given scenario, and a record that omits them cannot be reviewed against the market that actually occurred. The record is written at entry and amended only by dated entries.

Primary sources: <https://www.bis.org/> and <https://osf.io/prereg/>.

## Decision rules

- Record the pair, direction, notional, and the trade date with a timestamp.
- Record the strike in price and delta terms, and the delta convention used.
- Record the volatility, the premium, its currency, and the payment date.
- Record the expiry, the cut, and the settlement method.
- Record barrier, trigger, and monitoring terms for structures.
- For a hedge, record the delta and vega of the position being hedged.

## Procedure

1. Record the trade terms and conventions.
2. Record the premium conversion and payment date.
3. Record expiry, cut, and settlement.
4. Record any conditional terms.
5. Record the hedge position where applicable.
6. Review at each cut and at any barrier proximity.

## Anti-patterns

- Recording the strike in delta terms only.
- Omitting the delta convention, which makes the strike ambiguous.
- Leaving out the premium currency.
- Recording a barrier structure without the monitoring convention.
- Editing the record after the outcome.

## Done checklist

- [ ] Pair, direction, notional recorded.
- [ ] Strike in price and delta terms recorded.
- [ ] Vol, premium, currency, date recorded.
- [ ] Expiry, cut, settlement recorded.
- [ ] Conditional terms recorded.
- [ ] Hedge position recorded where applicable.

A record kept this way also survives staff changes: the conventions that are obvious to the person who traded the option are exactly the ones a later reader cannot reconstruct, and writing them down at entry costs a minute and saves an argument about whether the strike was 25 delta spot or forward.


## Sources

- Foreign exchange market conventions: <https://www.bis.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Market data and rates: <https://www.federalreserve.gov/>
