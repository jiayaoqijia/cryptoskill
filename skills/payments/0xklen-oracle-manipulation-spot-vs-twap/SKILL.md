---
name: oracle-manipulation-spot-vs-twap
description: Use when a contract prices assets from a pool, pair or oracle that can be moved inside one transaction. Checks whether a spot read is manipulable and pushes to a TWAP or Chainlink feed.
---

# Oracle manipulation: spot vs TWAP

A protocol is only as safe as its price source: any spot value read from a pool that can be traded within the same transaction is free to manipulate for one block.

## Procedure

1. Locate every price read: `grep -nE 'getReserves|slot0|latestRoundData|balanceOf\(|getAmountsOut|price0Cumulative' -r src/`.
2. Classify each source: AMM spot reserves (manipulable), AMM TWAP (costly), Chainlink aggregator (needs staleness/heartbeat checks), internal accounting (trust only if the writer is non-reentrant).
3. For AMM spot reads, compute the flash-loan cost: `cost ≈ 2 * amountIn * fee` on a constant-product pool; a $50m pool with 0.30% fee needs ~$300k to move ~2% — cheap relative to most exploits.
4. Check TWAP window length in seconds: reject any window under 600s for lending/minting logic (`windowSize < 600` is a red flag).
5. For Chainlink, verify all four: `answer > 0`, `updatedAt != 0`, `block.timestamp - updatedAt <= heartbeat`, and a non-zero `answeredInRound`.
6. Confirm the price read is not inside the same block as the action that depends on it, and cache the feed decimals: `AggregatorV3Interface(feed).decimals()`.
7. Simulate a manipulation: on a mainnet fork, take a whale-sized flash loan, swap, call the victim, then revert.

```solidity
uint256 bal = IERC20(WETH).balanceOf(PAIR);
IUniswapV2Pair(PAIR).swap(0, manipAmount, victim, "");
victim.borrow(maxBorrow); // must not under-collateralise
```

8. `forge test --match-test testOracleManip -vvvv` on `--fork-url $ETH_RPC_URL` and inspect the victim's state deltas.
9. Check the fallback path when the oracle reverts or returns stale data — a `try/catch` that defaults to a stale value is exploitable.
10. Record the source, window, manipulation cost, and whether the victim's state changed.

## Pitfalls

- `latestRoundData` read without a staleness check; during an outage the last price is returned forever.
- A "TWAP" computed as the average of two spot reads one second apart — still spot-manipulable.
- Reading `token.balanceOf(pool)` as the price for a share token; an attacker donates to inflate it.
- Chainlink on L2 (Arbitrum/Base) uses sequencer uptime feeds; ignoring the sequencer-down grace period breaks the staleness guard.
- Using `decimals()` of the feed but not of the base token, mixing 8- and 18-decimal maths.

## Verification

    forge test --match-test testOracleManip --fork-url $ETH_RPC_URL -vvvv

Pass: the manipulated-price call reverts or the victim's accounting is unchanged; a failing run shows the victim accepting a position it should refuse.

Report the price source, the manipulation cost in USD, and the test outcome.
