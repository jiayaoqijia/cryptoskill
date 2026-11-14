---
name: trading-alerts
description: Price alerts for any market - above or below a price, a trade's stop and target (long or short), a percent move from the previous close, a time on the exchange clock, the opening bell and minutes before the close, plus stop and target alerts for every open trade in the journal in one go. Works out each exchange's session from the data (NYSE, Nasdaq, NSE, BSE, LSE, TSE...) so holidays need no tables; each alert rings once; optional desktop notifications. Use when the user says "alert me when", "tell me if RELIANCE crosses 1400", "watch my stop", "remind me to close by 3:20", "is the market open", "when does NSE open", or right after a trade is planned or opened.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Price Alerts (`trading-alerts`)

Alerts watch the numbers so the user does not have to stare at a chart. **An alert is information,
never an order:** when a stop alert rings, nothing is sold by this skill. Protective orders at the
broker (bracket, stop-loss, GTT from trading-broker) do the stopping; alerts say what happened.

```bash
python3 scripts/alerts.py add --symbol RELIANCE.NS --above 1400
python3 scripts/alerts.py add --symbol AAPL --below 340 --note "under the 50-day"
python3 scripts/alerts.py add --symbol TSLA --stop 358.32 --side long        # rings at or below
python3 scripts/alerts.py add --symbol TSLA --target 370.04 --side long      # rings at or above
python3 scripts/alerts.py add --symbol INFY.NS --pct 3 --direction down
python3 scripts/alerts.py add --symbol NIFTYBEES.NS --open                   # NSE opening bell
python3 scripts/alerts.py add --symbol RELIANCE.NS --close 10                # 10 min before NSE closes
python3 scripts/alerts.py add --symbol AAPL --at 15:50 --label "flat by close"
python3 scripts/alerts.py add --from-journal                                 # every open trade's stop + target
python3 scripts/alerts.py check                    # exit 0 = something rang, 1 = nothing
python3 scripts/alerts.py check --notify           # also a desktop notification
python3 scripts/alerts.py clock RELIANCE.NS AAPL   # open / pre-open / closed, session times
python3 scripts/alerts.py list | remove ID | reset [ID]
```

Options on `add`: `--date YYYY-MM-DD` (watch that day only), `--rearm` (ring again after the price
goes back across), `--note`.

## How it works

- `check` fetches only the symbols in the rules (free, delayed Yahoo quotes; or the configured
  provider, e.g. a broker feed for live prices) and rings each rule once. Time, open and close alerts ring
  once per trading day, only on days the exchange has a session.
- Times are the **exchange's local time** (NSE 09:15-15:30 IST, NYSE 09:30-16:00 ET...), worked out
  from the data, never from the computer's time zone.
- Rules: `~/.trading-skills/alerts.json`; what rang: `state/alerts.json`.

## Steps

1. Right after trading-plan / trading-broker opens a trade, offer `add --from-journal` and a
   close-of-day alert for intraday trades. Confirm every new rule back: symbol, type, level, day.
2. While trades are open, run `check` every few minutes: `/loop 5m` or a scheduled task. Quotes are
   delayed and a price can pass a level between two checks: say so when it matters.
3. When a stop or target rings, check the position at the broker (trading-broker `positions`) and
   record the fill in trading-journal. When a close alert rings for an intraday trade, close it the
   normal way: trading-risk check -> trading-broker preview -> the user's explicit confirm. Never act
   for the user.
