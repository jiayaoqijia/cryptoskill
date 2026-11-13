---
name: fx-quoting-and-pip-value
domain: investing/fx-quoting-and-pip-value
trigger: "Converting a quoted FX price and position size into money at risk."
anti_trigger: "Not for forecasting a pair, and not for portfolio currency hedging."
scope: "Base and quote conventions, pip, lot size, and profit in the account currency."
status: seedling
---

# FX quoting and pip value

## Standard

Every FX quote has a base currency and a quote currency, and the number says how much of the quote currency buys one unit of the base. EUR/USD at 1.0850 means one euro costs 1.0850 dollars. Confusing the base for the traded asset is the first error, and it produces a position that is the opposite of the intended one.

Position size then depends on the pair and on the account currency. A standard lot is a hundred thousand units of the base currency, a mini lot is ten thousand, and a micro lot is a thousand, but the money value of a one-pip move differs across pairs and across account currencies. That conversion has to be done explicitly, because a size that is prudent in one pair can be two or three times the risk in another.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the pair with the base first, and state what one unit of the base costs in the quote currency.
- Record the pip definition for the pair: four decimals for most, two for yen pairs.
- Compute pip value in the account currency, not in the quote currency.
- Record the lot size used and the resulting notional in the base currency.
- Record the stop distance in pips and the resulting money risk, then check it against the risk budget.
- Where the account currency is not in the pair, record the conversion rate used and its date.

## Procedure

1. Write the pair in base/quote form and the current rate.
2. Confirm the pip definition and the contract size for the venue.
3. Convert one pip into the account currency.
4. Choose the position size, then compute the notional.
5. Compute the money risk from the stop distance.
6. Record the arithmetic so a later reviewer can reproduce it.

## Anti-patterns

- Treating the quote currency as the asset traded.
- Sizing by lot count across pairs with different pip values.
- Computing risk in the quote currency and forgetting the conversion.
- Ignoring the venue's contract size when it is not the standard lot.
- Recording a size without the rate that produced it.

## Done checklist

- [ ] Pair written base first with the rate.
- [ ] Pip definition confirmed.
- [ ] Pip value computed in the account currency.
- [ ] Notional recorded in the base currency.
- [ ] Money risk computed from the stop.
- [ ] Conversion rate and date recorded.

## Sources

- Triennial survey of foreign exchange turnover: <https://www.bis.org/>
- Foreign exchange rates and market data: <https://www.federalreserve.gov/>
- Investor education on currency products: <https://www.investor.gov/introduction-investing>
