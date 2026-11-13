---
name: fair-value-and-basis
domain: investing/fair-value-and-basis
trigger: "Working out what the future should trade at relative to the cash index."
anti_trigger: "Not for predicting the index, and not for portfolio policy."
scope: "Cost of carry, dividends, and the difference between fair value and the traded basis."
status: seedling
---

# Fair value and basis

## Standard

Fair value is the price the future should trade at if it is to be equivalent to buying the index today and financing it to expiry. It equals the cash index plus the financing cost over the remaining term, minus the dividends expected to be paid on the index's constituents before expiry. When the future trades above that level the basis is rich, and when below it is cheap, relative to the financing available to the marginal market participant.

The word marginal matters. The rate that determines fair value is the rate at which large participants can finance, not the rate a retail account pays, and the dividend forecast is an estimate. That is why a basis that looks exploitable to a small trader is often just the spread between two financing rates, and why the record should state which rate and which dividend estimate were used.

Primary sources: <https://www.cmegroup.com/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the cash index level and the time to expiry, in days, on an actual/365 or 360 basis as the market convention requires.
- Record the financing rate used and its source; state that it is the rate available to the participant, not the policy rate.
- Record the dividend estimate for the period and its source.
- Compute fair value and compare it with the traded future.
- Record the difference as a basis in index points and as an annualised percentage.
- Record whether the difference is consistent with the financing-rate spread rather than with a forecast.

## Procedure

1. Collect the cash index level, the future's price, and the days to expiry.
2. Collect the financing rate and the expected dividends.
3. Compute fair value from carry minus dividends.
4. Compare the traded price with fair value.
5. Express the difference in points and annualised.
6. Record the calculation and its inputs with dates.

## Anti-patterns

- Computing fair value with a retail borrowing rate and calling the result an arbitrage.
- Ignoring dividends, which can be a large part of the basis.
- Comparing a future with a cash index that has a different composition or a stale close.
- Treating a rich basis as a directional signal.
- Using the policy rate as the financing rate.

## Done checklist

- [ ] Cash level, future price, and days recorded.
- [ ] Financing rate recorded with source.
- [ ] Dividend estimate recorded.
- [ ] Fair value computed.
- [ ] Basis expressed in points and annualised.
- [ ] Interpretation recorded.

## Sources

- Index futures and settlement data: <https://www.cmegroup.com/>
- Policy rates and market data: <https://www.federalreserve.gov/>
- Short-rate series for financing: <https://fred.stlouisfed.org/>
