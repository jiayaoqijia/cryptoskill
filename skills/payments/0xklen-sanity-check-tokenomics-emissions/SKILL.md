---
name: sanity-check-tokenomics-emissions
description: Use when reviewing a token's supply, emission schedule, inflation, or FDV: computes annual inflation, daily sell pressure versus liquidity, and unlock cliffs that can crater price.
---

# Sanity check tokenomics emissions

Emissions are supply that must be sold to pay contributors and farmers; the question is whether that daily sell pressure is a small fraction of real liquidity or a cliff that overwhelms it.

## Procedure

1. Gather four numbers: max supply, circulating supply, annual emission (tokens/yr), and price. `FDV = max_supply * price`; `market_cap = circulating * price`.

2. Annual inflation % = `emission / circulating * 100`. A 100M/yr emission on 400M circulating is 25% dilution per year — every holder is diluted 25% unless demand grows faster.

3. Daily sell pressure = `emission_daily * price`. Compare to average daily DEX volume. Worked example: 100M tokens/yr at $2 → 274,000 tokens/day → $547,945/day. Against $5M daily volume that is 11% of volume, structurally capping price:

   python3 -c "print(100e6/365*2, 100e6/365*2/5e6)"
   547945.2 0.1096

4. Find the cliff: mark months where a scheduled unlock exceeds 20% of circulating. Walk the vesting schedule rather than trusting a summary.

5. Cross-check the pie: a team + investor allocation above 40% with a cliff inside 6 months is a supply overhang; compare the vesting total to the emissions budget.

6. Verdict rule: sustainable only if `daily_emissions_value < 2% of daily volume` AND no single month unlocks > 10% of circulating. Otherwise label it emission-driven and avoid holding through unlocks.

## Pitfalls

- Reading FDV as if fully diluted supply were liquid — the sellable float is circulating, and unlocks add to it.
- Ignoring that emissions paid in the token to LPs are immediately sold by yield farmers, so advertised "yield" is dilution.
- Trusting a static schedule: real contracts can re-mint or extend emissions via governance; check the mint function is capped or renounced.

## Verification

    python3 -c "print(274000*2, 274000*2/5e6)"
    548000 0.1096

Rebuild daily emission = annual/365, multiply by price, and divide by volume; the ratio is the pressure test.

Report inflation %, daily sell pressure, the largest single unlock, and the verdict, with the numbers.
