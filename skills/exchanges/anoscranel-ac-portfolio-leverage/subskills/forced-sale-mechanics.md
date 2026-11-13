---
name: forced-sale-mechanics
domain: investing/forced-sale-mechanics
trigger: "Understanding what happens to holdings when a margin call is not met."
anti_trigger: "Not for predicting when a call will occur, and not for tax computation."
scope: "What gets sold, in what order, at what price, and the tax consequence that follows."
status: seedling
---

# Forced-sale mechanics

## Standard

When a call is not met, the broker sells collateral to restore the requirement, and it does so on its own timetable. The order is not chosen by the client: the broker will typically sell whatever is liquid and sufficient, which may be the position the client most wanted to keep, and it may sell into a falling market because that is when calls happen.

The consequence is not only the realised loss but its character. A forced sale converts an unrealised position into a realised one, with whatever tax treatment follows, and it may realise gains in the same year as other income. The record should therefore state which holdings would be sold first, the likely price impact, and the tax consequence of that sale — before the call, when there is still a choice.

Primary sources: <https://www.finra.org/> and <https://www.irs.gov/>.

## Decision rules

- Record the broker's stated liquidation policy and its discretion.
- Identify which holdings would be sold first under the policy, and why.
- Estimate the price impact of selling each in a stressed market.
- Record the realised-gain or loss consequence of a forced sale at a stated price.
- Record the timing: whether the broker acts intraday, at close, or on notice.
- Where the policy is discretionary, record the worst plausible sequence.

## Procedure

1. Read the margin agreement's liquidation clause.
2. Rank holdings by the broker's likely sale order.
3. Estimate the price impact for each under stress.
4. Compute the tax consequence at a stated sale price.
5. Record the intraday versus end-of-day timing.
6. Write the forced-sale scenario in currency.

## Anti-patterns

- Assuming the client chooses what is sold.
- Assuming the sale happens at a fair price.
- Ignoring the tax character of a forced realisation.
- Treating the liquidation clause as boilerplate.
- Modelling a forced sale in a calm market.

## Done checklist

- [ ] Broker liquidation policy recorded.
- [ ] Likely sale order identified.
- [ ] Price impact estimated under stress.
- [ ] Tax consequence computed at a stated price.
- [ ] Timing recorded.
- [ ] Scenario written in currency.

The tax consequence deserves particular care in a leveraged account, because a forced sale can realise gains that push the holder into a higher band and can impose a liability in the same year the portfolio has fallen, which is the worst possible pairing of events.

## Sources

- Margin agreements and liquidation practice: <https://www.finra.org/>
- Investor education on margin risk: <https://www.investor.gov/introduction-investing>
- Tax treatment of realised gains: <https://www.irs.gov/>
