# Free data sources for platform DD (no API keys)

Verified 2026-09-16 from the Hermes server (curl + python3, no browser, no keys).

## 1. DefiLlama protocol API — TVL, per-chain, hacks, raises, mcap

```bash
curl -s "https://api.llama.fi/protocol/<slug>" -o p.json
python3 - <<'EOF'
import json; d=json.load(open('/tmp/p.json'))
print('name',d.get('name'),'cat',d.get('category'),'chains',d.get('chains'))
print('current',d.get('currentChainTvls'))          # per-chain TVL — check the user's chain!
tv=d.get('tvl') or []                                # [{date,totalLiquidityUSD}]
print([(x['date'], round(x['totalLiquidityUSD'])) for x in tv[-3:]])
print('hacks',[(h.get('date'),h.get('amount')) for h in (d.get('hacks') or [])])
print('mcap',d.get('mcap'))
EOF
```

- Slug = last path segment of `defillama.com/protocol/<slug>`; product sub-protocols have their own
  slug (e.g. `krystal`, `krystal-auto-farm-vault`, `krystal-community-vault`).
- `hacks == []` = no recorded exploit **in DefiLlama's dataset** (say it that way).
- Fundraising / audit metadata is inconsistent here — `web_extract` on
  `defillama.com/protocol/<slug>` gives the HTML panel (Total Raised, investors, Income Statement)
  when the JSON fields come back empty. Do both.
- Parent vs product TVL: sum the product slugs, don't trust the parent alone. A *manager*-layer
  protocol's TVL only counts its own vault contracts, **not** positions users manage directly.

## 2. Blockscout v2 — keyless multichain wallet read

Host pattern: `https://<host>.blockscout.com/api/v2/...` — **host ≠ DefiLlama chain name**
(`eth.blockscout.com`, not `ethereum.blockscout.com`, which is a 404 — re-verified 2026-09-24).

| Host | Status 2026-09 |
|---|---|
| `base.blockscout.com` | OK |
| `eth.blockscout.com` | OK |
| `arbitrum.blockscout.com` | OK |
| `polygon.blockscout.com` | OK |
| `optimism.blockscout.com`, `gnosis.blockscout.com` | 301 (redirect; follow with `-L`) |
| `bsc|ronin|hyperevm|berachain.blockscout.com` | 404 — no instance, use another route |

```bash
A=0x<addr>
curl -s "https://base.blockscout.com/api/v2/addresses/$A"                  # native balance, rate, flags
curl -s "https://base.blockscout.com/api/v2/addresses/$A/token-balances"    # ALL balances (see note)
curl -s "https://base.blockscout.com/api/v2/addresses/$A/token-transfers?type=ERC-20"
curl -s "https://base.blockscout.com/api/v2/addresses/$A/counters"
```

Reading the output:

- `coin_balance` is wei/1e18; `exchange_rate` is USD per native token → value it in code.
- `/token-balances` items are `{"token": {...}, "value": "<raw int>"}` and the token's address field
  is **`address_hash`** (there is no `address` key — a `t["token"]["address"]` read raises KeyError).
  The same object carries `exchange_rate`, `decimals`, `reputation` (spam/scam flag) and
  `holders_count`, so most tokens can be valued without any price API.
- Re-checked 2026-09-24: `/token-balances` returned **2,172 items** for one whale wallet, not 50 —
  the old "newest 50 only" claim is wrong. Cap your *valuation* calls instead (40 addrs per
  DefiLlama-coins request, 30 per DexScreener, 50 per Jupiter), not the read.
- `/counters` returning `transactions_count: 0` while token transfers exist means the address is
  indexed for transfers only — not that it was never used.
- Fingerprinting: dozens of "Claim: …", "t.me/s/claim…", "visit to claim", fake `USDC`/`USDT`
  symbols on random contracts ⇒ airdrop-farmer wallet, not an LP account with size. Say what the
  *real* tokens sum to (that is the number worth quoting).
- Blockscout's `total.value` in transfer items can be null/short for some tokens — parse
  defensively (`int(v or 0)`), don't trust a 0 you got from a bad cast.

## 3. Protocol docs — GitBook (very common for DeFi docs)

- `GET <docs-host>/llms.txt` → complete page index (also `/<page>.md` for clean markdown of any page).
- `GET <page-url>.md?ask=<natural-language question>` → GitBook answers with excerpts + sources.
  Useful when the fact is spread across pages.
- Convert to `/tmp` + python, or `web_extract` (markdown route reads well). Fee pages are tables —
  copy them into the report verbatim.
- Apps' own APIs (`api.<product>.app/...`) often sit behind a Cloudflare JS challenge and answer
  plain curl with `403` + `<title>Just a moment...</title>`. That is a **coverage gap, not a
  verdict**: record the gap and pivot to DefiLlama + Blockscout + docs.

## 4. X/Twitter post text without login

`curl -sL "https://cdn.syndication.twimg.com/tweet-result?id=<status_id>&lang=en&token=a" -H "User-Agent: Mozilla/5.0"`
→ `.text`, `.created_at`, `.favorite_count`, `.conversation_count`, `.user`, `.mediaDetails[].media_url_https`,
`.quoted_tweet`, and **`.entities.urls[].expanded_url`** (resolves the `t.co` link — this is how you
learn the platform and spot `?r=<handle>` referral params). Full ladder in the `social-post-lookup`
skill (its X/Twitter reference file).

## 5. Media transcription

`pbs.twimg.com/media/<file>?name=large` is public CDN — download, then `vision_analyze` with
"transkrip apa adanya: semua angka, nama pool, URL yang kelihatan". Ask for the address-bar URL too:
promo screenshots have leaked `*-dev.` hostnames before.
