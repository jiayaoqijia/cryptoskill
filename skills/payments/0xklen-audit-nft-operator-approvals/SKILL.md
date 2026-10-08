---
name: audit-nft-operator-approvals
description: Use when auditing which operators or marketplaces can move an NFT holder's tokens. Enumerates live approvals, flags dangerous ones, and verifies revocations took effect.
---

# Audit NFT operator approvals

An `ApprovalForAll` granted to a marketplace or a malicious operator can move every token a holder owns; enumerate what is live, what each can move, and revoke the dead ones.

## Procedure

1. Read the operator state directly:

   ```
   cast call $NFT "isApprovedForAll(address,address)(bool)" $OWNER $OPERATOR --rpc-url $RPC
   cast call $NFT "getApproved(uint256)(address)" $ID --rpc-url $RPC
   ```

2. Bulk-enumerate operators from events for the owner:

   ```
   cast logs --from-block 0 --address $NFT "ApprovalForAll(address,address,bool)" $OWNER --json
   ```

3. Classify each operator by checking whether it has code:

   ```
   cast code $OPERATOR --rpc-url $RPC | wc -c     # tiny (2) means EOA, a red flag for ApprovalForAll
   ```

4. Revoke operators no longer used, from a trusted wallet rather than the site that requested them:

   ```
   cast send $NFT "setApprovalForAll(address,bool)" $OPERATOR false --rpc-url $RPC --private-key $KEY
   ```

5. Revoke a stale per-token approval:

   ```
   cast send $NFT "approve(address,uint256)" 0x0000000000000000000000000000000000000000 $ID --rpc-url $RPC --private-key $KEY
   ```

6. Verify every revocation landed by re-reading `isApprovedForAll` / `getApproved`.

7. If the collection uses an operator-filter registry, confirm the marketplace address is actually allowed, or a valid listing will fail to settle.

## Pitfalls

- Revoke.cash and similar tools are chain-specific; an approval on one chain does not appear on another.
- Approving a marketplace on a collection proxy does not carry to a new collection address after a migration.
- A signed marketplace listing can be replayed until expiry even after the on-chain approval is revoked.
- A batch revoke via multicall can fail partially; verify each approval after, not the batch status alone.
- Revoking an operator that a contract re-approves inside a hook is a no-op; check the balance-holder's real state afterwards.

## Verification

    cast call $NFT "isApprovedForAll(address,address)(bool)" $OWNER $OPERATOR --rpc-url $RPC

Pass: the call returns `false` for every operator you no longer use, and no token has a non-zero `getApproved`. Report the operators found, which were revoked, and the tx hashes.
