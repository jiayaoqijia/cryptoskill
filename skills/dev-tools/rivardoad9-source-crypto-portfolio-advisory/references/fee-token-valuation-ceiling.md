# Fee/revenue token: machine + valuation ceiling

Worked example: StonkFun / STONK, 30 Sep 2026 (all figures pulled live, sources dated).

## Why this shape

For a token whose only claim is a revenue-funded buyback/burn, the question is not "is the narrative
good" but "what is the machine worth". Narrative tokens get priced on story; fee tokens get priced on
run-rate × multiple, then cross-checked against the sector leader's revenue share. Stopping at "the
burn is real" only proves the mechanism — it says nothing about whether the price is cheap.

## Primary evidence: the platform's own API (keyless)

StonkFun (stonkfun.xyz) publishes machine-level numbers. Endpoints confirmed working 30 Sep 2026:

| Endpoint | Returns |
|---|---|
| `/api/public/v1/tokens/{mint}` | `market{priceUsd, marketCapUsd, fdvUsd, volume24hUsd, liquidityUsd, priceChange24h, peakMarketCapUsd}`, `quote{mint, symbol, category}`, `mode`, `transferFee.bps`, `flywheel.active`, `status`, `graduatedAt`, `createdAt` |
| `/api/public/v1/tokens/{mint}/burns` | `totals{amountTokens, valueUsdAtBurn, burnCount, lastBurnAt}` + `burns[]` (signature, amountTokens, `source: "buyback"`, burnedAt) ← the burn ledger |
| `/api/public/v1/stats` | `tokens{total, graduated, rewardLaunches, totalMarketCapUsd, totalVolume24hUsd}`, `revenue{totalRevenueUsd, totalBuybackUsd}`, `burns{totalValueUsdAtBurn, burnCount}`, `config{graduationMarketCapUsd, …}` |

`/burn`, `/burns`, `/platform` are 404 — the token-scoped plural path is the live one. The burn ledger
is the strongest evidence available: a `lastBurnAt` timestamp from **today** means the flywheel is
still running right now, which no promo page can prove.

## Worked example (STONK, 30 Sep 2026 12:05–12:10 UTC)

- Supply 809.957.358 (launched at 1B; mint + freeze authority null from day one → supply only falls)
- Burns: **190.013.364 = 19,0% of supply · $18.351.063 at burn · 21.154 events · last burn 12:08:05 UTC**
- Platform: 152.523 coins launched, 4.255 graduated (2,8%), 114.274 reward launches (75%)
- Cumulative revenue **$29.112.654**; cumulative buyback **$17.386.350 = 59,7%** ≈ the claimed 60%
- Platform volume 24h **$143.727.274** → implied blended take ~0,29% → run-rate ≈ **$420k/day ≈ $153M/yr**
- MC **$218,9M** → **P/S ≈ 1,4x** on today's run-rate (peak-hype day 11 Sep printed $2,21M revenue)
- Comps: PUMP ~**$1,84B** (revenue share 64,2%), PONS ~$569M (28,2%), BONK ~$300M
- **Share-parity check**: PUMP $1,84B × StonkFun share **7,58%** ≈ **$140M** vs live $218,9M → priced
  *at or above* its revenue share. Punchline: not cheap; upside requires share gain or meta growth,
  not a re-rating. That framing is what turned "great burn story" into an 8% sized swing, not a bet.
- Scenarios (each row carries its revenue assumption + multiple):
  bear $110–140M (−35/−50%) · base $380–540M (1,7–2,5x) · bull $1,2–2,2B (5,5–10x) · moon $3B+
- Structural risk found in the same pass: **the moat was copied in a week** (pump.fun Custom Pairs
  9 Sep, Holder Rewards 12 Sep) and by late Sep pump.fun was back above ~73% of daily launchpad
  revenue share. A 7-day revenue win is a peak moment, not a trend.
- Second-order risk of the reward model itself: a 3% transfer tax drained a large share of supply in
  several coins (ZCAT 61%, PURR 81%, GP 71%, RAYCAT 91%) — the revenue source is holder bleed.

## Deflation arithmetic (state it plainly)

`buyback_usd_per_day ÷ price = tokens burned per day`. Quote the **USD rate** and the invalidation
level (revenue/day below which the burn becomes cosmetic), not the token count — the count burned
shrinks as price rises, which is exactly the confusion bull threads exploit.

## Execution venue for quote-paired coins (xStock / alt-quote pools)

- StonkFun coins are Raydium LaunchLab/CLMM pools quoted in an xStock or another coin; stock-quoted
  coins get bought by routing through Jupiter, so the platform UI (stonkfun.xyz) always works and
  Jupiter-routing terminals usually do. Pick the venue that *routes the pool*, then optimise fees.
- Round-trip platform cost at ticket size (verify live before quoting): GMGN ~1% flat · FOMO ~0,5%
  with a **$0,95 minimum** → the minimum makes FOMO 6,3% on a $30 ticket, 3,8% on $50, and cheaper
  than 1% flat only above ~$190 per trade.
- The token's own transfer tax (StonkFun reward mode: 100 or 300 bps) is charged on **both** legs and
  dwarfs the venue delta — a 3% tax coin ≈ 8% round trip on GMGN vs ~7% on FOMO.
- Keep self-custody: connect the user's own wallet (Phantom) to a terminal web app; a custodial bot
  wallet cannot be verified on-chain, which breaks the "verify, don't trust the book" rule.

## Ranking the whole fee-token universe (keyless DefiLlama recipe)

When the ask is "which revenue/buyback coins are worth it right now" instead of "is this one token cheap", build the
universe rather than naming favourites:

1. `https://api.llama.fi/overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyRevenue`
   → protocols with `total24h` / `total7d` / `total30d` revenue. This endpoint carries **no market cap** (`mcap: 0`), and
   `/protocol/{slug}` fills `symbol` + `mcap` only for some entries.
2. Cross-index against market data instead of trusting either: CoinGecko
   `/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1..2` matched by UPPERCASE `symbol`
   (2 pages ≈ 500 coins), then rank by **annualized revenue yield = rev30 ÷ mcap × 12**.
3. **Sum a protocol's products before ranking.** DefiLlama lists each product as its own row — pump.fun and PumpSwap,
   Meteora DLMM / DAMM V2 / Dynamic Bonding Curve, Jupiter Aggregator / Perpetual / Lend, Lighter Perps / Spot. Ranked
   row-by-row the protocol looks small and lands in the wrong tier.
4. Sanity-filter rather than trusting the table: drop chain/stablecoin/CEX categories, and check tradability with
   `/api/v3/ticker/24hr?symbol=XUSDT` (spot) plus `/fapi/v1/premiumIndex?symbol=XUSDT` (perp) before recommending anything.
   A name whose protocol revenue rounds to zero will sit in the list — that is a finding (narrative-carried, like an RWA
   issuer with AUM but no fees), not a missing row.

### Two traps this screen always shows

- **The highest yields are the dying tokens.** Launchpad coins print 50–260% annualized yields precisely because price
  collapsed faster than revenue, so a yield table sorted descending is a list of things already down 40–60%/30d. Pair
  every yield with the 30d trend and an explicit "why is this cheap" answer before it reaches a shortlist.
- **Cliff size cannot be verified from DefiLlama.** `/emissions` answers 402 (paid tier), so unlock dates and sizes come
  from secondary sources — and those disagree. **Adjudicate before letting a cliff kill a candidate: an aggregator
  headline frequently quotes CIRCULATING SUPPLY, not the release size.** The tell is the number matching a known supply
  figure — a quoted "558M unlock" sitting on top of a 558M circulating supply is the supply total, while the real event
  was 7,1M ≈ 0,7% of supply ≈ $3M. Compare the quoted figure against BOTH circulating and total supply from market data,
  keep the source that states the round number and its share of supply; treat a mis-read cliff as a candidate wrongly
  deleted (and an unadjudicated one as a candidate wrongly admitted).

### Divergence screen: which tickers are mispriced against their own revenue

"Cari ticker yang miss di pricing dan fundamental" is a different cut of the same data — rank revenue growth
against price change and read the gap, rather than ranking the level.

1. **Join on `defillamaId`, not on `gecko_id`.** `/overview/fees` returns `gecko_id: null` on every row, so an
   id join matches nothing and looks like "no protocol has revenue". Map `/protocols` `id` → the fees row's
   `defillamaId`, then fall back to normalised `displayName`/`name` matching against CoinGecko names; report the
   coverage (roughly two thirds of a top-100 is normal). A token with no fees row is **unmeasured**, not clean —
   say that instead of implying it passed.
2. **Filter on revenue size before ranking any percentage.** Growth off a dust base is arithmetic noise: a chain
   with ~$30k/month of measured revenue prints "+139%" and an issuer with ~$90k prints "+423%", neither meaning
   anything. Require `rev30 ≥ $500k` first, then rank — without it, five dead chains own the top of the table and
   the real candidates sit below them.
3. **Read the sign combination, not just the rank.** `fund = avg(revenue Δ30d, fees Δ30d)`, `gap = fund − price Δ30d`.
   Positive gap with revenue flat-to-up is a candidate. Price down **and** revenue down **and** a high P/S is a
   **de-rating** — the market repricing a shrinking business — so label it that way instead of calling it cheap.
   Price holding while revenue falls is the overpriced case, and it is the more common one.
4. **Check the level is not one week.** Pull `/summary/fees/{slug}?dataType=dailyRevenue` and sum the last four full
   weeks: one spike week inflates the 30d comparison, a steady weekly band does not. A name whose weekly revenue
   halved over two months (a DEX going from ~$5M/wk to ~$2M/wk) is deteriorating even if its 30d number still prints
   a positive change.
5. **Pair every "cheap" with the mechanism that returns cash and the variable that kills it.** Buyback as a share of
   revenue, then the dependency: a launchpad's revenue dies with the meta, so a 4x P/S on peak-cycle volume is not the
   same 4x on trough volume. State the trough-case multiple out loud — that is the sentence that stops a screen from
   reading as a buy call.

### Screen mechanics that decide whether the table is usable

- **`/overview/fees` can come back without `symbol` at all** (not just `gecko_id: null`). Build name → symbol from
  `https://api.llama.fi/protocols` first, then fall back to matching the ticker's `name`; a symbol-only join silently
  yields "0 ticker joined" and looks like the market has no revenue data.
- **One call for prices when CoinGecko 429s:** `https://api.coinpaprika.com/v1/tickers?limit=1000` returns rank, mcap,
  volume and 1h/24h/7d/30d changes together — no `price_change_percentage` param, no second call. Reusable runner:
  `scripts/revenue_divergence_screen.py` (`--top`, `--min-rev`, `--min-mcap`; prints the yield table plus a
  `revCh30 − ch30` gap ranking).
- **Duplicate adapter rows are not "products" to sum.** The same protocol shows up several times with contradictory
  totals (one row at 0.00% yield and P/F 23.352 next to the real 27,6% / 3,6x). Dedupe by protocol name keeping the
  largest `total30d`, and only *sum* rows that are genuinely different products (pump.fun + PumpSwap, Jupiter
  Aggregator + Perp + Lend). Skipping the dedupe produces a table sorted by garbage.
- **DefiLlama revenue is gross; the holder yield is what the framework pays out.** A 10,7% "yield" on a stablecoin
  issuer turned out to be ~4% once the actual allocation (buyback + staking rewards + burn share of net surplus) was
  read from its quarterly report. Before quoting a yield as holder return, find the split in docs/governance and quote
  the split, not the gross number.
- **Print FDV/mcap beside the yield for every shortlisted name.** A float of 23–25% turns a 4x-on-float "cheap" into
  20x+ on FDV, and a token with 4x supply still to unlock is not mispriced, it is early. Overhang ≥2x = watchlist at
  best.
- **Re-run the names from the previous screen and retract them by name.** This user remembers the earlier shortlist
  and compares: a ticker whose revenue fell 30% while its price fell 11% has become relatively *expensive* — say
  "thesis-nya udah nggak valid" with both numbers instead of quietly dropping it from the table.

### Turning the universe into a ranked shortlist (the shape he asks for)

Five gates, each scored 0–2, total out of 10 — publish the per-gate scores beside the total so the ranking is auditable
and the user can re-weight it himself:

| Gate | 2 | 1 | 0 |
|---|---|---|---|
| Revenue yield = rev30 ÷ mcap × 12 | ≥ 4% | 2–4% | rounded to zero, or no revenue row |
| Buyback / burn | mechanism named (fee % → open-market buy → burn) and running | announced, under review, or unverified | none found |
| Unlock safety | fully vested, or next event ≲ 1% of supply | next event unverified | cliff ≥ ~3% of supply or ≥ 10% of mcap inside the window |
| Catalyst | dated, verifiable, 2027-relevant | narrative without a date | none |
| Alpha vs BTC (30d AND 90d) | positive in both windows | positive in one | negative in both |

- **A buyback mentioned only in a promo post scores 1, not 2.** Verification is one search per name against docs /
  governance / an announcement that names the fee split — the mechanism is the evidence, not the adjective.
- **Measure alpha from venue daily klines, not from a price table** (token `klines?interval=1d&limit=100` vs the same
  for `BTCUSDT`); a token listed for less than the window has no 30d alpha — mark it `n/a` and say which window you used
  instead of quietly substituting a shorter one.
- **Comps and sector share beat raw multiples** for the top of the list: a token trading above the market-cap share of
  its sector leader is priced, not cheap (see the STONK/PUMP share-parity check above).
- Close the answer with the dated calendar of the events the screen turned on (each unlock/announcement date a line) —
it is the part he acts on, and it converts a static ranking into something to monitor.
- **Open the chat answer with one regime line** (BTC.D + breadth + total mcap from `~/.hermes/scripts/market_regime.py`).
Since these screens surface names at the bottom of their 30d range, the regime line is what stops the table from reading
as "buy everything today": with dominance rising, the honest framing is "fundamentals haven't broken, entries are staged".

## From a ranking to a fair value (the "fair value-nya berapa, undervalued atau overvalued?" follow-up)

A ranking says which name is relatively better; a fair value says what price the cash flow supports. Same
universe, three steps:

1. **Let the market price the multiple, then price each name off it.** Fix ONE unit convention first —
   `mult = mcap_M ÷ (rev30_M ÷ 30 × 365)`. Filter the universe (mcap ≥ $80M, revenue > 0), then take
   p25 / median / p75 of `mult` and a median **per category** (reference run: Dexs ≈ 21x, Derivatives ≈ 23x,
   Launchpad ≈ 9x, aggregator ≈ 19x, Lending ≈ 28x). Use the category median as the fair multiple: the raw
   universe median (~23x) flattens a launchpad against a lender and prices both wrong.
2. **Adjust for revenue trend, not for the story.** Weight each product row's `change_7dover7d` by its own
   revenue to get one week-over-week figure per protocol, then scale the fair multiple: ≥ +5% → ×1,1 ·
   −5…+5% → ×1,0 · −15…−5% → ×0,9 · −25…−15% → ×0,8 · ≤ −25% → ×0,65.
3. **Publish a band, not a point.** `fair price = price × (ann_rev × fair_mult) ÷ mcap`, then ±30% on the
   multiple for the bear/bull ends and one line of `undervalued / wajar / overvalued` from fair ÷ price.
   A single number implies a precision the model does not have.

**Always publish both verdicts — circulating and fully diluted.** A verdict computed on circulating mcap
flips when the float is thin: a name with ~23% of supply circulating sat at 22,8x on float but 97,8x on FDV
against a 23,3x sector median. Print `MC/rev` and `FDV/rev` side by side and say which one the
"undervalued" label came from — fair on float and 4x the sector on FDV is expensive, not fair.

**State what the model cannot see in the same message:** no unlock weighting (a cheap revenue multiple on a
name with a cliff ahead is not cheap), no buyback-quality weighting (an automatic daily burn is not a
discretionary one that can be paused), and the multiple is the market's current mood for that category —
when the whole sector is being de-rated, a screen built on today's multiple calls everything undervalued.
Sanity-check before publishing: `mult` lands between ~1x and ~200x, and the revenue yield is on the same
scale as the sector.

### Three measurement traps

- **Never quote DefiLlama's own change fields (`change_30dover30d`, `change_7dover7d`) as revenue growth.** They are
  computed on a different basis than the daily series and can flip the sign: a name whose `change_30dover30d` read
  **+20,4%** summed to **−21%** (last 30 days vs the prior 30) from `totalDataChart`. Sum the daily series yourself, and
  if a field number already reached the user, retract it in the same message with both figures — a silent swap reads
  as fabrication.

- **Never measure revenue momentum as today's 24h revenue ÷ the 30d daily average.** It reads every
  protocol as decaying on low-volume days (weekends) and produced a "55 of 61 protocols are shrinking"
  claim that had to be retracted. Use `change_7dover7d` for week-over-week momentum, and `average1y` for the
  LEVEL — it is a DAILY average over the year (`average1y × 365 ≈ total1y`), so compare `rev30 ÷ 30` against
  it, never `rev30` itself. Level and momentum can disagree: a name well above its yearly average with a
  negative week is a correction off a peak, not a collapsing business.
- **A unit mix fails silently.** Computing a multiple with mcap in $M against absolute-dollar revenue yields
  0,0x multiples and upside in the millions of percent, and a garbled console print hides it. Fix the unit
  convention once, print the assembled result dict with explicit separators, and check the 1x–200x band
  above before any verdict reaches the user.
