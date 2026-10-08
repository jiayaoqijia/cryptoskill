---
name: revoke-token-approvals
description: Use when cleaning up token allowances after activity. Enumerates Approval events for an owner, identifies live spenders, and resets each to zero with a verified transaction.
---

# Revoke token approvals

Every unlimited approval an old contract still holds is a standing invitation. This skill enumerates the approvals an address has granted, finds the ones still live, and resets them, verifying each revoke landed.

## Procedure

1. Enumerate `Approval` events where your address is the owner, across the tokens you have touched:
   `cast logs --from-block 0 --address $TOKEN "Approval(address,address,uint256)" $OWNER --rpc-url $ARCHIVE_RPC`
   For a full sweep use an indexer (Etherscan `getLogs` API, or Revoke.cash's API), since a full-range log scan needs archival access.
2. For each `(token, spender)` pair, read the live allowance and keep the nonzero ones:
   `cast call $TOKEN "allowance(address,address)(uint256)" $OWNER $SPENDER --rpc-url $RPC`
3. Reset each to zero. `approve(spender, 0)` is accepted by every ERC-20 (some tokens also accept a direct set to a lower nonzero value):
   `cast send $TOKEN "approve(address,uint256)" $SPENDER 0 --account deployer --rpc-url $RPC`
   Batch many revokes into one transaction with a `multicall` when you control the caller, or send them individually with serialized nonces.
4. Skip spenders you actively use; revoking those breaks integrations and you will re-approve on the next interaction.
5. Verify each revoke took effect before moving on.
6. Keep the list of revoked pairs in a note so a future drain review can prove the allowance is gone.
7. Re-scan monthly, since new dApps add new spenders continuously.

## Pitfalls

- Some tokens require setting a nonzero allowance before zero, or revert on a zero transition (older USDT-likes); handle the revert and set a small value first, then zero.
- A revoke transaction costs gas; on a congested chain, batch to amortize, but remember a batched revoke from a smart account is one signature, not N.
- Scanning logs from block 0 without an archive node returns nothing or times out; use an indexer or the explorer API instead.
- Revoking the token-to-Permit2 approval clears every inner Permit2 allowance, which can surprise you if a dApp depends on it.
- A spender address reused by a proxy can become malicious after an upgrade, so an allowance that was safe is not permanently safe.

## Verification

    cast call $TOKEN "allowance(address,address)(uint256)" $OWNER $SPENDER --rpc-url $RPC
    # expect 0 for each pair you revoked

Report the pairs revoked and the confirmed zero allowance for each, quoting the read commands.
