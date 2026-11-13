---
name: venues-and-routing
domain: investing/venues-and-routing
trigger: "Understanding where an equity order goes and who is on the other side."
anti_trigger: "Not for choosing a broker, and not for predicting execution quality."
scope: "Exchanges, alternative venues, dark pools, and how retail orders are routed and paid for."
status: seedling
---

# Venues and routing

## Standard

US equity trading is fragmented across exchanges and alternative venues, and the order you send is routed by your broker according to its own logic. That logic may include payment for order flow, internalisation, and best-execution obligations that are satisfied statistically rather than order by order. Understanding this determines who trades against you and at what price.

The reference price is the national best bid and offer, assembled from the venues. Your fill can be at that price, inside it, or worse, and the difference is the execution quality that disclosure statistics attempt to measure. A broker's statistics describe its aggregate flow; they do not promise the next order's fill.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/rules-guidance>.

## Decision rules

- Record the broker's routing disclosure and whether it receives payment for order flow.
- Record whether the order is internalised or sent to a venue.
- Compare fills with the reference price at the time of the order, not the closing price.
- Treat aggregate execution statistics as evidence about the broker, not about your order.
- Record dark-pool exposure where the broker discloses it.
- Where execution quality matters, record the measurement method before trading.

## Procedure

1. Pull the broker's routing and payment-for-order-flow disclosures.
2. Record the order's routing path where the confirmation shows it.
3. Compare the fill with the reference price at submission.
4. Record the slippage and whether it is consistent with the disclosed practice.
5. Check the broker's execution statistics with their measurement window.
6. Record the routing facts with the trade record.

## Anti-patterns

- Assuming an order goes to an exchange.
- Comparing a fill with the day's close instead of the reference at submission.
- Treating a broker's average statistics as a guarantee.
- Ignoring payment for order flow when assessing conflicts.
- Assuming dark-pool fills are worse without measuring.

## Done checklist

- [ ] Broker routing disclosure pulled.
- [ ] Routing path recorded where disclosed.
- [ ] Fill compared with the reference price at submission.
- [ ] Slippage recorded.
- [ ] Execution statistics checked with their window.
- [ ] Routing facts stored with the record.

## Sources

- Regulatory context for order routing and execution: <https://www.sec.gov/investor>
- Rule context for best execution and disclosure: <https://www.finra.org/rules-guidance>
- Investor education on order handling: <https://www.investor.gov/introduction-investing>

The useful discipline is to keep a record of what actually happened to your orders: the reference price at submission, the venue shown on the confirmation, and the fill. After a few dozen trades the pattern is visible, and it is more informative than any published average.
