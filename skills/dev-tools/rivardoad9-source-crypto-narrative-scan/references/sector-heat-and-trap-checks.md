# Sector heat + trap checks (additions worked out 2 Oct 2026)

Method additions for the narrative-scan flow. SKILL.md could not be patched on 2 Oct 2026 (curator
read-before-write guard vs. skill_view dedup), so the method lessons live here — treat this file as
part of the procedure, not as an optional appendix.

## Step: sector heat via CoinGecko categories (keyless, cross-sector)

GMGN's trench feeds only show memecoin churn; a *sector* rotation (gaming, AI, RWA) shows up as one
cluster of categories, not one mint. Fastest read:

```bash
curl -s -H "User-Agent: Mozilla/5.0" https://api.coingecko.com/api/v3/coins/categories
# per-category token detail (24h/7d/30d + ATH distance):
curl -s -H "User-Agent: Mozilla/5.0" "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=<id>&order=market_cap_desc&per_page=50&page=1&price_change_percentage=24h,7d,30d"
```

- **Cluster test:** siblings moving together = real meta (2 Oct 2026: Simulation Games +27.8%, Gaming
  Utility +12.7%, Breeding +10.4%, Play-to-Earn +9.3%, Axie +8.8%, Arcade +8.1%, Gaming Governance
  +7.9%, Card Games +7.5%). One category green while siblings are red = one token or a composition
  artifact → see "Category % can be an artifact".
- Filter to `market_cap > $100M` before ranking, or $50k ghost categories top the list.
- Columns that pick a *trade*: `7d`/`30d` change, `ath_change_percentage` (room left), and turnover
  `total_volume`/`market_cap` (>3× on a small cap = active speculation worth investigating; ALICE at
  6.4× was the standout).
- **Rate limits:** keyless CoinGecko 429s on shared IPs. Sleep ~2.5 s, retry 429 with ~12 s backoff,
  prefer one batched `coins/markets?ids=a,b,c` call over many single-token calls. CoinPaprika's
  `tickers/<id>` needs a coin ID (tickers like `sand`/`ilv` 404) — use it only with IDs, otherwise
  stick to CoinGecko + DexScreener.
- **DEX reality check:** `https://api.dexscreener.com/latest/dex/tokens/<address>` is keyless and
  generous. Read pool liquidity + 24h volume before ranking anything as a pick.

## Trap checks (run these before publishing any picks)

1. **Category % can be a composition artifact.** "Tokenized Assets +101% / RWA +42%" in 24h while
   Tokenized Stocks was −0.8% = one newly-tagged asset (`figure-heloc`) entering the category. Open
   the category token list before quoting a sector number; if the move isn't broad, call it
   reclassification, not a rally.
2. **A top gainer can be a dying asset.** SWEAT +177%/24h came one day after the Sweat Foundation
   announced Sweat Wallet and SWEAT **end 30 Dec 2026** — a dead-cat bounce on a wind-down. For every
   big mover run `web_search "<token> surge/pump reason"`; if a termination, exploit, or delisting
   sits behind it, name it in the excluded/"jebakan" section rather than the picks.
3. **Dust-ticker search = "not found".** 60+ `market search` hits with 1–30 holders and <$100k MC
   means the ticker cannot be located — say so and ask for chain/address; never promote the largest
   of the dust (a $24M-MC/117-holder mint is still fake). Same for event memecoins: dozens of $2k
   mints with no dominant winner (GTA6 clones) are not a lane, and saying so *is* the finding.
4. **Narrative without liquidity is not a trade.** Real product + real story can still be un-sizeable
   ($PLAY: 7,627 holders but a $129k pool and $993 daily volume). Story-rich but illiquid → "watch".
5. **Momentum = 7d/30d/turnover, not today's candle.** Once a leader prints +47% in a day (SAND), the
   entry is gone; give a pullback zone instead of a chase.

## Report-shape additions the user expects

- **Hunt a dated external catalyst** and state the window: 2 Oct 2026 → gaming underwritten by
  GTA 6 on **19 Nov 2026** (pre-load 12 Nov), reaffirmed on Take-Two's 7 Aug 2026 earnings call;
  "buy the anticipation, expect sell-the-news on the date".
- **Excluded list is mandatory**, by ticker: traps (SWEAT), dust verdicts (QTC, GTA6 clones),
  already-run micro-caps (MAGIC/OMI/ALU/TAKE/CAH), leaders already +47% (SAND), and
  hard-catalyst-but-illiquid names (GMEE at $138k liquidity, $PLAY) — the user reads this as proof
  nothing was missed.
- **CEX-listed picks are outside the Solana LP engine** → say "SL manual wajib", never imply
  automated coverage.
- Diff against the dated snapshots in this directory (`narrative-snapshot-*.md`) and answer
  "same meta as last time, cooling or accelerating?" explicitly.
