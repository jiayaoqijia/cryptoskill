---
name: fx-barriers-and-digitals
domain: investing/fx-barriers-and-digitals
trigger: "Trading an FX barrier or digital option and its behaviour near the trigger."
anti_trigger: "Not for recommending structured products, and not for generic option theory."
scope: "Knock-ins, knock-outs, one-touch, and the behaviour near the trigger."
status: seedling
---

# FX barriers and digitals

## Standard

A barrier option is a standard option with a condition attached: it either comes into existence when a level trades (knock-in) or ceases to exist when a level trades (knock-out). The condition changes the payoff in a discontinuous way, which is why barrier options are cheap relative to the equivalent vanilla and why their hedging is difficult close to the trigger.

The behaviour near the barrier is the risk. A knock-out option's delta accelerates as the trigger approaches, because the value is collapsing towards zero, and a hedger who is short that option must buy increasing amounts of the underlying into the level — which can itself push the market towards the trigger. Digital options have the same characteristic in a sharper form: their payoff is a step, so the delta near the strike is enormous and the position cannot be hedged continuously.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the barrier level, the observation convention, and whether it is continuously monitored.
- Record whether the barrier is monitored on spot, on a fixing, or on a stated source.
- Record the payoff on the trigger side and on the non-trigger side.
- Record the delta and vega near the barrier, and the rehedging assumption.
- Record the gap risk: what happens if the level trades through with no liquidity.
- Record the counterparty's discretion, if the confirmation gives any.

## Procedure

1. Record the structure and the barrier terms.
2. Record the monitoring convention and the price source.
3. Compute the payoff on each side of the barrier.
4. Estimate the delta near the trigger and the rehedging cost.
5. Record the gap scenario.
6. Write the terms summary and the trigger plan.

## Anti-patterns

- Treating a barrier option as a vanilla with a slightly different strike.
- Ignoring whether the barrier is monitored continuously or at a fixing.
- Assuming the hedge can be adjusted at the trigger price.
- Selling a digital without sizing the step risk.
- Missing a discretion clause in the confirmation.

## Done checklist

- [ ] Barrier level and monitoring recorded.
- [ ] Price source recorded.
- [ ] Payoffs on both sides recorded.
- [ ] Delta near trigger estimated.
- [ ] Gap scenario written.
- [ ] Discretion clauses recorded.

## Sources

- Foreign exchange market conventions: <https://www.bis.org/>
- Market data and rates: <https://www.federalreserve.gov/>
- Investor education on complex products: <https://www.investor.gov/introduction-investing>
