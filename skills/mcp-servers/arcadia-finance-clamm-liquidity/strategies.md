# Strategy Templates

These are templates and examples — not the only valid approaches. Adapt parameters to current conditions. Use selection.md to evaluate whether a strategy fits before executing.

## Key Parameter Notes

- **`write_account_add_liquidity`** capital sources: `deposits` array (wallet tokens), `use_account_assets=true` (existing account collateral), or both. Supports depositing multiple tokens and minting multiple LP positions in one tx. The backend swaps everything to the optimal ratio for the LP. You do NOT need to `write_account_deposit` first: `write_account_add_liquidity` handles the wallet transfer atomically. Check allowances first (`read_wallet_allowances`), then approve if needed (`write_wallet_approve`).
- **V4 spot accounts CAN mint LP** but cannot leverage (set `leverage: 0`). V3 margin accounts (created with a `creditor`) can both mint LP and leverage. If the user wants leveraged LP, create a V3 margin account with a creditor (`account_version: 3`).
- **`numeraire`** in `write_account_deleverage`: the debt token you're repaying (e.g. WETH when repaying WETH debt). `write_account_add_liquidity` auto-detects numeraire: no param needed.
- **`leverage`**: `0` = no leverage. `2` = 2x. Do NOT use `1` for no leverage: use `0`. When `leverage > 0`, borrowing is handled internally by `write_account_add_liquidity`: do NOT call `write_account_borrow` separately.
- **LP NFT details**: after `write_account_add_liquidity`, call `read_account_info` to find `asset_address` (the position manager contract) and `asset_id` (NFT token ID) in the positions list: needed for unstake/remove/claim actions.
- **`amount: "max_uint256"`** in `write_account_repay` repays all debt in full.
- **`slippage`** is in basis points: 100 = 1%, 50 = 0.5%.
- **`salt`** in `write_account_create` is a random uint32 used for deterministic address derivation. Use any random 32-bit integer (e.g. `Math.floor(Math.random() * 2**32)`).
- **`creditor`** = the lending pool address you want to borrow from. Set at account creation via `write_account_create`. Determines which asset the account can borrow. **Required for leveraged LP strategies.** Omit for spot-only accounts (no borrowing, but LP minting still works with `leverage: 0`).
- **`write_account_withdraw`**: pass exact amounts from `read_account_info`. Does NOT support `"max_uint256"`: will error.
- **Getting the account address after creation:** The address is deterministic from the salt. It's visible in the tx receipt events. Or call `read_account_info(wallet_address: ...)` after creation to list all accounts.

---

## Core Lifecycle (all strategies)

```
Open:    check allowances → approve tokens if needed → create account → add liquidity (atomic: deposit + swap + mint + borrow) → enable automation
Monitor: read_account_info (health), read_account_pnl (profitability)
Adjust:  add collateral or repay debt if health drops; remove + re-add liquidity to manually rebalance range
Close:   disable rebalancer → unstake → atomic close (burn LP + swap + repay) → withdraw
```

### Batching vs splitting

**Default: always use atomic tools.** `write_account_add_liquidity` batches opening, `write_account_close` batches closing, `write_account_deleverage` batches debt repayment from collateral. These reduce transaction count and eliminate exposure to price movement between steps.

**When to split:** In high-volatility markets or for low-liquidity pools, atomic transactions may revert because on-chain state diverges from when the backend computed the calldata. If an atomic tool fails, fall back to individual tools with tighter slippage. Always try atomic first — split only on failure.

---

## Strategy A: Delta Neutral Leveraged LP

**Goal:** Earn LP trading fees with minimal directional exposure to the volatile asset.

**Mechanism:** In a VOLATILE/STABLE pool (e.g., WETH/USDC), borrow the volatile asset (WETH) to fund the LP position. Your LP long exposure ≈ your debt short exposure → approximately delta neutral.

**Why it works:**

- LP position is ~50% WETH, ~50% USDC by value at any given price
- You borrow WETH to provide it → WETH debt ≈ WETH held in LP
- Net WETH exposure ≈ 0 (small residual from IL)
- You earn LP fees on the full leveraged notional

**Preconditions:** `fee_APY > borrow_APY` (check selection.md §1)

### Step-by-step

> Addresses below are Base mainnet examples. Always verify current addresses via `read_pool_list` and `read_asset_list` before executing.

```
// 1. FIND A POOL
read_strategy_list(chain_id: 8453)
→ Filter for volatile/stable pair (WETH/USDC, cbBTC/USDC, etc.)
→ Note: strategy_id (integer), pool_protocol (Slipstream V1/V2, UniV3, UniV4), fee_APY

// 2. CHECK BORROW COST
read_pool_list(chain_id: 8453)
→ Find the WETH lending pool (address: 0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2)
→ If borrow_apy > fee_apy → stop, strategy not profitable

// 3. CREATE MARGIN ACCOUNT (V3 + creditor = can borrow/leverage)
write_account_create(
  salt: <random uint32, e.g. 3141592653>,
  account_version: 3,   // V3 margin — required for leverage
  creditor: "0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2",  // WETH lending pool — enables borrow
  chain_id: 8453
)
→ Submit tx, note deployed account address from tx receipt
→ Or call read_account_info(wallet_address: ...) to find the new account address

// 4. CHECK ALLOWANCE + APPROVE (skip approve if already sufficient)
read_wallet_allowances(
  owner_address: <owner_wallet>,
  spender_address: <account_address>,
  token_addresses: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],  // USDC
  chain_id: 8453
)
// → If allowance is insufficient or zero:
write_wallet_approve(
  token_address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  // USDC
  spender_address: <account_address>,
  amount: "max_uint256",
  chain_id: 8453
)

// 5. OPEN LEVERAGED LP (atomic: pull USDC from wallet + borrow WETH + swap to ratio + mint LP)
// No separate write_account_deposit needed: write_account_add_liquidity handles the wallet transfer atomically.
write_account_add_liquidity(
  account_address: <account_address>,
  wallet_address: <owner_wallet>,
  positions: [{ strategy_id: <integer from step 1> }],
  deposits: [{ asset: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", amount: "10000000000", decimals: 6 }],  // 10,000 USDC — pulled from wallet
  leverage: 2,        // 2 = 2x leverage (0 = no leverage, 3 = 3x, etc.)
  slippage: 100,      // 100 = 1% slippage tolerance (basis points)
  chain_id: 8453
)

// 6. ENABLE AUTOMATIONS — one call, one transaction
// Include every automation you want active: the intents array is the full desired state.
// Add claim_merkl only if the pool has Merkl incentives (check fee APY breakdown in step 1).
write_account_automations(
  account_address: <account>,
  position_id: <lp_nft_id>,          // backend resolves protocol + tokens from this
  intents: [
    { kind: "compound_fees" },       // reinvest fees/rewards between rebalances
    { kind: "rebalance", strategy: { kind: "out_of_range", min_rebalance_time: 3600 } },
    { kind: "claim_merkl" }
  ],
  chain_id: 8453
)
// → Returns { valid, plan, diff, human_summary, transaction } — broadcast the transaction
```

### Monitoring

```
// Run periodically (daily or on request)
read_account_info(account_address: <account_address>, chain_id: 8453)
→ health_factor = 1 - (used_margin / liquidation_value). Higher = safer.
    1        → no debt (safest)
    > 0.5    → healthy
    0.2–0.5  → monitor closely, consider adding collateral or reducing debt
    < 0.2    → ACTION REQUIRED — close to liquidation
    0        → liquidation threshold
    < 0      → past liquidation

Note: Each lending pool adds a fixed minimum margin (denominated in the pool's numeraire,
typically a few dollars in value) to the debt when computing used_margin
(used_margin = open_debt + minimum_margin). For small positions this fixed overhead
dominates, pushing HF lower than the leverage ratio suggests — e.g. HF ~0.3 at 2×
instead of ~0.5–0.7. Increase position size for a healthier starting HF.

read_account_pnl(account_address: <account_address>, chain_id: 8453)
→ If net yield is consistently negative → evaluate exit

read_pool_list(chain_id: 8453)
→ If borrow_APY risen above fee_APY → exit signal
```

### Responding to health factor drops

```
// Option A: Add collateral (raises health factor, cheapest)
// Check allowance first — skip approve if already sufficient
read_wallet_allowances(owner_address: <wallet>, spender_address: <account>, token_addresses: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"], chain_id: 8453)
write_wallet_approve(token_address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", spender_address: <account>, amount: "max_uint256", chain_id: 8453)
write_account_deposit(account_address: <account>, asset_addresses: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"], asset_amounts: ["<amount>"], chain_id: 8453)

// Option B: Repay some WETH debt (reduces leverage)
// NOTE: you must approve the WETH pool to spend WETH from your wallet first — check allowance, then approve if needed
read_wallet_allowances(owner_address: <wallet>, spender_address: "0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2", token_addresses: ["0x4200000000000000000000000000000000000006"], chain_id: 8453)
write_wallet_approve(token_address: "0x4200000000000000000000000000000000000006", spender_address: "0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2", amount: "max_uint256", chain_id: 8453)
write_account_repay(
  pool_address: "0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2",  // WETH pool
  account_address: <account>,
  amount: "<raw_weth_amount_in_wei>",  // e.g. "100000000000000000" = 0.1 WETH
  chain_id: 8453
)

// Option C: Atomic sell USDC collateral → repay WETH debt (one flash tx, no wallet WETH needed)
write_account_deleverage(
  account_address: <account>,
  asset_from: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  // sell USDC from account
  amount_in: "<usdc_amount_to_sell>",                          // collateral amount to sell (input side, NOT debt amount)
  numeraire: "0x4200000000000000000000000000000000000006",     // WETH = debt token being repaid (NOT the stable side here)
  creditor: "0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2",    // WETH lending pool
  slippage: 100,
  chain_id: 8453
)
```

### Closing

**ALWAYS try the atomic close first** — it batches everything into 1-2 transactions instead of 6+.

#### Preferred: Atomic close (1-2 transactions)

```
// 0. Disable automation first (prevents the rebalancer from acting during close)
read_asset_manager_current(account_address: <account>, chain_id: 8453)
// → take the rebalancer's address from `enabled`, then:
write_account_automations_delta(
  account_address: <account>,
  disable: [<rebalancer_address>],
  chain_id: 8453
)

// 1. Get account state — need asset list for the close call
read_account_info(account_address: <account>, chain_id: 8453)

// 2. Unstake if staked (required before close)
write_account_stake(action: "unstake", asset_address: <staked_pm_address>, asset_id: <nft_id>, account_address: <account>, chain_id: 8453)

// 3. Atomic close: burns LP + swaps all tokens to USDC + repays debt — ONE transaction
write_account_close(
  account_address: <account>,
  assets: [
    { asset_address: "<position_manager>", asset_id: <nft_id>, amount: "1", decimals: 1 }
  ],
  receive_assets: [{ asset_address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", decimals: 6 }],  // receive USDC
  slippage: 100,
  chain_id: 8453
)

// 4. Withdraw remaining assets to wallet
write_account_withdraw(
  account_address: <account>,
  asset_addresses: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],
  asset_amounts: ["<balance>"],
  chain_id: 8453
)
```

#### Fallback: Two-step close (if atomic fails)

If the full atomic close fails, split into two steps:

1. `write_account_close(close_lp_only=true)`: burns LP only, tokens stay in account
2. Then use individual tools: `write_account_deleverage` → `write_account_withdraw`

#### Last resort: Manual step-by-step

Only if both atomic approaches fail:

```
write_account_stake(action: "claim", ...)   // claim fees
write_account_remove_liquidity(adjustment: <amount>)   // partial decrease
write_account_deleverage(...)               // swap collateral → repay debt
write_account_repay(amount: "max_uint256")             // repay remaining from wallet
write_account_withdraw(...)                            // withdraw all to wallet
```

**Key risks:**

- IL: WETH price deviation from entry accumulates IL. Rebalancer mitigates but doesn't eliminate.
- Liquidation: If WETH pumps sharply, health factor drops toward 0. Keep health factor above 0.5.
- Borrow cost: WETH utilization spikes can make strategy unprofitable quickly.
- Agent role: periodic health monitoring only — the rebalancer handles range management.

---

## Strategy B: Protocol Owned Liquidity (POL)

**IMPORTANT: Different objective.** POL is NOT a yield-maximizing strategy. It prioritizes capital preservation and reliable market liquidity provision.

**Who uses it:** DAOs, protocols, and treasuries that need to:

- Maintain consistent liquidity for their token pair at all times
- Protect treasury capital from large IL
- Provide deep liquidity to traders regardless of yield

### How POL differs from retail LP

| Dimension      | Retail (delta neutral)     | Protocol Owned Liquidity             |
| -------------- | -------------------------- | ------------------------------------ |
| Objective      | Maximize fees + yield      | Reliable market presence             |
| Range          | Narrow (high fee capture)  | Wide or dynamic (capital protection) |
| Rebalancing    | Aggressive (stay in range) | Conservative (minimize cost)         |
| Leverage       | Yes                        | No — protect principal               |
| IL tolerance   | Moderate (offset by fees)  | Low — preserving treasury            |
| Success metric | Fee APY > borrow APY       | Liquidity depth maintained           |

### POL rebalancer behavior

The `protocol_owned_liquidity` strategy type uses a dynamic range algorithm (k1/k2 coefficients) that adjusts range width based on price deviation. It maintains a "base range" for core liquidity plus a "limit order" component for excess. The rebalance threshold determines how far price must move before repositioning. This results in fewer rebalances (lower cost) at the expense of occasionally being partially out-of-range.

### Setup

```
// Same tools, different intent — no leverage, wider slippage tolerance

// 1. Check allowance + approve treasury tokens (skip approve if already sufficient)
read_wallet_allowances(owner_address: <treasury_wallet>, spender_address: <account>, token_addresses: [<token>], chain_id: 8453)
write_wallet_approve(token_address: <token>, spender_address: <account>, amount: "max_uint256", chain_id: 8453)

// 2. Create account (separate from retail positions)
// For POL without leverage, a spot account (V4) works fine.
// Use V3 + creditor only if you want the option to leverage later.
write_account_create(
  salt: <random uint32>,
  account_version: 0,  // V4 spot — no leverage needed for POL
  chain_id: 8453
)

// 3. Deposit treasury tokens
write_account_deposit(account_address: <account>, ...)

// 4. Open LP (no leverage — deposits are pulled from wallet)
write_account_add_liquidity(
  account_address: <account>,
  wallet_address: <treasury_wallet>,
  positions: [{ strategy_id: <from step 1> }],
  deposits: [{ asset: <token_address>, amount: <raw_amount>, decimals: <decimals> }],
  leverage: 0,        // 0 = no leverage (NOT 1 — use 0 for unleveraged)
  slippage: 200,      // 2% — wider tolerance for POL
  chain_id: 8453
)

// 5. Enable the rebalancer on the POL strategy
// The backend routes POL to the unified rebalancer and its POL strategy hook;
// tuning params are part of the intent, all optional with the defaults shown.
write_account_automations(
  account_address: <account>,
  position_id: <lp_nft_id>,
  intents: [{
    kind: "rebalance",
    strategy: {
      kind: "protocol_owned_liquidity",
      initial_range: 200000,
      base_range: 50000,
      k1: 0,
      k2: 0,
      rebalance_threshold: 25000,
      limit_order_withdrawal_threshold: 50000,
      fraction_excess_to_limit_order: 500000,
      deadzone: 20000,
      target_token0_ratio: 500000
    }
  }],
  chain_id: 8453
)
```

POL runs on the unified V2.1.1 rebalancer, which is the only deployment that speaks the POL strategy hook ABI. You do not select it or its hook: pass `strategy.kind: "protocol_owned_liquidity"` and the backend resolves both.

### Monitoring for POL

```
read_account_info → verify position is in range (primary check: no liquidation risk since no leverage)
read_account_pnl  → track IL vs. fee income
                   Note: net negative IL is EXPECTED and ACCEPTABLE for POL
                   The treasury is "paying" for market liquidity
read_strategy_recommendation → check if rebalancing is needed
```

**POL monitoring goal:** Ensure sufficient liquidity is deployed and treasury capital is not eroding excessively — not maximizing return.

## Upgrade to Aero (MetadexCL V1)

Aero CL succeeds the Slipstream pools (Aerodrome on Base, Velodrome on Optimism) at the Aero launch, and the new AERO token succeeds the old one on Base. `write_account_aero_upgrade` upgrades one account in one flashAction signed by the owner: every Slipstream V1, V2 and V3 position, staked or not, moves into the Aero CL pool with the same pair and variant at the same range and tick spacing (when Aero has no pool at that tick spacing, the user picks another one), and every unit of old AERO (loose in the account, unclaimed rewards, an old-AERO pair) becomes the new AERO. Chains: Base and Optimism. Robinhood has nothing to upgrade.

The backend decides what can move. Report its statuses and reasons as given; never decide eligibility yourself.

### Step-by-step

```
// 1. The cheap check: status and counts per account, no calldata. Empty accounts and failed_accounts: nothing to do.
read_account_aero_upgrade(wallet_address: <wallet>, chain_id: 8453)

// 2. If automations are enabled, keep their intents and config: the old managers are replaced after the move
read_asset_manager_current(account_address: <account>, chain_id: 8453)

// 3. The plan and, when anything can go now, the one transaction
write_account_aero_upgrade(account_address: <account>, chain_id: 8453)

// 4. Sign and broadcast as the account owner

// 5. Reconnect automations when managers_to_reconnect is not empty (new position id from read_account_info)
write_account_automations(account_address: <account>, position_id: <new_aero_id>, intents: [<from step 2>], mode: "save", chain_id: 8453)

// 6. Verify: dex_protocol metadexcl_v1 or staked_metadexcl_v1, old AERO shown as the new AERO, automation lists the reconnected managers
read_account_info(account_address: <account>, chain_id: 8453)
```

### Plan statuses

| `status`             | Meaning and next step                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ready`              | Sign `transaction` (`gas` is the backend's estimate). Items whose status is `waiting` or `blocked` stay where they are; their `reason` says why.                                                                                                                                                                                                                                                                                                                                                         |
| `choices_required`   | A position has status `choose`: Aero has no pool at its tick spacing, and another tick spacing can take it. Ask the user to pick one of its `options` whose `disabled_reason` is null (`tick_spacing`, `fee`, `apy`, `tvl_usd`, `is_new`, `range_widened`) and call again with `choices`, so one transaction moves everything. When ready items exist the plan already carries a `transaction` that moves only those: sign it alone only when the user wants to leave the `choose` position where it is. |
| `waiting`            | Nothing moves on its own. Each item's `reason` says why (see below). A waiting item with an option whose `disabled_reason` is null can still move with that option in `choices`; ask the user. Otherwise do not retry in a loop.                                                                                                                                                                                                                                                                         |
| `not_open`           | The AERO token upgrade contract does not accept deposits at the moment (it opens at `opens_at`). An upgrade that converts old AERO cannot be built until it does.                                                                                                                                                                                                                                                                                                                                        |
| `nothing_to_upgrade` | Nothing can move: no Slipstream position and no old AERO on the account, or every item is `blocked`. If `managers_to_reconnect` still lists active managers, the positions already moved but the automations were never reconnected: reconnect them (below).                                                                                                                                                                                                                                             |

### Item reasons

| `reason.code`               | Status  | Meaning                                                                                                                                                                                                       |
| --------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pool_not_on_aero`          | waiting | Aero has no pool with an Arcadia strategy on this pair yet.                                                                                                                                                   |
| `staking_not_open`          | waiting | The Aero pool's gauge is not live on Arcadia yet. The position stays staked where it is.                                                                                                                      |
| `no_reward_feed`            | waiting | The chain has no price feed for the staked Aero reward token yet. The position stays staked where it is.                                                                                                      |
| `target_price_mismatch`     | waiting | The Aero pool's price is too far from the market price to move safely now.                                                                                                                                    |
| `range_price_mismatch`      | waiting | The Aero pool's price and the old pool's price sit on different sides of the range edge, so the position's tokens cannot open the same range yet.                                                             |
| `widened_range_holds_price` | waiting | Only other tick spacings exist, and the widened range there holds the price, which the one-sided position cannot fill. It can move once the price leaves that range.                                          |
| `old_aero_at_range_edge`    | waiting | The old pool's price is near the range edge where the position holds no old AERO, so the upgrade cannot count on converting it. It can move once the price moves away, or with loose old AERO in the account. |
| `migration_paused`          | waiting | Aero has paused the AERO token upgrade.                                                                                                                                                                       |
| `budget_exhausted`          | waiting | The AERO token upgrade has too little new AERO left for this account now.                                                                                                                                     |
| `new_aero_cap_reached`      | waiting | The account's lending pool is at its limit for the new AERO, so old AERO in this margin account waits until the limit is raised.                                                                              |
| `account_unhealthy`         | waiting | The account's collateral is below what its debt requires, so the upgrade would revert. Add collateral or repay debt first.                                                                                    |
| `exposure_limit`            | waiting | A lending pool limit for one of the account's assets is reached, so the upgrade would revert. It can go once the limit is raised.                                                                             |
| `empty_position`            | blocked | The position holds no liquidity. Close it from the position page.                                                                                                                                             |
| `dust_position`             | blocked | The position is too small to re-create on Aero. Close it from the position page.                                                                                                                              |
| `range_not_alignable`       | blocked | The range fits no Aero tick spacing. Close the position and open a new one on Aero.                                                                                                                           |
| `no_target_pair`            | blocked | The position pairs old AERO with the new AERO, so there is no Aero pair to move it to. Close it from the position page.                                                                                       |

An option's `disabled_reason` uses `staking_not_open`, `no_reward_feed`, `range_price_mismatch`, `price_mismatch` (its pool is too far from the market price) or `range_mismatch` (its tick spacing cannot hold the range).

When the transaction's simulation reverts, the tool returns the plan with an `error` and no transaction. Rebuild once and report if it fails again. `tenderly_sim_status: unavailable` means Tenderly did not answer and the transaction is unsimulated: call once more before signing. A 422 saying a pool is not selectable: drop that pick and ask again. After a transaction confirms, pass its block as `min_block` on the next call.

A moved position's `old_aero_leg.converted: false` means this upgrade returns that leg to the account as old AERO, which a later upgrade converts. `rewards.becomes: null` means the rewards keep their token (VELO stays usable on Optimism). A plan without a transaction can still show `tenderly_sim_status: failure`: the account's health or a lending pool limit refused the move, and its items wait on `account_unhealthy` or `exposure_limit`. Report those reasons and do not rebuild.

`slippage` (bps, 1 to 1000) bounds the price the mint accepts. Omit it: the backend uses 150, or 500 when the owner is a contract such as a Safe.

### Several accounts

Pass `accounts` (up to 10 of one owner) instead of `account_address` for one plan and transaction per account in `results[]`. `multisends` groups the accounts that got a transaction, in order, so that each group's `gas` adds up to at most `max_gas_per_tx`: a Safe signs one MultiSend per group with those accounts' transactions. The accounts share one AERO upgrade budget, so plan them together. A result with `status: error` keeps its slot.

### Reconnecting automations

The move mints a new position, so automations on the old Slipstream position stop applying. `managers_to_reconnect` lists the old managers (`kind`, `old_address`) and their Aero replacements (`new_address`). Call `write_account_automations` in `save` mode with the new `position_id` and the intents the account had. Omit `protocol` so the backend resolves `metadexcl_v1` from the position: a stale `slipstream_*` value would compile Slipstream managers. The save disables the old managers in the same transaction. When `old_managers_still_needed` is true a Slipstream position stays on the account (it waits for its Aero pool), so keep the old managers: enable the Aero position with `write_account_automations_delta` instead. Settings are recompiled from intents, not copied: restate custom rebalancer settings from `read_asset_manager_current`. Each Aero manager holds one config per account, so when several old Slipstream managers of one kind had different settings, ask the user which to keep. When an item has `target.tokens_flipped: true` the pair sorts the other way on Aero: swap `token0` and `token1` in the intents' token fields (`tokens`, `convert_tokens`, `profit_token`) use 1e6 minus the token0 ratios and swap `trigger_lower_tick_ratio` with `trigger_upper_tick_ratio`, or leave that automation off and tell the user. The reconnect is a separate transaction: until it confirms, the Aero positions run without automations, so a Safe should queue it right after the upgrade. On Optimism and Robinhood there is no CoW Swapper, so compounding a staked Aero position's xAERO reward is rejected there; `claim_rewards` works.

### Margin vs spot

Spot and margin accounts hold Aero positions, staked or not, on Base, Optimism and Robinhood, within each lending pool's limits. A staked position whose Aero pool has no gauge on Arcadia yet waits with `staking_not_open`, or with `no_reward_feed` where the reward token has no price feed; it is never unstaked.

### VELO in the wallet

Separate from the account upgrade: `write_wallet_upgrade_velo` with `owner_address` (Optimism only) upgrades VELO in the wallet to 0.044 new AERO per VELO, paid to the same address on Base after the Hyperlane message lands. It returns ordered `transactions` (an approve when needed, then the payable deposit). VELO inside an account must be withdrawn first with `write_account_withdraw`. VELO stays usable, so this is optional. Errors name the reason: `not_open` (with the opening time), `paused`, `budget_exhausted`, `recipient_not_deployed` (a contract wallet that does not exist on Base).
