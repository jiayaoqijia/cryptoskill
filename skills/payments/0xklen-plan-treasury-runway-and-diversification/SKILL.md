---
name: plan-treasury-runway-and-diversification
description: Use when assessing a DAO or protocol treasury: computes stable-denominated runway, flags native-token concentration, and sets a diversification and payout policy.
---

# Plan treasury runway and diversification

A treasury's runway is measured in stable assets divided by stable burn; a treasury that is 80% its own token has a long paper runway and a short real one, because selling it is the price.

## Procedure

1. Split the treasury by asset class — stables, blue-chip (ETH/BTC), and native token — and report each in USD and %.

2. Compute monthly burn and runway. Worked example: $10M treasury, $400k/month burn in stables. If stables are 30% ($3M), real runway = `3,000,000/400,000 = 7.5 months`. A headline "$10M/400k = 25 months" wrongly assumes the native token sells at today's price with no impact.

3. Compute liquidation-adjusted native value: selling size eats its own liquidity. Realizable ≈ `min(notional, 20% * pool_liquidity)`; a token with $5M pool depth cannot realize $3M without ~15% impact.

4. Set policy targets: >= 12 months of burn in stables, <= 25% in the native token, and a rule to convert a fixed share of native inflows (e.g. 50% of protocol fees) to stables monthly rather than in one block.

5. Model a stress case — native price -50%, burn +50% — and recompute runway:

   python3 -c "print(3e6/400000, 3e6/(400000*1.5))"
   7.5 5.0

6. Match the payout source to a stable stream; paying contributors in the native token passes the price risk to them and depresses the token further.

## Pitfalls

- Counting unsold native tokens at spot as runway; the treasury can only spend what the market will absorb.
- Ignoring that most DAO native holdings are locked or thinly traded governance tokens whose sale moves price more than the cash raised.
- Assuming burn is fixed: audits, grants, and buybacks spike it exactly when the token is cheapest.

## Verification

    python3 -c "print(3e6/400000, 3e6/600000)"
    7.5 5.0

Stables divided by burn gives the honest runway; stress it with burn * 1.5.

Report each asset class, stable runway, stress runway, and the concentration flag.
