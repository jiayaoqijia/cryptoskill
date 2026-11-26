---
name: aave-supply
description: Supply USDC the owner holds to Aave V3 on Base so it earns interest. Use when the owner wants idle USDC put to work in a lending market. Builds an exact-amount approval and the supply call, for the owner to approve in their wallet.
metadata:
  version: "1"
  author: recipes.jaw.eth
  chains: "8453"
---

# Supply USDC to Aave V3 on Base

Two calls, sent together: approve the Aave pool for the exact amount, then supply it. The owner approves both in one wallet request.

## Addresses (Base, chain id 8453)

| Label | Address |
| --- | --- |
| USDC (Circle) | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 |
| AAVE_POOL (Aave V3 Pool) | 0xA238Dd80C259a72e81d7e4664a9801593F98d1c5 |

Use only these two addresses. If the owner names another token or market, this recipe does not apply.

## Steps

1. Ask the owner how much USDC to supply, unless they already said. Convert it to base units: USDC has 6 decimals, so 12.5 USDC is 12500000.
2. Call `jaw_get_assets` with `chainIds` [8453] and `assetTypes` ["erc20"]. Check the account holds at least that much USDC at the address above. If it holds less, tell the owner and stop, or offer `jaw_add_funds` with `chainId` 8453.
3. Get the owner's account address from the `account` field of `jaw_session_status`. It is the `onBehalfOf` argument, so the position belongs to the owner.
4. Call `jaw_prepare_calls` with two actions, in this order:
   - `to` USDC, `function` "approve(address spender, uint256 amount)", `args` [AAVE_POOL, the amount in base units as a decimal string]. Approve exactly the amount. Never approve an unlimited amount or a larger one.
   - `to` AAVE_POOL, `function` "supply(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)", `args` [USDC, the same amount, the owner's account, "0"].
5. Call `jaw_simulate_calls` with `chainId` 8453 and the returned calls. If it fails, show the owner the reason and stop.
6. Call `jaw_send_calls` with `chainId` 8453, the calls exactly as `jaw_prepare_calls` returned them, and `recipes` set to ["aave-supply@1"].
7. Show the owner the link, end your turn, and follow the request with `jaw_get_calls_status` after they reply.

## Rules

- The approval is for the exact supply amount and nothing more.
- Do not change the calls after `jaw_prepare_calls` returns them.
- The USDC supplied to Aave earns a rate that changes over time, and the owner can take it out later with the aave-withdraw recipe.
