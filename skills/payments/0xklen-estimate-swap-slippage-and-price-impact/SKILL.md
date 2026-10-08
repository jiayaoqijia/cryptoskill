---
name: estimate-swap-slippage-and-price-impact
description: Use when sizing a swap, setting a minimum-received value, or separating pool fee from price impact. Computes Uniswap v2/v3 output and slippage before signing.
---

# Estimate swap slippage and price impact

On an AMM the quoted output bakes in fee plus price impact; conflating them hides how much of a bad fill is the pool moving versus the protocol taking its cut, and a loose `amountOutMin` either reverts or invites a sandwich.

## Procedure

1. Uniswap v2 output with the 0.3% fee (997/1000): `out = (dx * 997 * y) / (x * 1000 + dx * 997)`, where `x`, `y` are the input-side and output-side reserves.

2. Worked example — pool 1,000 ETH / 2,000,000 USDC, sell 20,000 USDC for ETH:

   python3 -c "print((20000*997*1000)/(2000000*1000+20000*997))"
   9.87163...

   So `out = 9.8716 ETH`.

3. Split the effects. Mid price 2,000 USDC/ETH gives a no-impact 10.0 ETH output:
   - total slippage = `1 - 9.8716/10 = 1.284%`.
   - fee = 0.3% (the 997/1000 factor).
   - price impact ≈ `1.284% - 0.3% = 0.984%`, matching `dx/(x+dx) = 20000/1,020,000` scaled.

4. For v3, never estimate — quote:

   cast call $QUOTER "quoteExactInputSingle((address,address,uint256,uint24,uint160))((uint256,uint160,uint32,uint256))" $ARGS --rpc-url $RPC

   The third return value counts initialized ticks crossed; more ticks means more slippage.

5. Set `amountOutMin = quote * (1 - tol)`. For pools with depth > $10M use tol 0.1–0.5%; below $1M use 1–3% and split the order. Tolerance is a sandwich budget: 3% on a $10k swap exposes up to $300.

6. Re-quote immediately before signing; a quote older than one block (12s) is stale on volatile pairs.

## Pitfalls

- Using the `getReserves` spot price as the fill price ignores the impact term entirely on large orders.
- Setting `amountOutMin = 0`, which some router defaults do, hands the whole tolerance to a searcher.
- For fee-on-transfer or rebasing tokens the received amount differs from the quote; measure the actual balance delta, not the quote.

## Verification

    python3 -c "o=(20000*997*1000)/(2000000*1000+20000*997); print(o, 1-o/10)"
    9.87163... 0.012837...

Matches `getAmountsOut` for the same reserves; a divergence means reserves changed between the read and the quote.

Report quoted out, fee, price impact, and tolerance, with the pool and block used.
