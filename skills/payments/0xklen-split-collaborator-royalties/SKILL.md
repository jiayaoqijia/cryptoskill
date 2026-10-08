---
name: split-collaborator-royalties
description: Use when an NFT drop has multiple creators and proceeds or royalties must be divided. Verifies shares sum correctly, the receiver is solvent, and rounding dust stays claimable.
---

# Split collaborator royalties

When a drop has multiple creators the split must be enforced by a contract that pays each wallet on withdrawal, not by a promise in the announcement.

## Procedure

1. Use a `PaymentSplitter` (OpenZeppelin) or equivalent with shares fixed at deploy:

   ```
   cast call $SPLITTER "totalShares()(uint256)" --rpc-url $RPC
   cast call $SPLITTER "payee(uint256)(address)" 0 --rpc-url $RPC
   ```

2. Verify the shares sum exactly to `totalShares`. A mixed denominator (shares of 100 against a total of 10000) silently overrides a collaborator's cut.

3. Confirm the splitter is both the mint-proceeds receiver and the `royaltyInfo` receiver:

   ```
   cast call $NFT "royaltyInfo(uint256,uint256)(address,uint256)" 1 1000000000000000000 --rpc-url $RPC
   ```

4. Check rounding. With shares 1/2/3 of 6 and a 1 wei balance the smallest share rounds to 0 and stays stuck; release the whole balance, not per-wei.

5. Verify `release(payee)` succeeds for every payee:

   ```
   cast send $SPLITTER "release(address)" $PAYEE --rpc-url $RPC --private-key $KEY
   ```

6. For any push-based split, confirm a failed send to one payee does not block the others; prefer pull (`release`).

7. Test with a fork:

   ```
   forge test --match-test testSplitRounding --fork-url $RPC -vvv
   ```

## Pitfalls

- Shares set against a denominator other than the sum let one collaborator drain more than their cut.
- A payee address that is a contract reverting on receive bricks a push payout for everyone.
- A splitter that only handles ETH while the sale pays WETH leaves royalties unreachable.
- Changing shares after the first withdrawal creates an inconsistency; splits should be immutable.
- Payments smaller than the 21000-gas send cost are uneconomical to release, so dust accumulates and must be claimable in bulk.

## Verification

    forge test --match-test testSplitRounding --fork-url $RPC -vvv

Pass: the sum of payee balances plus residual dust equals the deposit across random balances, and each share's bps matches the agreement. Report the shares, the splitter address, and the rounding result.
