---
name: model-peg-arbitrage-credibility
description: Use when judging whether a stablecoin's peg is credible or merely tolerated. Works out the profit of minting and redeeming against a market price and tests whether arbitrage is executable at scale.
---

# Model peg arbitrage credibility

A peg is held by whoever profits from restoring it. If mint/redeem arbitrage is blocked by gates, fees, or capital limits, the peg survives only on sentiment. Model the arbitrage leg by leg and find the size at which it stops paying.

## Procedure

1. Record the market price and the par redemption value: par = 1.00 minus the redemption fee.
2. Loss leg: buy at 0.995 in the market, redeem at 0.999, gross spread `0.004` before costs.
3. Subtract costs: issuer fee (say 0.1%), settlement time (capital cost over T+2 at, e.g., 5% APR, about 0.027%/2 days), and gas.
   `python3 -c "print(round(0.999-0.995-0.001-0.00027,5))"`  -> 0.00273 net.
4. Find the size limit: redemption may be capped per day, KYC-gated, or restricted to whitelisted market makers, which caps the arbitrage and extends the depeg.
5. For crypto-backed coins the arbitrage is PSM-style: `cast call $PSM "tin()(uint256)"` and `tout()` give entry/exit fees; if both are 0 the peg is soft-locked near 1.
6. Stress it: if arbitrage capital absorbs only $X/day and sellers want $10X/day, the peg breaks in proportion to the imbalance.
7. Distinguish "arbitrage profitable" from "arbitrage permitted": the second decides the depeg duration.

## Pitfalls

- Ignoring settlement time: a 1-day wait at 8% APR erodes 0.022% of edge, more than many spreads.
- Assuming a CEX discount can be closed by minting when mint is KYC-gated to primary dealers.
- A "0% fee" PSM with a `line` (debt ceiling) already full provides no arbitrage at all.
- Treating a stable price in one deep pool as evidence of credibility when that pool is subsidised by the issuer.
- Gas and the priority fee spike during a depeg exactly when you need the arbitrage leg to land.
- A spread locked by minting is only earned when the redeemed dollars clear the bank, days later.
- Arbitrage that requires holding a whitelisted status is a privilege, not a market force.
- If the redemption counterparty is the same entity as the issuer, its discretion, not the contract, sets the terms.

## Verification

    python3 -c "print(round(0.999-0.995-0.001-0.00027,5))"
    0.00273
    cast call $PSM "tin()(uint256)" --rpc-url $RPC            # entry fee in wad

Report the net arbitrage edge, the size cap, and whether the peg rests on executable arbitrage or on trust.
