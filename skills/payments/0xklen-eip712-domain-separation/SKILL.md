---
name: eip712-domain-separation
description: Use when signing or verifying EIP-712 typed data. Confirms every domain field — name, version, chainId, verifyingContract, salt — matches the intended target and rejects under-specified domains.
---

# Enforce EIP-712 domain separation

The EIP-712 domain is what binds a signature to one contract on one chain; an omitted field widens the set of places a signature is valid. This skill checks each domain field against the target and refuses signatures whose domain is incomplete.

## Procedure

1. Read the actual domain separator from the contract and compare it to the one you hashed:
   `cast call $CONTRACT "DOMAIN_SEPARATOR()(bytes32)" --rpc-url $RPC`
2. Verify the five declared fields of the domain:
   - `name` — matches the contract's `name()` (or the exact string it uses),
   - `version` — e.g. `"1"`; a version bump changes every signature,
   - `chainId` — must be present and equal the live chain (`cast chain-id --rpc-url $RPC`),
   - `verifyingContract` — must equal the address actually verifying,
   - `salt` — required only when `verifyingContract` is absent; not both, not neither.
3. Recompute the domain hash locally and compare to step 1:
   ```javascript
   import { hashDomain } from 'viem';
   const domain = { name: 'MyToken', version: '1', chainId: 1, verifyingContract: token };
   console.log(hashDomain({ domain }));
   ```
4. For typed data, print the full message struct and confirm the wallet displays the same fields you signed. If the wallet shows a raw hash instead of the struct, do not sign.
5. Reject any domain missing `chainId` or `verifyingContract`, or using a wildcard.

## Pitfalls

- Two contracts deployed at the same address on two chains with identical domains accept each other's signatures; the `chainId` field is the only separator.
- An uninitialized `DOMAIN_SEPARATOR` cache can return a stale value after a chain fork; re-read it on the new chain.
- `salt` and `verifyingContract` together are redundant and some verifiers reject it; use exactly one.
- A wallet that renders the struct but hashes a different domain is indistinguishable to the user — always compare the domain hash you computed to the contract's.

## Verification

    cast call $CONTRACT "DOMAIN_SEPARATOR()(bytes32)" --rpc-url $RPC
    # expect it to equal the locally computed hashDomain() for the intended domain

Report the contract's domain separator, the locally computed hash, and whether they match, quoting the commands.
