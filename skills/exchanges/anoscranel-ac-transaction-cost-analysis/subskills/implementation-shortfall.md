---
name: implementation-shortfall
domain: investing/implementation-shortfall
trigger: "Measuring the gap between the decision price and the achieved price."
anti_trigger: "Not for predicting execution prices, and not for venue selection."
scope: "Decision price to execution price, and the components in between."
status: seedling
---

# Implementation shortfall

## Standard

Implementation shortfall measures the difference between the value of an order at the moment the decision was made and the value actually achieved, including the opportunity cost of any quantity left unfilled. It is the most complete single measure of trading cost because it captures what a delay costs, what an unfilled order costs, and what the executed portion paid, all in one number.

Its weakness is the decision price itself. The moment of decision is not recorded in any system, so most implementations use the arrival price — the mid at the time the order reached the desk — which excludes the delay between decision and arrival. That exclusion is not small for strategies whose signal decays quickly, and the record should state which convention was used rather than presenting the result as the whole cost.

Primary sources: <https://www.cfainstitute.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the reference price used and how it was observed.
- Record the quantity filled and the quantity unfilled.
- Record the opportunity cost of the unfilled quantity at a stated price.
- Record the components: spread, impact, delay, and opportunity.
- Record the sample period and the number of orders.
- Where the decision price is unavailable, record the arrival-price convention.

## Procedure

1. Record the order, its decision or arrival price, and the time.
2. Record each fill with its price and time.
3. Compute the executed-portion cost against the reference.
4. Compute the unfilled portion's opportunity cost.
5. Sum and decompose into components.
6. Write the shortfall summary with its reference price named.

## Anti-patterns

- Using arrival price and calling it total cost.
- Excluding unfilled quantity from the cost.
- Comparing shortfall across strategies with different decay speeds.
- Computing on a sample too small to separate from noise.
- Ignoring the sign: a favourable fill is still a deviation to be explained.

## Done checklist

- [ ] Reference price and convention recorded.
- [ ] Fills recorded with times.
- [ ] Executed cost computed.
- [ ] Opportunity cost computed.
- [ ] Components decomposed.
- [ ] Sample size recorded.

The measure is also vulnerable to a favourable fill it did not cause: an order that happens to execute during a market move in the portfolio's favour produces a negative shortfall, which is a result to be explained rather than a skill to be claimed, and a record that reports only the average hides how often that happened.

## Sources

- Investment performance and trading standards: <https://www.cfainstitute.org/>
- Market structure and execution disclosure: <https://www.sec.gov/investor>
- Execution quality guidance: <https://www.finra.org/>
