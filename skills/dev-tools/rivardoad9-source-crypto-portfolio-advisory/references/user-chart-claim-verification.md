# Verifying the user's own TradingView charts against live data (before opining)

Companion to `drawdown-and-trim-decisions.md`. Worked 7 Okt 2026: the user sent five weekly/daily
screenshots (TAO, WLD, VIRTUAL, ONDO, BTC, ETH) with the claim *"semua lagi retest, lebih wise buy and
hold aja kalau tokennya proven"*. This is a recurring request shape — his charts arrive as proof of a
thesis and usually want a verdict, not a commentary.

## Rules

1. **Never read the verdict off the screenshot.** Rebuild every claim from the exchange: Binance keyless
   — `api.binance.com/api/v3/klines?symbol=<SYM>&interval=1w|1d&limit=400` plus
   `/ticker/24hr?symbols=["…"]` for live price + 24h change. Run `scripts/chart_claim_verify.py`.
2. **Recompute his indicator and show it matches.** This buys the credibility to then talk about what he
   missed: Stoch(5,3,3) weekly computed 72,32/74,29 vs the chart's 72,30/74,28 → *"chart lu bener, bisa
   dipercaya"* lands far better than "menurut gw".
3. **Labels and percentages on the chart are TARGET LEVELS, not prices** (memory: `'%' = LEVEL TUJUAN`).
   Vision descriptions of chart text are unreliable — one screenshot was read as WLD $0,9490 while live
   was $0,5170. Verify the pair, then quote the live number and say which drawn level it sits on
   (WLD $0,517 ≈ his own 0,5180 support = "ini momen keputusan, bukan retest yang udah kelar").
4. Per name, recompute: 200/50-EMA on **both** weekly and daily (above/below + %), 52w high/low and
   position in range, % bounce off the 52w low, Stoch weekly **and** daily, and the last 4-5 bars as %
   changes. A table beats prose.

## The two checks that change the answer

- **Structure-break test** — weekly close vs the high of the previous 11 weeks. All five names printed
  *"BELUM break struktur"*: the wedge / trendline-break / triangle are **anticipatory** patterns, and what
  the user calls a retest is a retest of a **bounce**, not of a breakout. Use exactly that distinction.
- **Acceleration + oscillator level** — count the last 3-4 daily bars. Red and deepening
  (WLD −2,4 → −1,5 → −4,1 → −6,3%) is selling pressure, not support-testing. Weekly Stoch 68-83 with
  daily Stoch 30-45 and no oversold print (<20) = *"belum ada trigger beli; ini zona tunggu"*, then hand
  over the trigger (daily Stoch <20, or BTC reclaiming its prior structure) instead of a vague "sabar".

## Testing "buy and hold kalau tokennya proven" — don't argue with the framework

Acknowledge what is right first (structure intact, the name really is the most substantial holding), then
test the word *proven* with the ATH table: pull the all-time high from the same klines for **every**
holding **and BTC**. Worked case: BTC −33,6% from its own ATH while TAO −76,5%, ONDO −60,1%,
VIRTUAL −70,2%, WLD −95,7%, BOME −96,8%. Punchline that landed: **conviction does not reduce drawdown —
size does**; the most "proven" asset in crypto was down a third.

Then the three conditions for a legitimate buy-and-hold, checked per name:

1. **Thesis** intact, not just price (control-continuity events fail this — ONDO: founder died, succession
   dispute, 36% of float unlocking Jan 2027).
2. **Size survives −60%** without a forced sale (23% of book = yes; 41% = no).
3. **Cash left to add** on capitulation (USDT at 11,5% = no dry powder).

Verdict shape: *hold* the name that passes (with a level that invalidates it: weekly close below 252 for
TAO), *cut to cap* the name whose thesis broke, and never add at weekly Stoch 70-83 with five red dailies.

## The beta line that explains his own P&L

Put the 24h moves side by side: BTC −2,9% vs ETH −5,1%, WLD −8,6%, VIRTUAL −9,6%. Alts print **2-3x BTC**,
so a 100%-alt book takes 2-3x every BTC wobble. That is the mechanism behind *"kok porto gw turun lebih
cepet dari market"* — structural, not luck. Reuse for every "market lagi turun semua" message.

## Pitfall: disambiguate the percentage before computing anything

*"cut 10% nih? … 1300 equity gw, dari 1400 top"* was the user reporting **equity −10% from the top**, not
asking for a 10% trim. Treating it as a trim request answered the wrong question and had to be walked
back. When a percentage arrives without a referent, resolve it first (trim-%-of-position vs
drawdown-%-from-top vs % of account) — or compute both. The recovery that worked: pull
`binance_porto_history.jsonl`, state the verifiable top / now / drawdown, and continue from there.
