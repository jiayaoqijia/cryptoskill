---
name: compute-constant-product-lp-share-value
description: Use when pricing a share of an x*y=k AMM pool, adding or removing liquidity, or checking whether an LP mint is fair. Derives reserves, LP token supply, and the USD value of a position from on-chain data.
---

# Compute constant-product LP share value

An LP token is a claim on a fraction of pool reserves; mint and burn amounts follow the `sqrt(x*y)` invariant, and getting the arithmetic wrong silently dilutes existing LPs or overpays a depositor.

## Procedure

1. Read reserves and total supply:

   cast call $PAIR "getReserves()(uint112,uint112,uint32)" --rpc-url $RPC

2. Define the invariant liquidity `L = sqrt(x_0 * y_0)` in raw base units. `token0`/`token1` are sorted by address, not by symbol — confirm which side is ETH before dividing.

3. First mint mints `sqrt(dx*dy)` LP tokens and requires `sqrt(dx*dy)/L == dy/y_0 == dx/x_0` (within the 0.5% k-check). A subsequent mint mints `total_supply * dx / x_0`, which must also equal `total_supply * dy / y_0`.

4. Worked example — pool 100 ETH / 200,000 USDC:
   - `L = sqrt(100 * 200000) = 4472.135` (human units).
   - deposit 1 ETH + 2,000 USDC (ratio 1:2000, exactly fair).
   - minted = `4472.135 * 1/100 = 44.72` LP tokens.
   - new `L = 4516.855`, depositor owns `44.72/4516.855 = 0.990%` of the pool.

5. Value a position: `share = lp_balance / total_supply`; `value_usd = share * (x*p_x + y*p_y)`.

6. Removing: `amount0 = x * burn / total_supply`, `amount1 = y * burn / total_supply`. Verify the LP balance with:

   cast call $PAIR "balanceOf(address)(uint256)" $LP --rpc-url $RPC

7. Sanity check the implied spot `y/x` against an external oracle; a mismatch > 1% between reserves says one side is stale or skewed.

## Pitfalls

- Mixing decimals: USDC has 6, ETH 18, so a naive `sqrt(x*y)` in JS loses precision and the mint reverts on the k-check. Use BigInt throughout.
- Assuming a mint is fair because the USD amounts match — it is the token-ratio that must match, and the ratio is set by the (possibly manipulated) reserves.
- Forgetting the pool can be skewed by a just-before sandwich: minting at skewed reserves mints fewer LP tokens than fair, gifting value to the attacker.

## Verification

    python3 -c "import math; print(math.sqrt(100*200000), 4472.135*1/100)"
    4472.135... 44.72135

Matches the mint amount implied by the depositor's reserves ratio. A divergence means the pool reserves were read after a blocking transaction.

Report reserves, L, share, and USD value, each with the `getReserves` call and block behind it.
