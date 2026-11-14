# Workflows

Paths are relative to the `skills/` folder. Each step names the skill and the command.

## 1. First-time setup (5 minutes, no API keys)

1. trading-setup: `setup.py init --equity 100000 --currency USD --benchmark SPY --risk-pct 1`
2. trading-setup: `setup.py doctor`
3. trading-start: `brief.py --watchlist assets/watchlists/us-mega-caps.txt`

## 2. Idea -> trade (swing)

1. trading-market: is the tide in? (`regime.py`)
2. trading-scanner or trading-patterns: find candidates
3. trading-chart: confirm trend, volume, levels, weekly agreement
4. trading-plan: entry / stop / target / size (`--regime-adjust --save`)
5. trading-odds `setup`: odds of target before stop (optional, recommended)
6. trading-risk `check`: must PASS
7. trading-broker `preview` -> user confirms -> `submit --confirm CODE`
8. trading-journal `note`: thesis and grade

## 2b. Intraday day trade (any exchange)

1. Before the open: `trading-market` (exposure), `trading-scanner` / `trading-patterns` for candidates,
   `trading-news` and `trading-earnings` on each (results inside the trade = skip or size down).
2. After the open: `trading-entry watchlist` or `watch SYMBOL` - wait for a CLOSED bar beyond the
   opening range (NSE 09:15-09:30, NYSE 09:30-09:45 by default).
3. On a trigger: `trading-plan` with the printed entry and a stop from the range, `trading-odds setup`
   for a reality check, `trading-risk check`, `trading-broker preview` -> the user's confirm (use your
   broker's intraday product, e.g. MIS).
4. `trading-alerts add --from-journal` plus `--close 10` so the position is closed before the bell.
5. After the close: `trading-journal` close the trade, weekly `trading-review`.

## 3. Strategy research

1. Write rules (trading-scanner `--check`)
2. trading-backtest with `--oos-start` and `--report`, 10+ years, several symbols
3. Vary parameters with `--set`; reject fragile results
4. trading-odds `trades --csv` on the backtest trades for drawdown ranges
5. Paper-trade it (trading-broker, paper broker) for weeks before going live
6. trading-review `--setup NAME` to compare live/paper to the backtest

## 4. Daily routine

- **Pre-market:** `brief.py --watchlist list.txt --report brief.html`
- **During the session:** plan -> gate -> preview/confirm for each trade
- **End of day:** trading-broker `process` (paper), trading-journal `close` / `note`, `gate.py status`
- **Weekly:** trading-review `--period week --report week.html`

## 5. Automation (what to schedule, what never to)

Safe to schedule (read-only or paper):
- `brief.py` pre-market and after the close, emailed or posted
- `router.py process` after the close (paper fills, journal sync)
- `review.py --period week` every weekend
- screener / pattern scans on a watchlist, saving hits to a file
- `news.py --watchlist FILE` every 15-60 minutes (only new items are shown)
- `alerts.py check --notify` every 5 minutes while trades are open
- `insiders.py congress --new --read` hourly on weekdays; `insiders.py deals` after the Indian close
- `entry.py watch SYMBOL` in the background during the session (it reports; it never orders)

Scheduling options: the agent's own scheduled tasks, or system cron, e.g.
`35 21 * * 1-5 cd ~/trading-skills/skills/trading-start && python3 scripts/brief.py --watchlist ~/watchlist.txt --report ~/brief.html`

Never fully automate live order submission with these skills. The confirm step is a deliberate
human check. Fully automated live trading generally needs your own broker app with the controls
your broker and regulator require (registered static IP, algo identifiers, kill switches, audit).

## 6. Risk-off day

`gate.py status` shows the daily loss or streak limit hit -> stop opening trades.
Optionally `router.py kill on --reason "daily limit"`. Review tomorrow, not today.
