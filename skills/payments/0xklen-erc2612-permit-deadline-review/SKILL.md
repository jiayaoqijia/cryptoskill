---
name: erc2612-permit-deadline-review
description: Use when reviewing or issuing an ERC-2612 permit signature. Sets a short deadline, caps the approved value, verifies spender and nonce, and checks the domain before signing.
---

# Review an ERC-2612 permit deadline

A permit is an approval with no transaction and no gas, and it stays valid until its deadline expires. This skill bounds that window to minutes, caps the amount, and verifies the spender and nonce so a leaked or replayed permit cannot move the whole balance.

## Procedure

1. Read the token's current permit nonce for the owner; a replayed permit with the same nonce reverts, but a fresh one is dangerous:
   `cast call $TOKEN "nonces(address)(uint256)" $OWNER --rpc-url $RPC`
2. Verify the domain the permit is bound to:
   `cast call $TOKEN "DOMAIN_SEPARATOR()(bytes32)" --rpc-url $RPC`
   Confirm the token supports EIP-2612 by checking that `permit`, `nonces`, and `DOMAIN_SEPARATOR` all exist.
3. Set the deadline tightly. For an interactive flow use `deadline = now + 1200` seconds (20 minutes); never `type(uint256).max`, which is a permit that never expires.
4. Set `value` to the exact amount needed, not `MAX_UINT256`. A permit to `MAX` is an unlimited approval that costs the attacker no gas to obtain.
5. Confirm the `spender` is the contract you intend (a router or vault) and not an arbitrary address.
6. Confirm the `owner` in the permit is the address you are signing from and not one derived from a different path.
7. Sign only after re-reading the spender and value in the wallet UI, and confirm the chain id in the domain.
8. If you are the verifier, enforce a maximum acceptable deadline on-chain and revert anything longer.

## Pitfalls

- A permit with a far-future deadline is functionally an unlimited, unrevocable approval; revoking it requires either an on-chain `approve` reset or waiting out the deadline.
- Permits are front-runnable: anyone who sees a pending permit can submit it first and consume the nonce. Set short deadlines and submit promptly.
- A permit for one token, signed for the wrong `spender`, can be presented to any contract that calls `permit` on that token.
- EIP-2612 support is not universal; tokens without it silently lack `permit`, and calling it reverts or, on some proxies, does nothing.
- The `value` in a permit is the allowance amount, not a transfer amount; setting it to `MAX` is an approval, not a payment.

- A permit signed over a chain with a forked twin is replayable there if the domain omits the chain id.
- Reading `nonces` from a stale block can show an old value; read at `latest` right before signing.
- A UI that hides the deadline is hiding the single field that governs how long the risk lasts.

## Verification

    cast call $TOKEN "nonces(address)(uint256)" $OWNER --rpc-url $RPC && cast call $TOKEN "DOMAIN_SEPARATOR()(bytes32)" --rpc-url $RPC
    # expect a monotonically increasing nonce and a domain separator matching the token

Report the permit nonce, the domain separator, the spender, and the chosen deadline in seconds, with the commands behind them.
