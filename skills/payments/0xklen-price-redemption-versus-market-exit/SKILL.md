---
name: price-redemption-versus-market-exit
description: Use when a stablecoin holder must convert and the market is off peg. Compares exiting at the issuer for par against selling into a pool, including the size-dependent slippage.
---

# Price redemption versus market exit

When you need out there are two doors: redeem at the issuer for par (with fees and a wait) or sell into the market now at whatever the book pays. Price both at your actual size before choosing.

## Procedure

1. Get the market quote for your exact size, not the mid:
   `cast call $CURVE "get_dy(int128,int128,uint256)(uint256)" $i $j $AMOUNT --rpc-url $RPC`
   The `get_dy` for the full size embeds the slippage you will actually pay.
2. Get the issuer terms: redemption fee, minimum size, KYC requirement, and settlement time.
3. Compute the market proceeds after slippage and any pool fee:
   `python3 -c "print(round(amount*price*(1-slip),2))"`.
4. Compute the redemption proceeds: `amount - fee`, discounted for T+N settlement at the cost of capital.
5. Compare: if the market pays more than redemption minus time cost and is deep enough to absorb size without moving, sell; otherwise redeem.
6. For large size, split across venues and model the marginal price of each tranche rather than the average.

## Pitfalls

- Quoting `get_dy` at 1 unit and extrapolating to a 10M exit; slippage is convex, not linear.
- Forgetting the redemption fee is often waived for large primary dealers but charged to retail.
- Ignoring that a market exit crystallises a taxable disposal while a redemption may be a 1:1 exchange of like assets.
- Selling into the same pool as everyone else during a depeg: the exit door narrows exactly when you want it.
- The market quote can be better than par in a premium depeg, which is its own arbitrage with its own gate.
- A pool's `get_dy` reverts or returns nonsense when reserves are imbalanced near an empty side; guard the call.
- Routing through an aggregator adds a hop whose slippage the direct quote hides.
- Redemption proceeds may land in a bank account you cannot instantly wire out; the second leg has its own delay.

## Verification

    cast call $CURVE "get_dy(int128,int128,uint256)(uint256)" $i $j $AMOUNT --rpc-url $RPC
    python3 -c "print(round(market_net - redeem_net, 2))"   # positive => sell into market

Report both net proceeds at your real size, the settlement time of each, and the chosen exit.
