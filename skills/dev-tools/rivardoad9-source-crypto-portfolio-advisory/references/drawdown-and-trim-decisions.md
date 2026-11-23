# Drawdown attribution + trim-vs-hedge decisions (and the emotional question)

Companion to `holdings-thesis-verification.md` (checks) and `portfolio-state-reconciliation.md` (state).
Worked on 7 Okt 2026 for a book of ONDO/TAO/WLD/VIRTUAL/BOME/USDT, ~$1,3k.

## 0. AMENDMENT to the checks: there are SIX, not five

Check 6 — **company / control continuity** — for any token whose value rides on an operating company
(RWA, exchange, infra). A dated corporate event outranks TVL, partnerships and regulatory news:

- ONDO, mid-Sep 2026: founder Nathan Allman died (confirmed on the company's own blog + X). Reporters
  then wrote the company was **shopped to buyers** (denied by the company, estate declined comment) and
  a **succession/ownership dispute** followed. The token had peaked $0,6077 on 28 Sep and bled −23%
  after. The earlier sector story (SEC Innovation Exemption carve-outs, unlock overhang, no fee capture,
  weak macro) was all true and still incomplete — **control risk was the layer that explained the
  divergence**, and the first answer missed it because it only searched price/TVL/regulatory lanes.
- Search recipe: `"<company> founder/CEO/leadership"`, `"<company> acquisition/sale/for sale"`,
  `"<company> succession/control"`. Then check whether the token's issuer entity is the one in play.

## 1. Drawdown attribution from the snapshot history (do this before any advice)

Snapshots live in `~/.hermes/data/binance_porto_history.jsonl` (one JSON per ~30 min: `ts`, `total_usd`,
`rows[]` with per-asset `usd`). Compute — never eyeball:

1. `peak = max(rows, key=total_usd)`, `cur = rows[-1]` → drawdown in $ and % from the *tracked* top.
2. **State the window.** If history starts after the top the user remembers ("gw dari 1400 top"),
   say what you can verify (e.g. top $1.391,56 @ 5 Okt 15:30 → −6,6%) and label the older number
   unverifiable. Never silently adopt the remembered top.
3. Per-asset delta from peak → now, and sort by size. Two traps:
   - **A stablecoin delta is a reallocation, not a loss.** USDT −$126,80 with VIRTUAL +$101,60 is the
     user *buying* VIRTUAL, not money evaporating. Report it as a trade and mark that entry's own P&L
     (~−20% in the worked case) — that is a decision the user made, not market drift.
   - Sum of per-asset deltas must equal the total delta; if it does not, the snapshot has an asset the
     parser missed (`rows`/`holdings` key drift).
4. **Uniformity test.** If every coin is down only −4%…−8,5% from its own peak, nothing collapsed:
   the book is one systematic **beta** position. Compare with BTC over the same window (BTC −3,5% from
   $87,2k while the book fell −6,6% ⇒ ~2x BTC beta). "Bukan sial, tapi buku 100% alt tanpa hedge" is
   the honest punchline; a single-coin collapse story would need a coin down 2–3x the rest.

## 2. Sizing a trim in ATR units (why "cut 10%" is usually cosmetic)

```python
atr14_daily = mean(true_range[-14:])          # from the daily kline
trim_pct_of_position = 0.10                   # what the user proposed
# verdict: if trim_pct * position_value < atr14 * position_value -> it is ONE day of normal noise
```

Worked case: ONDO ATR14 = 10,4%/day; a 10% trim ($54 of $539) moved the weight 41,2% → 37,1% and paid
$0,05 in fees — i.e. it buys nothing. Always convert the proposed trim into (a) % of portfolio after the
trade, (b) ATRs of risk removed, (c) $ realized loss, and print all three:

| cut | sell | position after | % of porto | fee 0,1% |
|---|---|---|---|---|
| 10% | $53,89 | $484,99 | 37,1% | $0,05 |
| 40% | $215,55 | $323,33 | 24,7% | $0,22 |
| to cap 12% | $381,90 | $156,98 | 11,9% | $0,38 |

Also give the scenario table in **$ and % of portfolio** (0,42 → −$59 = −4,5% porto; 0,40 → −$82 =
−6,3%; 0,52 → +$55 = +4,2%) — the user reads portfolio impact, not token %.

## 3. When the user refuses to sell: hedge instead of arguing

The user's stated preference is to let positions run; a hedge removes risk without realizing the loss,
which is usually the option that actually gets executed. Binance perp facts to pull
(`fapi/v1/premiumIndex?symbol=<PAIR>`): existence, mark, **funding sign/magnitude**.

- Positive funding ⇒ a short **receives** it (worked case +0,005%/8j ≈ +5,5%/yr) — the hedge is
  self-funding.
- **Liquidation distance is set by leverage, not size**: 3x ≈ +33% adverse move, 5x ≈ +20%. On a token
  with 10%/day ATR that has printed +26% days, 5x is a coin-flip to get liquidated right before the pump
  the user is hoping for. Size so margin fits the free stablecoin balance at 3x (worked case: full hedge
  needed $178 margin vs $151 USDT ⇒ half-hedge at 3x, ~$89 margin).
- Say plainly: spot risk ≈ neutralized, tokens stay in the wallet, upside capped. Then present the
  three-way ladder (structured partial trim / hedge / do nothing with its number).

## 4. The communication pattern for "gw rasa sayang bgt"

1. **Numbers first**, moralizing never. The attachment is a bias — name it once, in one line, then get
   back to arithmetic ("$92 itu udah hilang; yang ada di depan cuma eksposur 41% di token dengan
   control risk").
2. Quantify the feeling: equity −6,6% from top ≠ the coin's −23% — show both so the user stops anchoring
   on a remembered peak.
3. Always name the worst option explicitly: *"yang jangan lu lakuin: cut 10% buat ngerasa lebih tenang —
   itu opsi paling mahal karena nggak beli apa-apa, cuma nunda keputusan yang sama 2 minggu lagi."*
4. State the trigger levels that will change the recommendation (e.g. 2 daily closes below $0,46; $0,52
   reclaim) and that the lane's snapshots are watching them — the user then decides from data.
5. Also surface what the trader did *not* ask about but is load-bearing: here, **ammo** — USDT fell
   $277,86 → $151,07 (11,5%) during the dip, i.e. no dry powder left for a rebalance.

## 5. Systemic shock (exchange hack / withdrawal halt): rank strength, don't go shopping

When the whole tape gaps down on one event, the question changes from "what is cheap" to "who is funded
and what am I holding". Four steps, in this order.

**A. Verify the shock before pricing it.** Two independent outlets (BBC/FT/Guardian/Reuters) plus the
platform's own account; a pasted announcement is a lead, not a fact. Then
`curl -s https://api.binance.com/sapi/v1/system/status` → `{"status":0,"msg":"normal"}` proves only that
the **trading engine** is normal — deposits/withdrawals are a separate rail with no public status field.
Never translate "API normal" into "withdrawals open". While withdrawals are frozen, market risk has
converted into counterparty risk: say which one each dollar is sitting in.

**B. Rank strength with `scripts/crash_relative_strength.py`, never from a watchlist you remember.**
It prints 24h / 7d, % from the shock-day open, 10-day drawdown, position inside the 30d range, and 4h
EMA20/50 stretch, with BTC's 7d subtracted. Three readings that change the answer:

- **Relative strength is not an entry.** A name up ~20% in a −5% week sits 7–12% above its 4h EMA20; buying
  there is chasing. Quote a limit at EMA20, stop under EMA50, and print the R:R (worked: HYPE 92,4 vs EMA20
  86,2 and EMA50 82,5 → bid 86–88, stop 82, target 97,7 ≈ 2:1).
- **Yesterday's leader can flip to laggard in one session.** LINK led on the 7d screen and was −6,2% vs
  BTC −5,1% a day later. Re-run the screen and re-quote the earlier pick; do not repeat it from memory.
- **A spike is not strength.** +48% on $20–40M daily volume is a one-day liquidity event. Keep those names
  out of the candidate table and say why they failed, or the number gets read as a recommendation.

**C. When cash ≈ 0, the answer is a trim, not a buy.** With $0,16 of USDT, "bid X" really means "sell Y at
its worst price of the day". Name the weakest holding — below both 4h EMAs, worst shock-window number,
lowest position in the 30d range — size the trim in ATR units (§2), and park the proceeds in a limit order
*below* market. Cash is the only instrument that reduces risk during a halt; more alt beta does not.

**D. Never let the proceeds land in another laggard.** One session sold the weakest name and put ~$50 of it
into a second laggard that the same screen had just ranked below BTC. After any sale, restate the ranked
list before the next buy; if the new destination is not on the leaderboard, say so with the numbers rather
than letting the user discover it later.
