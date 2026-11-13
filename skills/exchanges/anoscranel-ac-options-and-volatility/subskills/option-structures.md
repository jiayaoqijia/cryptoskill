---
name: option-structures
domain: crypto-trading/option-structures
trigger: "Choosing an option structure and understanding the exposure it creates."
anti_trigger: "Not for recommending a trade, and not for pricing."
scope: "Spreads, straddles, covered calls, and protective puts, and the exposure each creates."
status: seedling
---

# Option structures

## Standard

A structure is a combination of options whose payoffs combine into a specific exposure. The common ones are: a long call or put, directional with defined premium at risk; a vertical spread, directional with capped payoff and lower cost; a straddle or strangle, a bet on movement with no direction; a covered call, income against a held asset with upside capped; and a protective put or collar, insurance against a fall at a stated cost.

Each has a characteristic greek profile, and that profile is the real content. A covered call is short volatility and short gamma with capped upside; a long straddle is long gamma and long vega, paying theta for the privilege. Choosing a structure means choosing which of those exposures the situation calls for, and whether the premium is worth it.

Primary sources: <https://www.cboe.com/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- State the exposure the structure creates, in greeks, before stating the structure's name.
- Record the maximum loss and maximum gain explicitly; a structure without a stated maximum is not understood.
- Compare the structure's cost with the alternative of doing nothing or holding the underlying.
- Record the breakeven points and the probability implied by the price.
- For covered calls, record the capped upside as a cost, not as free income.
- For spreads, record the assignment and early-exercise risk on the short leg.

## Procedure

1. Write the exposure required: direction, volatility, time, and tail.
2. Map candidate structures to that exposure.
3. Compute maximum loss, maximum gain, and breakevens for each.
4. Compare the greeks of candidates.
5. Choose and record the structure with its exposure and cost.
6. Set the review conditions: underlying move, vol change, time decay.

## Anti-patterns

- Choosing a structure by name without its greeks.
- Presenting a covered call as income without the capped upside.
- Ignoring assignment risk on a short leg.
- Comparing structures on cost without comparing exposures.
- Holding a structure past the thesis that justified it.

## Done checklist

- [ ] Required exposure stated.
- [ ] Candidates mapped to exposure.
- [ ] Maximum loss, gain, and breakevens computed.
- [ ] Greeks compared.
- [ ] Structure chosen and recorded with cost.
- [ ] Review conditions set.

## Sources

- Options strategies education: <https://www.cboe.com/>
- Investor education on options: <https://www.investor.gov/introduction-investing>
- Options disclosure and regulatory context: <https://www.sec.gov/investor>

The naming convention is the least important part of a structure and the most frequently confused: the same payoff can be constructed several ways, and the greeks are the identity. A record that describes the exposure rather than the name survives a change of venue or terminology.
