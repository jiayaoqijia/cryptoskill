---
name: multisig-threshold-and-signer-rotation
description: Use when configuring a Safe or similar multisig, or when rotating a signer. Chooses a threshold that resists both theft and lockout, and orders add/set/remove so the wallet is never briefly ungovernable.
---

# Multisig threshold and signer rotation

The threshold is a trade between an attacker's difficulty and your own ability to sign under pressure. This skill picks M-of-N with concrete rules and rotates signers without ever leaving the wallet below a working quorum.

## Procedure

1. Choose M so that a single compromised signer cannot move funds and a single unavailable signer cannot freeze them. 3-of-5 and 4-of-7 are the common targets; avoid 1-of-N (no protection) and N-of-N (no redundancy).
2. Read the current configuration before changing anything:
   `cast call $SAFE "getThreshold()(uint256)" --rpc-url $RPC`
   `cast call $SAFE "getOwners()(address[])" --rpc-url $RPC`
3. Rotate in the safe order: **add the new signer first**, raise the threshold if needed, then **remove the old signer last**. Removing before adding can drop the signature count below the threshold and lock you out.
4. Execute the rotation as multisig calls, not a single owner action: `addOwnerWithThreshold(newSigner, newThreshold)`, then `removeOwner(prevOwner, oldSigner, finalThreshold)`.
5. Keep signer keys on separate hardware devices and in separate physical locations; a multisig of five keys on one laptop is a single-signer wallet.
6. Record the new owner set and threshold, and confirm at least M signers can still reach their device after the change.
7. Announce the rotation to co-signers out of band so a stolen or unexpected owner is spotted immediately.

## Pitfalls

- `removeOwner` requires the owner that precedes the removed one in the linked list; passing the wrong `prevOwner` corrupts the owner list.
- Raising the threshold above the number of currently reachable signers bricks the wallet until enough devices are recovered.
- A `swapOwner` looks atomic but still needs M signatures; if those signers are offline during an incident the rotation stalls.
- Changing owners at a predictable time is observable; an attacker with one key can front-run a rotation. Use a private submission channel for the rotation transaction.
- A threshold of 1 in a "multisig" is a single signer with extra steps and no protection.
- Adding a signer without raising the threshold lowers the effective security of the wallet.

- Threshold changes emit events; a rotation you did not authorize is the earliest sign of an owner compromise.
- A signer who only ever signs from a hot browser wallet defeats the multisig's device separation.
- Keep one offline backup signer able to reach the threshold if two online signers are lost at once.

## Verification

    cast call $SAFE "getOwners()(address[])" --rpc-url $RPC && cast call $SAFE "getThreshold()(uint256)" --rpc-url $RPC
    # expect the intended owner set and M <= count of reachable signers

Report the resulting owner set, the threshold, and the number of reachable signers, with the commands behind them.
