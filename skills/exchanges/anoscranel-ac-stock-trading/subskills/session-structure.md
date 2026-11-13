---
name: session-structure
domain: investing/session-structure
trigger: "Choosing which part of the trading day to use, and what the gap does."
anti_trigger: "Not for predicting the opening direction, and not for market-structure theory."
scope: "Pre-market, opening auction, intraday, closing auction, and the overnight gap."
status: seedling
---

# Session structure

## Standard

A stock trades in several distinct sessions, and each has its own liquidity and price formation. The pre-market is thin, with wide spreads and quoted sizes that are often indicative; the opening auction concentrates a full night's information into a single clearing price; the continuous session carries most of the volume; and the closing auction is where index funds and passive flows execute. Trading the same size in different sessions is a different trade.

The overnight gap is the structural consequence. A position held from the close to the next open is exposed to everything that happened while the market was shut, and the exposure cannot be managed with a stop, because the stop is not watched when the market is closed. That is why overnight risk is a sizing decision: the position either fits a plausible gap or it does not.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record the session in which the order will execute and the typical spread at that hour.
- Record the position's exposure to the overnight gap in currency.
- Size so that a gap of the name's recent worst magnitude leaves the account within its risk budget.
- Record whether the closing auction is part of the plan; participation there is a different order type.
- Record the pre-market liquidity, which may be a fraction of the day's.
- Where the strategy requires an exit at a specific time, record what happens if the market is halted.

## Procedure

1. Map the sessions and the venue's order types for each.
2. Sample spread, depth, and volume by session for the name.
3. Compute the overnight gap exposure at the intended size.
4. Compare with the name's recent gap distribution.
5. Decide the entry and exit sessions, and record why.
6. Record the halt contingency.

## Anti-patterns

- Assuming the pre-market price is executable at size.
- Treating a stop as protection overnight.
- Sizing from intraday liquidity and then holding through the close.
- Ignoring the closing auction when passive flows are large.
- Planning an exit at a time when the name is habitually thin.

## Done checklist

- [ ] Session plan recorded.
- [ ] Spread and depth sampled by session.
- [ ] Overnight gap exposure computed.
- [ ] Gap distribution compared.
- [ ] Entry and exit sessions justified.
- [ ] Halt contingency recorded.

## Sources

- Market structure and trading session context: <https://www.sec.gov/investor>
- Trading practice and investor guidance: <https://www.finra.org/>
- Investor education on equity trading: <https://www.investor.gov/introduction-investing>
