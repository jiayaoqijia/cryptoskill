# Meteora DLMM LP pool screening (built 27 Sep 2026)

An LP sleeve decision was made from a pool scan, and the scan's top results turned out to be a trap.
This is the corrected method, the evidence, and the cost model.

## The trap (27 Sep 2026 evidence)

Scanned 799 DLMM pools → 158 in the engine band (TVL $50–500k, volume ≥$10k) → 22 with coverage ≥2,5×
for a $300 position. Coverage = (position × fee_24h ÷ TVL) ÷ round-trip cost.

Sorting by coverage gave the highest scores to the *worst* tokens:

| Pool | coverage | fee/TVL | token 24h | holders | verdict |
|---|---|---|---|---|---|
| e/acc-SOL | 35,4× | 82,6% | **−67,6%** | 19.902 | 2 days old, −84% from ATH |
| GP-SOL | 12,3× | 28,6% | −46,6% | 23.114 | dumping (3%/3% tax) |
| YAP-SOL | 11,6× | 27,1% | −64,4% | 4.935 | dumping |
| PAID-USDC | 11,2× | 26,1% | −30,8% | 42.314 | deepest real liquidity ($2,34M) |
| ELON-SOL | 7,9× | 18,4% | −52,6% | 10.011 | dumping |
| OP-SOL | 5,3× | 12,2% | **+48,7%** | 1.809 | thin holders |
| COLLECT-SOL | 4,8× | 11,2% | **+45,0%** | 8.343 | healthy candidate |
| pill-USDC | 4,0× | 7,5% | **+8,7%** | 3.712 | most stable |

Mechanism (hypothesis consistent with the data): fee/TVL explodes when flow is one-sided — volume is
dominated by sellers and the LP absorbs the inventory on the way down. e/acc showed 109.304 buy vs 90.695
sell *transactions* while price fell 67% → small-ticket retail dip-buying against larger distribution. The
fee number is real; the IL that comes with it is what kills the cycle.

**Rule: fee/TVL answers "is there volume", not "is this pool safe to LP". Always pair it with the token's
own price trend, holder count and age.** This also plausibly explains why a naive fee/TVL × volume ranking
produces bad live cycles even when the fee numbers look great.

## Cost model (drives the entry threshold)

```
rt   = 0.008 * SOL_price + 0.02 * position_size      # gas ≈ 0.008 SOL, exit slippage 2%
need = 2.5 * rt                                       # 2.5× coverage target
fee_tvl_needed = need / position_size
```

| Position | Round-trip | Needs fee_24h | Needs fee/TVL |
|---|---|---|---|
| $200 | $5,99 | $14,98 | 6,11% |
| $300 | $6,99 | $17,48 | 5,83% |
| $500 | $10,99 | $27,48 | 5,50% |
| $1.000 | $20,99 | $52,48 | 5,25% |

Break-even (1×) ≈ 2,4% fee/TVL. Tokens with buy/sell tax (GP: 3%/3%) push real exit cost to ~5% — raise
the threshold or skip them.

## Entry filter

1. fee/TVL ≥5% **AND** token not down >10% in 24h
2. holders ≥3.000 · token age ≥7 days · pool TVL ≥$60k
3. security re-checked at every entry: mint+freeze revoked, top10 ≤25%, tax 0, LP burned/blackholed
4. position ≤1–2% of pool TVL
5. TP +5% / SL −8% / **exit within 24h**

## Data pull

```python
# 100/page max, browser UA required, sort_by/order params → HTTP 400 (sort locally)
q = urllib.request.Request(f"https://dlmm.datapi.meteora.ag/pools?page={p}&page_size=100",
                           headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'})
```

Nested dicts — unwrap: `tvl` (float), `fees` / `volume` / `fee_tvl_ratio` (dict key `24h`), `apr`, `apy`,
`dynamic_fee_pct`, `name`, `address`, `token_x`/`token_y` ({address, symbol, holders, market_cap, price}).

> ⚠️ **NEVER read fee/TVL from `fee_tvl_ratio.24h` — it is a PERCENT value, not a ratio**
> (`0.238` means 0.238%, not 23.8%). Using it raw inflates every fee/TVL by 100× and makes
> every pool look like it clears the coverage gate. Compute it locally:
> `fee_tvl = fees["24h"] / tvl`. The engine does exactly this
> (`flowmetrix-ai-agent/src/services/meteora.ts:132-139`). Any fee/TVL figure above ~25%/day
> in an old table is almost certainly this bug — recompute before trusting it.

Enrich each candidate token with:
- `https://dlmm.datapi.meteora.ag/pools/<pool_address>` → token addresses in the pool
- `https://api.dexscreener.com/latest/dex/tokens/<token>` → mcap, liquidity, vol 24h, 1h/6h/24h change,
  `pairCreatedAt` (age)
- `gmgn-cli token security --chain sol --address <token>` → `top_10_holder_rate`, mint/freeze renounced,
  `buy_tax`/`sell_tax`, LP lock/burn

Print the rejects with their numbers — the rejects are the evidence that the filter earns its keep.

## Meteora pools-page "Filter by" panel → engine gate mapping (1 Oct 2026)

The app UI exposes fewer knobs than the engine gate. Map them like this:

| UI field | Set to | Note |
|---|---|---|
| Fee/TVL min–max | 5% – 25% | 25% = `MAX_FEE_TVL_RATIO` (the anti-trap upper bound); real floor at $300 is 5,79% |
| Fee/Active TVL min | 2,4% (= 1× break-even); 5% if strict | |
| Bin Step min–max | leave blank | bin step sets fee-per-swap vs grid width, not profitability; filter here drops good pools |
| DLMM Fee Collection Mode | default or Quote | Quote pays fees in SOL/USDC, no base-token bag to sell |
| DAMM V2 (all) | leave unchecked | the engine scans DLMM only; Fee Scheduler pools have time-decaying fees that invalidate fee/TVL |

UI cannot filter: token 24h change, holder count, pool age, security, so always run the per-pool entry filter
(section "Entry filter" above) after the UI screen.

Runnable screen: `~/.hermes/scripts/lp_screen_meteora.py --position 300 --top 20 --json out.json`
(pages datapi until a page has no pool in the $50–500k band; enriches top N via DexScreener; flags
token-24h / holders / coverage failures and prints the reject histogram as evidence).

## Status

The automated screen for the FlowMetrix engine was still being assembled when the engine was paused on
22 Sep 2026 (see the `flowmetrix-ops` skill). The criteria above are the validated manual method; treat the
automation as unbuilt until someone actually runs it end to end.
