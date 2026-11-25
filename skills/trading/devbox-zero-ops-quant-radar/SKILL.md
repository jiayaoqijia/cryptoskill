---
name: quant-radar
description: >-
  Zero-dependency Python CLI for real-time cross-exchange perpetual funding
  arbitrage across Hyperliquid, Binance, and Bybit, Polymarket NegRisk
  sum-to-1 and short-dated mispricing scanning, fee-aware delta-neutral paper
  trading (with 4h rollover hysteresis, immediate sign-inversion stop-loss,
  and extreme spike-regime filtering), and anti-spam Webhook/Telegram alerts.
---

# quant-radar

Run real-time market scans, delta-neutral paper-trading simulations, and threshold alerts from a single standard-library Python script (`scripts/radar.py`).

- **Runtime:** Python 3.8+ standard library only (`urllib`, `json`, `argparse`).
- **Auth:** No API keys required for market scans or paper trading (queries public read-only Hyperliquid Mainnet and Polymarket Gamma APIs).
- **Safety default:** Strictly read-only analytics and local simulation (`$0` live capital at risk). Outbound notifications require explicit webhook/Telegram credentials and support `--dry-run`.

## When to Use

- Scanning live cross-exchange perpetual funding rate spreads across **Hyperliquid (`HlPerp`)**, **Binance (`BinPerp`)**, and **Bybit (`BybitPerp`)** with liquidity and taker-fee break-even filters.
- Detecting **Polymarket NegRisk** multi-outcome sum-to-1 mispricings (`BUY_ALL_YES` / `SELL_OVERPRICED_YES`) and **short-dated high-probability yield** markets (`<= 35d`).
- Running a persistent, fee-aware **delta-neutral paper portfolio** with 4h rollover exit hysteresis, negative sign-inversion stop-loss, and spike-regime entry filtering.
- Generating human-readable market digests or dispatching cooldown-throttled **Webhook / Telegram** threshold alerts in scheduled jobs.

## CLI Usage Examples

Invoke `scripts/radar.py` from the skill directory (pass explicit `--ledger` and `--state-file` paths outside the skill bundle when running persistently):

```bash
# 1. Cross-venue perp funding scan (Hyperliquid vs Binance vs Bybit)
python scripts/radar.py funding --min-oi 500000 --min-vol 1000000 --rt-fee-bps 18

# 2. Polymarket NegRisk sum-to-1 & short-dated bond scan
python scripts/radar.py polymarket --limit 40 --min-vol 10000

# 3. Concise text digest (or add --json for combined structured payload)
python scripts/radar.py digest
python scripts/radar.py digest --json

# 4. Persistent fee-aware delta-neutral paper portfolio
python scripts/radar.py paper \
  --ledger ./paper_ledger.json \
  --equity 1000 \
  --min-apr 25 \
  --max-entry-apr 500 \
  --exit-apr 8 \
  --emergency-exit-apr -25 \
  --confirm-exit-ticks 2

# 5. Preview threshold alerts without sending (--dry-run)
python scripts/radar.py notify \
  --min-spread-apr 60 \
  --max-breakeven-hours 36 \
  --min-bond-apr 40 \
  --cooldown-min 60 \
  --state-file ./alert_state.json \
  --dry-run

# 6. Live alert dispatch via environment variables (generic JSON webhook or Telegram Bot API)
QUANT_RADAR_WEBHOOK="https://hooks.example.com/..." \
  python scripts/radar.py notify --min-spread-apr 60 --state-file ./alert_state.json

TELEGRAM_BOT_TOKEN="..." TELEGRAM_CHAT_ID="..." \
  python scripts/radar.py notify --min-spread-apr 60 --state-file ./alert_state.json
```

### Subcommand Reference

| Subcommand | Key Flags & Defaults | Purpose |
| --- | --- | --- |
| `funding` | `--min-oi 500000`, `--min-vol 1000000`, `--rt-fee-bps 18.0` | Rank liquid cross-venue funding spreads and single-venue HL funding |
| `polymarket` | `--limit 40`, `--min-vol 10000` | Flag NegRisk sum-to-1 deviations and `0.5–35d` high-probability yields |
| `digest` | `--json` | Emit compact text brief (or combined JSON snapshot) of funding + Polymarket |
| `paper` | `--ledger`, `--equity 1000`, `--min-apr 25`, `--max-entry-apr 500`, `--exit-apr 8`, `--emergency-exit-apr -25`, `--confirm-exit-ticks 2` | Update persistent delta-neutral paper ledger with elapsed-time accrual and risk guards |
| `notify` | `--min-spread-apr 50`, `--max-breakeven-hours 48`, `--min-bond-apr 40`, `--cooldown-min 60`, `--state-file`, `--webhook`, `--telegram-token`, `--telegram-chat-id`, `--dry-run` | Filter signals, enforce per-key cooldown, and post to Webhook / Telegram |

## Output Schema

All subcommands except plain-text `digest` print UTF-8 JSON to `stdout`.

### `funding`

```json
{
  "observed_utc": "2026-11-24T12:00:00Z",
  "liquid_markets_scanned": 64,
  "filters": { "min_oi_usd": 500000.0, "min_vol_usd": 1000000.0, "rt_fee_bps": 18.0 },
  "top_cross_venue_arb": [
    {
      "symbol": "EXAMPLE",
      "mark_px": 1.25,
      "oracle_px": 1.249,
      "basis_bps": 8.01,
      "oi_usd": 4200000.0,
      "vol_24h_usd": 12500000.0,
      "hl_hourly_rate": 0.0001,
      "hl_apr_pct": 87.6,
      "cash_carry_breakeven_hours": 15.0,
      "venues": {
        "HlPerp": { "rate": 0.0001, "interval_hours": 1.0, "apr_pct": 87.6 },
        "BinPerp": { "rate": 0.0001, "interval_hours": 8.0, "apr_pct": 10.95 }
      },
      "best_cross_arb": {
        "long_venue": "BinPerp",
        "short_venue": "HlPerp",
        "long_apr_pct": 10.95,
        "short_apr_pct": 87.6,
        "spread_apr_pct": 76.65,
        "breakeven_hours": 20.57
      }
    }
  ],
  "top_single_hl_funding": [],
  "all_cross_venue_by_symbol": {},
  "all_predicted_venues": {}
}
```

### `polymarket`

```json
{
  "observed_utc": "2026-11-24T12:00:00Z",
  "events_scanned": 40,
  "negrisk_sum_deviations": [
    {
      "event": "Event Title",
      "url": "https://polymarket.com/event/event-slug",
      "outcomes_count": 4,
      "yes_sum": 0.978,
      "raw_edge_pct": 2.2,
      "direction": "BUY_ALL_YES",
      "vol_24h_usd": 180000.0
    }
  ],
  "short_dated_high_prob_bonds": [
    {
      "question": "Market question?",
      "side": "YES",
      "price": 0.955,
      "days_to_expiry": 9.5,
      "gross_return_pct": 4.71,
      "annualized_apr_pct": 181.04,
      "vol_24h_usd": 95000.0,
      "url": "https://polymarket.com/event/event-slug"
    }
  ]
}
```

### `paper`

Returns and saves the ledger state: `created_utc`, `last_updated_utc`, `snapshots_count`, `initial_equity_usd`, `cash_usd`, `mark_to_market_equity_usd`, `net_return_pct`, `realized_pnl_usd`, `total_fees_paid_usd`, `total_funding_accrued_usd`, `open_positions` (dict keyed by `symbol`, tracking `long_venue`, `short_venue`, `entry_spread_apr_pct`, `last_spread_apr_pct`, `breakeven_hours`, `margin_usd`, `notional_usd`, `entry_fee_usd`, `accrued_funding_usd`, `below_exit_ticks`, `missing_quote_ticks`), and `closed_trades` (appends `closed_utc`, `exit_fee_usd`, `net_pnl_usd`, `close_reason`).

### `notify`

Returns `dry_run`, `sent`, `targets`, `alert_count`, `matched_total`, `suppressed_by_cooldown`, plus `message` + `alerts` (each with `key`, `kind`, `headline`, `metrics`) on dry-run/empty sends, or `delivery` (`webhook_status` / `telegram_ok`) on live dispatch.

## Methodology Details

Read [references/methodology.md](references/methodology.md) before tuning thresholds or interpreting edge cases:

- Multi-interval funding APR annualization and fee break-even formulas
- 4h settlement rollover hysteresis (`--confirm-exit-ticks`) and missing-quote protection
- Sign-inversion stop-loss (`--emergency-exit-apr`) and spike-regime filter (`--max-entry-apr`)
- Polymarket NegRisk overround/underround and short-dated bond yield math

## Risk Caveats

- **Indicative quotes vs. executable fills:** Hyperliquid `predictedFundings` and Polymarket Gamma `outcomePrices` are indicative snapshots; verify live CLOB orderbook depth, bid-ask spread, maker/taker VIP tiers, and slippage before executing live orders.
- **Cross-venue execution & liquidation risk:** Delta-neutral perp arbitrage spans two separate margin accounts. Price basis divergence, asymmetric liquidation thresholds, withdrawal latency, and borrow/margin limits can cause leg imbalance even when net delta is nominally zero.
- **Funding rate non-stationarity:** Predicted funding can flip sign between intervals, especially on thin or event-driven pairs. High APR alone does not guarantee positive net PnL if holding duration is shorter than `breakeven_hours`.
- **Polymarket structural risk:** NegRisk events may exclude an implicit "Other" outcome or have wide spreads across tail outcomes; short-dated high-probability markets carry binary tail risk and UMA oracle dispute/settlement lockup beyond `endDate`.
- **Not financial advice:** This skill provides market analytics and paper-trading tooling only; it does not place live trades.

## Ecosystem & Resources

- **Open-Source CLI Repository:** [quant-radar-cli on GitHub](https://github.com/devbox-zero-ops/quant-radar-cli) — MIT-licensed source, issue tracker, and tests.
- **Free Browser Tool Suite:** [XiaheAI Hub](https://devbox-zero-ops.github.io/xiaheai-hub/) — local browser utilities including DeFi impermanent-loss, APY, and position-sizing calculators.
- **Commercial White-Label Source Kit:** [XiaheAI ZeroSuite Pro](https://devbox-zero-ops.github.io/xiaheai-hub/pro.html) — full multi-tool source bundle for teams extending or self-hosting the toolkit.
