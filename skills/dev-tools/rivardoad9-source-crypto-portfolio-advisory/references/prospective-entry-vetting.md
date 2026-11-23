# Vetting a prospective entry ("<token X> worth it masuk nggak?")

Companion to the five holding checks in SKILL.md. Those answer "is this thesis sound"; these gates
answer "should I enter *now*, at *this* price". Worked end-to-end 30 Sep 2026 on `NOSH` (Robinhood
Chain) vs `PAID` (Solana) — the session that asked "nosh worth it untuk kita masuk ga? kalo
dibanding paid apakah narasinya seksi".

## Gate 1 — Does the token capture anything? (read the project's own docs)

Fetch `link.website` from `gmgn-cli token info --raw`, then the landing page **and `/docs`**. The
question is not "is the product real" but **"does the token have a documented claim on the money the
product makes"**.

- Nosh: docs described creator fees routed 80% to a per-collection NFT vault / 20% treasury, split
  hardcoded in an ownerless EIP-1167 clone with no withdraw function, NFTs raffled to holders via
  drand/OpenVRF. Mechanism real (39 coins, 77 collections, 1,867 NFTs swept) — **and `$NOSH` is not
  mentioned anywhere in it.** Fee claim: none ⇒ no fundamental floor, attention-only asset.
- PAID: creator fees routed to the X account a coin is launched for. Rail status: **paused**
  ("X Money payouts are paused until further notice" on its own homepage) ⇒ thesis currently broken.

Report both halves: *"produknya jalan, tapi tokennya nggak dapet apa-apa"*.

## Gate 2 — Cohort exit ratio (the timing gate that outranked a 85,9/100 DD score)

```bash
gmgn-cli token holders --chain <chain> --address <CA> --tag smart_degen --limit 15 --raw
gmgn-cli token holders --chain <chain> --address <CA> --tag renowned   --limit 15 --raw
```

```python
rows = d.get('data', d); rows = rows.get('list') or rows.get('holders') or []
lifetime = sum(float(h['total_cost'] or 0) for h in rows)   # NOT 'cost'
pnl      = sum(float(h['profit'] or 0) for h in rows)
held     = sum(float(h['amount_cur'] or 0) for h in rows)
exited   = [h for h in rows if float(h['amount_cur'] or 0) == 0]
biggest  = sorted(((float(h['profit'] or 0), h['address'], h['last_active_timestamp'])
                   for h in exited), reverse=True)[:4]
```

`cost` = cost basis of the **current bag only** (0 once the wallet exited); `total_cost` = lifetime
spend. Summing `cost or total_cost` mixed the two denominators and returned **$560** against a true
lifetime **$57,420**. `last_active_timestamp` is Unix seconds — convert before saying "they left
today".

NOSH result: smart money 15 wallets / $57,420 lifetime → +$5,344, **14 exited, 1 holding 0.02%**;
KOL 11 wallets / $71,706 → +$67,803 (one wallet alone +$60,759), **7 exited, 4 holding 0.48%**, with
the bulk of exits inside the previous 12 hours. That, not the DD score, decided the verdict.

## Gate 3 — Trend and flow (read before quoting a price)

From `token info --raw`: `price_1m/5m/1h/6h/24h`, `volume_1h/6h/24h`, `buy_volume_24h` vs
`sell_volume_24h`, `swaps_*`; from `stat`: `holder_count`, `top_entrapment_trader_percentage`,
`bot_degen_rate`, `top_10_holder_rate`, `wallet_tags_stat`, `dev.creator_token_status`.

NOSH at the ask: $0,003475 · −5,5%/1h · −7,3%/6h · 6h volume $125k vs $2,94M/24h · net sells
$1,52M vs $1,41M · 55,4% entrapment volume · 57,2% bot-degen · −36% from ATH. Distribution,
whatever yesterday's score said.

## Gate 4 — Sibling comparison ("narasinya seksi nggak")

Same brand family makes the narrative measurable. NOSH (`usenosh.app`) vs PAID (`usepaid.app`):

| | NOSH | PAID |
|---|---|---|
| mcap / liquidity | $3,47M / $228k | $10,31M / $930k |
| holders / smart / KOL / whales | 3.793 / 138 / 11 / 3 | 42.439 / 582 / 87 / 289 |
| volume 24h | $2,94M | $9,31M |
| from ATH | −36% | −80% |
| product rail | live (1.867 NFTs swept) | **paused** |

Report both axes separately: the sexier narrative can belong to the sibling whose core rail is dead,
and the one with the working product can have a token that captures nothing. Answering "narasi mana
yang seksi" without also saying "dan itu nggak bikin tokennya punya lantai" invites buying the wrong
one.

## Gate 5 — Access friction

Chain, bridge requirement, and whether the monitored lanes can watch or stop the position. Robinhood
Chain needs a bridge and sits outside the Solana-based guard lanes ⇒ the entry would be manual, with
a manual invalidation level. Say it out loud; for small capital it changes the answer.

## Native-token price discipline

Never infer the native price from one trade's USD total ÷ that tx's native delta — a single tx can
cover only part of the same minute's trades. One such inference yielded $226/SOL against a true $119
and produced a reported "$57" for a 0,2505 SOL outflow that was really ~$30. Price it from an
independent source (CoinGecko `simple/price`, DefiLlama coins, Binance), and when a wrong figure has
already gone out, correct it explicitly and name the mistake.

## Where the money left (keyless — no API key needed)

```python
EPS = ["https://api.mainnet-beta.solana.com", "https://solana.public-rpc.com",
       "https://free.rpcpool.com"]     # rotate: the first may 429/403 under a batch
sigs = rpc("getSignaturesForAddress", [W, {"limit": 20}])["result"]
for s in sigs:
    tx = rpc("getTransaction", [s["signature"],
             {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])["result"]
    keys = [k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"]]
    if W not in keys: continue
    i = keys.index(W); pre, post = tx["meta"]["preBalances"], tx["meta"]["postBalances"]
    d = (post[i] - pre[i]) / 1e9
    if d < -0.1:                        # net outflow from W
        print(s["signature"][:16], d,
              [(k, (post[j] - pre[j]) / 1e9) for j, k in enumerate(keys)
               if j != i and (post[j] - pre[j]) > 0.05])     # the recipient(s)
```

## Reply shape this user expects

Verdict in line one (`belum worth masuk` / `masuk kecil aja`), evidence under short headers, then
"worth it when …" (what would change the answer), ticket-lottery sizing with an explicit invalidation
level only as a forced fallback, and the closing line `bacaan data, bukan saran investasi`.
