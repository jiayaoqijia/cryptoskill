# Standing portfolio risk monitor (health + allocation + on-chain flow + verified news)

Class of ask: "bikin dashboard risiko portofolio", "porto health", "alokasi kemana aja", "ada whale
akumulasi atau distribusi gak di token gw", "news token yang gw hold". This is the *monitoring* sibling of
the advisory workflow — same honesty rules, different cadence (recurring, delta-only) and different
deliverable (a page + a silent-until-changed cron).

Reference implementation on this host: `~/.hermes/scripts/porto_risk.py` (CLI that emits the whole dict),
`~/.hermes/scripts/porto_intel.py` (on-chain flow + news layer), `~/.hermes/scripts/porto_dashboard.html`
(page), served by the existing board server on `/risk` + `/api/risk`. Page-serving mechanics →
`localhost-dashboard-serving`.

## 1. Health score (visible breakdown, not a mystery number)

Weighted composite out of 100 per token, then a portfolio roll-up = value-weighted average of holdings:

| component | weight | what it measures |
|---|---|---|
| trend | 24 | price vs MA20/MA50, 30d change |
| alpha | 16 | 7d return minus BTC's 7d return |
| narrative | 14 | theme 7d perf, alpha vs market, breadth, volume trend |
| whale | 12 | monitored whale net + long share (zero if notional is thin) |
| liquidity | 12 | MC/FDV, turnover, ATH distance |
| dilution | 14 | % locked/vesting, inflation rate, cliff proximity |
| stability | 8 | daily σ, beta |

Grades: **A ≥78, B ≥62, C ≥45, D <45**. Re-read the grades after any reweighting and sanity-check them —
a thin meme grading "A" means the weights are wrong, not that the token is safe. Scores are a *ranking
device for attention*, never a buy signal; say that on the page.

## 2. On-chain accumulation vs distribution (keyless)

Two sources, both free, and they must corroborate each other:

**A. DEX flow (DexScreener).**
1. Contract addresses: CoinGecko `/coins/markets?vs_currency=usd&symbols=…` gives each coin's `id`, then
   `/coins/{id}?…` returns `platforms` (`{chain: address}`). Cache this ~7 days. Hardcode an address
   override when CoinGecko has no platform row for a known token.
2. `https://api.dexscreener.com/latest/dex/tokens/{addr1,addr2,…}` → pairs. **Never search by symbol** —
   symbol search returns dust/junk pairs with absurd liquidity.
3. Reference pair = largest **24h volume** (not largest liquidity; liquidity alone picks a dead pool on a
   side chain). Report the chain + dex + txns so the user can see where the number comes from.
4. `net_pressure = (buys − sells) / (buys + sells)` from `txns.h24`; label **akumulasi** > +0.15,
   **distribusi** < −0.15, else **netral**.
5. Confidence gate: treat as evidence only when `volume.h24 ≥ $250k` and `liquidity.usd ≥ $300k`;
   otherwise print "keyakinan rendah — pair tipis, jangan jadiin dasar".
6. Native-chain tokens (e.g. TAO/Bittensor) have **no DEX pool** — say that explicitly and fall back to
   the whale book instead of showing a blank or, worse, a fake number.

**B. Whale positioning (Hyperliquid book).** Net per coin, long share, wallet count long/short. Store the
per-coin net in the snapshot every run so the next run can print **Δ vs sebelumnya** — a single snapshot is
not a signal, a delta is. Normalise units defensively (`prev.get("net") if not None else
prev.get("net_m")*1e6`) so a unit change doesn't silently produce a garbage delta.

Reported output is a *proxy*, never "exchange netflow" — real netflow is paid. Frame it as "flow DEX +
posisi whale" and keep both numbers adjacent.

## 3. Verified-news gate (so noise doesn't reach the card)

Do **not** build a new feed — reuse an existing classified store if one exists (this host:
`~/.hermes/data/crypto_impact.db`, rows with `source`, `level`, `score`, `why`, publishing time; sources
are already tier-1: CoinTelegraph, The Block, Decrypt, Bitcoin Magazine, SEC.gov, CFTC.gov). Rules:

- Match the holding by ticker (word-boundary regex) **or** project name, in title + summary.
- Window: 30 days per token, 7 days for market-wide items.
- **✅ terverifikasi** = tier-1 source AND (`level` HIGH/MED, or a real event tag in `why`, or an event
  keyword: partnership / integration / launch / listing / tokenize / acquisition / funding / ETF /
  buyback / burn / lawsuit / settlement / upgrade). A LOW-level item from a tier-1 outlet about a real
  event is still "verified" — the classifier's LOW usually means "no market-wide impact keyword", not
  "made up".
- **⚠️ perlu dicek** = tier-1 source, impact not yet clear.
- **Dropped** = price predictions, TA/forecast/"could moon", listicles, how-to-buy, opinion, social feeds.
  Count them and print the count on the page so the filter is auditable ("23 item noise dibuang").
- Macro items are a *separate* short list (≤4), filtered to market-structure tags (ETF, institution,
  regulation, exchange) — otherwise unrelated hacks of random protocols leak into the "market news" block.
- Cron that consumes this: notify only on **new** verified items (diff against the previous snapshot's
  news titles), never a daily re-send of the same headline.

## 4. Honest-limits block (put it in the page AND the report)

- DEX flow is a DEX-side proxy, not exchange netflow (paid).
- Whale book = the wallet set being tracked, not the whole chain.
- Unlock data: DefiLlama `/unlocks` (advance cliffs) is a paid endpoint — keep a curated
  `data/<tool>_unlocks.json` (`date`, `kind: cliff|monthly`, `pct_float`, `pct_supply`) and admit it is
  partial rather than implying full coverage.
- Everything is read-only: the monitor never places or cancels an order.

## 5. Presentation rules that survived review

- Cash belongs in the allocation chart, otherwise the legend sums to <100% and the user reads it as a bug.
- "Over cap" is called out per token with both numbers (`41.9% > cap 12%`) plus the action word (TRIM).
- Unlock cliffs get a highlighted banner; drop the duplicate line from the generic negatives list.
- Concentration and unlock go at the **top** of the negatives list — the risks most often ignored.
- Delta cron prints nothing on the happy path; `--delta` on first run says "baseline" and the wrapper
  suppresses that line so the first cron tick isn't a false alarm.
