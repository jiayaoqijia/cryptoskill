# Autonomous Strategy Framework

This guide helps agents make informed decisions about perpetual futures trading across exchanges.
You are not expected to follow rigid rules — use this as a decision framework and develop your own judgment over time.

## Core Concepts

### Funding Rate Mechanics
- Funding settles **every 1 hour** on every venue except Aster, whose interval is **per symbol** (from its fundingInfo `fundingIntervalHours`)
- QFEX funding rates are unverified: excluded from scans / arb; shown only with `arb scan --rates --include-unverified` (display only)
- Positive rate = longs pay shorts, negative rate = shorts pay longs
- Rates are displayed annualized: per hour ≈ `annual / 8760`
- Scan opportunities: `perp --json arb scan --min 5` (shows grossSpread, netSpread, longExch, shortExch)

### Opportunity Cost Awareness

**This is critical.** Before switching any position, calculate the FULL cost of the switch:

```
Switch Cost =
  + close current position (trading fee + slippage)
  + withdraw from exchange (gas fee + time)
  + bridge to target chain (bridge fee + gas + time)
  + deposit to new exchange (gas fee + time)
  + open new position (trading fee + slippage)
```

Query each component:
```bash
perp --json -e <FROM> trade check <SYM> <SIDE> <SIZE> --leverage <L>   # close cost estimate
perp --json funds bridge quote --from <CHAIN> --to <CHAIN> --amount <AMT>  # bridge cost
perp --json -e <TO> trade check <SYM> <SIDE> <SIZE> --leverage <L>     # open cost estimate
```

**Only switch if:**
```
expected_hourly_gain × expected_hours_held > total_switch_cost × safety_margin
```

Where `safety_margin` should be at least 2x — rates can change before you finish switching.

### Time Cost
Switching is not instant. Estimate total transition time:
- Exchange withdrawal: 1-30 minutes
- Bridge transfer: 1-20 minutes (CCTP ~2-5 min, deBridge ~5-15 min)
- Exchange deposit confirmation: 1-10 minutes

During transition, you are **unhedged**. Price can move against you. Factor this risk in.

## Funding Rate Arbitrage

### How It Works
1. Find a symbol where Exchange A pays significantly more funding than Exchange B
2. Go short on Exchange A (receive funding) and long on Exchange B (pay less funding)
3. Net = funding received - funding paid - fees
4. The position is market-neutral (delta-hedged) — you profit from the rate spread

### Discovery Loop
```bash
perp --json arb scan --min 5             # find spreads > 5% annual (shows longExch/shortExch/netSpread)
perp --json arb scan --rates             # raw funding rates across all exchanges
perp --json arb scan --history <SYMBOL>  # historical funding for a symbol
# NOTE: legacy 'arb rates'/'arb prices'/'arb dex' are removed — all routes go through 'arb scan'
```

### CRITICAL: Reading arb scan Results

The `arb scan` output tells you EXACTLY what to do:

```
longExch: "hyperliquid"   → open LONG on this exchange
shortExch: "pacifica"     → open SHORT on this exchange
grossSpread: 15.2         → funding spread, annualized %
netSpread: 12.87          → annualized % after round-trip trading costs amortized over --hold-days (default 7)
                            (and --bridge-cost if given)
```

**Rules:**
1. **ALWAYS follow longExch/shortExch directions exactly.** DO NOT reverse them.
2. **NEVER enter if netSpread ≤ 0.** Negative netSpread = loss after fees over the assumed hold. A shorter real hold makes costs weigh more — re-scan with your `--hold-days`.
3. The direction logic: go LONG where funding is negative (longs receive), go SHORT where funding is positive (shorts receive).

**Why these directions?**
- Positive funding (+) = longs pay shorts → you want to be SHORT to receive
- Negative funding (-) = shorts pay longs → you want to be LONG to receive

### Decision Framework
When evaluating an arb opportunity:

1. **Is the spread real?** Check if rates are stable or spiking temporarily
   - Query rates multiple times over 15-30 minutes
   - A spike that reverts in 1 hour is not worth switching for

2. **What's my current position earning?**
   - If already in a profitable arb, switching has opportunity cost
   - Calculate: `current_hourly_income vs new_hourly_income - switch_cost`

3. **How long will the spread persist?**
   - Historical funding tends to mean-revert
   - Higher confidence in moderate, stable spreads (e.g. 10–50% annualized netSpread) than extreme spikes (hundreds of % annualized)

4. **Can I execute both legs atomically?**
   - Both positions should open near-simultaneously to minimize directional exposure
   - If capital needs to bridge first, you're exposed during transit

### Hold Duration Target

**Before entering any arb position, set a target hold duration.** This is critical for calculating whether the position is worth entering.

```
Expected Funding = notional × (grossSpread% / 100) × target_hours / 8760
Entry/Exit Cost  = open_fees + close_fees + slippage (both legs)
Net Profit       = Expected Funding - Entry/Exit Cost
```
(`netSpread` already does this amortization for `--hold-days`; pass `--hold-days` = your target to read it directly.)

**Only enter if Net Profit > 0 with a comfortable margin.**

Guidelines for hold duration:
- **Moderate, stable spreads (≈10–50% annualized):** target days, not hours — the funding must accumulate past entry/exit costs.
- **Elevated spreads (≈50–100% annualized):** shorter targets; likely to compress. Take profit earlier.
- **Spikes (well above 100% annualized):** revert quickly — enter only if the funding over a few settlements covers entry/exit costs.

**Re-evaluate at each funding settlement (hourly on most venues):**
1. Is the spread still above breakeven for the remaining target hours?
2. If spread compressed, should I exit early or extend the hold?
3. Has a better opportunity appeared? (Remember: switching has its own cost)

**Track your actual hold durations vs targets over time.** This builds intuition for how long spreads persist on each exchange pair.

Example entry decision log:
```
Entry: BTC HL↔PAC | $1000/leg | grossSpread 80% annual | Target hold: 7d
Expected funding: 1000 × 0.80 × 168 / 8760 ≈ $15.3
Entry/exit cost: ~$4 (fees + slippage, both legs, open + close)
Net expected: ≈ $11 → ENTER (arb scan --hold-days 7 netSpread > 0 agrees)
Day 3 check: grossSpread compressed to 10% → remaining 4d earn ≈ $1.1 → EXIT if it keeps falling / flips, or a better net opportunity exists
Actual hold: 3d | log actual funding vs estimate
```

### Monitoring Active Positions
```bash
perp --json portfolio                    # unified multi-exchange view
perp --json risk status                  # cross-exchange risk assessment (level, violations, canTrade)
perp --json -e <EX> account positions    # per-exchange positions
perp --json arb scan --min 5             # are current rates still favorable?
```

### Order Execution: Matched Size, Sequential Legs

**The #1 rule of arb execution: BOTH LEGS MUST HAVE THE EXACT SAME SIZE.** A size mismatch means you have net directional exposure — the whole point of arb is to be delta-neutral.

#### Step 1: Determine Matched Order Size

Before placing ANY order, compute a single `ORDER_SIZE` that BOTH exchanges can fill:

```bash
# 1. Check orderbook depth on BOTH sides
perp --json -e <LONG_EX> market book <SYM>     # check asks (you're buying)
perp --json -e <SHORT_EX> market book <SYM>     # check bids (you're selling)

# 2. Find immediately fillable size at best 2-3 ticks
#    LONG side: sum ask sizes at best 2-3 ask levels → fillable_long
#    SHORT side: sum bid sizes at best 2-3 bid levels → fillable_short

# 3. ORDER_SIZE = min(fillable_long, fillable_short, desired_size)
#    The SMALLER side limits your matched size.
```

**Example:**
```
LONG exchange asks:  $85.00 × 0.5, $85.01 × 0.3 → fillable = 0.8
SHORT exchange bids: $85.10 × 0.4, $85.09 × 0.2 → fillable = 0.6
Desired size: 1.0

→ ORDER_SIZE = min(0.8, 0.6, 1.0) = 0.6
→ Both legs get exactly 0.6
```

**CRITICAL: Each exchange has its own minimum order size and step size.**
```bash
perp --json -e <EX> market info <SYM>    # check maxLeverage, volume, openInterest
```
Round `ORDER_SIZE` to the coarser step size of the two exchanges. If the matched size falls below either exchange's minimum, the arb is NOT executable at this size — reduce target or skip.

#### Step 2: Execute Legs Sequentially with Same Size

Prefer `perp --json arb exec <SYM> <LONG_EX> <SHORT_EX> <USD>` — it does exactly this: long first, then the short sized to the verified long fill, reconcile always on, and an unconfirmed leg quarantines the symbol. Manual legs (below) only when `arb exec` cannot be used.

Once you have a single `ORDER_SIZE`, execute both legs using THAT EXACT SIZE:

```bash
# Leg 1: Open on exchange A
perp --json -e <LONG_EX> trade market <SYM> buy <ORDER_SIZE>

# Verify leg 1 filled
perp --json -e <LONG_EX> account positions

# Leg 2: Open on exchange B with SAME size
perp --json -e <SHORT_EX> trade market <SYM> sell <ORDER_SIZE>

# Verify leg 2 filled
perp --json -e <SHORT_EX> account positions
```

**After both legs, verify sizes match:**
```bash
perp --json -e <LONG_EX> account positions    # size = X
perp --json -e <SHORT_EX> account positions   # size must = X
```
If sizes differ (partial fill, rounding), immediately adjust the larger position to match the smaller one.

#### Step 3: Split Large Orders with `trade split`

For large orders, use the built-in orderbook-aware split execution instead of manual chunking:

```bash
# Single exchange: split $5000 buy into depth-based slices
perp --json -e <EX> trade split <SYM> buy 5000

# With options
perp --json -e <EX> trade split <SYM> buy 5000 --max-slippage 0.5 --max-slices 5 --delay 2000

# Or use --split flag on market command
perp --json -e <EX> trade market <SYM> buy <SIZE> --split
```

How it works:
1. Fetches fresh orderbook before each slice
2. Walks levels via `computeExecutableSize` to find fillable amount at target slippage
3. Places IOC limit at worst acceptable price within slippage tolerance
4. Waits for book to refresh, repeats until target filled or max slices reached

**For arb, both legs must still match.** Use `trade split` on each side independently with the same total USD, then verify sizes match:

```
Leg A: perp --json -e <LONG_EX> trade split <SYM> buy 5000
Leg B: perp --json -e <SHORT_EX> trade split <SYM> sell 5000
→ Verify positions, adjust if sizes differ
```

**Rules:**
1. Each chunk re-checks orderbook depth — liquidity changes between slices
2. For arb: same total USD on both sides, verify matched sizes after execution
3. If one leg fails → STOP immediately, do NOT continue
4. Assess exposure: retry the failed leg, or unwind the completed leg
5. NEVER execute multiple orders on one side without matching the other

#### Using Limit Orders for Better Execution
For non-urgent entries, use limit orders at best bid/ask instead of market:
```bash
perp --json -e <EX> trade limit <SYM> buy <PRICE> <ORDER_SIZE>   # limit order (GTC default; --tif ALO = post-only)
```
This avoids crossing the spread but risks not getting filled. Set a timeout and fall back to market if unfilled. **Both legs must still use the same `ORDER_SIZE`.**

#### Closing Arb Positions: Same Rules Apply
When exiting, close BOTH legs with the SAME size:
```bash
perp --json -e <LONG_EX> trade close <SYM>     # closes full position
perp --json -e <SHORT_EX> trade close <SYM>     # closes full position
```
If positions already have mismatched sizes, close to the smaller size first, then close the remaining delta on the larger side.

### When to Exit
- Spread compressed below your breakeven (including fees)
- One side's funding flipped direction
- Better opportunity found (after accounting for switch cost!)
- Risk limits breached

## Risk Management — THE MOST IMPORTANT SECTION

**Risk management is more important than profit.** A single liquidation can wipe out months of funding rate income. Every decision you make should be filtered through risk first, profit second.

### Understanding Liquidation

When your margin drops below the maintenance requirement, the exchange force-closes your position at a loss. This is **liquidation** — it is catastrophic and must be avoided at all costs.

**Check liquidation distance for every open position:**
```bash
perp --json risk liquidation-distance        # shows % distance from liq price for ALL positions
perp --json -e <EX> account positions        # shows liquidationPrice per position
perp --json -e <EX> account margin <SYM>     # detailed: liquidationPrice, marginRequired, marginPctOfEquity
```

**Liquidation distance is configurable by the user.** You MUST ask the user what risk tolerance they want:
```bash
# Ask user: "What minimum liquidation distance do you want? (default: 5%)"
perp --json risk limits --min-liq-distance <USER_CHOICE>
```

**Action rules based on `risk liquidation-distance` output:**
- `status: "safe"` → no action needed
- `status: "warning"` → monitor more frequently (every 5 minutes)
- `status: "danger"` → alert user, recommend reducing position size

### Leverage and Margin Mode

#### Leverage
Higher leverage = closer liquidation price = higher risk. For funding rate arb:
- **Recommended: 1x-3x leverage.** Arb profits are small but consistent — no need to amplify risk.
- **NEVER exceed 5x for arb positions.** The goal is to collect funding, not to speculate.
- For directional trades (non-arb), leverage should be set according to user's risk tolerance, but always confirm with user.

**Set leverage BEFORE opening a position:**
```bash
perp --json -e <EX> trade leverage <SYM> <LEVERAGE>
# Example: perp --json -e hl trade leverage BTC 2
```

#### Cross vs Isolated Margin

| Mode | Behavior | Use When |
|------|----------|----------|
| **Cross** | All positions share the same margin pool. One position's loss can liquidate everything. | Single position per exchange, or highly correlated positions |
| **Isolated** | Each position has its own margin. Liquidation of one doesn't affect others. | Multiple independent positions, recommended for arb |

**For funding rate arb, use ISOLATED margin.** Each leg should be independent — if one side gets liquidated, the other side survives.

```bash
perp --json -e <EX> wallet manage margin <SYM> isolated   # set isolated margin
perp --json -e <EX> trade leverage <SYM> <LEV> --isolated   # set leverage + isolated at once
```

**Check current settings:**
```bash
perp --json -e <EX> account settings         # shows leverage and margin_mode per symbol
```

### Risk Limits — Configure Before Trading

Set your risk limits FIRST, before any trading activity.
Limits can be set in **USD or % of equity** (when both are set, the stricter one applies):
```bash
perp --json risk limits \
  --max-leverage 5 \
  --max-margin 95 \
  --max-position-pct 80 \
  --max-drawdown 500 \
  --max-position 50000 \
  --max-exposure 100000 \
  --daily-loss 200 \
  --min-liq-distance 5
```

**Use % limits for small portfolios.** A $65 portfolio with `--max-drawdown 500` is meaningless.
With `--max-drawdown-pct 10`, the effective limit auto-adjusts to $6.50.

**IMPORTANT: Ask the user about their risk tolerance BEFORE setting limits.** Key questions:
- "How much leverage are you comfortable with?" (default: 5x for arb)
- "What's your maximum acceptable loss?" (default: $500)
- "How close to liquidation are you willing to get?" (default: 5%)

These limits are enforced by `perp risk check`. Always run it before trades:
```bash
perp --json risk check --notional 1000 --leverage 3
# Returns: { "allowed": true/false, "reason": "...", "riskLevel": "low/medium/high/critical" }
```

**If `allowed: false`, do NOT proceed.** Report to user why.

### The Risk Monitoring Loop

**This is your primary responsibility.** While positions are open, run this loop continuously:

#### Every 15 minutes:
```bash
perp --json risk status                      # overall risk level + violations
perp --json risk liquidation-distance        # % distance from liq price for ALL positions
perp --json -e <EX> account positions        # check each position's P&L
```

Check the output:
- `risk status` returns `level` (low/medium/high/critical) and `canTrade` (boolean)
- If `level` is "high" or "critical" → take action immediately
- If `canTrade` is false → do NOT open new positions
- Check `violations[]` for specific issues

#### Every hour (at funding settlement):
```bash
perp --json portfolio                        # total equity across exchanges
perp --json arb scan --min 5                  # are rates still favorable?
perp --json -e <EX_A> account positions      # P&L on leg A
perp --json -e <EX_B> account positions      # P&L on leg B
```

Compare each position's unrealized P&L. In a perfect arb, they should roughly offset. If one side is losing significantly more than the other is gaining, investigate — the hedge may not be balanced.

#### Immediate action triggers:
| Condition | Action |
|-----------|--------|
| `risk status` level = "critical" | Reduce positions immediately |
| Liquidation price within 10% of current price | Reduce that position's size |
| `canTrade` = false | Stop all new trades, focus on reducing risk |
| One arb leg closed unexpectedly | Close the other leg IMMEDIATELY (naked exposure) |
| Unrealized loss > max-drawdown limit | Close losing positions |
| Margin utilization > 80% | Do not open new positions |

### Position Sizing

Think in terms of total capital across all exchanges:
```bash
perp --json portfolio                        # totalEquity, marginUtilization, concentration
```

Rules of thumb:
- **Single position notional < 80% of that exchange's available balance**
- **Total margin used < 80% of total equity** — leave buffer for adverse moves
- **Capital in transit (bridging) counts as "at risk"** — it's not available for margin

### Per-Exchange Balance Constraints

**CRITICAL: You can only trade with the balance available ON THAT EXCHANGE.**

Each exchange holds its own separate balance. Before entering any arb:
```bash
perp --json portfolio -e <EX_A>                 # check available balance on exchange A
perp --json portfolio -e <EX_B>                 # check available balance on exchange B
```

**Size each leg to fit the available balance on that exchange:**
```
Wrong:  total portfolio = $65 → 25% = $16 per leg → but Exchange A only has $10
Right:  Exchange A has $10, Exchange B has $15 → max leg size = $10 (limited by smaller side)
```

If one exchange has insufficient balance:
- Reduce position size to fit the smaller balance, OR
- Bridge capital first (but account for bridge fees + time + unhedged risk during transit)

### Stop Loss for Arb Positions

Even "market-neutral" arb can lose money if:
- One exchange goes down and you can't manage that leg
- Extreme funding spike in the wrong direction
- Slippage on entry/exit far exceeds estimates

**Always set stop losses on both legs** (`long|short` = the OPEN position's side; legs are reduce-only, sized to the live position):
```bash
perp --json --dry-run -e <EX_A> trade tpsl <SYM> long  --sl <PRICE>              # leg A (long): SL below mark
perp --json -e <EX_A> trade tpsl <SYM> long  --sl <PRICE>
perp --json -e <EX_B> trade tpsl <SYM> short --sl <PRICE>                       # leg B (short): SL above mark
perp --json -e <EX> trade tpsl <SYM> long --sl <PRICE> --tp <PRICE>             # TP + SL together
```

### What to Track Over Time
As you operate, build awareness of:
- Which symbols consistently have the best funding spreads
- Which exchange pairs have the lowest switching cost
- Typical bridge times for each route
- How quickly funding rate spikes mean-revert
- Your own execution quality (slippage vs estimates)
- **How close your positions have come to liquidation** — learn from near-misses

This is YOUR operational knowledge. Use it to make better decisions over time.

## Capital Efficiency

### Cross-Exchange Capital Allocation
Your capital is split across exchanges. Rebalancing has real costs:
```bash
perp --json funds bridge quote --from solana --to arbitrum --amount 1000
perp --json funds rebalance plan                  # auto-compute optimal moves across exchanges
```

Before rebalancing, ask:
- Is the capital earning anything where it currently sits?
- Is the destination opportunity worth the bridge fee + downtime?
- Can I use the capital more efficiently without moving it?

### Idle Capital
Capital sitting in an exchange wallet but not in a position is earning 0%.
Options:
- Open a low-risk funding collection position
- Bridge to where it's more useful
- Sometimes idle cash IS the right position (dry powder for opportunities)

## Summary

Your job is not to blindly follow rules — it's to develop judgment:
- Every switch has a cost. Calculate it before acting.
- Rates change hourly. What's profitable now may not be in 2 hours.
- Build pattern recognition over time.
- The best arb is one you're already in, not one you're chasing.
