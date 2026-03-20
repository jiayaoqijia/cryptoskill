# Autonomous Trading Reference

This document contains detailed configuration and behavior for autonomous trading mode, cron-based monitoring, and the learning/adaptation system.

For the main skill overview, see [SKILL.md](../SKILL.md).

---

## Operating Modes

### Supervised Mode (Default)

All trades require explicit user confirmation before execution. The agent:

- Analyzes tokens and presents recommendations with reasoning
- Waits for user approval before executing any buy or sell
- Monitors stop-loss/take-profit conditions and **notifies** the user, but does NOT auto-execute
- Reports portfolio status and scan results for user review

### Autonomous Mode (Opt-in)

Enable by setting `require_trade_confirmation: false` in `memory/trading-preferences.json`.

**Automatic actions (no user confirmation needed):**
- Scanning trending tokens (default: top 10 per scan)
- Running full analysis pipeline on candidate tokens
- Checking portfolio status and PnL
- Executing trades that pass ALL criteria in the Bullish Checklist
- Stop-loss sells when unrealized loss exceeds threshold
- Take-profit sells when gain exceeds target

**Still requires user confirmation even in autonomous mode:**
- Risk level is "medium" (ambiguous signals)
- Position size exceeds user-defined max
- Selling at a loss outside stop-loss rules
- Any action outside the defined entry/exit strategies

**Reporting:**
- After each trade: summarize analysis result + trade details (concise text, not raw JSON)
- After each scan: brief summary of tokens scanned, why they passed/failed
- On errors: report the issue and suggest next steps

---

## Automated Monitoring (Cron)

The recommended setup uses **two OpenClaw cron jobs** working together:

| Job | Interval | Purpose |
|-----|----------|---------|
| `stop-loss-tp` | Every **5 min** | Check portfolio, notify on stop-loss / take-profit conditions |
| `discovery-scan` | Every **1 hour** | Discover new tokens, analyze, and recommend qualifying ones |

This separation ensures time-sensitive monitoring runs frequently, while the heavier discovery + analysis pipeline runs at a sustainable pace.

### Default Setup — Supervised (Recommended)

Run this to install both cron jobs in supervised mode (analysis-only, no auto-execution):

```bash
source ~/.openclaw/workspace/.env && bash scripts/cron-examples.sh setup-default
```

### Autonomous Setup

For autonomous trading (auto-buys and auto-sells), use:

```bash
source ~/.openclaw/workspace/.env && bash scripts/cron-examples.sh setup-autonomous
```

> **WARNING:** Autonomous mode enables automatic trade execution. Only use with a dedicated low-value wallet.

### Manual Cron Configuration

```bash
# Job 1: Stop-loss / Take-profit — every 5 minutes
openclaw cron add \
  --every 5m \
  --name "stop-loss-tp" \
  --prompt "Load the kryptogo-meme-trader skill. Source .env. Call /agent/portfolio with the agent wallet.
For each open position:
- If unrealized PnL ≤ -stop_loss_pct → notify user with sell recommendation (stop-loss).
- If unrealized PnL ≥ +take_profit_pct → notify user with sell recommendation (take-profit).
Read thresholds from memory/trading-preferences.json (defaults: stop_loss_pct=30, take_profit_pct=100).
Report triggered conditions to the user. Do NOT auto-execute sells. If no action needed, stay silent."

# Job 2: Discovery & Analysis — every 1 hour
openclaw cron add \
  --every 1h \
  --name "discovery-scan" \
  --prompt "Load the kryptogo-meme-trader skill. Source .env. Execute the full discovery workflow:
1. Read memory/trading-preferences.json for current parameters.
2. Read memory/trading-lessons.md (if exists) to avoid known bad patterns.
3. Check open positions count — skip buying if at max_open_positions.
4. Scan for candidates:
   - Pro/Alpha tier: call /signal-dashboard (sort_by=signal_count, page_size=10).
   - Free tier: call /agent/trending-tokens with min_market_cap filter.
5. Run top candidates through the 7-step analysis pipeline.
6. Send recommendations to the user. Do NOT auto-execute buys.
7. Update memory/trading-state.json with scan timestamp.
8. If any trades were closed since last scan: run post-trade reflection and update trading-lessons.md.
Report ALL findings to the user. If nothing happened, stay silent."
```

### Quick Commands

```bash
# List active cron jobs
openclaw cron list

# Pause trading (remove both jobs)
openclaw cron remove stop-loss-tp
openclaw cron remove discovery-scan

# Resume
source ~/.openclaw/workspace/.env && bash scripts/cron-examples.sh setup-default
```

### First-Time Auto-Setup (Agent Instruction)

The first time this skill is loaded, check if `stop-loss-tp` and `discovery-scan` cron jobs exist (via `openclaw cron list`). If not, proactively offer to set them up.

### Alternative: Heartbeat-Based Monitoring

If you prefer a simpler setup (one check every ~30 min instead of two cron jobs), add this to `HEARTBEAT.md`:

```markdown
## Trading Agent
- Check portfolio: call /agent/portfolio, report stop-loss/take-profit conditions to user
- Scan for opportunities: use signal dashboard (Pro/Alpha) or trending tokens API
- Send recommendations to user for approval
- Log closed trades to journal, run post-trade reflection
- ALWAYS report any triggered condition to the user
```

**Tradeoff:** Heartbeat batches everything into one turn (~30 min intervals). Stop-loss notifications could be delayed up to 30 minutes.

### Monitoring Workflow

1. **Portfolio check** (every 5 min via `stop-loss-tp`)
   - Notify on stop-loss if unrealized loss > `stop_loss_pct`
   - Notify on take-profit if unrealized gain > `take_profit_pct`
   - Flag stale positions (held > 7 days with no significant movement)
2. **Signal scan** (every 1h via `discovery-scan`)
   - **Pro/Alpha tier:** Use `/signal-dashboard` first — pre-filtered for smart money activity
   - **Free tier:** Fall back to `/agent/trending-tokens` with filters
   - Run top results through the 7-step analysis pipeline
   - Send recommendations to user
3. **State persistence** → Save to `memory/trading-state.json`
4. **Learning check** → If any trades were closed since last check:
   - Log outcome to `memory/trading-journal.json`
   - Run post-trade reflection
   - If loss >20%, trigger Loss Post-Mortem
   - If 20+ trades or 7+ days since last review, trigger Strategy Review

### Notification Rules

**Mandatory — agent MUST message the user when:**
- Any trade condition is triggered (stop-loss, take-profit, buy recommendation)
- A position is flagged for manual review (medium risk, stale, etc.)
- An error prevents normal operation (API down, insufficient SOL, quota exceeded)

**Stay silent when:**
- Portfolio checked, no action needed
- Tokens scanned, none qualified

### Kill Switch

To immediately stop all autonomous trading:
1. **Remove cron jobs:** `openclaw cron remove stop-loss-tp && openclaw cron remove discovery-scan`
2. **Remove Trading Agent section from HEARTBEAT.md** (if using heartbeat mode)
3. **Remove or rename `.env`** — prevents any API calls or signing

### Failure Recovery

If the agent crashes or session ends mid-trade:
- On startup, **ALWAYS** call `/agent/portfolio` first to check current holdings
- Compare with `memory/trading-state.json` to detect any untracked positions
- Report any discrepancies to the user immediately

---

## Learning & Adaptation

The agent improves over time by recording every trade, analyzing outcomes, and adjusting its strategy.

### Trade Journal

Every trade (buy or sell) MUST be logged to `memory/trading-journal.json` immediately after execution:

```json
{
  "trades": [
    {
      "id": "2026-02-25T14:30:00Z_BONK",
      "token_mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
      "symbol": "BONK",
      "chain_id": "501",
      "action": "BUY",
      "amount_sol": 0.1,
      "token_amount": 150000000,
      "price_at_entry": 0.0000234,
      "market_cap_at_entry": 1500000,
      "timestamp": "2026-02-25T14:30:00Z",
      "entry_reasoning": {
        "cluster_ratio": 0.35,
        "cluster_change_1d": 0.05,
        "smart_money_count": 3,
        "dev_exited": true,
        "sniper_cleared": true,
        "signal_source": "signal_dashboard",
        "risk_level": "low"
      },
      "outcome": null
    }
  ]
}
```

When a position is closed, update the BUY entry's `outcome`:

```json
{
  "outcome": {
    "exit_price": 0.0000468,
    "exit_timestamp": "2026-02-26T09:15:00Z",
    "exit_reason": "take_profit",
    "pnl_sol": 0.1,
    "pnl_pct": 100.0,
    "holding_duration_hours": 18.75,
    "cluster_ratio_at_exit": 0.28,
    "lesson": "Cluster started distributing 2h before exit — could have sold earlier"
  }
}
```

### Mandatory Post-Trade Reflection

After every SELL (win or loss), the agent MUST:
1. Compare entry reasoning with actual outcome
2. Identify what analysis got right and what it missed
3. Write a one-sentence `lesson` in the outcome record
4. If loss >20%, do a Loss Post-Mortem

### Loss Post-Mortem

When a trade results in loss >20%:
1. Re-run analysis on the token at current state
2. Identify the miss: signal ignored? Timing error? External event?
3. Classify: `signal_miss`, `timing_error`, `external_event`, `parameter_drift`, `overconfidence`
4. Log to `memory/trading-lessons.md`

### Periodic Strategy Review

**Trigger:** Every 20 trades OR every 7 days.

1. Calculate aggregate stats (win rate, avg win/loss, best strategies, holding duration)
2. Identify patterns
3. Propose parameter adjustments to the user
4. Save review to `memory/strategy-reviews/YYYY-MM-DD.md`
5. Update preferences only after user approves

### Learning Memory Files

| File | Purpose | Updated |
|------|---------|---------|
| `memory/trading-journal.json` | Every trade with entry reasoning + outcome | After every trade |
| `memory/trading-lessons.md` | Patterns learned from losses | After losing trades |
| `memory/strategy-reviews/YYYY-MM-DD.md` | Periodic aggregate analysis | Every 20 trades or 7 days |
| `memory/trading-preferences.json` | Current strategy parameters | When user approves changes |
| `memory/trading-state.json` | Runtime state (open positions, last scan) | After every action |

### What the Agent Should NOT Do

- **Never auto-adjust parameters without user approval**
- **Never delete journal entries**
- **Never ignore a post-mortem**
- **Never blame "market conditions" without specifics**

---

## Implementation Notes & Lessons

### 1. Transaction Signer Must Match Your Wallet

Before signing, always verify that the fee payer matches your `SOLANA_WALLET_ADDRESS`. Always pass `wallet_address` in the `POST /agent/swap` request body.

### 2. `/agent/swap` Supports `wallet_address` Parameter

When provided, the unsigned transaction uses that address as fee payer and signer. Without it, the API defaults to the wallet associated with your API key.

### 3. Labels Are History, Not Current State

`/token-wallet-labels` returns behavioral labels based on historical actions. **Always verify current holdings via `/balance-history`** before making risk decisions.

### 4. Analysis Pipeline Order Is Mandatory

Never skip to trading without completing analysis:
1. Signal dashboard / trending tokens → candidates
2. Market cap / liquidity filter → eliminate small/illiquid tokens
3. Cluster multi-timeframe analysis → assess accumulation/distribution
4. Label + `/balance-history` verification → confirm sell pressure
5. Decision checklist → final go/no-go
6. Swap + sign + submit → execute trade
