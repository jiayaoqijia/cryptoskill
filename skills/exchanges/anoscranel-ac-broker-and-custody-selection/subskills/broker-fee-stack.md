---
name: broker-fee-stack
domain: investing/broker-fee-stack
trigger: "Computing the total cost of holding and using an account."
anti_trigger: "Not for comparing investment performance, and not for choosing a fund."
scope: "Commission, spread, FX conversion, custody and inactivity fees, and the total cost of holding an account."
status: seedling
---

# Broker fee stack

## Standard

The advertised commission is one line of a longer bill. The rest arrives as spread, currency conversion margin, custody or platform fees, inactivity charges, transfer fees, and the cost of cash held at a low rate. For a long-term investor the recurring lines dominate, and for an active one the spread and conversion lines do.

Currency conversion is the most commonly underestimated. A provider that quotes a commission-free trade may apply a margin to the exchange rate on every purchase and sale of a foreign asset, and that margin repeats with each transaction. Expressed annually, it can exceed the commission it replaced, which is why the record converts every fee into the same units: basis points per year at the account's actual activity level.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.sec.gov/investor>.

## Decision rules

- Record every fee line with its trigger and its frequency.
- Convert each recurring fee into basis points per year at the stated activity level.
- Record the FX conversion margin separately from any stated commission.
- Record inactivity, custody, and platform fees even when currently waived.
- Record exit costs: transfer fees, closing fees, and residual cash handling.
- Compare providers on the total at the same activity level, not on the headline.

## Procedure

1. Collect the provider's full fee schedule and terms.
2. Classify each fee as per-trade, periodic, or event-driven.
3. Estimate the annual cost at the account's expected activity.
4. Convert the FX margin into an annual drag.
5. Add exit costs amortised over the expected holding period.
6. Record the total and the assumptions behind it.

## Anti-patterns

- Comparing providers on commission alone.
- Ignoring FX margin because the trade was "commission-free".
- Overlooking a fee because it is currently waived.
- Estimating activity at a level the account will not sustain.
- Forgetting the cost of leaving.

## Done checklist

- [ ] All fee lines recorded with triggers.
- [ ] Recurring fees converted to annual basis points.
- [ ] FX margin recorded separately.
- [ ] Waived fees recorded with their conditions.
- [ ] Exit costs recorded.
- [ ] Total compared at equal activity.

The comparison is only fair when both providers are costed at the same activity level and the same holding period: a provider that is cheap per trade and expensive per year wins a heavy trader and loses a buy-and-hold investor, and the record should show which of the two the account actually is.

## Sources

- Investor education on account costs: <https://www.investor.gov/introduction-investing>
- Broker-dealer disclosure context: <https://www.sec.gov/investor>
- Exchange-rate and inflation data: <https://fred.stlouisfed.org/>
