---
name: replay-protection-across-forks
description: Use when signing on a chain that may fork or when a signature could be valid on more than one network. Enforces EIP-155 chain ids, EIP-712 domain chainId binding, and rejects legacy v=27/28 payloads.
---

# Replay protection across forks

A signature without a chain binding is a transaction an attacker can broadcast on every network that shares the key. This skill forces a chain id into every signed payload and treats pre-EIP-155 and cross-chain-reusable signatures as unsafe.

## Procedure

1. Require EIP-155 on every transaction: the signature must include `chainId`. Decode the `v` value from a signed tx:
   `cast to-dec <v>` — EIP-155 `v = chainId * 2 + 35`. A `v` of 27 or 28 is unprotected and replayable.
2. Verify the chain id the tx was signed for:
   `cast chain-id --rpc-url $RPC` and confirm the payload's chain matches.
3. For typed-data signatures, require `chainId` inside the EIP-712 domain. A domain with no `chainId` (or `chainId: 0`) is replayable across chains.
4. For a fork you intend to transact on, confirm the fork's chain id differs from the source chain's. A checkpoint fork that keeps the same chain id inherits every signed tx.
5. When a project hard-forks and replicates balances, treat every pre-fork signature as public; re-sign only after the fork with the new chain id.
6. Reject any request to sign with `v=27/28` or a domain that omits `chainId`, and say the reason.
7. After a new fork appears, re-run any automation that holds signed-but-unbroadcast transactions.

## Pitfalls

- EIP-712 hashes are replayable on any contract that uses the same domain and the same verifying contract address on another chain; the `chainId` field is what stops that.
- A signature over a `permit` with a missing chain id can be lifted onto a forked network and used to move the user's tokens there.
- `eth_sign` (the raw `0x19` prefix) carries no domain at all; it is the worst case and should be refused.
- Same-nonce cross-chain reuse looks harmless because nonces are per-chain, but reusing identical signed bytes across chains is the actual replay vector — regenerate the signature per chain.
- A wallet that defaults to legacy transactions on a chain that supports EIP-155 produces replayable output without warning.

- A signature over a message with no chain binding can be replayed on any chain the same key exists on.
- Wallet software that reuses a cached `chainId` across a fork produces signatures valid on both chains.
- After a fork, re-check any hardcoded chain id in tests and scripts, not just production config.
- Signing a hash rather than structured data removes the only place a chain id could be embedded.

## Verification

    cast chain-id --rpc-url $RPC && cast to-dec <v>
    # expect EIP-155 v form (v >= 35) and the decoded chain id to equal the printed chain id

Report the chain id and the decoded `v`, confirming the signature is EIP-155 bound, with the commands run.
