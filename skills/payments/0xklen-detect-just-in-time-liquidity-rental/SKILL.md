---
name: detect-just-in-time-liquidity-rental
description: Use when a swap's execution looks oddly good, or when auditing a block for JIT liquidity: spotting a mint and immediate burn around a swap in one block, and measuring who captured the LP fee.
---

# Detect just-in-time liquidity rental

Just-in-time liquidity is a mint immediately before a large swap and a burn immediately after it inside the same block, so the attacker collects the swap's fee without bearing any inventory risk — a pattern that is invisible in end-state pool balances.

## Procedure

1. Pull the block's logs for the pool and filter for liquidity events adjacent to the swap:

   ```bash
   cast logs --from-block $N --to-block $N --address $POOL \
     "Mint(address,uint256,uint256)" "Burn(address,uint256,uint256)" --rpc-url $RPC
   ```

2. Order the events by log index. A JIT fingerprint is `Mint, Swap, Burn` with the mint and burn from the same address and no intervening swap.

3. Confirm the JIT provider entered and exited in one block by checking its token balances at block boundaries: if its LP balance at `N-1` and `N` are equal (or zero), it held the position for exactly zero blocks.

4. Attribute the fee. Compute the deposit's share of the pool at mint time (`base_liquidity / (base_liquidity + minted)`) — that fraction of the swap fee is what the JIT provider captured, at the expense of passive LPs.

5. Measure the sandwich-adjacent case: if the JIT provider's burn also moves price against the swapper's remaining tolerance, it is a JIT sandwich and the loss to the user is larger than the fee.

6. Compare the sum of DEX fees paid by LPs in the block: if one address captured more than 40% of a pool's fee in a single block with no prior LP history, treat it as JIT.

7. Log the pattern with block, pool, provider, deposit, fee-captured, and whether a sandwich leg is present. Repeat occurrences from one address are a JIT bot, not a market maker.

## Pitfalls

- Looking only at end-of-block state, where the JIT position is gone. The evidence lives in log ordering, not balances.
- Confusing JIT with a legitimate single-block arbitrage that happens to touch liquidity; the arb does not mint LP tokens.
- Ignoring the swap's own logs. A Mint and Burn with no Swap between them is a deposit/withdraw churn, not JIT.
- Missing that a JIT sandwich charges the user twice: the fee and the adverse price move.
- Assuming a specific pool implementation. Balancer, Uniswap v3, and v4 all emit different liquidity events; normalise them first.

## Verification

    cast logs --from-block $N --to-block $N --address $POOL "Mint(address,uint256,uint256)" "Burn(address,uint256,uint256)" --rpc-url $RPC

A `Mint, Swap, Burn` sequence in log-index order from one address, with equal LP balance at block boundaries, confirms JIT. Report the pool, provider, fee captured, and whether a sandwich leg is present.
