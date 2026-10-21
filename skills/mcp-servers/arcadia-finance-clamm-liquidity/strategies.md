# Strategy Templates

These are templates and examples — not the only valid approaches. Adapt parameters to current conditions. Use selection.md to evaluate whether a strategy fits before executing.

## Key Parameter Notes

- **`write.account.add_liquidity`** capital sources: `deposits` array (wallet tokens), `use_account_assets=true` (existing account collateral), or both. Supports depositing multiple tokens and minting multiple LP positions in one tx. The backend swaps everything to the optimal ratio for the LP. You do NOT need to `write.account.deposit` first — `write.account.add_liquidity` handles the wallet transfer atomically. Check allowances first (`read.wallet.allowances`), then approve if needed (`write.wallet.approve`).
- **V4 spot accounts CAN mint LP** but cannot leverage (set `leverage: 0`). V3 margin accounts (created with a `creditor`) can both mint LP and leverage. If the user wants leveraged LP, create a V3 margin account with a creditor (`account_version: 3`).
- **`numeraire`** in `write.account.deleverage`: the debt token you're repaying (e.g. WETH when repaying WETH debt). `write.account.add_liquidity` auto-detects numeraire — no param needed.
- **`leverage`**: `0` = no leverage. `2` = 2x. Do NOT use `1` for no leverage — use `0`. When `leverage > 0`, borrowing is handled internally by `write.account.add_liquidity` — do NOT call `write.account.borrow` separately.
- **LP NFT details**: after `write.account.add_liquidity`, call `read.account.info` to find `asset_address` (the position manager contract) and `asset_id` (NFT token ID) in the positions list — needed for unstake/remove/claim actions.
- **`amount: "max_uint256"`** in `write.account.repay` repays all debt in full.
- **`slippage`** is in basis points: 100 = 1%, 50 = 0.5%.
- **`salt`** in `write.account.create` is a random uint32 used for deterministic address derivation. Use any random 32-bit integer (e.g. `Math.floor(Math.random() * 2**32)`).
- **`creditor`** = the lending pool address you want to borrow from. Set at account creation via `write.account.create`. Determines which asset the account can borrow. **Required for leveraged LP strategies.** Omit for spot-only accounts (no borrowing, but LP minting still works with `leverage: 0`).
- **`write.account.withdraw`**: pass exact amounts from `read.account.info`. Does NOT support `"max_uint256"` — will error.
- **Getting the account address after creation:** The address is deterministic from the salt. It's visible in the tx receipt events. Or call `read.account.info(wallet_address: ...)` after creation to list all accounts.

---

## Core Lifecycle (all strategies)

```
Open:    check allowances → approve tokens if needed → create account → add liquidity (atomic: deposit + swap + mint + borrow) → enable automation
Monitor: read.account.info (health), read.account.pnl (profitability)
Adjust:  add collateral or repay debt if health drops; remove + re-add liquidity to manually rebalance range
Close:   disable rebalancer → unstake → atomic close (burn LP + swap + repay) → withdraw
```

### Batching vs splitting

**Default: always use atomic tools.** `write.account.add_liquidity` batches opening, `write.account.close` batches closing, `write.account.deleverage` batches debt repayment from collateral. These reduce transaction count and eliminate exposure to price movement between steps.

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

> Addresses below are Base mainnet examples. Always verify current addresses via `read.pool.list` and `read.asset.list` before executing.

```
// 1. FIND A POOL
read.strategy.list(chain_id: 8453)
→ Filter for volatile/stable pair (WETH/USDC, cbBTC/USDC, etc.)
→ Note: strategy_id (integer), pool_protocol (Slipstream V1/V2, UniV3, UniV4), fee_APY

// 2. CHECK BORROW COST
read.pool.list(chain_id: 8453)
→ Find the WETH lending pool (address: 0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2)
→ If borrow_apy > fee_apy → stop, strategy not profitable

// 3. CREATE MARGIN ACCOUNT (V3 + creditor = can borrow/leverage)
write.account.create(
  salt: <random uint32, e.g. 3141592653>,
  account_version: 3,   // V3 margin — required for leverage
  creditor: "0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2",  // WETH lending pool — enables borrow
  chain_id: 8453
)
→ Submit tx, note deployed account address from tx receipt
→ Or call read.account.info(wallet_address: ...) to find the new account address

// 4. CHECK ALLOWANCE + APPROVE (skip approve if already sufficient)
read.wallet.allowances(
  owner_address: <owner_wallet>,
  spender_address: <account_address>,
  token_addresses: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],  // USDC
  chain_id: 8453
)
// → If allowance is insufficient or zero:
write.wallet.approve(
  token_address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  // USDC
  spender_address: <account_address>,
  amount: "max_uint256",
  chain_id: 8453
)

// 5. OPEN LEVERAGED LP (atomic: pull USDC from wallet + borrow WETH + swap to ratio + mint LP)
// No separate write.account.deposit needed — write.account.add_liquidity handles the wallet transfer atomically.
write.account.add_liquidity(
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
write.account.automations(
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
read.account.info(account_address: <account_address>, chain_id: 8453)
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

read.account.pnl(account_address: <account_address>, chain_id: 8453)
→ If net yield is consistently negative → evaluate exit

read.pool.list(chain_id: 8453)
→ If borrow_APY risen above fee_APY → exit signal
```

### Responding to health factor drops

```
// Option A: Add collateral (raises health factor, cheapest)
// Check allowance first — skip approve if already sufficient
read.wallet.allowances(owner_address: <wallet>, spender_address: <account>, token_addresses: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"], chain_id: 8453)
write.wallet.approve(token_address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", spender_address: <account>, amount: "max_uint256", chain_id: 8453)
write.account.deposit(account_address: <account>, asset_addresses: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"], asset_amounts: ["<amount>"], chain_id: 8453)

// Option B: Repay some WETH debt (reduces leverage)
// NOTE: you must approve the WETH pool to spend WETH from your wallet first — check allowance, then approve if needed
read.wallet.allowances(owner_address: <wallet>, spender_address: "0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2", token_addresses: ["0x4200000000000000000000000000000000000006"], chain_id: 8453)
write.wallet.approve(token_address: "0x4200000000000000000000000000000000000006", spender_address: "0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2", amount: "max_uint256", chain_id: 8453)
write.account.repay(
  pool_address: "0x803ea69c7e87D1d6C86adeB40CB636cC0E6B98E2",  // WETH pool
  account_address: <account>,
  amount: "<raw_weth_amount_in_wei>",  // e.g. "100000000000000000" = 0.1 WETH
  chain_id: 8453
)

// Option C: Atomic sell USDC collateral → repay WETH debt (one flash tx, no wallet WETH needed)
write.account.deleverage(
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
read.asset_manager.current(account_address: <account>, chain_id: 8453)
// → take the rebalancer's address from `enabled`, then:
write.account.automations_delta(
  account_address: <account>,
  disable: [<rebalancer_address>],
  chain_id: 8453
)

// 1. Get account state — need asset list for the close call
read.account.info(account_address: <account>, chain_id: 8453)

// 2. Unstake if staked (required before close)
write.account.stake(action: "unstake", asset_address: <staked_pm_address>, asset_id: <nft_id>, account_address: <account>, chain_id: 8453)

// 3. Atomic close: burns LP + swaps all tokens to USDC + repays debt — ONE transaction
write.account.close(
  account_address: <account>,
  assets: [
    { asset_address: "<position_manager>", asset_id: <nft_id>, amount: "1", decimals: 1 }
  ],
  receive_assets: [{ asset_address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", decimals: 6 }],  // receive USDC
  slippage: 100,
  chain_id: 8453
)

// 4. Withdraw remaining assets to wallet
write.account.withdraw(
  account_address: <account>,
  asset_addresses: ["0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"],
  asset_amounts: ["<balance>"],
  chain_id: 8453
)
```

#### Fallback: Two-step close (if atomic fails)

If the full atomic close fails, split into two steps:

1. `write.account.close(close_lp_only=true)` — burns LP only, tokens stay in account
2. Then use individual tools: `write.account.deleverage` → `write.account.withdraw`

#### Last resort: Manual step-by-step

Only if both atomic approaches fail:

```
write.account.stake(action: "claim", ...)   // claim fees
write.account.remove_liquidity(adjustment: <amount>)   // partial decrease
write.account.deleverage(...)               // swap collateral → repay debt
write.account.repay(amount: "max_uint256")             // repay remaining from wallet
write.account.withdraw(...)                            // withdraw all to wallet
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
read.wallet.allowances(owner_address: <treasury_wallet>, spender_address: <account>, token_addresses: [<token>], chain_id: 8453)
write.wallet.approve(token_address: <token>, spender_address: <account>, amount: "max_uint256", chain_id: 8453)

// 2. Create account (separate from retail positions)
// For POL without leverage, a spot account (V4) works fine.
// Use V3 + creditor only if you want the option to leverage later.
write.account.create(
  salt: <random uint32>,
  account_version: 0,  // V4 spot — no leverage needed for POL
  chain_id: 8453
)

// 3. Deposit treasury tokens
write.account.deposit(account_address: <account>, ...)

// 4. Open LP (no leverage — deposits are pulled from wallet)
write.account.add_liquidity(
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
write.account.automations(
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
read.account.info → verify position is in range (primary check — no liquidation risk since no leverage)
read.account.pnl  → track IL vs. fee income
                   Note: net negative IL is EXPECTED and ACCEPTABLE for POL
                   The treasury is "paying" for market liquidity
read.strategy.recommendation → check if rebalancing is needed
```

**POL monitoring goal:** Ensure sufficient liquidity is deployed and treasury capital is not eroding excessively — not maximizing return.
