---
name: options-record
domain: crypto-trading/options-record
trigger: "Writing the record of an option position and its review conditions."
anti_trigger: "Not for recommending a position, and not for trade execution."
scope: "The written options record: structure, greeks, cost, maximum loss, and review triggers."
status: seedling
---

# Options record

## Standard

The options record documents the exposure taken, the price paid, the greeks at inception, the maximum loss, and the conditions under which the position is reviewed or closed. It is written before the order, like every decision record in this pack, and it is the document that makes a later review a comparison rather than a reconstruction.

The maximum-loss line is the record's most important field. Every short-option position has one, and a record that cannot state it has not understood the position. Similarly, the greeks at inception are the baseline against which the position's drift is measured; without them, "the position changed" has no meaning.

Primary sources: <https://www.cboe.com/> and <https://osf.io/prereg/>.

## Decision rules

- Record the structure, the legs, the strikes, the expiries, and the executable cost.
- Record the greeks at inception, with the model named.
- State the maximum loss and the maximum gain in currency.
- State the thesis as a falsifiable exposure: what must happen and by when.
- Set review triggers: underlying level, volatility level, time to expiry.
- The record is append-only; amendments are dated.

## Procedure

1. Record the structure and its legs with prices.
2. Record the greeks and the model.
3. Compute maximum loss and gain.
4. State the exposure thesis and its falsifier.
5. Set the review triggers with dates and levels.
6. File the record and reference it from the trade memo.

## Anti-patterns

- Recording a short-option position without a maximum loss.
- Omitting the model behind the greeks.
- Stating a thesis that cannot be falsified.
- Setting triggers with no levels.
- Editing the record after the position moves.

## Done checklist

- [ ] Structure and legs recorded with prices.
- [ ] Greeks recorded with the model named.
- [ ] Maximum loss and gain computed.
- [ ] Thesis and falsifier stated.
- [ ] Review triggers with levels and dates.
- [ ] Record filed and referenced.

## Sources

- Options disclosure and mechanics: <https://www.cboe.com/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Investor education on options risk: <https://www.investor.gov/introduction-investing>

The record's longevity depends on the levels it stores: a trigger without a level is a sentiment, and a thesis without a falsifier is a hope. Storing both means the review can start with a fact rather than with a memory of what was intended.

A record that states the maximum loss in currency, before the order, is the single most useful discipline in options: it forces the writer to see the tail while it still feels hypothetical, and it gives a later reviewer the one number that makes the position comparable across structures.

