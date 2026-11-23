# CA handoff + round-trip fee math (pair-paired launchpad coins)

Verified end-to-end 30 Sep 2026 on a Solana pair-paired launchpad coin (ticker `GP`). Companion to
`narrative-scan-multichain.md` (§3a has the endpoint list). Load when the user asks for the **contract
address** of a pick, or before publishing any entry/level plan.

## 1. "Mana CA-nya?" → hand over the whole identity block, not the mint

Every field has an exact JSON path in `GET https://www.stonkfun.xyz/api/public/v1/tokens/<MINT>`
(keyless). Read, then re-verify against GMGN `token info` before publishing:

| Ask | Path | Example (GP) |
|---|---|---|
| CA / mint | `data.token.mint` | `HTmQz7My…LP7YgUQ` |
| pool | `data.token.pool` | `FE1kGMg4…3fco` |
| quote asset (the narrative) | `data.token.quote.mint` + `.symbol` / `.name` / `.category` | `Xsv9hRk1…mwtD3re` = GLDX / GOLD / xStock |
| creator wallet | `data.launch.creator` | `5b1G6DKJ…tmPyEg` |
| tax | `data.token.transferFee.bps` | `300` = 3% |
| fee currency | `data.token.quoteOnlyFees` | `true` = tax paid in the quote asset |
| lifecycle | `data.token.status`, `graduatedAt`, `createdAt` | graduated, 8 Sep 2026 |
| platform-side market | `market.marketCapUsd`, `peakMarketCapUsd`, `priceChange24h`, `volume24hUsd`, `liquidityUsd` | $8,8M vs peak $32,5M (−73%), +16,9%/24h |

**Symbol match is not verification — read `name` too.** Ticker `GP` with `name = "RuneScape Gold"` and
`quote.symbol = GLDX` is a gold-meme paired against tokenized gold. Had we trusted the ticker, the
write-up would have described a different token. Also give the pool address so the user can route the
swap in the platform UI when Jupiter has no direct route (quote-asset pools need the quote asset).

## 2. Round-trip tax — state it next to the entry zone

```
round-trip tax = 2 × transferFee.bps / 10000      # in AND out
break-even move = round-trip tax / (1 − round-trip tax)   # ≈ 2× the rate for small rates
```

`100 bps (1%)` → >+2,0% BEP. `300 bps (3%)` → **>+6,4% BEP** before slippage. On an $8,8M mcap with
$319–517k liquidity that is a material drag → frame as **swing, not scalp**, and do not chase green
candles inside the BEP band.

- **GMGN `token info` does not carry the fee at all.** The launchpad record is the only source; a coin
  can look clean on GMGN and still charge 3%. A prior working summary of this same coin said "1–3%"
  and was wrong for it — re-read the field, never reuse a remembered rate.
- Liquidity disagrees by source too: platform `market.liquidityUsd` $319k vs GMGN `liquidity` $517k.
  Quote which source you used (same discipline as the volume discrepancy in Pitfall 2).

## 3. Fast momentum read (before recommending an entry)

`gmgn-cli token info` returns `price` as a **nested dict**:

```
price.price · price_1m · price_5m · price_1h · price_6h · price_24h
buys_1m/5m/1h/6h/24h · sells_* · volume_1m/5m/1h/6h/24h · swaps_24h
```

Compare `price` against `price_1h` / `price_6h`: a coin up double digits in the last hour is mid-pump —
say **"jangan kejar"** and give a pullback zone plus an invalidation level instead of an at-market entry.
This is how a "top pick" avoids becoming a chase-the-candle recommendation.

## 4. Sizing consequence

Thin liquidity + 300 bps tax ⇒ size down and say why in one line ("liq cuma $319k + tax 3% → size
kecil"). A dev still holding (`creator_token_status`) is a flag to name explicitly, not to average into.
