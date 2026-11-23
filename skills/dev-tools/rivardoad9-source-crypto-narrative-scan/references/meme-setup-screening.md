# Meme setup screening (when the ask is "meme apa yang punya setup / lagi diperbincangkan")

Companion to `crypto-narrative-scan` steps 1–2. The narrative steps answer *where the money is*.
This file answers the follow-up the user actually asks: **"cariin meme lagi yang potential setup"**.

Honest default: after a meme pump cycle the whole complex cools together. Most sessions the correct
answer is **"nothing here qualifies as a setup — say so"**, not a forced shortlist. The user rewards
that (he already pushed back once on being handed sells on thin-liquidity names without fresh data).

## 1. Quality gate (drop the noise before charting anything)

From `market trending` rows, keep only:

| field | threshold | why |
|---|---|---|
| `market_cap` | ≥ $1,000,000 | below this it is a mint, not a market |
| `liquidity` | ≥ $150,000 | you cannot exit a $50k pool |
| `rug_ratio` | < 0.25 | GMGN's rug heuristic |
| `is_wash_trading` | must be false | |
| `creator_token_status` | prefer `creator_close`; `creator_hold` = dev still holding supply | |

Then classify movers **before** ranking: `+300% 7d` **and** `−40%+ from 7d high` = post-blowoff
retrace, not a setup. `+1000%+` on the day (CAPYBARA +12,922%, BORDR +27,444%) = lottery row: name
it explicitly as excluded (SKILL.md pitfall 3) but never chart it as a candidate.

### Manufactured-volume check (turnover × bundler)
`turnover = volume / market_cap`. Normal memes: 0.1–3x. Combined with a high `bundler_rate`
(same-size bundle bots), extreme turnover = volume that was made, not traded.

Worked red flag — pPOLY (BSC, 8 Okt 2026): mc $5.5M, volume $88.8M → **turnover 16.1x**,
`bundler_rate` **0.41**, `is_wash_trading` false (so GMGN's own flag did not catch it). Excluded.
Do not use turnover alone: stock-pair tokens run 0.0–0.3x simply because their pools are huge.

## 2. Attention sweep — what is being discussed

```bash
gmgn-cli market hot-searches --chain sol --chain bsc --chain base --chain eth \
  --interval 24h --limit 100 --raw > /tmp/meme_scan/hs24.json
```

Top level is a **list of per-chain blocks** `[{interval, chain, version, tokens:[…]}]` — there is no
`.data` wrapper. Repeating tickers across chains (ZEC on sol $123M + bsc $270M) = a real cross-chain
theme; a ticker appearing at many different market caps = symbol spam, keep the address.

## 3. Signal feed parse shape (`market signal`)

```bash
gmgn-cli market signal --chain sol --groups '[{"signal_type":[12]},{"signal_type":[20]}]' --raw
```

Returns a **flat top-level list** (50 items per group). Per item:
`token_address`, `signal_type` (**12 = smart money, 20 = KOL**), `ath`, `market_cap`, `trigger_mc`,
`first_trigger_mc`, `trigger_at`, `signal_times`, `signal_times_by_type`, and a nested
`data{chain, address, symbol, launchpad}` (ticker lives there — `cur_data` is not always populated).

Aggregate in Python, never by eye:

```python
from collections import defaultdict
agg = defaultdict(lambda: {"n": 0, "types": defaultdict(int), "sym": "?", "mc": 0, "ath": 0, "last": 0})
for it in items:
    s = agg[it["token_address"]]; s["n"] += 1
    s["types"][{12: "SMART", 20: "KOL"}.get(it["signal_type"], it["signal_type"])] += 1
    d = it.get("data") or {}; s["sym"] = d.get("symbol") or s["sym"]
    s["mc"] = it.get("market_cap") or s["mc"]; s["ath"] = max(s["ath"], it.get("ath") or 0)
    s["last"] = max(s["last"], it.get("trigger_at") or 0)
```

Interpretation: a feed where the top row has n=3 and everything else n=1, at MCs of $2k–$700k, is
**micro-cap churn — no dominant accumulator**. Report that as the finding.

## 4. Structure pull (the actual "setup" test)

Two batched passes, one script, `sleep 4` between GMGN calls (rate-limit pitfall 7).

Pass 1 — `--resolution 1d --from <now-32d> --to <now>` for ~12 candidates → r1/r3/r7, % from 7d
high, % from 7d low, position in 7d range.
Pass 2 — `--resolution 4h --from <now-9d>` for the 3–5 survivors → EMA20/50 4H and the last 6 closes.

**Volume must be measured on the last COMPLETE candle, not the in-progress one.** See pitfall 10.
```python
va = statistics.mean(v[-9:-2])      # the 7 days before the last full day
vr = v[-2] / va                     # last full day vs that mean  → NOT v[-1]
```
For a Binance-listed benchmark (e.g. BOME) pull the same metrics from
`https://api.binance.com/api/v3/klines?symbol=X&interval=1d&limit=31` (keyless).

### Classification

| shape | test | call it |
|---|---|---|
| candidate | price **above** EMA20/50 4H, mid-range, volume expanding | genuine setup — give levels |
| cooldown | above EMA50 4H but volume contracting, −20…−40% from hi7 | wait for confirmation |
| falling knife | at/below the **low** of the 7d range, below all EMA 4H, 3+ consecutive lower 4H closes | **not a discount** — say so explicitly |
| post-blowoff | r7 ≫ +100% but −40%+ from hi7 | late, not a setup |
| dead | −50%+ r7, position < 5% of range | ignore |

Levels to hand over for a candidate: entry-valid (EMA20 4H), stop (below the 3d swing low),
target 1 (3d high), target 2 (9d high) — plus size discipline (meme ≤ 5–8% of portfolio per coin).

## 5. Worked example — 8 Okt 2026, ~17:00 WIB

Ask: "meme coin yang paling perform BOME, cariin meme lagi potential setup atau yang lagi
diperbincangkan."

Screen of 13 Solana memes: **only 2 sat above EMA50 4H** (BOME on Binance, baton). No clean
accumulation setup existed anywhere — the whole complex was in cooldown after the early-Oct pop
(last full-day volume 0.22–1.08x the prior week's mean).

| token | mc | r7 | from hi7 | pos in range | vs EMA50 4H | verdict |
|---|---|---|---|---|---|---|
| BOME (Binance) | — | **+12.1%** | −14.0% | ~59% | **above** (+6.3%) | genuine breakout — 10d range 0.00093–0.00105 broken, vol 4H 159M→893M/950M/738M |
| baton (sol) | $9.9M | +129.2% | −37.9% | 56% | **above** (+40%) | candidate, small size — vol 4H contracting 300k→107k |
| ZCAT (sol) | $45.6M | +0.1% | −38.7% | 36% | below (−8%) | cooldown |
| USELESS (sol) | $204M | −13.3% | −21.1% | 22% | below (−10%) | needs reclaim of 0.2167 |
| neet (sol) | $31.9M | −17.0% | −30.5% | **5%** | below (−18%) | falling knife, 5 straight lower 4H closes |
| STONK (sol) | $136.7M | −31.5% | −37.0% | 18% | below | cooldown |

Theme map that session (diff against `narrative-snapshot-2026-09-30.md`):
1. **Tokenized-stock pairs** still the meta with the real money — BSC: QQQB ($70M mc / $20M vol),
   SPCXB ($85M), NVDAB ($45M, liq $8.5M), AAPLB, XAUt, BNCB, 牛来 ($74M), MarsCoin ($94M);
   Solana `stonkfun`: STONK, ZCAT, GP, PURR.
2. **Zcash** running — ZEC hot-search #1 on Solana ($123M mc / $37M vol); Binance ZEC $1,228,
   vol24 $201M, **−27.6% off the 30d high of 1,698** (ran, then corrected); derivatives ZCAT (sol) + ZC (eth).
3. Big Solana memes cooling: USELESS, neet, STONK.

Also worth stating plainly when relevant: BOME's +12% was the *only* green row in the user's whole
book (TAO −3.1%, SOL −2.2%, SUI +0.7%), which is how you validate a "this one feels strongest" claim
with data instead of agreeing or arguing.
