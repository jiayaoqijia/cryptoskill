---
name: verify-erc2981-royalty-split
description: Use when a collection advertises creator royalties on secondary sales. Checks the ERC-2981 numbers, the receiver's solvency, and whether marketplaces actually enforce them.
---

# Verify ERC-2981 royalty payouts

ERC-2981 only reports royalty info; it does not force any marketplace to pay it. Verify the numbers, the receiver, and whether the receiver can actually withdraw the funds.

## Procedure

1. Read royalty info for a real token id and a reference sale price:

   ```
   cast call $NFT "royaltyInfo(uint256,uint256)(address,uint256)" 1 1000000000000000000 --rpc-url $RPC
   ```

   The second return value is the royalty amount in wei for a 1 ETH sale.

2. Confirm the interface is declared:

   ```
   cast call $NFT "supportsInterface(bytes4)(bool)" 0x2a55205a --rpc-url $RPC   # must be true
   ```

3. Check the receiver is a contract you can name, not an unlabelled EOA:

   ```
   cast code $RECEIVER --rpc-url $RPC | wc -c      # > 2 means contract
   cast call $RECEIVER "owner()(address)" --rpc-url $RPC
   ```

4. If the receiver is a `PaymentSplitter`, read the shares and confirm they sum to the denominator:

   ```
   cast call $SPLITTER "totalShares()(uint256)" --rpc-url $RPC
   cast call $SPLITTER "shares(address)(uint256)" $PAYEE --rpc-url $RPC
   ```

5. Compute the effective basis points the receiver reports and compare against what a live marketplace displays for the same collection — enforcement varies by marketplace and by listing type.

6. Look for a settable royalty: `grep -nE 'setDefaultRoyalty|setTokenRoyalty|_setDefaultRoyalty' src/*.sol`. If the owner can change the number, the advertised rate is not guaranteed.

7. Confirm royalties apply on secondary sales only and are not double-counted for the primary mint.

## Pitfalls

- Some marketplaces (post operator-filter era) ignore ERC-2981 entirely, so an on-chain `royaltyInfo` of 5% may pay 0%.
- A receiver set to a contract that reverts on receive bricks every royalty payout while still reporting a rate.
- `royaltyInfo` returning the full sale price as royalty indicates a decimals or denominator bug.
- An out-of-range `salePrice` argument (0) returns 0 royalty and is not a valid check.
- A royalty stored as a fraction with a wrong denominator (e.g. 500 means 500% not 5%) silently overcharges.

## Verification

    cast call $NFT "royaltyInfo(uint256,uint256)(address,uint256)" 1 1000000000000000000 --rpc-url $RPC

Pass: the returned amount equals the advertised bps of the sale price, `supportsInterface(0x2a55205a)` is true, and the receiver is a contract you can name. Report the bps, the receiver type, and whether enforcement is on-chain or marketplace-dependent.
