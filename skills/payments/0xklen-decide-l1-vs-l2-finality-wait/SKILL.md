---
name: decide-l1-vs-l2-finality-wait
description: Use when choosing how many confirmations to wait before crediting funds, reconciling an L2 deposit, or timing a withdrawal: covers L1 slots/epochs, L2 soft versus hard finality, and the 7-day L2->L1 exit.
---

# Decide L1 vs L2 finality wait

Finality differs by layer and direction: an L1 deposit is safe in ~2 epochs, an L2 deposit is soft-confirmed in seconds but not final until the batch posts, and an L2->L1 exit is a fixed 7-day window on optimistic rollups.

## Procedure

1. Know the clocks:
   - Ethereum L1: 12s slots, finality ~2 epochs = 64 slots ≈ 12.8 min. Reorgs past 1–2 blocks are effectively impossible after finality.
   - Optimism/Base: sequencer soft-confirms ~2s; the batch posts to L1 within minutes; the challenge/finality window is a 7-day fault-proof period.
   - Arbitrum: ~250ms sequencer, similar L1 posting; challenge window ~6.4 days.
   - zkSync/Starknet: a validity proof posts in minutes to hours, then L1 finality follows.

2. Set a deposit-credit policy by risk:
   - Exchanges crediting L2 USDC typically wait ~10–30 L2 confirmations (~1–2 min), a safety/abuse buffer rather than protocol finality.
   - A treasury crediting an L2 deposit should wait for the batch containing it to post to L1 and, for strict accounting, for L1 finality (~15 min).

3. L2->L1 withdrawal is not instant. The `proveWithdrawalTransaction` + `finalizeWithdrawalTransaction` pair enforces a 7-day delay on Optimism. Budget it; fast bridges that front it charge a fee and add counterparty risk.

4. Reorg safety: an L2 can reorg its own blocks if the sequencer restarts, so a soft-confirmed L2 deposit can vanish in that window. Never treat a 2s L2 confirmation as final for value transfer.

5. Verify a batch landed on L1 by reading the L1 inbox/portal for the batch covering your L2 block:

    cast block-number --rpc-url $L1_RPC ; cast block-number --rpc-url $L2_RPC

## Pitfalls

- Treating the L2 sequencer's "finalized" tag as L1 finality — it means ordered, not accepted by L1.
- Assuming all L2s exit in 7 days; zk rollups exit faster, and some L3s route through their own bridge with a different delay.
- Ignoring L1 data-gas cost: a batched L2 tx finalizes only when the batch lands, which under L1 congestion can slip.

## Verification

    cast block-number --rpc-url $L1_RPC ; cast block-number --rpc-url $L2_RPC

Confirm the L2 block's batch is included in an L1-final block; only then is the deposit final.

Report the direction, the confirmation policy chosen, and the L1 batch block observed.
