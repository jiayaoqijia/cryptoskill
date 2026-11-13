---
name: borrow-and-put-parity
domain: investing/borrow-and-put-parity
trigger: "Reading parity distortions in a hard-to-borrow stock's options."
anti_trigger: "Not for predicting prices, and not for short-selling mechanics in general."
scope: "Hard-to-borrow names, parity distortions, and what they imply."
status: seedling
---

# Borrow and put parity

## Standard

Put-call parity is an arbitrage relationship: a call, a put, the stock, and a bond must be priced consistently, or a conversion or reversal can lock in a profit. In practice the relationship breaks in specific directions, and the most common cause is the cost of borrowing the stock. When a name is hard to borrow, the synthetic short created by buying a put and selling a call becomes expensive, and the puts trade rich relative to the calls.

The distortion is information. Its size approximates the market's implied borrow cost over the option's life, which is why a wide parity gap in a name with heavy short interest is not free money but a price for something the option market can see. A trader who treats it as an arbitrage without checking borrow availability is arbitraging a constraint they cannot access.

Primary sources: <https://www.cboe.com/> and <https://www.finra.org/>.

## Decision rules

- Record the parity relationship and the implied forward price for each expiry.
- Record the gap between the implied forward and the actual forward.
- Record the borrow availability and fee for the underlying.
- Record whether the gap is consistent with borrow cost or with something else, such as a pending dividend or a corporate action.
- Record the execution cost of doing the conversion or reversal, including the borrow.
- Where the gap cannot be explained, record it as unexplained rather than as opportunity.

## Procedure

1. Compute the implied forward from the parity relationship.
2. Compare with the actual forward or the stock and financing.
3. Record the borrow fee and availability.
4. Check for dividends or corporate actions that explain the gap.
5. Compute the conversion's cost including borrow.
6. Write the parity summary with its explanation.

## Anti-patterns

- Calling a parity gap an arbitrage without checking borrow.
- Ignoring the dividend inside the expiry.
- Comparing gaps across expiries without the borrow term.
- Assuming a hard-to-borrow fee is stable over the option's life.
- Overlooking the recall risk on the short leg.

## Done checklist

- [ ] Parity and implied forward computed.
- [ ] Gap recorded.
- [ ] Borrow fee and availability recorded.
- [ ] Dividends and actions checked.
- [ ] Conversion cost computed.
- [ ] Explanation or unexplained status recorded.

## Sources

- Exchange option and parity data: <https://www.cboe.com/>
- Short sale and borrow guidance: <https://www.finra.org/>
- Investor education on options arbitrage: <https://www.investor.gov/introduction-investing>
