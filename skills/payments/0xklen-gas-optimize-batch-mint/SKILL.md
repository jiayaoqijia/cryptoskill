---
name: gas-optimize-batch-mint
description: Use when minting many NFTs in one transaction and per-token gas is too high. Measures the naive loop, applies a bitmap ownership layout, and verifies reads stay correct.
---

# Gas-optimize batch NFT minting

Minting N tokens in one transaction is dominated by ERC-721 ownership writes; a batch layout that writes ownership once cuts per-token cost, provided reads are updated to match.

## Procedure

1. Measure the naive loop first:

   ```
   forge test --match-test testMint10Naive --gas-report | grep -i mint
   ```

   Ten separate `_safeMint` calls typically cost ~50k gas each.

2. Adopt a batch layout that writes ownership once per batch (ERC-721A style) and stores packed owner data:

   ```
   grep -nE 'balanceOf|ownerOf|_ownerships|_packedAddressData|_currentIndex' src/ERC721A.sol
   ```

3. Confirm `ownerOf` and `balanceOf` are overridden to read the packed bitmap; otherwise the saving is lost at read time and reads return wrong owners.

4. Check the batch emits the ERC-2309 `ConsecutiveTransfer` event (and/or per-token `Transfer`) so indexers still see the mint:

   ```
   grep -nE 'ConsecutiveTransfer|emit Transfer' src/*.sol
   ```

5. Benchmark before and after with the same batch size:

   ```
   forge snapshot --match-contract MintGasTest && diff .gas-snapshot .gas-snapshot.bak
   ```

6. Ensure the batch is atomic — a revert mid-loop must roll back the whole batch:

   ```
   require(quantity <= maxPerTx, "too many");
   ```

7. Check the memory cost of large batches: a `uint256[]` in calldata is cheap; building it in memory for 1000 tokens is not.

8. Confirm receiver callbacks. `_safeMint` in a batch calls `onERC721Received` N times, opening N reentrancy windows; call it once or document unsafe minting.

## Pitfalls

- ERC-721A `ownerOf` on an uninitialized id returns the batch-start owner instead of reverting, so a burn can resurrect a token.
- Marketplace tools that count `Transfer` events undercount a batch mint that only emits `ConsecutiveTransfer`.
- `_safeMint` inside a batch loop calls the receiver hook N times, multiplying reentrancy surface.
- Skipping the ownership write for the first token makes `totalSupply` and ids disagree.
- Copying an ERC-721A implementation without its `_beforeTokenTransfers` override breaks approval clearing on transfer.

## Verification

    forge snapshot --match-contract MintGasTest && diff .gas-snapshot .gas-snapshot.bak

Pass: per-token gas is materially lower than the naive loop and `ownerOf`/`balanceOf` return correct values for every id in the batch. Report the gas per token before and after, the batch size, and the event emitted.
