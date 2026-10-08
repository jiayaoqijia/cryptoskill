---
name: force-include-a-transaction-through-l1-inbox
description: Use when a sequencer is censoring or halting your transaction and you need to force it onto the L2 by submitting through the L1 inbox or deposit contract.
---

# Force include a transaction through the L1 inbox

The canonical liveness escape on an L2 is to route the transaction through L1, where the sequencer has
no choice but to include it after a timeout — but each rollup exposes a different contract, and the
path only works if you build the exact message the inbox expects.

## Procedure

1. Identify the rollup family and its inbox contract before writing anything.
   - Arbitrum: the delayed inbox, address `0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f`.
   - OP Stack: the `OptimismPortal` deposit path (L1 to L2 always works); it is a deposit, not an
     arbitrary forced call, so encode accordingly.
   - zkSync Era: `requestL2Transaction` on the mailbox plus the priority queue.
   - Starknet: an `L1Handler` message consumed on L2.

2. For Arbitrum, submit an unsigned L2 transaction to the delayed inbox. The sequencer must include
   the delayed inbox within its grace period (24 h on Arbitrum One), after which anyone can call
   `forceInclusion` on the `SequencerInbox`:

       cast send 0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f \
         "sendUnsignedTransaction(uint256,uint256,uint256,address,uint256,uint256,bytes)" \
         800000 0 0 $TARGET 0 10000000000000000 0x<calldata> \
         --value 0 --rpc-url $L1RPC --private-key $L1KEY

3. For OP Stack, use the L1 standard bridge or portal deposit; the deposit is enqueued and executed by
   the sequencer on the L2, and remains executable even if the regular mempool is uncooperative:

       cast send $L1_STANDARD_BRIDGE \
         "depositETH(uint32,bytes)" 200000 0x --value 1ether --rpc-url $L1RPC

4. Record the L1 receipt and the message/leaf that was enqueued. For Arbitrum note the `InboxMessageDelivered`
   event and the ticket index; for OP note the `TransactionDeposited` event's deposit hash.

5. Poll for inclusion on the L2. If the sequencer honours the inbox, it appears within its normal
   latency; if not, wait out the grace period and trigger forced inclusion.

6. Budget the cost honestly: forced inclusion pays full L1 gas plus the L2 execution cost, and the
   calldata is not compressed the way the batcher's is, so a forced call is often an order of
   magnitude more expensive than a normal L2 transaction.

7. Log the transaction hashes on both L1 and L2 and the wall-clock latency so the escape's real
   speed is known for the next incident.

## Pitfalls

- Sending to the regular bridge when the sequencer is censoring *your address* — the deposit path is
  processed by the same sequencer, so verify the inbox contract is the force-inclusion path.
- Getting the gas limit or refund fields wrong on an Arbitrum unsigned transaction; the ticket can be
  created but fail to redeem, leaving funds stuck in the retryable.
- Assuming forced inclusion bypasses the L2 fee — it does not; the L2 execution still needs gas.
- Using an L1 account with insufficient ETH for L1 gas; the escape is gas-expensive exactly when L1 is
  congested.
- Forgetting that some chains (OP Stack historically) do not offer arbitrary forced L2 calls at all —
  only deposits — so a "forced transfer" for an existing L2 balance may be impossible.

## Verification

    cast receipt $L1_TXHASH --rpc-url $L1RPC --field status
    cast tx $L2_SEARCH_HASH --rpc-url $L2RPC   # once included, or read the queued message on L1
    # Arbitrum: the delayed-inbox message index advanced and, if needed, forceInclusion succeeded

Report the inbox contract used, the L1 transaction hash, the grace-period timer, and whether the
transaction executed on the L2 within it.
