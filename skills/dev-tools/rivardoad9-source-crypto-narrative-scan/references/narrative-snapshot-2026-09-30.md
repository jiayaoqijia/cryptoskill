# Worked example / baseline — "tokenized-stock pair" meta (30 Sep 2026)

Baseline snapshot so a future scan can answer "is this meta still alive, and is it the same one?".
All figures as read on 30 Sep 2026. Re-derive before quoting; do not treat as current.

## The narrative that won

**"Saham masuk on-chain"** — tokenized equities, and memecoins whose *quote/pair asset is a stock*.
Confirmed across four venues, which is what makes it a meta and not a launchpad feature:

| Venue | Evidence |
|---|---|
| Robinhood Chain (chainId 4663) | 99 stock/ETF tokens: combined MC $133.6M, **24h volume $589.1M**, liquidity $119.7M, **1,065,428 holders**; DEX record $1.33B/day (30 Aug), TVL $728M; tokenized stocks $150M TVL (9 Sep) |
| Solana — StonkFun | 152,435 coins launched; >$1.2B cumulative volume; platform token STONK $216M MC, 17–19% supply burned |
| BSC (flap_stocks / geniusfun) | QQQB $57.7M, NVDAB $34M, BNCB $28.6M, FXIon $21M, GSTOCK $17M |
| Copycat signal | pump.fun switched on stock pairs 9 Sep 2026 |
| Fundamental catalyst | NVDA Q2 (30 Aug): revenue $96.22B, +106% YoY, Q3 guide ~$108B |

## Ranked tokens as scored that day

**#1 SI — "Super Inu"** `DEW9dSN6QpWyNthphCpMmAbZP1Q4cEKR9xQXAri98WDP` (Solana, LaunchLab/StonkFun)
- **Pair `NVDAX` (tokenized NVIDIA), `mode: reward`, `transferFee 100 bps` paid to holders in NVDAX,
  `flywheel.active: true`** — i.e. the pair/reward config *is* the narrative
- MC $50.0M (peak $55.6M) · $0.0500 · **+113% 24h** · graduated 21 Sep (9 days old)
- Volume: **$18.5M platform-reported vs $56.9M GMGN aggregate** (top of Solana trending)
- 49,842 holders · 481 smart wallets · 61 KOL · top-10 12.36% · bot 56% · entrapment 23.9%
- Same mint the user had already flipped profitably ($17.83 → $36.55)

**#2 STONK** `6GmAFSYs4gk3FDao5FzzySQpPZaWsa4rUJHacpMpUNgx` (platform token, pair `SPYX`)
- MC $216.2M · $0.2669 · 103,714 holders · **1000 smart wallets (capped)** · 151 KOL
- ~19% of 1B supply burned (supply ≈ 810M derived from price×MC); 60% of revenue → buyback+burn
- Peak $0.4054 → −34%; entrapment 60.9%; dev `creator_hold`; X @LaunchOnSF; created 23 Jul 2026

**#3 PONS** `0x39dbed3a2bd333467115de45665cc57f813c4571` (Robinhood Chain, launchpad `pons`)
- MC $562.4M · $0.5624 · 101,288 holders · 554 smart · 171 KOL · $40.2M vol/24h · liq $4.45M
- Robinhood-Chain-native launchpad; largest distribution but late-stage + needs a bridge

Runners-up noted: ZCAT (pair ZEC, $57M MC, entrapment 69.7%, dev `creator_hold`), the underlying
stock tokens themselves (NVDA/SPY/META/cbBTC on Robinhood Chain), and BSC clones.
Explicitly excluded as lottery: SOON +73,988%/1h, VRAX +830×, GM +23,077%.

## Risks that had to be reported

- **StonkFun fee controversy** (Bitquery, window 23 Aug–22 Sep): reward wallet sold $56.3M in 30 days
  and paid holders back $56.2M, but **$1.41M went to wallets tied to the platform**; claimed $2.09M
  buyback was $1.23M (58% of the day's revenue). On some coins tax took >50% of supply
  (BUDDY 69%, ZCAT 61%).
- Reward-coin tax drag 1–3% per transfer on every trade.
- Bot/entrapment share high across the meta (SI bot 56%; STONK 60.9%; ZCAT 69.7%).
- Commoditization: pump.fun + BSC clones ⇒ mechanic is no longer a differentiator.
- Not early: SI already +347% off its low; STONK −34% from peak; PONS $562M.

## Watch-metrics used to verify "meta still alive" next time

1. Robinhood Chain 99-stock-token daily volume staying >~$400M (was $589M).
2. STONK burn/buyback continuing on-chain (supply still falling from ~810M).
3. New pair categories still launching (OPENAI, CARDS, NFLX, DJT, BP) — category expansion = meta
   alive; category stagnation + falling new-launch count = meta cooling.
4. Whether the copycats take share (BSC/Binance-version volume vs Solana's).

## Sources

GMGN (`market hot-searches` / `trending` / `signal`, `token info`, `market kline`), StonkFun public
API, hoodscan.co/stocks + GateNews + CMC-AI + cryptorank news snippets, Bitquery investigation
("Is StonkFun Dumping on Holders?"), blocmates StonkFun explainer. Baca-an rule-based, not advice.
