---
name: value-liquidity-mining-position-with-emission-decay
description: Use when valuing a liquidity-mining or gauge position: converts emissions to APR, applies reward-token price decay and vesting, and compares against impermanent loss and real yield.
---

# Value liquidity mining position with emission decay

Farming APR is quoted on emissions valued at today's price; if the reward token decays 50% before you sell, your realized APR halves, and the LP is simultaneously exposed to impermanent loss.

## Procedure

1. Emissions and TVL: `emissions_daily * price / TVL = daily rate`. Worked: 100,000 tokens/day at $2 = $200,000/day on $50M TVL → `0.4%/day` → `0.004*365 = 146%/yr` gross.

2. Apply decay: if the reward token halves over the holding period, realized rate roughly halves → 73%/yr. Discount further for the vesting schedule (rewards often vest over weeks, adding price risk before you can sell).

3. Subtract impermanent loss: an LP in a volatile pair averages ~-5.7% at a 2x move. `net = emission_apr - IL_drag - gas`. A 20% APR farm on a volatile pair can net below simply holding.

4. Separate real yield from emissions: fees paid in stables or ETH are real; emissions are dilution. `real_yield = fee_apr`; the rest is emission yield. If emissions exceed 80% of APR, the position is an emissions bet.

5. Gauge/boost mechanics: veToken boosts multiply your share of emissions but require locking the native token, adding a second exposure. Recompute share = `(your_ve + staked)/(total_ve + total_staked)`.

6. Exit cost: check the pool's exit fee (some charge 0.5–1%) and any token transfer tax, then compute break-even holding = `(entry + exit cost) / daily rate`.

7. Compare against a stablecoin-only yield (e.g. a lending market at 5%) — the farm must beat that on a risk-adjusted basis after IL and decay, or the capital belongs elsewhere.

## Pitfalls

- Comparing gross emission APR across farms with different reward tokens — a 300% APR in a token that halves is a 150% APR and still falling.
- Ignoring that emissions into an LP are sold by everyone, so the quoted price is the price before the sell pressure your own farming creates.
- Counting a vesting schedule's nominal APR while tokens are illiquid; realized value requires the unlock.

## Verification

    python3 -c "print(100000*2/50e6*365, 100000*2/50e6*365/2)"
    1.46 0.73

Daily $200k on $50M is 1.46x/yr gross; halve it for reward-token decay.

Report gross APR, decayed APR, IL drag, real-yield share, and break-even period.
