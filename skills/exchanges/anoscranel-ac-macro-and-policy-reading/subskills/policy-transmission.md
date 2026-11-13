---
name: policy-transmission
domain: investing/policy-transmission
trigger: "Understanding how a policy rate reaches asset prices and where the chain breaks."
anti_trigger: "Not for predicting policy, and not for choosing assets."
scope: "How a policy rate reaches asset prices: the channels, the lags, and the breaks."
status: seedling
---

# Policy transmission

## Standard

A policy rate reaches asset prices through channels: the cost of credit, the discount rate on future cash flows, the exchange rate, and the price of risk. Each channel has a lag measured in quarters, and each can be blocked — by fixed-rate borrowing, by balance-sheet constraints at lenders, or by expectations that the policy will be reversed.

The implication for an investor is that the reaction of an asset to a rate change is an empirical question about which channel dominates at that moment, not a mechanical rule. Recording which channel the analysis assumes, and the lag it implies, is what makes the claim testable.

Primary sources: <https://www.federalreserve.gov/> and <https://fred.stlouisfed.org/>.

## Decision rules

- Name the channel assumed: credit cost, discount rate, exchange rate, or risk price.
- Record the lag the channel implies and the evidence for it.
- Record what would block the channel in the current structure.
- Distinguish the policy rate from market rates along the curve.
- Do not infer an asset's reaction from the policy rate alone; record the intermediate link.
- Where the channel is unclear, record the claim as weak rather than selecting a channel by convenience.

## Procedure

1. Identify the asset and the channel through which policy should reach it.
2. Record the intermediate variables that carry the effect.
3. Record the lag and its evidence.
4. Identify blockers in the current structure.
5. Check whether the intermediate variables moved as the channel predicts.
6. Record the claim with the channel and lag stated.

## Anti-patterns

- Assuming a direct link from policy rate to asset price.
- Ignoring the lag when evaluating a claim.
- Selecting the channel that fits the recent move.
- Treating market rates as the policy rate.
- Forgetting fixed-rate structures that delay transmission.

## Done checklist

- [ ] Channel named.
- [ ] Intermediate variables recorded.
- [ ] Lag and evidence recorded.
- [ ] Blockers identified.
- [ ] Intermediate movement checked.
- [ ] Claim recorded with channel and lag.

## Sources

- Policy rates and market rates: <https://fred.stlouisfed.org/>
- Central-bank policy material: <https://www.federalreserve.gov/>
- Investor education on monetary policy: <https://www.investor.gov/introduction-investing>

The lag is the part that makes policy hard to trade: by the time the effect arrives, the market has usually priced the decision and moved on to the next one. Recording the lag is what stops a decision from being credited with a move that started before it.
