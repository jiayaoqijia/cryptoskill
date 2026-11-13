---
name: tick-and-lot-mechanics
domain: investing/tick-and-lot-mechanics
trigger: "Working with tick sizes, lot sizes, and minimum price increments."
anti_trigger: "Not for choosing a price level, and not for predicting spreads."
scope: "Tick sizes, lot sizes, minimum increments, and price improvement."
status: seedling
---

# Tick and lot mechanics

## Standard

A tick is the minimum price increment, and it is a rule, not a preference. Quotes and orders must sit on the tick grid, which means the spread has a floor set by the rule: where the tick is wide relative to the price, the spread cannot compress below one tick regardless of how competitive the venue is.

Lot sizes are the other rule. A round lot is the standard unit of quoting, and orders below it are treated differently by venues and by disclosure. Fractional shares have made small orders routine for retail, but the mechanics of quoting and of odd-lot treatment still follow the rule book.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/rules-guidance>.

## Decision rules

- Record the tick size for the instrument and whether a tick-size pilot applies.
- Record the spread in ticks as well as in currency; the tick floor explains a narrow spread.
- Record lot size and whether the order is round, odd, or fractional.
- Price improvement is recorded relative to the reference, not asserted.
- Where the tick is wide relative to price, record the floor and its effect on the spread.
- Odd-lot treatment is recorded where it affects execution or disclosure.

## Procedure

1. Identify the tick size and any pilot regime.
2. Express the spread in ticks as well as currency.
3. Identify the lot size and the order's classification.
4. Record any price improvement against the reference.
5. Note where the tick floor binds.
6. Record the mechanics with the trade.

## Anti-patterns

- Assuming a one-cent spread without checking the instrument.
- Ignoring the tick floor when assessing competitiveness.
- Treating a fractional order as a round lot for disclosure.
- Claiming price improvement without a reference.
- Assuming the same tick applies across venues and instruments.

## Done checklist

- [ ] Tick size and any pilot recorded.
- [ ] Spread expressed in ticks.
- [ ] Lot size and classification recorded.
- [ ] Price improvement measured against a reference.
- [ ] Tick-floor effect noted.
- [ ] Mechanics stored with the trade.

## Sources

- Regulatory context for tick and lot rules: <https://www.sec.gov/investor>
- Rule context for quoting and odd lots: <https://www.finra.org/rules-guidance>
- Investor education on trading increments: <https://www.investor.gov/introduction-investing>

The mechanics matter most for small orders and thin instruments, where one tick is a large fraction of the spread. In those cases the rule, not the market's competitiveness, is what sets your cost, and recording it prevents the error of attributing a structural cost to execution skill.
