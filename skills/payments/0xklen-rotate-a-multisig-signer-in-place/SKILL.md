---
name: rotate-a-multisig-signer-in-place
description: Use when a multisig owner must be replaced without redeploying the Safe. Swaps the owner with swapOwner, watches the threshold, and verifies the new signer controls the address before the old one is trusted to be gone.
---

# Rotate a multisig signer in place

Redeploying moves every asset and resets every approval; `swapOwner` replaces one owner and keeps the address and threshold, so the rotation is cheap and reversible-looking. This skill changes one owner at a time and proves the new key works before declaring the old one retired.

## Procedure

1. Record the current owners, threshold, and nonce:
   `cast call $SAFE "getOwners()(address[])" --rpc-url $RPC && cast call $SAFE "getThreshold()(uint256)" --rpc-url $RPC`
2. Have the incoming signer prove they control the new address by signing a message, and verify it, before it is added:
   `cast wallet verify --address $NEW_SIGNER "rotate-$SAFE-$(date +%s)" <signature>`
3. Build the `swapOwner(prevOwner, oldOwner, newOwner)` call. The `prevOwner` is the owner that precedes `oldOwner` in the linked list; get it wrong and the call reverts.
4. Route the swap through the normal signing ceremony: each signer recomputes the Safe transaction hash from the fields, not from the proposer's summary.
5. Expect the threshold to be unchanged. If owners drop below `t`, the Safe is bricked for normal execution — raise the threshold before removing if the count would fall under it.
6. After execution, confirm the owner set changed by exactly one address and the threshold is unchanged:
   `cast call $SAFE "getOwners()(address[])" --rpc-url $RPC`
7. Rotate one owner per transaction. Two swaps in one batch invite a prevOwner ordering bug that reverts the whole batch.

## Pitfalls

- Passing a stale `prevOwner` after another owner was removed earlier in the list reverts the swap; re-read the owner list immediately before building the call.
- Adding the new signer before verifying they control the address can strand quorum on a key nobody holds.
- Forgetting that a DelegateCall or a module can add owners through a different path; check modules are what you expect after rotation.
- Rotating to a signer on the same device or location as the one being replaced provides no resilience gain.
- The old owner should be removed, not merely "no longer used" — a live key is a live key until the Safe no longer counts it.
- A Safe with `threshold == n` tolerates no owner loss; rotating under that config means one failure bricks execution.
- Guard and module state is unaffected by `swapOwner`, but the guard's own signer list must include the new signer if it gates signer actions.
- Verify the new signer is a key that can actually sign, not a contract address with no signer.
- Update the address registry and the custody runbook in the same change, or the doc drifts from the chain.

## Verification

    cast call $SAFE "getOwners()(address[])" --rpc-url $RPC && cast call $SAFE "getThreshold()(uint256)" --rpc-url $RPC
    # expect exactly one address changed and the threshold identical to before

Report the old and new owner addresses, the threshold before and after, and the confirming read, quoting the outputs.
