---
name: funding-mechanics
domain: crypto-trading/funding-mechanics
trigger: "Calculate perpetual futures funding payments and examine premium index mechanics."
anti_trigger: "Use funding as a direct indicator of short-term price direction."
scope: "Calculates funding payments, premium index, clamp mechanics, and sign conventions on perpetual futures."
status: seedling
---

## Standard
Perpetual futures contracts lack expiry dates, requiring a synthetic anchor to tie contract prices to spot market prices. This anchor is funding, a periodic payment exchanged directly between long and short position holders. The funding payment mechanism relies on two core variables: the interest rate component and the premium index. The premium index measures the divergence between the perpetual contract price and the underlying spot index price, calculated through order book impact bids and asks. The interest rate is typically fixed by exchange specifications, reflecting the cost of capital differential between the quoted and base currencies.

Exchanges apply a clamp function to the premium index to prevent extreme rate volatility during market stress. The clamped premium index, combined with the interest rate, determines the funding rate for a specific settlement interval, usually every eight hours or hourly across venues. The sign convention dictates that when the perpetual contract trades at a premium over spot, the funding rate is positive; long positions pay short positions. Conversely, when the perpetual trades at a discount, the funding rate is negative; short positions pay long positions. The monetary payment for an individual position equals the position notional size multiplied by the funding rate, settled directly at the funding timestamp.

Primary sources for the claims in this step: <https://www.binance.com/en/support/faq/introduction-to-binance-futures-funding-rates-360033525031> and <https://www.bybit.com/en/help-center/article/Inverse-Contract-Funding>.

## Decision rules
- Calculate position notional using mark price, not execution price, when determining upcoming funding obligations.
- Verify the exact settlement interval and countdown timer on the specific trading venue, as intervals vary between one, four, and eight hours.
- Treat funding as a positioning tax or carrying cost rather than an independent directional signal or guaranteed yield.
- Account for position leverage when computing funding impact on margin ratios; high leverage amplifies funding cash flow sensitivity.
- Check whether the venue uses coin-margined or USD-margined contracts, as notional calculations and collateral currency risks differ fundamentally.

## Procedure
1. Extract the current mark price of the perpetual contract and the corresponding spot index price from the exchange public API or terminal.
2. Retrieve the current premium index and the interest rate component to compute the uncapped funding rate for the upcoming interval.
3. Apply the venue-specific clamp limits to determine the final funding rate.
4. Multiply the position size (in base or quote currency depending on contract type) by the mark price and the final funding rate to find the cash exchange amount.
5. Record the cash debit or credit against the account margin balance at the exact settlement timestamp.

## Anti-patterns
- Assuming funding payments occur continuously rather than discretely at fixed interval boundaries.
- Confusing the annualized funding percentage with simple yield without accounting for compounding and volatility.
- Ignoring margin buffer requirements during periods of extreme positive funding where long accounts face steady cash drains.
- Failing to verify whether contract specifications use last price or mark price for funding calculations.

## Done checklist
- [ ] Premium index divergence measured against spot index.
- [ ] Clamp function and interest rate factored into rate computation.
- [ ] Sign convention correctly applied (longs pay shorts on premium).
- [ ] Position notional and margin impact calculated for settlement.
- [ ] Venue settlement interval and contract type verified.

## Sources
- Binance Futures Funding Rate Mechanics Documentation: https://www.binance.com/en/support/faq/introduction-to-binance-futures-funding-rates-360033525031
- Bybit Perpetual Contracts Settlement Overview: https://www.bybit.com/en/help-center/article/Inverse-Contract-Funding
