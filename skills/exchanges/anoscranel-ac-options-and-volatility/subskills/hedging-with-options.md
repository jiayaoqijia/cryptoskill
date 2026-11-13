---
name: hedging-with-options
domain: crypto-trading/hedging-with-options
trigger: "Sizing and evaluating an option hedge against a portfolio exposure."
anti_trigger: "Not for directional trades, and not for predicting the underlying."
scope: "Protective puts and collars, the cost of insurance, and what the hedge does not cover."
status: seedling
---

# Hedging with options

## Standard

An option hedge buys protection with a defined cost and a defined limit. A protective put sets a floor below which losses stop, at the price of the premium; a collar finances the put by selling upside, which lowers the cost and caps the gain. Both are insurance contracts, and like insurance they should be evaluated on coverage, cost, and the exclusions.

The exclusions are what most hedge descriptions omit. A put protects against the underlying's fall at expiry, not against a gap through the strike before expiry without liquidity, not against basis risk between the hedge and the exposure, and not against the volatility cost if the hedge must be rolled. The record states what the hedge covers and what it does not.

Primary sources: <https://www.cboe.com/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- State the exposure being hedged, its size, and its beta to the hedge instrument.
- Record the strike, expiry, cost, and the resulting floor.
- Record the ratio of premium to the loss it protects against.
- State the exclusions: gap risk, basis risk, roll cost, and early expiry.
- Collars record the capped upside as a cost alongside the premium saved.
- Re-evaluate the hedge at each roll, not only at inception.

## Procedure

1. Define the exposure and its sensitivity to the underlying.
2. Choose strike and expiry to match the hedge horizon.
3. Compute the premium and the floor it creates.
4. Compute the cost per unit of protection.
5. Write the exclusions and the roll plan.
6. Record the hedge with its cost and limits.

## Anti-patterns

- Buying protection without computing what it costs per unit of loss avoided.
- Assuming a put protects against intraday gaps.
- Ignoring basis risk between the hedge and the book.
- Treating a collar as free because the premium nets to zero.
- Leaving the roll plan unwritten.

## Done checklist

- [ ] Exposure, size, and beta recorded.
- [ ] Strike, expiry, cost, and floor recorded.
- [ ] Cost per unit of protection computed.
- [ ] Exclusions stated.
- [ ] Collar upside cap recorded where used.
- [ ] Roll plan written.

## Sources

- Options hedging education: <https://www.cboe.com/>
- Investor education on risk management: <https://www.investor.gov/introduction-investing>
- Options disclosure context: <https://www.sec.gov/investor>

The insurance analogy is useful precisely because it exposes the trade-offs: a deductible is a strike, a premium is a cost, and an exclusion is a risk the policy does not cover. Reading a hedge the way an insurance buyer reads a policy produces better questions than reading it as a trade.
