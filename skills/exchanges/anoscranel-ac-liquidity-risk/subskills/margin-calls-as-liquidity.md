---
name: margin-calls-as-liquidity
domain: investing/margin-calls-as-liquidity
trigger: "Treating a collateral call as a cash deadline rather than a risk metric."
anti_trigger: "Not for margin mechanics on one position, and not for predicting calls."
scope: "When a collateral call becomes a cash deadline."
status: seedling
---

# Margin calls as liquidity

## Standard

A margin call is a liquidity event with a deadline. The amount is known, the deadline is fixed, and the settlement is cash or eligible collateral. That makes it different from a mark-to-market loss: the loss affects the balance sheet, while the call affects the ability to continue holding the position at all.

The liquidity question is whether the call can be met without selling the assets the call is about. A portfolio with a cash buffer meets calls from the buffer; one without sells collateral into the market that produced the call, which is the mechanism that turns a price move into a realized loss. The record therefore states the call amount against the buffer, not against total assets.

Primary sources: <https://www.bis.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the call amount, its currency, and its deadline with the timezone.
- Record the eligible collateral that could meet it, and the haircuts applied.
- Record the cash buffer available without selling the position at issue.
- Record the sale that would be required if the buffer is insufficient.
- Record the sequence: which asset would be sold first and at what discount.
- Record the escalation path if the buffer and sales together are insufficient.

## Procedure

1. Record the call and its deadline.
2. Record eligible collateral and haircuts.
3. Compare with the cash buffer.
4. Identify the sale required if the buffer is short.
5. Record the discount on that sale.
6. Write the sequence and the escalation.

## Anti-patterns

- Comparing the call with total assets rather than with liquid collateral.
- Ignoring haircuts on the collateral offered.
- Assuming a deadline can be extended.
- Planning to sell the illiquid asset last when it is the only one large enough.
- Treating the call as a valuation event rather than a deadline.

## Done checklist

- [ ] Call amount and deadline recorded.
- [ ] Eligible collateral recorded.
- [ ] Cash buffer compared.
- [ ] Required sale identified.
- [ ] Discount recorded.
- [ ] Escalation written.

The currency of the call also matters when collateral and obligation are denominated differently: a call in one currency met by selling assets in another adds an exchange-rate step, and a move in that rate between the call and the settlement can change the amount of collateral required even when the position has not moved at all.


## Sources

- Margin and collateral standards: <https://www.bis.org/>
- Investor education on margin risk: <https://www.investor.gov/introduction-investing>
- Market data for collateral valuation: <https://fred.stlouisfed.org/>
