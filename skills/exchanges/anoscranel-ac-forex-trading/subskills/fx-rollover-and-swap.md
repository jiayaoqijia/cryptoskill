---
name: fx-rollover-and-swap
domain: investing/fx-rollover-and-swap
trigger: "Working out the financing a position pays or earns overnight."
anti_trigger: "Not for forecasting interest-rate differentials, and not for portfolio hedging."
scope: "Tom-next, swap points, carry, and the triple swap that arrives weekly."
status: seedling
---

# FX rollover and swap

## Standard

A spot FX position has a settlement date two business days forward, and holding it past that date requires rolling the settlement forward. The roll is priced as swap points, derived from the interest-rate differential between the two currencies, adjusted by the dealer's markup. A position that earns the differential is a carry position; one that pays it is financing a trade that must outperform that cost.

Three details decide the real cost. The markup sits on both sides of the roll, so a pair traded in and out repeatedly pays it repeatedly. The value date rolls across weekends, which is why many venues apply a triple swap on a specific weekday. And the differential can change faster than the position, particularly when a central bank moves, so a carry that was positive at entry can turn negative without the exchange rate moving at all.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the swap points per night and whether they are a credit or a debit.
- Record the venue's triple-swap day and its effect on a weekly holding period.
- Compute the annualised carry as a percentage of notional, and compare it with the expected move required to justify the position.
- Record the markup by comparing the quoted swap with the interbank differential.
- Record what happens to carry if either central bank's rate changes.
- For positions held for weeks, record the cumulative swap to date.

## Procedure

1. Note the settlement convention for the pair.
2. Collect the swap points for long and short, and the triple-swap day.
3. Convert the points into a currency amount at the position size.
4. Annualise the carry as a percentage of notional.
5. Compare the carry with the markup and with the required move.
6. Record the financing, its direction, and its sensitivity.

## Anti-patterns

- Treating the swap as a minor detail on a multi-week position.
- Comparing a swap credit across venues without the markup.
- Ignoring the triple-swap day when estimating weekly cost.
- Assuming the differential is stable for the life of the trade.
- Quoting carry in points rather than as a percentage of notional.

## Done checklist

- [ ] Swap points recorded long and short.
- [ ] Triple-swap day recorded.
- [ ] Currency cost computed at position size.
- [ ] Carry annualised as a percentage.
- [ ] Markup compared.
- [ ] Sensitivity to a rate change recorded.

## Sources

- Foreign exchange settlement and market conventions: <https://www.bis.org/>
- Policy rates and interest-rate data: <https://www.federalreserve.gov/>
- Rate series for differentials: <https://fred.stlouisfed.org/>
