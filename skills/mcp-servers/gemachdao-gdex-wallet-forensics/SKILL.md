---
name: gdex-wallet-forensics
description: Reverse-engineer skill-proven HyperLiquid wallets into size-invariant forensic patterns — skill-vs-luck scorecards, hold-time/sizing asymmetry, and prevalence-gated aggregate edges. Read-only.
---

# GDEX: Wallet Forensics (Reverse-Engineer Winners)

Turn the HyperLiquid month-PnL leaderboard (plus any curated watchlist) into a
distilled, **size-invariant** intel artifact describing *what skill-proven
wallets actually do* — not their raw dollar PnL. The pipeline filters out
uncopyable market-makers, reconstructs each survivor's round trips, scores skill
vs luck, and reports only patterns that generalize across wallets.

**READ-ONLY.** This capability only reads public HyperLiquid data through
existing SDK reads (`getHlTopTradersByPnl`, `getHlTradeHistory`,
`getHlClearinghouseStateAll`). It never trades, settles, or moves funds.

## When to Use

- Building a reverse-engineering feed for a trading agent (what edges to encode)
- Ranking wallets by a skill score that discounts luck and martingale behavior
- Extracting clonable, size-invariant patterns (direction bias, coin focus,
  entry-hour clustering, let-winners-run exit asymmetry)
- Forcing a hand-vetted list of wallets into the analysis via a watchlist

## Prerequisites

- `@gdexsdk/gdex-skill` installed
- Authenticated via `loginWithApiKey()` — see **gdex-authentication**. Shared-key
  login is enough; no wallet or session signature is required (nothing here writes).

## SDK Method

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY, WinnerIntel } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

const intel: WinnerIntel = await skill.reverseEngineerWinners({
  watchlist: ['0xabc...'],  // optional: force hand-vetted wallets into the universe
  max: 12,                  // optional: cap on wallets pulled (default 12)
});

console.log(intel.desk_text);      // pre-rendered <1500-char brief
console.log(intel.scorecards[0]);  // top wallet by skill_score
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `watchlist` | `string[]` | No | Curated `0x` wallet addresses forced into the universe (bypass board pre-filters). |
| `max` | `number` | No | Cap on wallets pulled (watchlist first, then board survivors). Default 12. |

## MCP Tool

```
reverse_engineer_winners
  watchlist?: string[]   // curated wallet addresses to force into the universe
  max?:       number     // pull cap (default 12)
```

Returns the `WinnerIntel` artifact as JSON.

## The Pipeline (thresholds)

1. **Cheap board pre-filter** — drop the `allTime.pnl == -500` sentinel, drop
   turnover (`month.vlm / accountValue > 20`) but SKIP when `vlm <= 0`
   (unpopulated), keep `accountValue` in `[50k, 50M]`.
2. **MM / clonability filter** — drop a wallet if `fills_per_hour > 60` OR
   `median_fill_notional < 1000` OR `maker_fraction > 0.8` OR it has no fills / no
   reconstructable trades. A small directional taker cannot clone a liquidity provider.
3. **Round-trip reconstruction** — flat→flat per coin (via `startPosition`); a
   per-fill `mini_trade` fallback kicks in when the 2000-fill window is truncated
   (those scorecards are marked `UNKNOWN` with a caveat).
4. **Per-wallet scorecard** — `win_rate`, `payoff`, `expectancy`, `kelly_frac`,
   `machine_type` (TREND/MEANREV/MIXED/UNKNOWN), `martingale_ratio`,
   `top5_win_share`, median win/loss holds, `coin_weights`, `luck_flag`,
   `skill_score` (0–100) with a named component breakdown.
5. **Aggregate features** — only reported when held by **>=40% of survivors AND
   >=3 wallets**: direction bias, coin concentration, entry-hour block,
   hold-time asymmetry.
6. **`desk_text`** — a pre-rendered brief (<1500 chars) with a **THIN-FEED**
   banner when fewer than 3 clonable survivors remain (the live board is usually
   MM-dominated, so thin feeds are common — don't over-fit).

## Return Shape (`WinnerIntel`)

```typescript
interface WinnerIntel {
  generated_at: string;                 // ISO 8601 UTC
  universe: {
    board_n: number;
    cheap_survivors_n: number;
    pulled_n: number;
    survivors_n: number;
    filtered_counts: Record<string, number>;  // includes dropped_mm_or_empty
  };
  scorecards: WinnerScorecard[];        // sorted by skill_score descending
  aggregate_features: AggregateFeature[];
  desk_text: string;                    // <1500-char brief
}
```

Each `WinnerScorecard` carries `address`, `n_trades`, `win_rate`, `payoff`,
`expectancy`, `kelly_frac`, `machine_type`, `martingale_ratio`,
`top5_win_share`, `median_hold_win_h`, `median_hold_loss_h`, `coin_weights`,
`luck_flag`, `window_hours`, `method`, `skill_score`, `skill_components`, and
`caveats`. Each `AggregateFeature` carries `id`, `description`, `prevalence`,
`support_wallets`, `magnitude`, `confidence` (HIGH/MED/LOW), and `caveats`.

## Defensive Behavior

- One bad wallet never aborts the run — per-wallet reads are isolated; a failed
  read yields an empty fill list, and empty/uncopyable wallets are simply dropped.
- A missing month board yields a `WinnerIntel` with `survivors_n: 0` and the
  THIN-FEED `desk_text`, not an exception.
