# Strategy Selection & Parameterization

Use this guide to evaluate whether a strategy makes sense and how to configure it. Apply to any LP strategy — not just the delta neutral example in strategies.md.

---

## 1. Pool / Strategy Selection

```
read.strategy.list(chain_id: 8453)           // browse all LP strategies + fee APY
read.pool.list(chain_id: 8453)        // check borrow cost for leveraged strategies
```

**Viability check (leveraged):**

```
net_APY = fee_APY - (leverage - 1) × borrow_APY
```

Must be positive to justify the leverage cost. Higher leverage amplifies both sides.

**Pair type guidance:**

| Pair Type           | Example    | IL Risk  | Leverage Fit         | Range     |
| ------------------- | ---------- | -------- | -------------------- | --------- |
| Volatile / Stable   | WETH/USDC  | High     | Good (delta neutral) | Medium    |
| Correlated volatile | cbBTC/WETH | Moderate | Moderate             | Wider     |
| Stable / Stable     | USDC/USDT  | Very low | Low value            | Very wide |
| Same asset          | wstETH/ETH | Minimal  | Low value            | Tight     |

**Other signals to check:**

- Fee tier: higher fee tier (0.3%, 1%) = more fee per trade, better for volatile pairs
- Volume + TVL: high volume/TVL ratio = fees are being earned actively
- Active Merkl rewards: extra yield on top, check `read.strategy.list` APY breakdown

**`numeraire` — context-dependent meaning:**

- **`write.account.add_liquidity`**: `numeraire` = account base currency (typically the stable side, e.g. USDC for a WETH/USDC position). The backend uses it to denominate calculations and determine the optimal swap ratio. For WETH/USDC: `numeraire = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (USDC).
- **`write.account.deleverage`**: `numeraire` = the debt token you're repaying (e.g. WETH address when repaying WETH debt). This differs from the add liquidity usage.

---

## 2. Range Width

Range width is the central tradeoff in any LP strategy. It is set in the Arcadia platform after enabling the rebalancer. Understanding the full tradeoff is essential for choosing parameters — a simple fee APY comparison is not enough.

**Core principle:** The `strategy_apy` from `read.strategy.list` (list view) is the 7-day average APY computed for that strategy's **default range width** (configured per strategy — e.g. very narrow for stables, ±7.5% / balanced for most volatile pairs). It is sampled every ~3 hours and averaged over 7d. It already reflects a concentrated range — NOT a full-range / pool-level number. Choosing a different range width changes your actual yield: narrower = higher fee capture but more rebalancing cost/risk, wider = lower fees but fewer rebalances. Call `read.strategy.list(strategy_id: <id>)` to see APY broken down by range width (very_narrow, narrow, balanced, wide, very_wide, full_range). The net return after rebalancing costs, IL, and gas determines the optimal width — see the model below.

### The full tradeoff

**Narrower range → higher fee capture, but three compounding costs:**

1. **Delta risk:** A narrow position changes composition rapidly as price moves. A WETH/USDC position that was 50/50 quickly becomes 100% WETH or 100% USDC when price moves even slightly. Your net exposure to the volatile asset fluctuates heavily — you are not truly delta neutral across the range.

2. **IL crystallized per rebalance:** Every rebalance permanently locks in accumulated impermanent loss. It doesn't disappear by rebalancing — it gets realized. More frequent rebalancing means more IL crystallized over time.

3. **Rebalancing costs:** Each rebalance incurs gas costs plus swap slippage (the rebalancer must swap tokens to re-establish the target ratio for the new range). For small or low-fee positions, rebalancing costs can easily exceed earned fees.

**Wider range → lower fee capture, but lower compounding costs:**

- Position stays in range longer → fewer rebalances → less IL crystallized, lower costs
- Delta exposure is spread over a wider price band → composition changes slowly
- Suitable when rebalancing quota is limited (few stAAA, no AAA to pay gas)

### Model-based parameter selection (recommended)

Rather than guessing range width, build a simple expected value model using market data:

```
expected_net_return =
  fee_APY × (time_in_range_fraction)
  − rebalance_frequency × (gas_cost_per_rebalance + slippage_cost_per_rebalance)
  − IL_rate × rebalance_frequency
```

Inputs to estimate from market data:

- **time_in_range_fraction**: given the pool's historical volatility, how often does price stay within ±X% of the current price? Use `read.strategy.list` APY + historical vol data.
- **rebalance_frequency**: how many rebalances per day does the chosen range width require? Wider range = fewer rebalances.
- **gas_cost_per_rebalance**: check current chain gas price × ~4M units per rebalance.
- **IL_rate**: IL as a function of how far price moved before the rebalance; wider ranges accumulate less IL per rebalance.

Vary range width in the model and pick the width that maximizes expected net return for the current market regime. Reassess if volatility regime changes.

**Practical reference (starting point only):**

| Range Width    | Fee Multiplier     | Rebalance Frequency (volatile pair) |
| -------------- | ------------------ | ----------------------------------- |
| Narrow ±2–5%   | Very high (10–50×) | Potentially multiple per day        |
| Medium ±10–20% | Moderate (3–10×)   | Every few days in normal markets    |
| Wide ±30–50%   | Low (1.5–3×)       | Weekly or less                      |

**Decision shortcuts:**

- **Limited stAAA quota** (1 free rebalance/day) → wider range to avoid burning quota
- **High stAAA holdings** (≥9,000) → can sustain narrower range with the increased quota
- **Large position (≥$50k)** → automatically bypasses rate limits; narrower range viable
- **POL / capital preservation** → use wider range or dynamic POL algorithm. See strategies.md.

---

## 3. Leverage Sizing

Leverage multiplies both fee income and liquidation risk.

| Leverage                      | Use case                                    | Collateral ratio at entry | Health factor at entry |
| ----------------------------- | ------------------------------------------- | ------------------------- | ---------------------- |
| 1× (no borrow, `leverage: 0`) | Safe LP, no liquidation risk                | N/A                       | 1.0 (no debt)          |
| 2×                            | Classic delta neutral, volatile/stable pair | ~1.5–2×                   | ~0.5–0.7               |
| 3×+                           | Aggressive yield, only in stable conditions | < 1.5× — watch carefully  | < 0.5 — watch closely  |

**Minimum margin and small positions:** Each lending pool enforces a fixed minimum margin denominated in the pool's numeraire (e.g. WETH, USDC, cbBTC), typically a few dollars in value. This gets added to the debt in the health factor formula: `used_margin = open_debt + minimum_margin`. It ensures liquidations remain profitable (gas costs) and prevents dust attacks. For small positions, this fixed overhead dominates used margin, pushing health factor lower than the leverage ratio alone would suggest — e.g. 2× leverage normally targets HF ~0.5–0.7, but a small position might start at HF ~0.3. Increase position size for a healthier starting HF.

**Profitability check:**

```
borrow_APY × (leverage - 1) < fee_APY × leverage   → leverage is profitable
```

**Two safety metrics — collateral ratio vs health factor:**

The API returns `health_factor = 1 - (used_margin / liquidation_value)`. This is between 0 and 1: higher is safer. `1` = no debt, `0` = liquidation threshold. See SKILL.md Key Constraints.

A useful complementary metric is the **collateral ratio** — a rough estimate of how much buffer you have:

```
collateral_value × collateral_factor
─────────────────────────────────────  ≈ collateral ratio
         debt_value
```

Target collateral ratio ≥ 1.5 at entry (≈ health factor ~0.5+). Never open below 1.3 (≈ health factor ~0.3).

**When to use less leverage:**

- Borrow APY rising (utilization climbing in lending pool)
- Market showing high volatility (gap risk)
- Position already near support/resistance — a breakout would spike debt fast
- Health factor dropping toward 0.5 (check with `read.account.info`)

---

## 4. Combining Automation

| Combination                       | Compatible   | Notes                                                                                                                       |
| --------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------- |
| `rebalance` + `compound_fees`     | ✅ Yes       | Rebalance compounds at rebalance time; compound_fees adds compounding between rebalances.                                   |
| `rebalance` + `claim_rewards`     | ✅ Yes       | Claims yield between rebalances. Order is handled by the keeper's claim-before guard.                                       |
| `rebalance` + `claim_merkl`       | ✅ Yes       | Always combine when the pool has Merkl incentives. Zero conflict.                                                           |
| `compound_fees` + `claim_merkl`   | ✅ Yes       | Merkl rewards are claimed separately from trading fees.                                                                     |
| `compound_fees` + `claim_rewards` | ⚠️ Per token | Valid only as a partition: each yielding token must go to exactly one of the two, and every yielding token must be covered. |
| `add_to_lp` + anything            | ✅ Yes       | Independent fold. Only constraint: a folded token cannot be a convert `buy_token`.                                          |

---

## 5. Exit Signals

Monitor periodically with `read.account.info` and `read.account.pnl`. Exit or adjust when:

| Signal                           | Threshold                | Action                                |
| -------------------------------- | ------------------------ | ------------------------------------- |
| Borrow APY > fee APY             | Persists 3+ checks       | Exit strategy — no longer profitable  |
| Health factor falling            | < 0.5                    | Add collateral or reduce debt         |
| Health factor critical           | < 0.2                    | Immediate action required             |
| Position out-of-range repeatedly | Bot can't keep up        | Widen range or reduce leverage        |
| Net PnL negative over time       | Check `read.account.pnl` | Evaluate whether IL is outpacing fees |

**Closing in volatile conditions:** Atomic close (`write.account.close`) may revert during high volatility or for low-liquidity pools because on-chain state diverges from when the backend computed the calldata. If atomic close fails, fall back to individual tools with tighter slippage — see strategies.md closing section for the full fallback sequence.

---

## 6. Quick Checklist Before Opening a Position

```
[ ] read.strategy.list → fee_APY noted (7d avg for default range; call with strategy_id for per-range APY)
[ ] read.pool.list → borrow_APY noted (if leveraged)
[ ] net_APY = fee_APY - (leverage-1) × borrow_APY > 0
[ ] Pair type matches strategy (volatile/stable for delta neutral)
[ ] Range width: modeled or estimated for pair volatility + stAAA quota
[ ] Leverage targets collateral ratio ≥ 1.5 at entry (health factor ≥ 0.5)
[ ] Merkl rewards active? → plan to enable Merkl Operator
[ ] Prefer compounding or cash flow? → Compounder vs. Yield Claimer
```
