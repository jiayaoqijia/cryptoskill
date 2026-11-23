# Narrative scan — command recipes, keyless sources, parse snippets

Validated end-to-end 30 Sep 2026 (asked: "cari token dengan narasi terseksi saat ini + reasoning").
Authoritative CLI field/enum reference stays in the `gmgn-market` skill — this file is the *scan
recipe* built on top of it.

## 0. Discipline

- `gmgn-cli config --check` first; exit 0 = proceed.
- Batch 5–7 calls in ONE script with `sleep 5` between them, writing each result to `/tmp/<name>.json`.
  Much safer than many short tool calls (each of which spends a fresh rate-limit burst).
- **Failure signature: exit code 0 + 0 bytes on stdout.** The real error is on stderr. On
  `RATE_LIMIT_BANNED` stop and wait the announced reset — retries extend the ban.
- Redirect stderr per call (`2>>/tmp/err.txt`) so one bad call does not poison the batch; check
  `wc -c` on each output file.

## 1. Attention sweep (all chains, one call)

```bash
gmgn-cli market hot-searches --chain sol --chain bsc --chain base --chain eth --chain robinhood \
  --interval 24h --limit 50 --raw > /tmp/hs.json
```

Parse (the trap: `data` is a **list of per-chain blocks**, so `json.load(f).get('data')` on the
top-level list raises `'list' object has no attribute 'get'`):

```python
import json
d = json.load(open('/tmp/hs.json'))
blocks = d if isinstance(d, list) else d.get('data')
for blk in blocks:                      # blocks may also be nested lists — guard with isinstance
    if not isinstance(blk, dict): continue
    for t in (blk.get('tokens') or [])[:12]:
        print(blk['chain'], t['rank'], t['symbol'], t['market_cap'], t['volume'], t['visiting_count'])
```

Read: `visiting_count` = search heat, `market_cap`, `volume`, `holder_count`,
`price_change_percent` (interval change). Duplicate tickers at different MCs = symbol spam.

## 2. Money-flow sweep

```bash
for c in sol bsc base robinhood; do
  gmgn-cli market trending --chain $c --interval 24h --order-by volume --limit 30 --raw > /tmp/tr_$c.json
  sleep 5
done
gmgn-cli market trending --chain sol --interval 1h --order-by smart_degen_count --limit 40 --raw \
  > /tmp/tr_sm.json; sleep 5
gmgn-cli market trending --chain sol --interval 1h --order-by change1h --direction desc \
  --min-volume 200000 --min-marketcap 1000000 --limit 20 --raw > /tmp/g_sol.json; sleep 5
gmgn-cli market signal --chain sol --groups '[{"signal_type":[12]},{"signal_type":[20]}]' \
  --raw > /tmp/sig.json
```

- `--order-by` valid names: `default, swaps, marketcap, history_highest_market_cap, liquidity,
  volume, holder_count, smart_degen_count, renowned_count, gas_fee, price, change1m, change5m,
  change1h, creation_timestamp`. **`change` is invalid → HTTP 400**, and `change1h` requires
  `--direction desc` + min-volume/min-marketcap floors or dust fills the list.
- Signal feed items: `token_address, signal_type, trigger_at, trigger_mc, market_cap, ath,
  first_trigger_mc, signal_times, signal_times_by_type, cur_data, data`. There is **no symbol field** —
  join addresses against the trending files you already saved (build `addr → symbol` map from
  `data.rank[].address/symbol`).
- Type 12 = smart-money buy, 20 = KOL buy. Grouping many like this is normal: 95 events across ~80
  micro caps. "No dominant accumulator" is a legitimate, reportable conclusion.

## 3. Narrative identity — keyless ground truth

### 3a. Launchpad public API (the highest-signal source for *what a coin is*)

StonkFun (Solana pair-paired launchpad) — **no API key, no signup**:

```bash
curl -s "https://www.stonkfun.xyz/api/public/v1/tokens?sort=volume&pageSize=15"   # leaderboard
curl -s "https://www.stonkfun.xyz/api/public/v1/tokens?sort=newest&pageSize=60"    # fresh launches
curl -s "https://www.stonkfun.xyz/api/public/v1/tokens?status=aboutToGraduate&sort=volume&pageSize=10"
curl -s "https://www.stonkfun.xyz/api/public/v1/tokens/<MINT>"                     # one coin, full record
curl -s "https://www.stonkfun.xyz/api/public/v1/pairs?launchable=true"             # quote assets available
```

Fields that answer "what is this coin actually claiming?" (from `/tokens/<MINT>` → `data.token`):

| Field | Meaning |
|---|---|
| `quote.symbol` / `quote.category` | **the pair asset = the narrative** (`NVDAX`, `SPYX`, `OPENAI`, `ZEC`, `CARDS`, `SOL`, `DJT`, `BP`) |
| `mode` | `standard` (1% pool fee, creator share) vs `reward` (Token-2022 transfer tax paid to holders in the quote asset) |
| `transferFee.bps` | 100 = 1%, 300 = 3% tax on every transfer |
| `flywheel.active` | token is in the platform's buyback/burn leaderboard |
| `market.peakMarketCapUsd` / `priceChange24h` / `volume24hUsd` / `liquidityUsd` | platform-side market record |
| `graduatedAt` / `createdAt` / `status` / `graduationProgress` | age and lifecycle stage |
| `creator`, `links` | creator wallet and socials (often empty — check GMGN metadata too) |

`pagination.total` on `/tokens` gives platform-wide launch count (152,435 on 30 Sep 2026), which is
how you quote "how big is this launchpad" without a news article.

### 3b. Token metadata + wallet stats

```bash
gmgn-cli token info --chain <chain> --address <addr> --raw > /tmp/t.json
```

Pulls: `launchpad`, `link.website` (this is where an odd narrative leaks — e.g. a Solana coin whose
metadata pointed at a Truth Social post), `twitter_username`, `dev.creator_token_status`,
`wallet_tags_stat.{smart_wallets,renowned_wallets,sniper_wallets,bundler_wallets}`,
`stat.{holder_count,top_10_holder_rate,top_entrapment_trader_percentage,bot_degen_rate}`.
`market_cap` is absent → derive `price × total_supply`.

### 3c. Chain-level theme totals

- Robinhood Chain (chainId 4663): `robinscan.io` (explorer), `hoodscan.co/stocks` (all tokenized
  stock/ETF tokens + "the meme coins built on each"). NOTE: hoodscan is JS-rendered — `web_extract`
  returns headers only; take its totals from the search-result snippet or drive a real browser.
- News/search validation: CMC-AI "what is X" pages, Bitquery investigations, blocmates/CoinGecko
  explainers, DefiLlama for TVL/volume claims.

## 4. Report skeleton

```
VERDICT: <the narrative> — <enter? yes/no> in the first line
EVIDENCE: chain/protocol totals (volume, holders, TVL, catalyst)
#1 <TOKEN> (<address>) — MC, price, 24h, vol (platform vs aggregate), holders, smart/KOL,
   top10, bot/entrapment, age, "+X% from low / −Y% from ATH", its specific claim
#2 <TOKEN> — …
#3 <TOKEN> — …
REASONING: why money is behind it (value accrual / distribution / catalyst); say when there is none
RISKS: tax drag, bot & entrapment %, commoditization, platform controversy
PLAN (scenario, not advice): entry zone / invalidation / target / what would kill the thesis
"bacaan rule-based, bukan saran investasi."
Watch next: <the 2–3 metrics that would confirm or break the thesis>
```

Also save the same content as `~/obsidian-vault/<Topic> (DD Mon YYYY).md` and mention the filename —
this user keeps a vault and the dated note is how a later scan diffs "is the meta still alive?".
