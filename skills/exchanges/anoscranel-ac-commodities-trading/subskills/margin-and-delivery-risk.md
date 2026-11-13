---
name: margin-and-delivery-risk
domain: investing/margin-and-delivery-risk
trigger: "Managing futures margin and avoiding an unintended delivery obligation."
anti_trigger: "Not for predicting prices, and not for securities margin."
scope: "Initial and variation margin, notice days, and the obligations of a delivered contract."
status: seedling
---

# Margin and delivery risk

## Standard

Futures margin is performance bond, not a down payment: it is topped up daily through variation margin as the contract is marked to market, so a losing position drains the account continuously rather than at the end. That mechanic is what makes futures capital-efficient and what makes an under-funded position fail quickly, and the exchange can raise the requirement when volatility rises.

Delivery risk is separate and more administrative. Holding a long position into the first notice day makes it eligible for delivery of the physical good, and holding a short makes it eligible to deliver. For a trader who does not want the physical commodity, the rule is to close before the broker's cut-off, which is often several days before the exchange's last trading day, and to verify the position is flat rather than assuming an order was filled.

Primary sources: <https://www.cmegroup.com/> and <https://www.cftc.gov/>.

## Decision rules

- Record initial margin, maintenance margin, and the broker's additional requirement.
- Record the variation-margin currency and the account's funding source.
- Compute the adverse move that would consume the posted margin.
- Record the first notice day, the last trading day, and the broker's close-out cut-off.
- Record the roll plan and the date by which the position will be rolled or closed.
- Verify the flat position after closing, with a statement or a position report.

## Procedure

1. Record margin requirements and the broker's add-ons.
2. Compute the move that exhausts margin at the position size.
3. Record notice and cut-off dates for each contract held.
4. Set the roll or close date ahead of the cut-off, with a buffer.
5. Execute and verify the position is flat or rolled.
6. Record the margin and delivery status at each review.

## Anti-patterns

- Treating futures margin as a fixed deposit.
- Holding into the notice period because the position is profitable.
- Assuming the broker's cut-off matches the exchange calendar.
- Closing on the cut-off day with no buffer for a failed order.
- Failing to verify that a close executed.

## Done checklist

- [ ] Margin requirements recorded.
- [ ] Margin-exhausting move computed.
- [ ] Notice and cut-off dates recorded.
- [ ] Roll or close date set with buffer.
- [ ] Position verified flat or rolled.
- [ ] Status recorded at each review.

## Sources

- Exchange margin and delivery calendars: <https://www.cmegroup.com/>
- Regulatory guidance on futures and delivery: <https://www.cftc.gov/>
- Investor education on futures risk: <https://www.investor.gov/introduction-investing>
