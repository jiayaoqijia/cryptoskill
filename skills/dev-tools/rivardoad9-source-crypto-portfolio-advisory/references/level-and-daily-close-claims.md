# Level claims and "daily close" claims — verify against the exchange, not the sentence

Companion to `user-chart-claim-verification.md`. Worked case 8 Okt 2026, 05:0x WIB:
*"daily ondo lom close di 0.64"* → corrected one message later: *"0.46 mksdny"*.
Short, numeric-only messages like this are his normal register: a level plus a state
(closed / not closed / holding). The job is to verify the interaction against live data.

## 1. Sanity-check the level against the live range BEFORE analysing it

Check the quoted number against the last 1-2 weeks of klines. If it sits far outside that
range it is usually a digit slip (0.46 ↔ 0.64), a stale memory, or an OHLC column read as
close. In the worked case live was **0,4665** and the quoted level 0,64 = +37% away — the
first answer was built on the wrong level and had to be walked back after he self-corrected.
Cheap ordering that avoids it: pull live price + range → if |level − price| is > ~10% while
the recent range never touched it, ask or flag it in one line *before* computing anything.

## 2. "Belum close di <level>" is a two-candle check, and the boundary is 00:00 UTC = 07:00 WIB

Binance daily candles open at 00:00 UTC, i.e. **07:00 WIB**. At 05:06 WIB the running candle
had opened 07:00 WIB the previous day and closes at 07:00 WIB that morning. So:

- **last CLOSED candle** (opened previous 07:00 WIB) → the close that actually counts;
- **running candle** → open/high/low/current only. A wick below the level is **not** a close
  below it, and saying otherwise is the mistake to avoid.

Worked numbers: last closed 0,4914 · running candle O 0,4914 H 0,4934 L 0,4568 C 0,4665
(current) → *"belum close di 0,46"* TRUE, close lands 07:00 WIB (~1,9 jam lagi).

```python
k = get("https://api.binance.com/api/v3/klines?symbol=ONDOUSDT&interval=1d&limit=8")
# each row: [open_time, O, H, L, C, ...] — the LAST row is the running candle
t = get("https://api.binance.com/api/v3/ticker/24hr?symbol=ONDOUSDT")   # lastPrice, %24h, lowPrice/highPrice
close_at = now.replace(hour=7, minute=0, second=0)                      # next 07:00 WIB close
if close_at < now: close_at += timedelta(days=1)
```

## 3. Report shape that landed

Level distance in % (+1,41% above 0,46) · 24h range (0,4568–0,4945) · last closed daily close ·
the hour of the next close · **what that close would confirm or deny** (close < 0,4568 = first
daily breakdown; add context: the prior week's daily lows sat at 0,4832–0,4845, so today's low
is the lowest in a week). End with one line of thesis context for a name already flagged in the
vault (ONDO: founder succession dispute, Jan-2027 unlock) → *"kalau beneran breakdown, itu bukan
diskon"*. A bare price quote is not an answer to a level question; the interaction is.

## Pitfall

Do not restate the user's own level back to him as if it were data. Confirm the level with the
live range, then speak about the *candle* (closed vs running) and the *distance in %*. And keep
WIB throughout — his candles are read on WIB mornings, so a UTC-stamped "yesterday" is wrong
for him by 7 hours.
