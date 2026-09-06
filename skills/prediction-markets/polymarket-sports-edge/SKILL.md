---
name: polymarket-sports-edge
description: Find odds divergence between sportsbook consensus and Polymarket sports markets, then trade the gap.
metadata:
  author: "jim.sexton"
  version: "1.2.0"
  displayName: "Polymarket Sports Edge"
  difficulty: "intermediate"
---

# Polymarket Sports Edge

> **This is a template.** The default signal compares sportsbook consensus odds
> against Polymarket prices and trades when divergence exceeds a threshold.
> Remix it — adjust the sports, threshold, sizing, or add your own filters
> (e.g., only trade NBA, require minimum volume, weight by recency).

## What It Does

Scans active Polymarket sports markets and compares prices against the
sportsbook consensus from The Odds API. When a market is mispriced relative
to sharp bookmaker lines, it buys the underpriced side.

**The edge:** Sportsbook lines are set by professional oddsmakers with billions
in handle — they're extremely well-calibrated. Polymarket sports markets are
thinner and less efficient. When they disagree, the books are usually right.

## How It Works

Two parallel scanning modes run each cycle:

**Game-level (h2h):** Matches individual Polymarket game markets against sportsbook moneylines.

1. Fetch active sports markets from Simmer (`GET /api/sdk/markets?q=<sport>`)
2. Fetch current h2h odds from The Odds API for the same sports
3. Match markets to games by comparing team names
4. Calculate implied probability from the sportsbook consensus (average across all bookmakers)
5. Compare against the Polymarket price — if divergence exceeds the threshold, trade

**Futures (outrights):** Matches Polymarket championship/winner markets against sportsbook futures odds.

1. Fetch outrights from The Odds API (`_winner` sport keys, e.g., `basketball_nba_championship_winner`)
2. Search Simmer for futures markets (e.g., "NBA championship", "Super Bowl winner")
3. Match market questions to teams in the outrights data
4. Compare sportsbook implied probability vs Polymarket price and trade divergence

## Setup

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SIMMER_API_KEY` | Yes | — | Your Simmer API key |
| `THE_ODDS_API_KEY` | Yes | — | Free key from [the-odds-api.com](https://the-odds-api.com) (500 req/month free) |
| `LIVE` | No | `false` | Set to `true` for real trades. Default is dry-run. |
| `MIN_DIVERGENCE` | No | `0.08` | Minimum spread to enter a trade (8%) |
| `EXIT_SPREAD` | No | `0.02` | Exit when spread closes below this (2%) |
| `TRADE_AMOUNT` | No | `10.0` | Dollars per trade |
| `MAX_RESOLVE_DAYS` | No | `30` | Skip futures markets resolving beyond this (capital lock-up) |
| `MIN_SHARES_TO_SELL` | No | `5.0` | Polymarket minimum sell size |
| `API_TIMEOUT` | No | `30` | HTTP timeout in seconds |
| `SPORTS` | No | 7 sports | Comma-separated game-level Odds API sport keys |
| `FUTURES` | No | 4 leagues | Comma-separated futures sport keys |

### Get a Free Odds API Key

1. Go to [the-odds-api.com](https://the-odds-api.com)
2. Sign up for the free tier (500 requests/month)
3. Copy your API key
4. Set it: `export THE_ODDS_API_KEY=your_key_here`

## First Run Setup

When a user first installs this skill, walk them through these configuration
choices before running:

1. **API keys** — Confirm `SIMMER_API_KEY` and `THE_ODDS_API_KEY` are set.
2. **Divergence threshold** (`MIN_DIVERGENCE`) — Default is 8%. Lower values
   (e.g., 5%) find more trades but with thinner edges. Higher values (e.g., 10%)
   are more selective. Ask the user what level of aggression they prefer.
3. **Exit spread** (`EXIT_SPREAD`) — Default is 2%. This is when the arb is
   considered closed and the position is sold. Tighter values exit sooner.
4. **Trade size** (`TRADE_AMOUNT`) — Default $10 per trade. Ask the user what
   they're comfortable risking per position.
5. **Resolution window** (`MAX_RESOLVE_DAYS`) — Default 90 days. Skip futures
   markets that resolve beyond this horizon. Shorter = less capital lock-up,
   but may miss valid opportunities.
6. **Sports** — By default scans all major US sports plus EPL and MLS. The user
   can narrow to specific leagues if they prefer.
7. **Dry run** — Start with `LIVE=false` (the default) and review a few cycles
   of output before going live.

Explain each setting and its trade-offs so the user can make an informed choice.

## Running

```bash
# Dry run (default) — logs what it would trade
python sports_edge.py

# Live trading
LIVE=true python sports_edge.py
```

## Example Output

```
[Sports Edge] Scanning 7 sports + 4 futures... (dry_run=True, min_divergence=8%)
[Sports Edge] NBA: Found 6 games with odds
[Sports Edge]   Matched: "Will the Celtics win vs Pacers?" → Boston Celtics vs Indiana Pacers
[Sports Edge]     Polymarket YES: 0.58 | Books: 0.69 | Divergence: +0.11
[Sports Edge]   DRY RUN: Would buy YES at 0.58 (edge 11%) — 10.0
[Sports Edge] Futures NBA championship: Found 30 teams in outrights
[Sports Edge]   Matched: "Will the Celtics win the 2026 NBA Champion" → Boston Celtics
[Sports Edge]     Polymarket YES: 0.12 | Books: 0.22 | Divergence: +0.10
[Sports Edge]   DRY RUN: Would buy YES at 0.12 (edge 10%) — 10.0
[Sports Edge] Done. 2 opportunities found (dry run).
```
