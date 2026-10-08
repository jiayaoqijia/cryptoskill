---
name: prevent-mint-front-running
description: Use when an NFT drop is scarce and bots may snipe allowlist spots or token ids. Applies on-chain allowlisting, private submission, and id randomization to blunt front-running.
---

# Prevent mint front-running

Bots watch the mempool and buy scarce mints the moment a transaction is visible, sniping allowlist spots and rare token ids before a human's transaction lands.

## Procedure

1. Identify what a bot can predict: an open `mint()` with no allowlist, and token ids assigned by `totalSupply()`. If the id is knowable, bots can target a specific rare id.

2. Enforce the allowlist on-chain with a Merkle root or signature so a bot that is not listed cannot mint even after seeing the transaction:

   ```
   cast call $NFT "merkleRoot()(bytes32)" --rpc-url $RPC
   ```

3. Submit through a private or protected endpoint so the transaction is not visible before inclusion:

   ```
   cast send $NFT "mint(uint256)" 1 --private-key $KEY --rpc-url $PROTECT_RPC
   ```

4. Randomize token id assignment after mint time via a committed reveal (see commit-reveal), making id sniping pointless.

5. Consider `require(tx.origin == msg.sender)` only with eyes open — it blocks naive bot contracts but not a bot that owns an EOA.

6. Set a per-transaction and per-wallet cap so one bot cannot take an entire phase:

   ```
   grep -nE 'maxMintPerTx|maxPerWallet|require\(.*minted' src/*.sol
   ```

7. Add a commit-delay: `commit()` then `revealMint()` two blocks later, so mempool sniping gains nothing.

8. Race-test on a fork:

   ```
   forge test --match-test testSniping --fork-url $RPC -vvvv
   ```

## Pitfalls

- A public RPC rebroadcasts your transaction to the general mempool, defeating a private submission.
- Bots also watch the pending set and simulate; `tx.origin` checks do not stop EOAs.
- Reveal-after-mint removes id sniping but not supply sniping — keep the per-wallet cap too.
- A gas price set lower than the bots' guarantees your transaction is delayed, not protected.
- Accepting deposits before the allowlist check lets a bot's transaction reserve slots it later abandons.

## Verification

    forge test --match-test testSniping --fork-url $RPC -vvvv

Pass: a bot contract minting with a forged or absent proof reverts and the per-wallet cap holds under concurrent calls. Report the protection used (allowlist / private mempool / reveal) and the cap.
