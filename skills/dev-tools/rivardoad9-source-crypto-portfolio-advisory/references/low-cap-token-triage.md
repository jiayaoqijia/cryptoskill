# Low-cap token triage (mcap $5–80M)

Built 27 Sep 2026, when the user asked for a standing "low caps" segment in the daily radar (their
reference example is PAID: Solana, launched 15 Sep 2026, mint/freeze revoked, LP burned, tax 0%).
Low caps below ~$5M are lottery tickets, not portfolio: park them in the risk sleeve or reject them.

## 1. Screen (GMGN CLI)

```bash
# candidates — --interval is REQUIRED or the CLI errors out
gmgn-cli market trending --chain sol --interval 24h --order-by volume --raw \
  --min-marketcap 5000000 --max-marketcap 80000000 \
  --min-holder-count 5000 --min-liquidity 500000 --filter renounced frozen --limit 40
#   output shape: {"data":{"rank":[...]}}   (trenches instead returns {"completed":[],"near_completion":[],"new_creation":[]})

gmgn-cli token security --chain sol --address <addr> --raw   # for the top 3 only
#   → top_10_holder_rate, renounced_mint, renounced_freeze_account, buy_tax/sell_tax,
#     burn_status, honeypot, flags

gmgn-cli market trenches --chain sol --type completed --raw \
  --sort-by smart_degen_count --direction desc --min-volume-24h 40000 --min-swaps-24h 400
#   new launches: rank by smart_degen_count, but expect mcap $3k–$170k and rug_ratio up to 1.00
```

## 2. Identity pass (this is what makes the segment actionable)

A row of numbers is not a thesis. Take the `twitter_handle` from the screen and search for the project
before writing anything. Output is always one honest line of `identitas:`.

- **TEXTIT** (mcap ~$21M, top10 5,4%, 38 days, rug 0,12) — searched pump.fun + DexScreener: a pump.fun
  token with no product, no narrative, no site → `"proyeknya nggak jelas"`. Write exactly that. It is a
  finding, not a gap in the work.
- **fone (= ape on fone)** — pump.fun launch 27 Aug 2026, ~990M supply, sources Gate Learn /
  onchaincircus / bitrue → real identity, but a memecoin.
- **Symbol collisions are normal.** NEARKAT is a StonkFun memecoin whose rewards pay in $NEAR — it is not
  KAT on NEAR Protocol. Say which one you mean, and keep the symbol spelling identical in every section
  of a report (one run wrote "NEARPAD/NEARCAT" in one place and "NEARKAT" in another).
- If the only hits are aggregator pages that echo the ticker, say that too — do not upgrade it to a
  "project".

## 3. Read the reward mechanism — it is the thesis or the disqualifier

- **ZCAT (Anonymous Cat)** — StonkFun, 28 days, top10 16,1%, rug 0,03, base of 236 smart holders.
  3% transfer tax buys Zcash (ZEC) and distributes it to holders: a genuine fee flywheel. Cost: ~6%
  round-trip tax, liquidity only 2,3% of mcap. Verdict in practice: interesting, not yet enterable.
- **NEARKAT** — StonkFun, 8k holders, 3% tax paid in $NEAR, +77% in 24h. Momentum real, entry late →
  the next buyer is exit liquidity.
- Contrast with **PAID**: no tax, no flywheel, but 42k holders and the deepest liquidity in the set.
  Distribution structure can outrank a clever mechanism.

## 4. The two ratios that decide whether you can actually exit

| Ratio | Reject | Note |
|---|---|---|
| liquidity ÷ mcap | < ~5% | TEXTIT: liq $555k on $21M (2,6%) with vol ≈25× liq → dump-able, slippage blowout |
| volume24 ÷ liquidity | > ~10× | churn, not depth — frequently an active dump (see the `e/acc` case) |

PAID by comparison: liq $2,4M on $26M mcap (~9%) with 42k holders — the deepest, most exitable name in
the same screen, even while its price bled 30%.

## 5. Confirm with flow before writing "momentum"

Check the smart-money / KOL aggregate for that exact address. A lone KOL buy with no smart-money cluster
is hype, not confirmation — and named-wallet *sells* flip the call (a KOL sold $2,1k of `fone` on the same
day it was up 58%).

## 6. Reject list to print with numbers

top10 > 25% (MASK sat at 52,2%) · rug_ratio ≥ 0,5 · age < 7 days · wash-trading flag · mint or freeze not
revoked · >2% round-trip tax · liquidity < 2% of mcap · no identity after the pass.
Publishing the rejects with their numbers is what makes the screen look real to this user.

## 7. Sizing and verdict vocabulary

Low caps live in the risk sleeve: ≤5% of portfolio (≈$70 of $1,400), never funded by trimming core, never
the reason to skip the core. Verdicts are "belum layak masuk, tunggu <trigger konkret>" or "watch, jangan
masuk buta" — not a buy call. The user clicks; you never execute.
