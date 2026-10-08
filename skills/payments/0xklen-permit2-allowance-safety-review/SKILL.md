---
name: permit2-allowance-safety-review
description: Use when a dApp asks for a Permit2 approval or signature. Verifies the Permit2 contract address, sets a bounded amount and expiration, and prefers a scoped signature over an on-chain allowance.
---

# Review a Permit2 allowance

Permit2 replaces per-spender approvals with one token approval to Permit2 plus a scoped allowance to each spender. This skill keeps the outer approval bounded, the inner expiration short, and distinguishes signature-based transfers from standing allowances.

## Procedure

1. Confirm the Permit2 address is the canonical deployment for the chain (Uniswap's Permit2 is the same address on most EVM chains). Verify it on the explorer before approving anything.
2. Approve the token to Permit2, and only as much as needed. The common pattern is a limited approval, not unlimited:
   `cast send $TOKEN "approve(address,uint256)" $PERMIT2 1000000000 --account deployer --rpc-url $RPC`
3. Inspect the inner allowance Permit2 records for a spender:
   `cast call $PERMIT2 "allowance(address,address,address)(uint160,uint48,uint48)" $OWNER $TOKEN $SPENDER --rpc-url $RPC`
   The return is `(amount, expiration, nonce)`. Confirm `expiration` is near-term (for example now + 3600) and `amount` is bounded.
4. Prefer `SignatureTransfer` (a one-shot signed transfer) over a standing `Permit` allowance when you only need a single swap; the signature cannot be replayed after its nonce is used.
5. Check the expiration is a Unix timestamp, not a huge number: a `uint48` maximum is a never-expiring allowance.
6. Revoke by calling Permit2's `approve` for the spender with `amount=0` or a past `expiration`.
7. Re-read the allowance after any change to confirm the value moved in the direction you intended.

## Pitfalls

- One token approval to Permit2 covers every spender Permit2 records; a malicious dApp that gets an inner allowance can pull the full outer allowance. Keep the outer approval small.
- A Permit2 signature with no expiration is a reusable approval until the nonce is consumed; a signature-transfer permit is single-use, an allowance permit is not.
- Withdrawing the token approval to Permit2 later revokes every inner allowance at once, which is a useful panic action but breaks every integrated dApp.
- Permit2's witness data lets a signer bind extra parameters to the transfer; if the dApp shows a witness you do not recognize, decode it before signing.
- A spender can be re-pointed by a contract upgrade; an allowance that was safe yesterday may be attached to new code today.

- The Permit2 address is identical across chains by design; a lookalike at a different address is a fake.
- Signing a `PermitBatch` covering many tokens at once magnifies a single mistaken click into a full sweep.
- An allowance with a nonzero amount and a past expiration is already dead; zero it anyway for clarity.

## Verification

    cast call $PERMIT2 "allowance(address,address,address)(uint160,uint48,uint48)" $OWNER $TOKEN $SPENDER --rpc-url $RPC
    # expect amount within your cap and expiration within the next hour

Report the recorded allowance amount, expiration, and nonce, quoting the read command.
