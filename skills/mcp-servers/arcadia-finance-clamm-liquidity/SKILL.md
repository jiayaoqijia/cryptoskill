---
name: clamm-liquidity
description: Agent guide for clAMM management on Arcadia Finance. Covers 37 MCP tools (+1 dev), intent-based automation setup (compound fees, claim rewards, add to LP, rebalance, claim Merkl), the Slipstream to Aero migration, single-sided liquidity via ERC-4626 tranches, strategy selection framework, and strategy templates including delta neutral leveraged LP and protocol-owned liquidity.
user-invocable: true
---

# Arcadia Finance — clAMM Agent Guide

Arcadia is a platform for managing concentrated liquidity positions with automated rebalancing, compounding, yield optimization, and leverage. Positions live in Arcadia accounts, which can also borrow against their collateral. This skill covers everything needed to manage clAMM positions as an agent.

## Key Constraints

- **All `write_*` tools return unsigned transactions** (`{ to, data, value, chainId }`): you must sign and broadcast them. See "Transaction Signing" below.
- **Automation strategy config** (tick range, rebalance thresholds) is not currently settable via MCP — this requires Arcadia platform access.
- **Health factor** = `1 - (used_margin / liquidation_value)`. Higher is safer. `1` = no debt, `>0` = healthy, `0` = liquidation threshold, `<0` = past liquidation. Keep above 0.5 for leveraged positions; act immediately below 0.2.
- **Minimum margin**: each lending pool enforces a fixed minimum margin denominated in the pool's numeraire (e.g. WETH for the WETH pool, USDC for the USDC pool), typically a few dollars in value. This gets **added to the debt** when computing `used_margin` (i.e. `used_margin = open_debt + minimum_margin`). It ensures liquidations remain profitable (covering gas costs) and prevents dust attacks. For small positions the fixed minimum margin dominates the used margin, pushing health factor lower than the leverage ratio alone would suggest (e.g. HF ~0.3 at 2× leverage). Increase position size for a healthier starting HF. `write_account_add_liquidity` also validates deposits against per-asset minimum amounts from strategy risk factors.
- **`asset_id`** is always an integer (NFT token ID for LP positions, 0 for ERC20 tokens).
- **Wrapping ETH** — ETH must be wrapped to WETH before depositing. Call WETH's `deposit()` function (payable) with the ETH amount. No MCP tool for this, use your wallet.

## Transaction Signing

Write tools (`write_*`) return unsigned transaction calldata. This server does NOT sign or broadcast. After receiving a transaction object, you must:

1. **Sign** the transaction with the account owner's private key or wallet
2. **Broadcast** it to the appropriate chain (Base 8453, Unichain 130, Optimism 10, or Robinhood 4663)
3. **Wait** for the transaction receipt to confirm success

How you sign depends on your setup:

- **MPC wallet** (Fireblocks, Dfns, Turnkey) — pass the unsigned tx to your provider's signing API
- **Smart account** (Safe, Biconomy) — wrap the tx as a UserOperation or Safe transaction
- **Embedded wallet** (Privy, Dynamic) — use the provider's `sendTransaction` method
- **Direct private key** (development only): use the built-in `dev_send` tool (set `PK` in a `.env` file or MCP client config), or viem/ethers `sendTransaction` with a local signer

Example with viem:

```typescript
const hash = await walletClient.sendTransaction(tx);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
```

## Batching Philosophy

Arcadia's flash-action tools can batch multiple DeFi operations into a single atomic transaction. **Always prefer batched tools** — they reduce transaction count, gas cost, and exposure to price movement between steps.

**When to split:** In high-volatility markets or for low-liquidity pools, batched transactions may revert because on-chain state changes between when the backend computes calldata and when the transaction executes. If a batched tool fails, fall back to individual tools with tighter slippage. Always try batched first, split only on failure.

**Batched write tools (`write_account_add_liquidity`, `write_account_close`, `write_account_deleverage`, `write_account_swap`, `write_account_remove_liquidity`, `write_account_stake`) return time-sensitive calldata**: sign and broadcast promptly; calldata may expire after 30 to 60 seconds depending on market conditions. If a transaction reverts due to price movement, rebuild and retry at least once before falling back to individual tools.

## MCP Tools (37 + 1 dev)

### Read Tools

| Tool                           | When to use                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `read_account_info`            | Account overview + liquidation price. Pass `account_address` for detail (returns positions with `asset_address`/`asset_id`/`dex_protocol`, collateral, debt).                                                                                                                                                                                        |
| `read_account_history`         | Historical account value over time. Optional `days` param (default 14).                                                                                                                                                                                                                                                                              |
| `read_account_pnl`             | PnL and yield earned: use to check if a strategy is still profitable.                                                                                                                                                                                                                                                                                |
| `read_asset_list`              | List supported collateral assets (symbol, address, decimals). Use `search` to filter by symbol substring.                                                                                                                                                                                                                                            |
| `read_asset_prices`            | USD prices for one or more assets by address. Pass `asset_addresses` (single or comma-separated).                                                                                                                                                                                                                                                    |
| `read_wallet_balances`         | On-chain ERC20 balances and native ETH for a wallet. Use to pre-check if the wallet has enough tokens before depositing or adding liquidity.                                                                                                                                                                                                         |
| `read_wallet_allowances`       | Check ERC20 token allowances for a spender. Use before `write_wallet_approve` to avoid redundant approvals: skip if the current allowance is already sufficient.                                                                                                                                                                                     |
| `read_wallet_accounts`         | List all Arcadia accounts owned by a wallet address.                                                                                                                                                                                                                                                                                                 |
| `read_wallet_points`           | Points earned by a wallet address.                                                                                                                                                                                                                                                                                                                   |
| `read_pool_list`               | Lending pool TVL, APY, utilization, liquidity. Pass `pool_address` for detail + APY history (optional `days`, default 14).                                                                                                                                                                                                                           |
| `read_pool_info`               | Detail + APY history for a specific lending pool. Pass `pool_address`.                                                                                                                                                                                                                                                                               |
| `read_strategy_list`           | LP strategies with fee APY, underlyings, pool protocol. List view shows 7d avg APY for the strategy's default range (e.g. ±7.5% for volatile pairs). **Pass `strategy_id` to see APY per range width** (very_narrow → full_range): narrower range = higher APY but more rebalancing cost/risk. Use `featured_only: true` for curated top strategies. |
| `read_strategy_info`           | Detail for a specific strategy by `strategy_id`, including range-width APY breakdown.                                                                                                                                                                                                                                                                |
| `read_point_leaderboard`       | Points leaderboard. No `chain_id` needed: points are cross-chain.                                                                                                                                                                                                                                                                                    |
| `read_strategy_recommendation` | Rebalancing recommendation for an account. Uses 1d APY (not 7d like `read_strategy_list`), so numbers may differ.                                                                                                                                                                                                                                    |
| `read_asset_manager_intents`   | List the automation intents and their params. Pass `account_address` for live per-account availability plus the rule blocking anything unavailable.                                                                                                                                                                                                  |
| `read_asset_manager_current`   | What is enabled on an account now: decoded per-manager config, the intents it maps to, Merkl claim state, and superseded managers to clear.                                                                                                                                                                                                          |
| `read_account_aero_upgrade`    | Aero upgrade check: what a wallet's accounts (or one account) still have to move to Aero, with status and counts and no calldata. Empty accounts and failed_accounts lists mean nothing to do.                                                                                                                                                       |
| `read_guides`                  | Reference guides: `automation` (AM setup), `selection` (pool evaluation), `strategies` (step-by-step templates).                                                                                                                                                                                                                                     |

### Preferred Write Tools (atomic/multi-step — use these first)

These tools batch multiple operations into ONE atomic transaction. Always prefer these over individual tools.

| Tool                          | Batches                                                | When to use                                                                                                    |
| ----------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| `write_account_add_liquidity` | deposit + swap + mint LP + optional borrow             | Open LP position. Do NOT call `write_account_deposit` separately: this handles wallet transfer atomically.     |
| `write_account_close`         | burn LP + swap + repay debt (up to 3 steps)            | Close/exit a position. ALWAYS try this first. Tokens stay in account: follow up with `write_account_withdraw`. |
| `write_account_deleverage`    | swap collateral + repay debt                           | Repay debt using account collateral (no wallet tokens needed). Preferred for health factor fixes.              |
| `write_account_automations`   | resolve intents + validate + build setAssetManagers tx | Configure automations. Pass the full desired intents array; the backend picks the managers and encodes them.   |

### Individual Write Tools (use when batched tools fail or for standalone operations)

| Tool                              | When to use                                                                                                                                                                                                                                                                                                                                                               |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `write_wallet_approve`            | Approve a token for spending. **Required before `write_account_deposit`** and before `write_account_add_liquidity` (when depositing from wallet). Call `read_wallet_allowances` first to check if already approved.                                                                                                                                                       |
| `write_wallet_upgrade_velo`       | Upgrade wallet VELO on Optimism to the new AERO on Base: approve when needed, then the payable deposit. Optional, VELO stays usable.                                                                                                                                                                                                                                      |
| `write_account_create`            | Create a new Arcadia account (one-time setup). Use `account_version: 0` for the latest version (recommended).                                                                                                                                                                                                                                                             |
| `write_account_deposit`           | Deposit ERC20 tokens as collateral. NOT needed before `write_account_add_liquidity`: that tool handles deposits atomically.                                                                                                                                                                                                                                               |
| `write_account_withdraw`          | Withdraw assets to account owner. Account version auto-detected on-chain. Params: `asset_addresses[]`, `asset_amounts[]` (exact amounts, no max_uint256), optional `asset_ids[]` (0 for ERC20).                                                                                                                                                                           |
| `write_account_borrow`            | Borrow from a lending pool. NOT needed for leveraged LP: `write_account_add_liquidity` handles borrowing internally.                                                                                                                                                                                                                                                      |
| `write_account_repay`             | Repay debt from wallet (approve pool first). Use `amount: "max_uint256"` to repay in full. For repaying with account collateral, prefer `write_account_deleverage`.                                                                                                                                                                                                       |
| `write_account_swap`              | Swap assets within account (backend handles routing). For closing positions, prefer `write_account_close`.                                                                                                                                                                                                                                                                |
| `write_account_remove_liquidity`  | PARTIAL liquidity decrease only (position stays open). For full LP removal/exit, use `write_account_close`.                                                                                                                                                                                                                                                               |
| `write_account_stake`             | Stake, unstake, or claim rewards for an LP position. Direction auto-detected from `asset_address`.                                                                                                                                                                                                                                                                        |
| `write_pool_deposit`              | **Lend to earn yield.** Deposit the pool's underlying asset (USDC / WETH / cbBTC) into the ERC-4626 tranche, receive tranche shares that accrue interest from borrowers. Requires prior `write_wallet_approve` to the tranche. **Different from `write_account_deposit`**: that deposits collateral into your Arcadia account; this deposits as a lender.                 |
| `write_pool_redeem`               | **Lender exit.** Burn tranche shares and redeem the underlying asset, including accrued interest. Pass the owner's share balance (or a partial amount) in `shares`.                                                                                                                                                                                                       |
| `write_account_aero_upgrade`      | Upgrade an account to Aero (MetadexCL V1): its Slipstream positions move to Aero CL and its old AERO becomes the new AERO, in one flashAction. Returns the plan (items, reasons, pool options) and the transaction. Check first with `read_account_aero_upgrade`; wallet VELO on Optimism goes through `write_wallet_upgrade_velo`. See strategies.md, "Upgrade to Aero". |
| `write_account_automations_delta` | Change one automation without restating the rest: `enable` takes intents, `disable` takes asset-manager addresses from `read_asset_manager_current`. Prefer `write_account_automations` when setting the full desired state. See automation.md.                                                                                                                           |

### Dev Tools (only available when `PK` env var is set)

| Tool       | When to use                                                                                                                                                                                                                                 |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dev_send` | Sign and broadcast an unsigned transaction using a local private key. Pass the `{ to, data, value, chainId }` from any `write_*` tool. **Not for production**: use a dedicated wallet MCP server (Fireblocks, Safe, Turnkey, etc.) instead. |

## Shared Addresses

| Contract | Address                                      |
| -------- | -------------------------------------------- |
| Factory  | `0xDa14Fdd72345c4d2511357214c5B89A919768e59` |

### Lending Pools

Use as `pool_address` in `write_account_borrow` / `write_account_repay`, as `creditor` in `write_account_create` / `write_account_deleverage`. Same CREATE2 addresses on Base and Optimism. Unichain has no lending pools.

| Asset | Pool Address                                 | Chains         |
| ----- | -------------------------------------------- | -------------- |
| WETH  | `0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2` | Base, Optimism |
| USDC  | `0x3ec4a293Fb906DD2Cd440c20dECB250DeF141dF1` | Base, Optimism |
| cbBTC | `0xa37E9b4369dc20940009030BfbC2088F09645e3B` | Base only      |

### Asset Manager Addresses

Asset-manager addresses are resolved by the backend, not by this server, and are not passed to or returned by the automation tools. All require V3/V4 accounts. Older asset-manager versions remain on-chain for users who registered before the latest version shipped: `read_asset_manager_current` reports those as `deprecated` so they can be disabled, and reports the dex_protocol with no version suffix.

The addresses below are for reference and orientation only. The one you may actually need is the gas relayer, for paying for extra rebalances with AAA.

Standalone AMs (not tied to a DEX protocol, same address on all supported chains):

| Type           | Address                                      | Chains                   |
| -------------- | -------------------------------------------- | ------------------------ |
| Merkl Operator | `0x969F0251360b9Cf11c68f6Ce9587924c1B8b42C6` | Base, Optimism, Unichain |
| Gas Relayer    | `0xD938C8d04cF91094fecAF0A2018EAac483a40137` | Base, Optimism, Unichain |
| CoW Swapper    | `0xb988a32DeF54821Dde0D7382e8a74f1BE4da1f23` | Base only                |

Protocol-specific AMs (rebalancer, compounder, yield claimer). Slipstream V2 is Base-only. All other addresses apply to every chain where the protocol exists:

| Type          | Protocol               | Address                                      |
| ------------- | ---------------------- | -------------------------------------------- |
| Rebalancer    | Slipstream V1          | `0x5802454749cc0c4A6F28D5001B4cD84432e2b79F` |
| Rebalancer    | Slipstream V2          | `0x953Ff365d0b562ceC658dc46B394E9282338d9Ea` |
| Rebalancer    | Slipstream V3          | `0x37c6258aEe125d520B6f03fc2cb490955050D557` |
| Rebalancer    | Uniswap V3             | `0xbA1D0c99c261F94b9C8b52465890Cca27dd993Bd` |
| Rebalancer    | Uniswap V4             | `0x01EDaF0067a10D18c88D2876c0A85Ee0096a5Ac0` |
| Compounder    | Slipstream V1          | `0x467837f44A71e3eAB90AEcfC995c84DC6B3cfCF7` |
| Compounder    | Slipstream V2          | `0x35e59448C7145482E56212510cC689612AB4F61f` |
| Compounder    | Slipstream V3          | `0xd42A3Ac56456bD5422835B36C35Cacb6448ddCd9` |
| Compounder    | Uniswap V3             | `0x02e1fa043214E51eDf1F0478c6D0d3D5658a2DC3` |
| Compounder    | Uniswap V4             | `0xAA95c9c402b195D8690eCaea2341a76e3266B189` |
| Yield Claimer | Slipstream V1          | `0x5a8278D37b7a787574b6Aa7E18d8C02D994f18Ba` |
| Yield Claimer | Slipstream V2          | `0xc8bF4B2c740FF665864E9494832520f18822871C` |
| Yield Claimer | Slipstream V3          | `0x8c1Fbf38118fD5A704b6E7babcB7AF1a9A291980` |
| Yield Claimer | Uniswap V3             | `0x75Ed28EA8601Ce9F5FbcAB1c2428f04A57aFaA16` |
| Yield Claimer | Uniswap V4             | `0xD8aa21AB7f9B8601CB7d7A776D3AFA1602d5D8D4` |
| Rebalancer    | Aero CL (MetadexCL V1) | `0x9EA47b9db58970Ab5Ea686a5CaC3e80ec652d755` |
| Compounder    | Aero CL                | `0xd772812Ba8AeFBd4F2126E82e2D08a66856D0261` |
| Yield Claimer | Aero CL                | `0x0367C284b58d3531947c182C1aF203177Cc4D6ed` |

Aero CL managers have the same address on Base, Optimism and Robinhood.

Slipstream V3 on Optimism uses different addresses (exception to the deterministic deployment pattern):

| Type          | Address (Optimism)                           |
| ------------- | -------------------------------------------- |
| Rebalancer    | `0x33442fC10a20Aad0ddD73F6ae24500F5B370DC51` |
| Compounder    | `0x3e7b6997399eC402491c4A049e4CD727d3aA1738` |
| Yield Claimer | `0x3630bDb1Ac7cF8A435411391db75450350814F42` |

**Slipstream V1 vs V2 vs V3:** The pool determines the version, each pool is bound to a specific Slipstream version. `read_account_info` returns a `dex_protocol` field on LP positions (derived from the position manager address), so you can read the protocol directly from the account overview. For automations, prefer passing the position's id as `position_id` to `write_account_automations`, which resolves the protocol and tokens for you. If you have no position id, that value (`slipstream`, `slipstream_v2`, `slipstream_v3`, or their `staked_*` variants) is also accepted directly as the `protocol` param. MetadexCL V1 is Aero CL (`metadexcl_v1` / `staked_metadexcl_v1`); `staked_metadexcl_v1` covers both the staked module and the wrapper.

## Account Versions

Spot vs margin is determined by whether a **creditor** (lending pool) is set at account creation, not by version number.

- `account_version: 3` — **margin account** (created with a `creditor`). Can borrow, leverage, and mint LP. Uses an onchain whitelist of allowed collateral tokens.
- `account_version: 4` or `0` (latest) — **spot account** (no creditor, no borrowing). Can hold assets and mint LP with `leverage: 0`. Accepts any ERC20 (no onchain whitelist).
- `account_version: 1` or `2` — legacy. Not supported by current MCP tools (the automation tools require V3/V4).
- For **leveraged LP strategies**, use `account_version: 3` with a creditor.
- To check an existing account's version: call `read_account_info`: the response includes the account version.

## Chain-Specific Addresses

### Base (8453)

Protocols: Slipstream V1, Slipstream V2, Slipstream V3, Uniswap V3, Uniswap V4, Aero CL (MetadexCL V1), for spot and margin accounts.

| Token         | Address                                      | Decimals |
| ------------- | -------------------------------------------- | -------- |
| WETH          | `0x4200000000000000000000000000000000000006` | 18       |
| USDC          | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | 6        |
| cbBTC         | `0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf` | 8        |
| AERO          | `0x3f5bF3EdAc59d650D8fDf9657a71F2f904A3a4Ee` | 18       |
| AERO (legacy) | `0x940181a94A35A4569E4529A3CDfB74e38FD98631` | 18       |
| AAA           | `0xaaa843fb2916c0B57454270418E121C626402AAa` | 18       |
| stAAA         | `0xDeA1531d8a1505785eb517C7A28526443df223F3` | 18       |

### Optimism (10)

Protocols: Slipstream V1 (Velodrome), Slipstream V3, Uniswap V3, Uniswap V4, Aero CL (MetadexCL V1). No Slipstream V2, no cbBTC pool.

| Token  | Address                                      | Decimals |
| ------ | -------------------------------------------- | -------- |
| WETH   | `0x4200000000000000000000000000000000000006` | 18       |
| USDC   | `0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85` | 6        |
| OP     | `0x4200000000000000000000000000000000000042` | 18       |
| VELO   | `0x9560e827aF36c94D2Ac33a39bCE1Fe78631088Db` | 18       |
| WBTC   | `0x68f180fcCe6836688e9084f035309E29Bf0A2095` | 8        |
| wstETH | `0x1F32b1c2345538c0c6f582fCB022739c4A194Ebb` | 18       |
| xAERO  | `0xbdEaeA5205d16f34Cb40038052d91235D87B4C54` | 18       |

### Unichain (130)

Protocols: Slipstream V1, Uniswap V3, Uniswap V4. No Slipstream V2/V3. No lending pools.

| Token | Address                                      | Decimals |
| ----- | -------------------------------------------- | -------- |
| WETH  | `0x4200000000000000000000000000000000000006` | 18       |
| USDC  | `0x078D782b760474a361dDA0AF3839290b0EF57AD6` | 6        |
| WBTC  | `0x0555E30da8f98308EdB960aa94C0Db47230d2B9c` | 8        |
| UNI   | `0x8f187aA05619a017077f5308904739877ce9eA21` | 18       |
| VELO  | `0x7f9AdFbd38b669F03d1d11000Bc76b9AaEA28A81` | 18       |

### Robinhood (4663)

Protocols: Uniswap V3, Uniswap V4, Aero CL (MetadexCL V1). No Slipstream V1-V3. Lending pools: WETH and USDG.

| Token | Address                                      | Decimals |
| ----- | -------------------------------------------- | -------- |
| xAERO | `0x9e148C5716b5aAdCFD3B71cEAE9EE7a9e22C29E2` | 18       |

## Reference Files

- [automation.md](automation.md) — How to enable each automation type
- [selection.md](selection.md) — How to evaluate pools, choose range width, size leverage, combine automation
- [strategies.md](strategies.md): Step-by-step strategy templates: delta neutral LP, protocol-owned liquidity, and the upgrade to Aero
