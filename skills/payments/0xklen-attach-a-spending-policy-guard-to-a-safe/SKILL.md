---
name: attach-a-spending-policy-guard-to-a-safe
description: Use when a Safe smart account can send funds but has no on-chain spending policy. Attaches a guard module that blocks transfers above a cap or to non-allowlisted destinations before they execute.
---

# Attach a spending policy guard to a Safe

A multisig stops a single key from moving funds; it does not stop the legitimate signers from being tricked into an unbounded transfer. A guard executes before every transaction and can revert one that violates the policy, adding a mechanical check to the human one.

## Procedure

1. Write or select the guard contract. It implements `checkTransaction` (pre-execution) and `checkAfterExecution` (post), reverting on a violation:
   ```solidity
   function checkTransaction(address to, uint256 value, bytes calldata data, ...) external view override {
       require(elapsedSinceAdded(to) >= COOLDOWN, "destination cooling down");
       require(value <= perTxCap, "over cap");
   }
   ```
2. Deploy the guard and attach it in a test deployment first:
   `cast send $SAFE "setGuard(address)" $GUARD --account <safe-owner> --rpc-url $RPC`
   `setGuard` itself is a Safe transaction and must clear the threshold.
3. Verify the guard is active:
   `cast call $SAFE "getGuard()(address)" --rpc-url $RPC`
4. Confirm a policy-respecting transfer still passes and an over-cap transfer reverts, on a fork or testnet, before attaching on mainnet.
5. Make sure the guard cannot brick the account: an owner must always be able to reach `setGuard`/`disableModule` to remove a faulty guard. Test the removal path.
6. Record the guard address, its storage, and its upgrade authority in the custody runbook.

## Pitfalls

- A guard with a bug can lock the Safe permanently; test the "remove the guard" transaction before you need it.
- Guards watch only the Safe's own calls — funds moved via a module, a delegatecall, or an approved spender bypass `checkTransaction`; constrain those separately.
- Storing the allowlist in the guard means amending it is itself an owner transaction; budget for the signing round.
- A guard that only checks `value` misses token transfers where `value == 0` and the amount is in `data`; decode common selectors.
- Forgetting `checkAfterExecution` means a policy violation inside a batched call can slip through unwatched.

## Verification

    cast call $SAFE "getGuard()(address)" --rpc-url $RPC && cast send $SAFE <over-cap-call> --account <owner> --rpc-url $RPC
    # expect getGuard != 0x0 and the over-cap send to revert

Report the guard address, the cap and cooldown, and the reverted test transaction, quoting the outputs.
