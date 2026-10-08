---
name: send-a-cross-domain-message-and-verify-it
description: Use when sending a message or value between L1 and L2 through the canonical messenger and you must confirm delivery on the destination, not just submission.
---

# Send a cross-domain message and verify it

Submitting a cross-domain message is only the first half: the destination messenger relays it
asynchronously, and a message can be sent successfully yet never execute (or execute and revert), so
verification reads the destination's own delivery record.

## Procedure

1. Pick the canonical messenger, not a token bridge. OP Stack exposes `L1CrossDomainMessenger`
   (0x25ace71c97B33Cc4729CF772ae268934F7ab5fA1 on mainnet) and its L2 counterpart
   (0x4200000000000000000000000000000000000007). Arbitrum uses its Inbox/Outbox and retryable tickets.

2. Send with a sufficient `minGasLimit` / L2 gas limit for the destination call; too low and the relay
   reverts and the message must be replayed.

       cast send $L1_CROSS_DOMAIN_MESSENGER \
         "sendMessage(address,bytes,uint32)" $TARGET $CALLDATA 200000 \
         --value 0 --rpc-url $L1RPC --private-key $KEY

3. Capture the `messageHash` from the `SentMessage` event on the source chain. On OP Stack the hash is
   `keccak256(abi.encodeWithSignature("relayedMessage(bytes32)", hash))`-related; read it from logs:

       cast logs --address $L1_CROSS_DOMAIN_MESSENGER "SentMessage(address,address,bytes,uint256,uint256)" --rpc-url $L1RPC

4. Verify delivery by reading the destination messenger's record, which is authoritative:

       cast call $L2_CROSS_DOMAIN_MESSENGER "successfulMessages(bytes32)(bool)" $MSG_HASH --rpc-url $L2RPC

   `true` means it executed; `false` after the message was sent means it is pending or failed.

5. Confirm the *effect*, not just the flag. Read the state the destination call was supposed to change,
   because a relayed-but-reverted message can leave `successfulMessages` untouched while the target is
   unchanged.

6. For Arbitrum retryable tickets, read the ticket's status; a failed ticket can be redeemed manually
   with the same calldata, so treat "created but not executed" as recoverable:

       cast call $ARB_RETRYABLE "..." ... --rpc-url $L1RPC   # or use the Arbitrum SDK status

7. Record source tx, message hash, destination tx, and the verified state change together.

## Pitfalls

- Treating a successful L1 send as delivery; the relay is a separate step and can be delayed or fail.
- Under-providing the destination gas limit — the classic reason an OP cross-domain message reverts.
- Verifying `successfulMessages` on the wrong messenger (the L1 one when awaiting L2 delivery).
- Confusing a token bridge message with a messenger message; the two have distinct contracts and
  events.
- Ignoring that a reverted Arbitrum retryable is still redeemable (and will expire if not), leaving
  funds stranded.

## Verification

    cast call $L2_CROSS_DOMAIN_MESSENGER "successfulMessages(bytes32)(bool)" $MSG_HASH --rpc-url $L2RPC
    cast receipt $DEST_TXHASH --rpc-url $L2RPC --field status
    cast call $TARGET "balanceOf(address)(uint256)" $BENEFICIARY --rpc-url $L2RPC

Report the source tx, the `SentMessage` hash, the destination delivery flag, and the observed target
state change, each with the call that produced it.
