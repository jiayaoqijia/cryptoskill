# News-DB first-stop + unlock verification (worked 8 Okt 2026, ONDO)

Companion to `single-token-move-attribution.md` (the 6-step procedure) and
`catalyst-and-flow-verification.md` (catalyst hygiene rules). This file adds two things those two
don't cover: **where the catalyst actually lives before you go to the web**, and **how to verify a
token-unlock date** — the class of claim that got published wrong on 8 Okt 2026.

Trigger: "kenapa <token> naik/nge-pump?", "kok bisa naik padahal pasar merah?", any single-token move
attribution, and any time an unlock/vesting date is about to be used as a reason to buy or sell.

## 1. Query the local news DBs BEFORE web_search

Collectors are already running on this machine and their tables are queried instantly, offline, with
exact timestamps. Two of them matter:

```python
# media besar + akun X trader (cointelegraph, crypto_banter)
sqlite3 ~/.hermes/data/news_feeds.db \
  "select published_utc, source, title from items where title like '%ONDO%' order by published_utc desc"

# per-koin: news.google site:x.com/<handle> + situs/blog RESMI + media material
sqlite3 ~/.hermes/data/crypto_impact.db \
  "select pub_utc, sym, source, title from token_news where sym like '%ONDO%' order by pub_utc desc"
```

Schema:

| table | columns |
|---|---|
| `news_feeds.db::items` | `id, guid, source, title, link, categories, published_utc, summary, fetched_at` |
| `crypto_impact.db::token_news` | `link, sym, pub_utc, title, source, kind, level, first_seen` |

`published_utc` / `pub_utc` are ISO-8601 with offset for `items`; `fetched_at` tells you when the
collector saw it (useful to spot an item the collector is late on). Other DBs on the box, for other
questions: `liq.db` (Binance futures liquidations >$50k), `whale_alert.db` (on-chain whale flow),
`lowcap_alert.db`, `sm_watch.db` (smart-money watch), `crypto_impact.db` also holds the news-impact
radar.

### The negative finding is the valuable part

15 ONDO items existed in `token_news` and **every single one was 21 Sep – 6 Okt** (BlackRock
model-portfolios 24 Sep, KakaoPay 29 Sep, Private Markets launch 6 Okt). **Nothing from 8 Okt.**

That is not "no data" — it is a result: **the move was not driven by the token's own news flow**, so
the cause must be (a) fresh news the collector hasn't ingested yet, (b) the theme, or (c)
mechanics/positioning. Combined with the sector test (theme peers CFG +2,91%, PENDLE +0,76%, POLYX
0,00%, MKR +0,76% — all flat while ONDO ran +6,42% against BTC −0,63%), the shape is
**one token moved by one new item of information**.

Without the `published_utc` filter, all 15 "relevant-looking" headlines lead straight to a wrong
answer. This is the fresh variant of the Rule-1 staleness trap in
`catalyst-and-flow-verification.md`.

### Where the real catalyst was

Not in the DB — on the web: **the unnamed pre-IPO company behind Ondo Private Markets was revealed as
OpenAI**, and the note began trading 24/7 on the Ondo Perps order book (ChainCatcher, TokenPost,
The Block). Announced 6 Okt *without a name* → named 8 Okt = genuinely new information, which is what
qualifies it as a cause.

**Timeline check that seals it:** the article timestamp ≈ 20:35 WIB lines up with the 20:00 WIB
1-hour candle being the day's volume peak (2,89M USDT, ~4× the prior hours) and the jump
0,4914 → 0,4975. If the timestamp does not land on the volume candle, do not force the fit — that is
the signal it is not the cause.

**Foreign outlet clocks are not WIB.** Chinese outlets (ChainCatcher) stamp in CST (UTC+8) = **WIB − 1
hour**; US outlets UTC−4/−5. Shift the timezone before concluding a piece of news "came too late/early"
to be the trigger.

## 2. Sharpe the derivatives read (which endpoints actually answer "why")

`single-token-move-attribution.md` step 3 covers `openInterest` / `premiumIndex` / `fundingRate`.
These are sharper, because they give deltas rather than point-in-time values:

```python
get("https://fapi.binance.com/futures/data/openInterestHist?symbol=ONDOUSDT&period=1h&limit=25")
# -> sumOpenInterest + sumOpenInterestValue PER HOUR: 24h delta AND last-hour delta in one call
get("https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol=ONDOUSDT&period=1h&limit=6")
get("https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol=ONDOUSDT&period=1h&limit=6")
```

**The last-hour OI delta is the "new money arriving right now" signal** — the most relevant number when
the user asks mid-move. ONDO 8 Okt: OI $64,4M → $71,6M (+5,2% / 24h) *and* +$4,2M in the final hour
alone; funding only **+0,005%/8h**; top-trader long/short 3,15. Conclusion: **not a short squeeze —
fresh longs entering cheap.** Retail account ratio 1,75–1,81 vs top traders 3,06–3,19 = retail
hesitant, large positions long. Funding extreme (>0,1%/8h) or an OI blow-off is the opposite reading
(leveraged, longs already paying up) and must be flagged as risk.

## 3. Unlock / vesting dates — NEVER quote from memory

**The failure, 8 Okt 2026:** a stated reason for exiting ONDO was "unlock 24 Okt". Verified afterwards:
**wrong**. ONDO unlocks are **annual, every 18 Jan** (TGE 18 Jan 2024, vesting to Jan 2029). The next
one is **18 Jan 2027** — 1,71B tokens, 17,1% of supply, **35,1% of market cap**, 113 days out. The
monthly releases are **0,12%** = noise. Historical impact: average **−6,8% over 8 days** post-unlock,
and the 18 Jan 2026 unlock produced **−30,2% in 14 days** — which is exactly why a wrong date is
expensive: "unlock soon" sounds credible and nobody re-checks it.

Where to actually look:

| Source | What it gives | Note |
|---|---|---|
| `app.tokenomics.com/tokenomics/<token>/unlocks` | per-event table: date, token count, % of supply, **% of MCAP**, countdown, recipient split, **historical price impact of each unlock** | most complete and it extracts cleanly — use this |
| `defillama.com/unlocks/<protocol>` | summary only | JS-rendered; `web_extract` yields little more than "Unlocked 48.70%" — not enough for a date |
| `docs.<token>.foundation` | TGE, distribution policy, DAO proposals | good for confirming policy/mechanism |

Rules:

1. **An unlock date is a claim with the same sourcing bar as a catalyst** — date + named source, or it
   does not ship. `catalyst-and-flow-verification.md` Rule 1 applies verbatim.
2. Distinguish **cliff** (annual, large) from **monthly drip** (often <1%) — quoting the drip as the
   overhang is the mirror error of quoting a cliff that is years away.
3. Quote **% of market cap**, not just % of supply: the tradable worry is sell pressure relative to
   float value.
4. **If a date you already gave turns out wrong, correct it unprompted in the next reply** — name the
   wrong claim, the right one, and the source ("gw pernah bilang unlock 24 Okt, itu salah, yang bener
   18 Jan 2027, sumber tokenomics.com"). Then **re-state the reasons that still hold**, because
   retracting one leg of an argument can change the whole conclusion — and the user needs to see which
   part survives.

## 4. Mechanical detail: "daily close" has a timezone

Binance daily klines close at **00:00 UTC = 07:00 WIB**. Before 07:00 WIB, `klines[-1]` is the
**still-open** day and `klines[-2]` is the last legitimate completed close. Reading `k[-1]` as "today's
close" before 07:00 WIB produces a false "the level broke" call. This matters twice: when reporting a
daily-close level, and when scripting a watcher (`~/.hermes/scripts/ondo_wall_alert.py` reads `k[-2]`).

## 5. Public-page snapshots can be stale and self-contradicting

During the ONDO incident a CoinGecko snippet claimed "24h −1,20%, range $0,4928–$0,5256" — flatly
contradicting the Binance live tape (+6,42%, range $0,4583–$0,4976) **and** Binance's own daily close
series for that week. **Venue API is the source of truth for price; aggregator pages/snippets are
supporting material only.** Never mix two snapshots taken at different times into one table, and never
let a cached snippet override the venue.

## 6. Report shape lessons from this incident

- **Name the cause in the first sentence** when it is found. The user asked a two-word question
  ("ondo pump"); they wanted the catalyst's name, not the procedure.
- **Say the opportunity cost with a number** when the user just exited that token: ONDO +5,7% from
  their fill 0,4707 = **$15,4 on 575,2 units = 1,2% of equity** — and say that it is small.
- **State the weakness of the catalyst itself.** The Ondo note is not OpenAI equity, carries no
  shareholder rights, is non-US-only, and Ondo has no OpenAI affiliation → the price rose on a
  **narrative**, not on cash flow to the token. Good stories leave as easily as they arrive.
- **Turn "I'll watch it" into an actual silent watcher.** Do not close with a promise; install a
  `no_agent` cron whose stdout is empty unless the falsification level is breached (pattern: job
  "ONDO tembok 0,50", 07:05 WIB, reads `k[-2]`, message style per `cron-output-style`). Give the level
  a number that can be checked (ONDO: daily close > 0,5000; the wall was six daily closes between
  0,4914 and 0,5016 on 1–6 Okt). A 9-hour wiggle is not a decision unit; a daily close is.
