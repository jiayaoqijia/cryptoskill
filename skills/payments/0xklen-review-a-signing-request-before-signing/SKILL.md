---
name: review-a-signing-request-before-signing
description: Use when asked to approve a transaction or message. Decodes calldata, resolves addresses to labels, checks amount, spender, chain, and contract verification, and refuses to sign anything unreadable.
---

# Review a signing request before signing

The last chance to stop a drain is the moment before the signature, not after. This skill turns the raw request into named fields a human can check and blocks the signature if any field is unknown or unexplained.

## Procedure

1. Decode the calldata. You must be able to name the function and every argument:
   `cast calldata-decode "transfer(address,uint256)" 0xa9059cbb000000000000000000000000...`
   If the selector is unknown, resolve it:
   `cast 4byte 0x095ea7b3` → `approve(address,uint256)`
2. Resolve every address to a label. Never sign to a bare hex string:
   - the `to` address: is it a verified contract? check the explorer for a source match,
   - the spender/operator/recipient: is it the entity you expect,
   - check for a lookalike (first and last 4 hex chars can match while the middle differs).
3. Check the value and the amount independently on both sides of the same unit:
   `cast to-unit 1000000 --ether` → confirm the decimal amount, do not eyeball raw 1e6-scale integers.
4. Confirm the chain id and the chain the RPC is on before you trust any label:
   `cast chain-id --rpc-url $RPC`
5. Simulate the exact transaction and read the asset deltas:
   `cast run <txhash> --fork-url $RPC`
6. For approvals, verify the amount is the minimum needed, not `2^256-1`, and check the spender against your allowlist.
7. Only if every field maps to a name and an expected effect, sign.

## Pitfalls

- `approve(spender, MAX_UINT256)` is indistinguishable from a theft grant once signed; treat unlimited approval as a critical finding.
- A decoded function name can lie. Compare the selector to the verified source, not to a name in a UI.
- Address poisoning works because humans compare prefixes; compare the full 40 hex characters or paste them into a tool.
- Signing for a chain id you did not verify lets the same signature be replayed on another chain.

## Verification

    cast calldata-decode "<sig>" <data> && cast 4byte <selector> && cast chain-id --rpc-url $RPC
    # expect a named function, a real signature, and the chain id you intended

Report the decoded function, the resolved spender and recipient, the amount in human units, and the chain id, with each command behind it.
