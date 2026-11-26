---
name: jaw-recipes
description: List of the JAW recipes, the tested guides for common wallet tasks. Use it to see which recipes exist and how to fetch one before building calls for lending, withdrawing or consolidating tokens.
metadata:
  version: "1"
  author: recipes.jaw.eth
  chains: "8453"
---

# JAW recipes

A recipe is a tested guide for one wallet task. It names the contracts and calls to use, so you do not have to find them yourself. Recipes are optional: when none fits the owner's request, build the calls as usual.

## Recipes

- aave-supply: put USDC the owner holds to work in Aave V3 on Base. Tag `aave-supply@1`.
- aave-withdraw: take USDC the owner supplied to Aave V3 on Base back to their wallet. Tag `aave-withdraw@1`.
- token-consolidation: swap several small ERC-20 balances on one chain into a single token, in one batch. It runs through `jaw_swap` and has no tag.

## Fetch one

Call `jaw_find_recipe` with the recipe name to read its guide and, when the recipe has them, its addresses and its tag. Call it with no name, or with an `intent`, to list the recipes on a network. A host that reads skills over MCP can instead call `skills/get` with the recipe's URI, which has the form `skill://jaw-recipes/recipes.jaw.eth/v1/<name>/SKILL.md`.

## Use one

When the calls you send with `jaw_send_calls` follow a recipe that has a tag, pass the tag in its `recipes` argument. A recipe with no tag is never passed there.
