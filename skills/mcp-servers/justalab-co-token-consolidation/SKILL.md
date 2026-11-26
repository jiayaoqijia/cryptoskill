---
name: token-consolidation
description: Swap several small ERC-20 balances the owner holds on one chain into a single token, in one batch the owner approves once. Use when the owner wants to clean up dust or merge many tokens into USDC or another ERC-20. Guide only, no manifest.
metadata:
  version: "1"
  author: recipes.jaw.eth
  chains: "8453"
---

# Consolidate ERC-20 balances into one token

This guide uses the `legs` input of `jaw_swap`. It builds no calls by hand and names no contract: the server quotes each leg from a DEX pool and the owner approves the whole batch in the wallet.

## How legs work

- `legs` takes 2 to 5 different ERC-20s on one chain, each with an amount in base units, and swaps each into `destinationToken` in one batch.
- `originChainId` and `destinationChainId` must be the same chain. `destinationToken` must be an ERC-20, not the native coin, and must not also appear as a leg.
- Each leg is quoted from its own DEX pool, never the swap backend. Each gets an approval of exactly its amount and a swap that pays the account at least that leg's minimum out.
- The server simulates the whole batch from the account. If a leg has no pool, the wallet holds too little, or the batch fails the simulation, no link opens and the result names the leg.
- The legs are quoted again when the link opens. If one leg is on other terms, the whole swap ends.
- With `legs`, send no `originToken`, `amount`, `permissionId` or `minOutputAmount`. Only one swap link can wait per connection at a time.
- This guide covers Base only.

## Steps

1. Work on Base (8453). Ask the owner which token to consolidate into, and default to USDC if they have no preference. If they want another chain, say this guide covers Base only.
2. Call `jaw_get_assets` with `chainIds` [the chain] and `assetTypes` ["erc20"]. List the ERC-20s the wallet holds. Leave out the destination token and any token the owner wants to keep.
3. Show the owner the tokens and amounts you plan to swap and let them drop any. Do not swap a token the owner did not agree to.
4. Call `jaw_find_token` with the chain id and the destination token as `query`, and take its address from an exact match. If the match is not exact, ask the owner.
5. If a leg is worth very little, tell the owner that the network fee may exceed what it returns.
6. Call `jaw_swap` with `originChainId` and `destinationChainId` both set to the chain, `destinationToken`, and `legs`: one { `originToken`, `amount` } per token, with the wallet's full balance in base units for each token the owner agreed to swap. `legs` needs 2 to 5 tokens, so with more than 5 split them into batches of 5 or fewer where none has a single token (for 6, send 4 and 2), and finish one swap before the next. A single token goes in a plain `jaw_swap` with `originToken` and `amount` and no `legs`; this also applies when the owner keeps only one token in step 3.
7. If the result is a refusal such as `leg_not_dex`, `leg_repeated` or `balance_low`, read which leg it names, drop it or swap it alone with `jaw_swap`, and tell the owner.
8. Show the owner the link on its own line with one sentence of what it does, end your turn, and follow the swap with `jaw_swap_status` and its `swapId` after they reply.
