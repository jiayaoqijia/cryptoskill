# Entry screen on liquid CEX pairs — "kurang ya, jadi masuk mana sekarang?"

Companion to `prospective-entry-vetting.md`. That one is for meme/low-cap on-chain asks (GMGN holder
cohorts, dev score, entrapment). **This one is for the liquid-universe question**: the user just heard
a token falls short of the bar ("TNSR 6/10") and asks *"berarti kurang ya, brrti skrng bagusnya masuk
mana, ILV kah?"* — i.e. pick the best current entry out of a real candidate list.

Worked end-to-end 2 Okt 2026: TNSR 6/10 → ILV (previous pick, already stale) vs NFT/metaverse basket vs
HBAR vs XRP. Result: **HBAR** chosen, ILV/ALICE/GRAM rejected.

## Step 0 — build the universe from live mcap, not the script's built-in list

`entry_screen.py` ships a curated ~60-symbol list. Fine for "kurang ya, masuk mana sekarang". Wrong when the
ask is *"analisa dari top 100"* or a from-scratch book: a curated list makes the answer an artifact of
whatever someone typed in earlier, and the user will read it as bias.

- `api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h,7d,30d`
  returns rank, mcap, aggregate volume, circulating/total, and the 7d/30d changes in one keyless call.
- Intersect with Binance: keep a symbol only if `<SYM>USDT` is in `exchangeInfo?permissions=SPOT` with
  `status == "TRADING"`. Drop stables and wrapped/LSTs by symbol name (USDT, USDC, USDE, USDS, WBTC, WETH,
  STETH, RETH, ...) — a $1,00 token otherwise passes every gate and tops the table.
- Expect ~55–60 survivors out of 100. That intersection **is** the investable universe for a ~$1k book.

**The single-venue gap**: a top-15 name with no Binance pair disappears from the screen entirely. HYPE is the
standing example — strongest trend in the top 100, zero rows in the output, because it trades on Hyperliquid.
Pull it from its own venue, keyless:
`POST https://api.hyperliquid.xyz/info` body `{"type":"candleSnapshot","req":{"coin":"HYPE","interval":"1d","startTime":<ms>}}`
(fields `o/h/l/c/v`). Its `v` is that venue's own notional and runs far below the aggregate figure — use
CoinGecko for the liquidity gate and the venue candles only for technicals. Do not just drop the name:
missing the strongest large-cap trend makes the whole screen look ignorant.

**When `--screen` returns `total lolos: 0 dari N`, that IS the finding** — and the script prints only PASS
rows, so the zero tells the user nothing and reads as "you didn't really look". Recompute the four gates
yourself across the same universe and print every name with a gate string (`YYYY`, `YYYn`, `nYnn`, ...), sorted
by gates passed, then quote the counts: "0 dari 58 lolos 4/4, 20 nama lolos 3/4, dan hampir semuanya gagal di
gate volume". A tape where nothing clears the gates produces a BTC + cash book; the table is what earns that
answer.

## Step 1 — mechanical screen (first pass ONLY)

`scripts/entry_screen.py --screen` (Binance spot klines 1d `limit=700` + `ticker/24hr`, stdlib only).
Per symbol compute: price, 7d/30d %, `pos90 = (cur-low90)/(high90-low90)`, MA30, EMA21/50/200 (seed the
EMA from the full 700-bar series or EMA200 is wrong), vol7avg/vol30avg, quoteVolume 24h, upside to
high90, downside to MA30, `RR = upside/downside`.

Keep-the-candidate filter: `cur > EMA200` (uptrend), `pos90 < 82` (not extended), `quoteVolume > $8jt`
(can actually be sized), `vol7/30 > 1.05` (volume arriving). ~7 of 46 liquid pairs passed.

`pos90` and "% of the 30d range" are different questions and can disagree sharply in the same tape (BTC: 80%
of its 90d range but 24% of its 30d range — it fell, then chopped near the bottom of the new range). Always
name the window you are quoting. A note that says "pos 24%" beside a screen that said "pos90 80" reads as two
contradictory numbers, and this user checks.

## Step 2 — structure verification (MANDATORY, kills most first-pass “winners”)

The mechanical RR alone produced **three false positives in one session** — never publish one without this:

| symbol | mechanical RR | what printing the high90 DATE revealed |
|---|---|---|
| ALICE | 1,99 | high90 0,2467 = **1 Okt**, vol $17,9jt (12× avg) → **rejected next day**, close −15% from high = distribution |
| GRAM | 2,15 | high90 1,81 = **5 Jul** (stale, about to roll out of the window); 26–28 Sep spike to 1,74 failed; latest-day volume $4,7jt = dead |
| ILV | 0,29 | high90 4,40 = **13 Sep** → today was a **retest**, not a new-high breakout, and 7d volume was 0,76× 30d (no confirmation) |

Rules that follow:

1. **Always print the date of high90/low90**, never the value alone. Upside-to-high90 is meaningless if
   the high is (a) months old / about to roll out of the 90d window, or (b) yesterday's blowoff.
2. **Breakout vs retest/reclaim.** New close above a *prior* high with volume = breakout. Price testing
   an older high from below = retest/reclaim. Do not call a retest a breakout — this user checks.
3. **Check whether the spike was rejected.** Blowoff day at N× volume followed by a close −10…−15% off
   the high = distribution, not consolidation.
4. **Volume trend after a spike**: falling volume while price holds **above the spike low** = post-spike
   flag (constructive). Falling volume while price drifts back **into** the spike body = failing.
5. **Absolute liquidity in USD.** A “hot” name doing $1–2jt/day cannot be sized at any R:R; the laggards
   of a hot basket usually lag because their flow is thin — that is not an edge, it is the reason.
6. **Chasing test**: if distance to high90 is small (+4%) while the honest stop is far (−15%), RR < 0.5 →
   the answer is "not now", however good the story is.

## Step 3 — the valid pattern (worked: HBAR)

- **Spike day 28 Sep**: close +27,2%, high 0,1310, low 0,0941, volume **$200jt ≈ 9× the 30d average**
  ($22,5jt) → real volume, RSI 81 (overbought, flagged as such).
- **4 days after**: volume decaying 87,9 → 47,1 → 30,3 → 10,7jt while price **held above the spike low**
  and stayed **+21,7% above EMA200** → post-spike flag, pos90 63,7% (not extended).
- **Shelf = the old high it must reclaim** (0,10977 = 30 May high); price sat 2,8% below it → that is the
  confirmation level.
- **Plan**: entry retest 0,103–0,107 · stop close <0,0975 (−8,7%) · T1 0,1229 (+15%) · T2 0,1310 (+23%) ·
  RR ≈ 2:1 · safe confirmation = daily close > 0,10977 · sizing small (5% modal, 2 tranches).
- Contrast **XRP**: liquid ($233jt/day) but price mid-range (1,48–1,70 for 6 weeks, pos90 78,6%) → correct
  answer is "entry only < 1,50", i.e. name the price at which it becomes a buy.

## Step 4 — catalyst dating, including what to throw away

- Every catalyst needs **a date + one named source**. HBAR: IDTrust (Hashgraph Group) listed in the
  **IBM Cloud Catalog, 23 Sep 2026** — company release on GlobeNewswire, covered by Phemex blog and
  cryptoticker.
- **State the catalyst's strength honestly.** That one is *soft*: the 28 Sep spike started 08:00 UTC,
  **before** NVIDIA's agent-safety release hit the wires, so the move was mostly technical + RWA-narrative
  rather than a single news event. Saying "soft" is part of the report, not a hedge.
- **Discard unconfirmed derivations.** The "BlackRock ICS US Treasury MMF tokenized on Hedera via
  Securitize" story was *reportedly* — never confirmed — so it was explicitly excluded from scoring.
- Catalysts older than ~45 days are stale: note the start date and cut the score.

## Step 5 — hot-meta basket check (why the answer is often "skip", not "rotate")

When the user points at a hot meta (NFT/metaverse/GameFi), print **pos90 for every member** before
recommending a laggard: SAND 91% · AXS 93,5% · AAVE 95,9% · GALA 99,7% · ILV 88,8% · IMX 88,9%. When
most of the basket sits at 85–100% of its 90d range, the rotation is **late** and the honest answer is
**skip the basket**; "rotate into the laggard" is not an edge when the laggard's flow is $1jt/day.

## Reply shape that lands

Verdict in line one (`<X>? bukan` / `yang paling waras: Y`) → why the old candidate is dead, with numbers
→ the basket's pos90 table (why the whole meta is late) → new candidate with dated catalyst + levels
(entry/stop/T1/T2) + RR + small tranche sizing → one liquid alternative and the price at which it becomes
a buy → closing line `nggak ada yang lolos 8/10 hari ini` when that is true (this user wants honesty over
a forced pick). Attach **one** chart PNG (levels + EMA200 + entry band, from `make_setup_chart.py`), and
save the full write-up as a dated Obsidian note.
