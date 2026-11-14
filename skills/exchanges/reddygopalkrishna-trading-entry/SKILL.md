---
name: trading-entry
description: Entry timer for intraday setups in any market - watches bar by bar and says the moment a setup triggers, waiting (and how far), still forming, expired or market closed. Opening-range breakout (first 15 minutes by default) or a break of any level you give, long or short, on 1, 2, 5 or 15-minute bars, with an optional volume check and a no-entries-near-the-close cutoff. Reads each exchange's session from the data (NSE 09:15, NYSE 09:30, LSE 08:00...), replays past sessions for practice, and hands the trigger to trading-plan with stop ideas. Never places an order. Use when the user says "tell me when to get in", "watch RELIANCE", "has it broken out", "did it break the opening range", "time my entry", "ORB", "check my watchlist for breakouts", or after a scan finds a setup.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Entry Timer (`trading-entry`)

The entry timer turns a setup into one moment: the bar that confirms it. **Only closed bars count.**
A price that pokes through a level mid-bar is not an entry; a bar that CLOSES beyond it is. Then it
says the time and price, suggests stops, and stops. It never buys anything.

```bash
python3 scripts/entry.py check RELIANCE.NS                    # 15-min opening range, 5-min bars
python3 scripts/entry.py check AAPL --side short              # close below the range low
python3 scripts/entry.py check NVDA --setup level --level 151.20 --min-volume-x 1.5
python3 scripts/entry.py check TCS.NS --interval 1m --or-minutes 30
python3 scripts/entry.py watch INFY.NS --until 14:30          # one line per closed bar, exits on the trigger
python3 scripts/entry.py watchlist --watchlist ~/my_list.txt  # every symbol once, triggered first
python3 scripts/entry.py check AAPL --offline saved/ --now "2026-11-13 10:15"   # replay a past session
```

Exit code 0 = triggered, 1 = not (waiting, forming, expired, closed). A trigger is saved to
`~/.trading-skills/state/entry.json`.

## The rule

- **Opening range (`orb`):** high and low of the first `--or-minutes` (15) of the session. Long
  trigger: first closed bar after the range whose close is ABOVE the high. Short: close BELOW the low.
- **Level (`level`):** the same against `--level PRICE` (a 20-day high, a pattern pivot from
  trading-patterns), checked after the first `--or-minutes`.
- **Exactly at the level is not beyond it.** One trigger per setup per day: the first.
- **Volume (`--min-volume-x 1.5`):** the trigger bar's volume must be 1.5x the range bars' average.
- **Cutoff:** no new entries in the last 30 minutes (`risk.no_entries_last_minutes`, or
  `--last-minutes`); after that the setup is expired.
- A trigger more than a bar old is flagged: a late entry is a different trade - re-plan from the
  price now.

Session times come from the data, so holidays and half days are handled; with CSV data the session
is inferred from the first bar. Free Yahoo intraday data is delayed (typically 15 minutes for NSE,
less for US): with a broker data feed set as the provider, prices are live.

## Steps

1. Get the symbol (or run `watchlist` after trading-scanner / trading-patterns). Check trading-news
   for it first.
2. `check SYMBOL`. Tell the user the status in one line.
3. To wait for it: run `watch SYMBOL --until HH:MM` in the background, or `check` on a `/loop 5m`.
   Keep the computer awake while it watches.
4. On a trigger: say the time and price and that **nothing was placed**. Then trading-plan with the
   printed command (entry, a stop from the range, target), then trading-risk, then trading-broker
   preview and the user's explicit confirm.
5. Never call an entry early because a bar looks like it will close beyond the level, and never run
   trading-broker from a background watch: nobody is there to confirm.

Practice first: replay past sessions with `--offline` / `--now`, and paper-trade the setup before
using real money. A clean signal is information, not a promise.
