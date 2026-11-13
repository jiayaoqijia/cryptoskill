---
name: rates-option-record
domain: investing/rates-option-record
trigger: "Writing the record of a rates option position and its conventions."
anti_trigger: "Not for recommending a trade, and not for the confirmation itself."
scope: "The written record: instrument, vol convention, exercise, and hedge."
status: seedling
---

# Rates option record

## Standard

The rates option record states the instrument, the volatility convention and the model, the exercise schedule, the DV01 and vega, and the hedge. Those fields are not interchangeable with those of an equity option record, because the same trade can be described in two volatility conventions that differ by an order of magnitude and in two models that disagree on a Bermudan.

The record's second function is to preserve the calibration. A swaption's value depends on the curve used to discount and on the volatility surface used to price, and both change daily. Recording the inputs at entry means a later review can distinguish a position that lost because rates moved from one that lost because the surface repriced, which are different lessons for the trader.

Primary sources: <https://www.bis.org/> and <https://osf.io/prereg/>.

## Decision rules

- Record the instrument, expiry, tenor, strike, direction, and notional.
- Record the volatility type and, for normal vol, the units.
- Record the model and its calibration instruments.
- Record the exercise schedule for Bermudan structures.
- Record DV01 and vega by bucket, with the hedge.
- Record the curve and surface inputs used, with their time.

## Procedure

1. Record the instrument terms.
2. Record the volatility convention and model.
3. Record the calibration inputs and their time.
4. Record the exercise schedule where applicable.
5. Record DV01, vega, and the hedge.
6. Review at each trigger and record what changed.

## Anti-patterns

- Recording a swaption without its tenor.
- Omitting the volatility convention.
- Recording greeks without the model.
- Leaving out the calibration inputs.
- Reviewing the profit and loss without the surface move.

## Done checklist

- [ ] Instrument terms recorded.
- [ ] Volatility convention and model recorded.
- [ ] Calibration inputs recorded with time.
- [ ] Exercise schedule recorded.
- [ ] DV01, vega, hedge recorded.
- [ ] Reviews record surface and curve changes.

A final field deserves a line of its own: the purpose of the position, whether it hedges a liability, expresses a view, or structures a callable exposure. Without it, a review cannot tell whether a correct outcome on the wrong question is a success, and the record becomes a list of terms rather than a decision.

The record is also the only place where a model change can be detected after the fact, which matters because a switch of model alters the reported greeks without the market having moved at all.


## Sources

- Market conventions and standards: <https://www.bis.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Rate and volatility data: <https://www.federalreserve.gov/>
