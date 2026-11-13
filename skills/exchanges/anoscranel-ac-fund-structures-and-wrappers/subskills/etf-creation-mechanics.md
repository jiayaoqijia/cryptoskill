---
name: etf-creation-mechanics
domain: investing/etf-creation-mechanics
trigger: "Understanding how an ETF's price is held close to its net asset value."
anti_trigger: "Not for fund cost comparison, and not for predicting a premium or discount."
scope: "Authorised participants, in-kind baskets, and the arbitrage that holds price to NAV."
status: seedling
---

# ETF creation mechanics

## Standard

An exchange-traded fund keeps its price near net asset value through a creation and redemption process. An authorised participant can deliver a basket of the underlying securities to the fund in exchange for new shares, or redeem shares for the underlying, and the profit from that arbitrage is what closes a gap between the traded price and the value of the holdings.

The mechanism depends on the participant's ability to trade the basket. When the underlying is liquid, creation is cheap and the arbitrage is tight; when the underlying is illiquid or has stopped trading, the arbitrage becomes expensive or impossible, and the ETF can trade at a discount to a net asset value that is itself stale. That is why an ETF's premium or discount widens exactly when the underlying market is closed or dislocated.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the fund's creation and redemption terms, including the basket size and any cash component.
- Record the identity and number of authorised participants, since concentration weakens the arbitrage.
- Record the historical premium or discount range and its behaviour in stress.
- Record the underlying market's trading hours relative to the ETF's, since a mismatch widens the gap.
- Record any creation suspension that occurred and what happened to the price.
- Record whether settlement is in-kind or cash, which changes the arbitrage's cost.

## Procedure

1. Read the prospectus for creation and redemption mechanics.
2. Record the basket composition and minimum size.
3. Record the participant count and any concentration.
4. Record the premium or discount history.
5. Record the trading-hours mismatch and any suspensions.
6. Write the analysis with the stress behaviour named.

## Anti-patterns

- Assuming the arbitrage is always available and costless.
- Treating a premium or discount as free money without the creation mechanics.
- Ignoring the trading-hours mismatch between the ETF and its underlying.
- Overlooking participant concentration, which makes the arbitrage fragile.
- Assuming net asset value is current when the underlying has stopped trading.

## Done checklist

- [ ] Creation and redemption terms recorded.
- [ ] Basket composition and size recorded.
- [ ] Participant count recorded.
- [ ] Premium or discount history recorded.
- [ ] Hours mismatch recorded.
- [ ] Suspension history recorded.

## Sources

- ETF structure and disclosure: <https://www.sec.gov/investor>
- Market practice guidance: <https://www.finra.org/>
- Investor education on exchange-traded funds: <https://www.investor.gov/introduction-investing>
