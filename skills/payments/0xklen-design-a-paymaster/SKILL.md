---
name: design-a-paymaster
description: Use when building or reviewing a paymaster that sponsors gas for ERC-4337 UserOperations, and you must avoid the deposit-drain and replay failure modes.
---

# Design a paymaster

A paymaster pays gas on behalf of users by depositing ETH into the EntryPoint and validating
each op. The security of the design rests on three things: a replay-proof signature, a hard
spend cap, and a `postOp` that cannot be griefed into draining the deposit.

## Procedure

1. Fund the paymaster's EntryPoint deposit. `balanceOf` on the EntryPoint is the spendable
   balance; the paymaster's own ETH balance is irrelevant to the EntryPoint.

       cast send $ENTRYPOINT "deposit()" --value 1ether --account paymaster --rpc-url $RPC
       cast call $ENTRYPOINT "balanceOf(address)(uint256)" $PAYMASTER --rpc-url $RPC

2. Stake the paymaster if its validation reads external state (ERC-20 price, allow-list).
   Unstaked paymasters hit storage-access rules and bundlers reject the op.

       cast send $ENTRYPOINT "addStake(uint32)" 86400 --value 1ether \
         --account paymaster --rpc-url $RPC

3. In `validatePaymasterUserOp`, verify an EIP-712 signature over the `userOpHash` (which
   commits to chain id and EntryPoint), check the op against a per-sender allowance, and write
   that allowance down so the same signed intent cannot be replayed.
4. Return `validationData` packed as `(aggregator, validUntil, validAfter)`; set `validUntil`
   to a short window (e.g. now + 5 minutes) for one-shot sponsorships so an expired signature
   cannot be reused.
5. Cap the gas the op may consume: bound `verificationGasLimit`, `callGasLimit` and
   `paymasterVerificationGasLimit` in your signing policy, and reject ops above the cap before
   signing.
6. Implement `postOp` to charge the actual `actualGasCost` and keep it gas-cheap; a revert or
   OOG there reverts the whole op.

## Pitfalls

- Unlimited sponsorship with no per-user cap lets anyone drain the deposit in a loop; require an
  allowance that decreases before signing.
- Signing over the userOp fields without the chain id and EntryPoint address enables cross-chain
  and cross-EntryPoint replay.
- A paymaster whose `postOp` does external calls or loops can be griefed into out-of-gas,
  reverting the user's op; keep `postOp` O(1) and storage-only.
- An ERC-20 paymaster that prices gas from a spot DEX quote is manipulable — an attacker moves
  the pool, the paymaster undercharges, and the deposit bleeds.
- Depositing to the wrong EntryPoint version (v0.6 vs v0.7) leaves the v0.7 deposit at zero and
  bundlers reject every op.
- Forgetting `addStake` when validation touches external storage causes bundlers to drop the op
  with a "paymaster not staked" simulation error.

## Verification

    cast call $ENTRYPOINT "balanceOf(address)(uint256)" $PAYMASTER --rpc-url $RPC   # before
    curl -s -X POST "$BUNDLER" -H 'content-type: application/json' \
      --data '{"jsonrpc":"2.0","id":1,"method":"eth_estimateUserOperationGas",
               "params":[{"sender":"0x...","callData":"0x...","paymaster":"'$PAYMASTER'"},"'$ENTRYPOINT'"]}' | jq .
    cast call $ENTRYPOINT "balanceOf(address)(uint256)" $PAYMASTER --rpc-url $RPC   # after: lower

Report the EntryPoint deposit before and after a sponsored op, confirming it decreased by
roughly the op's actual gas cost.
