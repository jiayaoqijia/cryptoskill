# LP position economics — "spot, LP, atau trade meme?" (27 Sep 2026)

When the user asks **where** to play rather than **which platform**, the deciding number is coverage
at *their* size — not a dashboard APR. Worked case: modal $337 → user then said $1,400, and the whole
answer moved because the thresholds are size-dependent.

## 1. The rule (same shape for every AMM venue)

```
fee earned in 24h = pool_fee24h × (your_size / pool_tvl)
round-trip cost   = gas + exit_slippage × your_size      # Solana memecoins: gas ≈ 0.008 SOL, slippage 2%
coverage          = fee earned / round-trip cost          # require ≥ 2.5× (FlowMetrix MIN_FEE_COST_COVERAGE)
```

Gas is a fixed cost, so **smaller positions need a higher fee/TVL**:

| size | RT cost | needs fee24h | needs fee/TVL 24h |
|---|---|---|---|
| $200 | $4.89 | $12.22 | 6.11% |
| $300 | $6.99 | $17.48 | 5.83% |
| $500 | $10.99 | $27.48 | 5.50% |
| $700 | $14.99 | $37.48 | 5.35% |
| $1,000 | $20.99 | $52.48 | 5.25% |

Consequences to state out loud: (a) a token with a Token-2022 transfer fee (300 bps one-way ≈ 6% RT)
raises the bar by ~6 points before fees count; (b) don't exceed ~1–2% of pool TVL (a $400 ticket in a
$63k pool = 0.63%, fine; $1,000 = 1.6% and you move the price on your own exit); (c) anything above
~25% fee/TVL is an outlier (fee spike / token dumping / wash), not healthy yield — quote it, don't sell it.

## 2. Meteora DLMM pool table (the screener behind the numbers)

```bash
python3 scripts/meteora_lp_scan.py 500            # band filter + coverage for a $500 ticket
curl -s -H 'User-Agent: Mozilla/5.0' "https://dlmm.datapi.meteora.ag/pools?page_size=100&page=1"
```

- `page_size` honoured, `limit` ignored; default order = TVL desc. **`sort_by` / `sort_key` / `order` /
  `direction` all return `"data": []`** → paginate 6–12 pages and sort client-side.
- Bare `urllib` (no UA header) → **HTTP 403**; `curl` or `User-Agent: Mozilla/5.0` fixes it.
- Fields: `tvl`, `fees{24h,7d,30d}`, `volume{24h,…}`, `fee_tvl_ratio`, `apr`/`apy`, `created_at`
  (s or ms), `token_x`/`token_y` (`.symbol`, `.address`), `pool_config`, `is_blacklisted`.
- **Use absolute `fees`, never volume** (volume/TVL >10×/day = churn/wash); cross-check holders and
  mint/freeze authorities separately — `gmgn-cli token security --chain sol --address <mint> --raw`.
- DefiLlama `yields` does **not** carry most DLMM memecoin pools → it cannot answer this question.

## 3. Worked scan (both runs, same day, 800-pool samples)

Band = TVL $50k–500k, vol 24h ≥ $10k, age ≥ 48h (the engine's own filters). Result: 153 pools in band,
**16–17 clearing the ≥2.5× bar** — i.e. a "no candidate clears the breakeven gate" engine state coexists
with a rich pool set. **"Gate rejected everything" is a claim about the shortlist, not about the market**;
the engine ranks fee/TVL × volume, keeps the top 3 and then drops candidates on `no-wsol`, age and
bin-width. Before concluding a regime is dead, run this scan.

Top of the band in both runs: GP-SOL (~32% fee/TVL, TVL $144k, ~14× coverage on $400–500) · ELON-SOL
(20.7%, $63k, ~9×) · parafactual-SOL (14.9%, $52k) · OP-SOL (14.6%, $98k) · COLLECT-SOL (12.6%, $86k).
All meme pairs — the fee *is* the compensation for volatility; treat as 24h cycles with TP/SL, not holds.

## 4. Market-regime check (is any of this actually hot?)

Cheap, keyless-ish reads that beat vibes, 27 Sep 2026:
- CoinGecko majors + `alternative.me` Fear & Greed: BTC 94th percentile of its 90d range, SOL **100th**
  (at range high), F&G 70 Greed → spot entry here is chasing, so DCA in 2–3 tranches.
- DefiLlama: `api.llama.fi/overview/dexs/solana?dataType=dailyVolume` (24h $2.16B, **−17.5% d/d, −25.1% 7d**),
  `summary/fees/meteora-dlmm` ($1.09M/24h vs $997k 7d avg) → chain activity cooling while LP fees stayed rich.
- `gmgn-cli market trenches --chain sol --type completed --raw` + `track smartmoney --chain sol --limit 100 --raw`:
  quote **smart-money ticket size** and fresh-launch `volume_1h`, not token counts. 100 smart-money rows
  totalling ~$5.2k in small tickets + fresh launches at ~$0 volume_1h ⇒ memecoin conditions are thin.
  Parse quirks: field names differ per category (`usd_market_cap` populated on `new_creation`, 0 on
  `completed`) — print the first row's keys before trusting any field; the envelope is
  `{completed:[…], near_completion:[…], new_creation:[…]}`.

## 5. Venue take-rate line (the number most dashboards hide)

Convert every venue to "what fraction of the yield reaches me":
**Meteora DLMM = LP keeps 90% of swap fees, 0% performance fee** · Krystal Auto-Farm = 10% of all rewards
· Nest (HyperEVM) = LPs receive **0% of fees**, emissions only (see `nest-hyperevm-lp-2026-09.md`).
State the take-rate before quoting any APR.

## 6. Answer shape that worked

Rank the *venues for this user's actual edge + size* (LP > spot > memecoins here), give an allocation
table in dollars, and attach the one number that governs it (coverage at their size). Then the honest
caveats: IL risk is absolute in dollars, high-fee pools are meme pairs, and the venue whose take-rate is
highest loses by default. Never end with "mau gw buatkan?" — deliver the plan.
