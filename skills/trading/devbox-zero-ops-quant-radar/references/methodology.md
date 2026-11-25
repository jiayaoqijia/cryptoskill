# quant-radar Methodology & Math Reference

This reference documents the exact formulas and risk-control state machine implemented in `scripts/radar.py`.

## 1. Funding APR Annualization & Break-Even Math

Perpetual exchanges settle funding on different cadences (commonly `1h` on Hyperliquid `HlPerp` vs. `4h` or `8h` on Binance `BinPerp` and Bybit `BybitPerp`). Comparing raw per-interval rates directly produces false spreads, so `annualize_rate(rate, interval_hours)` normalizes every venue quote to a common 365-day APR:

```text
apr_pct = rate * (24.0 / interval_hours) * 365.0 * 100.0
```

Examples:
- `0.0001` (`0.01%`) per `1h` interval -> `0.0001 * 24 * 365 * 100 = 87.60% APR`
- `0.0004` (`0.04%`) per `4h` interval -> `0.0004 * 6 * 365 * 100 = 87.60% APR`

### Cross-Venue Delta-Neutral Spread

For each liquid symbol (`oi_usd >= min_oi_usd` and `vol_24h_usd >= min_vol_usd`) with at least two predicted venue quotes:

1. Sort venues ascending by `apr_pct`.
2. Assign `long_venue` to the lowest APR venue (least paid / most received by longs) and `short_venue` to the highest APR venue (most received by shorts).
3. Compute annualized gross funding carry:

```text
spread_apr_pct = short_apr_pct - long_apr_pct
```

### Taker-Fee Break-Even Hours

`calc_breakeven_hours(net_apr_pct, rt_fee_bps)` estimates how many hours a spread must persist to recover round-trip entry + exit taker fees across both legs:

```text
hourly_pct      = net_apr_pct / (365.0 * 24.0)
fee_pct         = rt_fee_bps / 100.0
breakeven_hours = fee_pct / hourly_pct
```

Default conservative round-trip taker fee constants:
- Cross-venue perp arbitrage (`DEFAULT_CROSS_VENUE_RT_BPS`): `18.0 bps` (`0.18%`, approximating `0.035%` Hyperliquid + `0.055%` CEX per side across open and close).
- Single-venue cash-and-carry (`DEFAULT_CASH_CARRY_RT_BPS`): `15.0 bps` (`0.15%`, approximating `0.035%` Hyperliquid + `0.040%` spot per side across open and close).

At `spread_apr_pct = 87.6%` and `rt_fee_bps = 18.0`, `hourly_pct = 0.01%/h` and `breakeven_hours = 18.0h`.

## 2. Paper Portfolio Execution & Risk Controls

`update_paper_portfolio(...)` simulates a conservative `1x`-notional delta-neutral portfolio (`max_positions = 3`, equal margin allocation `initial_equity_usd / max_positions`):

- **Fee accounting:** Deducts `rt_fee_bps / 2` on entry and `rt_fee_bps / 2` on exit. Mark-to-market equity (`mark_to_market_equity_usd`) also subtracts estimated exit fees for currently open positions.
- **Elapsed wall-clock accrual:** On each valid tick, funding cashflow accrues strictly over actual UTC hours elapsed since `last_mark_ts`:

```text
accrued_usd = notional_usd * (cur_spread_apr / 100.0) * (elapsed_hours / (365.0 * 24.0))
```

- **Full-universe mark-to-market & missing-quote protection:** Open positions look up current venue rates across `all_cross_venue_by_symbol` and `all_predicted_venues` (not just the top-12 leaderboard). If either leg quote is temporarily missing from the feed, `missing_quote_ticks` increments and the trade is held rather than closed on missing data.

### 4h Rollover Hysteresis (`--confirm-exit-ticks`, default `2`)

At UTC `:00` settlement boundaries (particularly 4h/8h CEX funding rollovers), predicted CEX funding rates briefly reset toward baseline before perp-index premiums rebuild. Naive single-tick exit rules close healthy positions right at rollover and pay unnecessary round-trip taker fees to re-enter minutes later.

- When `cur_spread_apr < exit_apr` (default `8.0%`), `below_exit_ticks` increments by `1`.
- The position closes only once `below_exit_ticks >= confirm_exit_ticks` consecutive valid ticks.
- Any valid tick with `cur_spread_apr >= exit_apr` resets `below_exit_ticks` to `0`.

Engineering write-up: [Why 4h Funding Rollovers Break Cross-Exchange Perp Arbitrage Bots](https://dev.to/devboxzeroops/why-4h-funding-rollovers-break-cross-exchange-perp-arbitrage-bots-and-a-pure-python-fix-4elc).

### Immediate Sign-Inversion Stop-Loss (`--emergency-exit-apr`, default `-25.0`)

Hysteresis should not delay exits when carry flips sharply negative against the held direction (for example, `long_venue` spikes high positive while `short_venue` turns deeply negative).

- Whenever `cur_spread_apr <= emergency_exit_apr`, the ledger **bypasses `--confirm-exit-ticks`** and closes on tick 1 (`close_reason: "emergency sign-inversion stop: ..."`).
- This bounds downside funding bleed during regime reversals while preserving rollover tolerance for shallow dips between `emergency_exit_apr` and `exit_apr`.

### Extreme Spike-Regime Entry Filter (`--max-entry-apr`, default `500.0`)

Extreme headline funding spreads (`> 500% APR`) often arise from transient squeezes, news shocks, or thin books that snap back or invert within a single interval—too fast to clear `breakeven_hours` plus execution slippage.

- During entry selection, candidates with `spread_apr_pct > max_entry_apr` (when `max_entry_apr > 0`) are skipped.
- Setting `--max-entry-apr 0` disables the upper cap; otherwise entries are bounded to `[min_apr, max_entry_apr]`.

## 3. Polymarket NegRisk Overround & Short-Dated Bond Math

`analyze_polymarket_events(...)` inspects active, non-closed events from the Polymarket Gamma API filtered by 24h volume (`--min-vol`, default `$10,000`).

### NegRisk Sum-to-1 Overround / Underround

In a mutually exclusive, collectively exhaustive NegRisk multi-outcome market with $N \ge 2$ active outcomes, one outcome settles to `$1.00` and all others settle to `$0.00`. Summing active `YES` prices yields the book's implied total probability:

```text
yes_sum      = sum(p_yes_i for i in active_outcomes)
raw_edge_pct = (1.0 - yes_sum) * 100.0
```

An event is flagged when `yes_sum < 0.992` or `yes_sum > 1.015`:

- **Underround (`yes_sum < 0.992`, `raw_edge_pct > +0.8%`):** `direction = "BUY_ALL_YES"`. Buying 1 share of every `YES` costs less than `$1.00` for a `$1.00` payout if the outcome set is truly exhaustive and executable at ask prices.
- **Overround (`yes_sum > 1.015`, `raw_edge_pct < -1.5%`):** `direction = "SELL_OVERPRICED_YES"`. Aggregate `YES` prices exceed `$1.00`, indicating positive overround (potential mint-and-sell or selective `NO` basket opportunity, subject to CLOB bid depth and collateral rules).

Operational checks before acting on NegRisk flags:
1. Confirm the event has no unpriced/implicit "Other" outcome that could invalidate the sum-to-1 identity.
2. Verify live CLOB ask/bid sizes rather than relying on mid/last `outcomePrices`.
3. Account for gas, fees, and partial-fill leg risk across $N$ outcomes.

### Short-Dated High-Probability Yield ("Bond") Math

For active binary markets with `volume24hr >= min_vol`, time to expiry `0.5 <= days_left <= 35.0`, and dominant side (`YES` or `NO`) price `0.88 <= top_px <= 0.988`:

```text
gross_return_pct   = ((1.0 - top_px) / top_px) * 100.0
annualized_apr_pct = ((1.0 - top_px) / top_px) * (365.0 / days_left) * 100.0
```

Example: `top_px = 0.95` with `10.0` days to expiry yields `gross_return_pct = 5.26%` and `annualized_apr_pct = 192.11%`. Remember that annualized APR amplifies small-probability tail events and ignores capital lockup during oracle resolution or dispute windows.

## 4. Alert Selection & Cooldown State

`select_alerts(...)` emits structured records with stable deduplication keys:
- `funding:{symbol}:{long_venue}:{short_venue}` when `spread_apr_pct >= min_spread_apr` and `breakeven_hours <= max_breakeven_hours`.
- `negrisk:{url_or_event_prefix}` for all flagged NegRisk deviations.
- `bond:{side}:{question_prefix}` when `annualized_apr_pct >= min_bond_apr`.

`filter_cooldown(...)` suppresses any key sent within `--cooldown-min` (default `60` minutes), persists updated timestamps only on live sends (never during `--dry-run`), and automatically prunes keys older than 7 days.
