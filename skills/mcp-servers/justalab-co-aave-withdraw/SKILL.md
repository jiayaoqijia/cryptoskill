---
name: aave-withdraw
description: Withdraw USDC the owner supplied to Aave V3 on Base back to their wallet. Use when the owner wants to take USDC out of the Aave lending market, partly or in full. Builds the withdraw call for the owner to approve in their wallet.
metadata:
  version: "1"
  author: recipes.jaw.eth
  chains: "8453"
---

# Withdraw USDC from Aave V3 on Base

One call to the Aave pool. The pool takes the USDC out of the owner's supplied position and sends it to the address you name. No approval is needed.

## Addresses (Base, chain id 8453)

| Label | Address |
| --- | --- |
| USDC (Circle) | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 |
| AAVE_POOL (Aave V3 Pool) | 0xA238Dd80C259a72e81d7e4664a9801593F98d1c5 |
| AAVE_DATA_PROVIDER (Aave V3 Protocol Data Provider) | 0x0F43731EB8d45A581f4a36DD74F5f358bc90C73A |
| AAVE_ORACLE (Aave V3 Oracle) | 0x2Cc0Fc26eD4563A5ce5e8bdcfe1A2878676Ae156 |

Use only these four addresses. The data provider and the oracle are only read, never called.

## Steps

1. Ask the owner how much USDC to withdraw, or whether to withdraw everything. Convert a fixed amount to base units: USDC has 6 decimals, so 12.5 USDC is 12500000.
2. Get the owner's account address from the `account` field of `jaw_session_status`. It is the `to` argument of the withdrawal, so the USDC lands in the owner's wallet and nowhere else.
3. Read the position from the chain with one `jaw_read_contracts` call: `chainId` 8453 and these `reads`, in this order, with the owner's account in place of `ACCOUNT`.

   ```json
   [
     { "address": "0xA238Dd80C259a72e81d7e4664a9801593F98d1c5", "functionName": "getUserAccountData", "args": ["ACCOUNT"],
       "abi": [{ "type": "function", "name": "getUserAccountData", "stateMutability": "view",
         "inputs": [{ "name": "user", "type": "address" }],
         "outputs": [{ "name": "totalCollateralBase", "type": "uint256" }, { "name": "totalDebtBase", "type": "uint256" },
           { "name": "availableBorrowsBase", "type": "uint256" }, { "name": "currentLiquidationThreshold", "type": "uint256" },
           { "name": "ltv", "type": "uint256" }, { "name": "healthFactor", "type": "uint256" }] }] },
     { "address": "0x0F43731EB8d45A581f4a36DD74F5f358bc90C73A", "functionName": "getUserReserveData",
       "args": ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "ACCOUNT"],
       "abi": [{ "type": "function", "name": "getUserReserveData", "stateMutability": "view",
         "inputs": [{ "name": "asset", "type": "address" }, { "name": "user", "type": "address" }],
         "outputs": [{ "name": "currentATokenBalance", "type": "uint256" }, { "name": "currentStableDebt", "type": "uint256" },
           { "name": "currentVariableDebt", "type": "uint256" }, { "name": "principalStableDebt", "type": "uint256" },
           { "name": "scaledVariableDebt", "type": "uint256" }, { "name": "stableBorrowRate", "type": "uint256" },
           { "name": "liquidityRate", "type": "uint256" }, { "name": "stableRateLastUpdated", "type": "uint40" },
           { "name": "usageAsCollateralEnabled", "type": "bool" }] }] },
     { "address": "0x0F43731EB8d45A581f4a36DD74F5f358bc90C73A", "functionName": "getReserveConfigurationData",
       "args": ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],
       "abi": [{ "type": "function", "name": "getReserveConfigurationData", "stateMutability": "view",
         "inputs": [{ "name": "asset", "type": "address" }],
         "outputs": [{ "name": "decimals", "type": "uint256" }, { "name": "ltv", "type": "uint256" },
           { "name": "liquidationThreshold", "type": "uint256" }, { "name": "liquidationBonus", "type": "uint256" },
           { "name": "reserveFactor", "type": "uint256" }, { "name": "usageAsCollateralEnabled", "type": "bool" },
           { "name": "borrowingEnabled", "type": "bool" }, { "name": "stableBorrowRateEnabled", "type": "bool" },
           { "name": "isActive", "type": "bool" }, { "name": "isFrozen", "type": "bool" }] }] },
     { "address": "0x2Cc0Fc26eD4563A5ce5e8bdcfe1A2878676Ae156", "functionName": "getAssetPrice",
       "args": ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],
       "abi": [{ "type": "function", "name": "getAssetPrice", "stateMutability": "view",
         "inputs": [{ "name": "asset", "type": "address" }], "outputs": [{ "name": "", "type": "uint256" }] }] }
   ]
   ```

   Each result is a list in the order of the outputs above, with numbers as decimal strings. Name them:
   - C, D, T and H: positions 0, 1, 3 and 5 of the first read. C and D are the collateral and the debt in US dollars with 8 decimals, T is the account's liquidation threshold in basis points (7800 is 78%), and H is the health factor with 18 decimals.
   - S and E: positions 0 and 8 of the second read. S is the USDC the owner has supplied, in base units, and E says whether it counts as collateral.
   - L: position 2 of the third read, USDC's liquidation threshold in basis points.
   - P: the fourth read, USDC's price in US dollars with 8 decimals.

   If a read fails, say you cannot check the position and do not withdraw until the owner confirms they accept that. If S is less than the amount, tell the owner how much they have supplied and stop. If D is "0", there is no loan and nothing to check, so go on to step 4. If E is false, the USDC is not collateral and the withdrawal leaves the health factor as it is, so tell the owner that and go on to step 4.
   Otherwise the withdrawal lowers the health factor, and Aave only refuses it below 1, so a withdrawal that goes through can still leave the loan close to liquidation. With A the amount in base units, the factor after the withdrawal is (C × T - A × P / 1000000 × L) / (D × 10000). It is what Aave computes at today's prices, and deposits that are not collateral (a threshold of 0) are already left out of C and T. Tell the owner the factor now (H / 10^18) and after. For example, 5,000 USDC and 15,000 syrupUSDC against a 3,000 USDC loan give a factor of 1.30, and withdrawing 1,000 USDC leaves 1.04. At or below 1.2, refuse the amount and offer a smaller one. From 1.2 to 2, warn that a small price move could liquidate the loan and continue only if the owner confirms the amount. With a loan open, never withdraw everything.
4. Call `jaw_prepare_calls` with one action: `to` AAVE_POOL, `function` "withdraw(address asset, uint256 amount, address to)", `args` [USDC, the amount in base units as a decimal string, the owner's account]. To withdraw everything (only when D is "0"), pass the maximum uint256, "115792089237316195423570985008687907853269984665640564039457584007913129639935": Aave documents it as the way to withdraw the whole supplied balance, and the pool sends what the owner has, not that number.
5. Call `jaw_simulate_calls` with `chainId` 8453 and the returned call. If it fails, show the owner the reason and stop.
6. Call `jaw_send_calls` with `chainId` 8453, the call exactly as `jaw_prepare_calls` returned it, and `recipes` set to ["aave-withdraw@1"].
7. Show the owner the link, end your turn, and follow the request with `jaw_get_calls_status` after they reply.

## Rules

- Never send the withdrawn USDC to an address other than the owner's account.
- Do not change the call after `jaw_prepare_calls` returns it.
