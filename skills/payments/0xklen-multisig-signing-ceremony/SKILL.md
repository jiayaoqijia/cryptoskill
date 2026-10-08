---
name: multisig-signing-ceremony
description: Use when executing a multisig transaction with signers on separate devices. Recomputes the Safe transaction hash independently, confirms the payload out of band, and collects only verified signatures.
---

# Run a multisig signing ceremony

A multisig only protects you if each signer verifies the payload rather than trusting the proposer's summary. This skill recomputes the hash of the exact transaction on every signer's own machine and refuses signatures that do not match.

## Procedure

1. The proposer publishes the fields — `to`, `value`, `data`, `operation`, `safeTxGas`, `baseGas`, `gasPrice`, `gasToken`, `refundReceiver`, `nonce` — over a channel separate from the one carrying the signature.
2. Every signer independently computes the EIP-712 hash from those fields, using the Safe's `domainSeparator` and the same `safeTxHash` struct, and compares it to the proposer's hash:
   ```javascript
   import { hashTypedData } from 'viem';
   const safeTxHash = hashTypedData({
     domain: { chainId: 1, verifyingContract: safe },
     types: safeTxTypes, primaryType: 'SafeTx', message: txFields,
   });
   ```
3. Confirm the `safeTxHash` shown on the hardware device equals the independently computed hash. If not, stop.
4. Verify the `data` decodes to the intended call and the `to` address is the intended target, on each signer's own machine:
   `cast calldata-decode "<sig>" <data>`
5. Confirm the Safe nonce is the next expected one; a stale nonce means another tx queued and the payload is out of band:
   `cast call $SAFE "nonce()(uint256)" --rpc-url $RPC`
6. Collect the signatures, confirm the count reaches M, and execute. Verify the executed tx hash and that the Safe nonce incremented by exactly one.

## Pitfalls

- Signing from a link that fills the payload for the device is exactly the attack: a signer must type or copy fields into their own tooling, not trust a pre-filled form.
- Two different transactions with the same Safe nonce both hang in the queue; one executes and the other is stranded.
- `operation = 1` (delegatecall) changes the signature semantics and is far more dangerous than a `call`; require explicit review.
- Off-chain signatures can be collected over hours; a field change between the first and last signature invalidates the hash for the late signers and should be detected, not ignored.

## Verification

    cast call $SAFE "nonce()(uint256)" --rpc-url $RPC && cast calldata-decode "<sig>" <data>
    # expect the nonce to have advanced by one and the calldata to decode to the intended call

Report the independently computed `safeTxHash`, the decoded call, and the pre/post Safe nonce, with the commands behind them.
