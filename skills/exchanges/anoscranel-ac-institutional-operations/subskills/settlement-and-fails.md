---
name: settlement-and-fails
domain: investing/settlement-and-fails
trigger: "Handling settlement timing and a trade that fails to settle."
anti_trigger: "Not for predicting settlement failures, and not for legal advice."
scope: "Settlement cycles, buy-ins, and what a fail actually costs."
status: seedling
---

# Settlement and fails

## Standard

A trade settles when the securities and the cash change hands, and the interval between trade and settlement is the cycle, conventionally measured in business days from trade date as T+1 or T+2 depending on the market and instrument: shorter cycles reduce counterparty exposure and compress the time available to fix a break. A trade that does not settle on its due date fails, and the fail is a financing and operational event rather than a cancellation: the obligation remains, the buyer does not receive the securities, and the seller does not receive the cash.

The cost of a fail is mostly in the funding and in the replacement. A buyer who has not received securities cannot deliver them onward, so a single fail can propagate; a seller who has not received cash must fund the gap. Buy-in procedures exist to force completion, and their cost falls on the failing party, which is why settlement discipline is a capital issue rather than an administrative one.

Primary sources: <https://www.bis.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the trade date, the settlement cycle, and the resulting settlement date.
- Record the reason for any change to that date, such as a holiday calendar.
- Record the fail: the date, the quantity, and the reason where known.
- Record the funding consequence and the onward obligations affected.
- Record the buy-in procedure and its cost allocation.
- Record the resolution and the date it was completed.

## Procedure

1. Record trade and settlement dates with the calendar applied.
2. Monitor settlement status on the due date.
3. Record any fail and its cause.
4. Trace onward obligations that depend on the failed delivery.
5. Record the funding cost and the buy-in exposure.
6. Record resolution and close the item.

## Anti-patterns

- Treating a fail as a cancelled trade.
- Ignoring onward deliveries that depend on the failed one.
- Forgetting holiday calendars when computing the settlement date.
- Assuming buy-in costs are borne by the buyer.
- Leaving a fail open without an owner.

## Done checklist

- [ ] Trade and settlement dates recorded.
- [ ] Calendar applied.
- [ ] Fails recorded with cause.
- [ ] Onward obligations traced.
- [ ] Funding and buy-in exposure recorded.
- [ ] Resolution recorded.

The propagation is the reason fails are managed centrally rather than trade by trade: a single undelivered position can block several downstream deliveries, and the cost of resolving them together is far lower than resolving each in isolation, which is why the record should trace the dependency net rather than the individual trade.


## Sources

- Settlement standards and infrastructure: <https://www.bis.org/>
- Market structure and settlement context: <https://www.sec.gov/investor>
- Investor education on settlement: <https://www.investor.gov/introduction-investing>
