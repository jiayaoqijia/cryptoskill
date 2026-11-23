# Nest Exchange (HyperEVM) LP — worked case, 27 Sep 2026

Question asked: *"deepdive nest exchange, tempat buat nge LP di jaringan hyperliquid — apakah wise untuk nyoba partisipasi disana modal $200–300?"*
Sources used: `docs.usenest.xyz/llms.txt` + 12 `.md` pages, live `app.usenest.xyz/api/blaze/liquidity-pools`, DefiLlama API (`nest`, `nest-cl`, `nest-amm`), CoinGecko (`nest-2`, `hyperliquid`), NestBoard, Algebra case study, SolBotRank.

## What the product is
MetaDEX (ve(3,3)) on **HyperEVM** (not HyperCore), live 15 Nov 2025, single chain, no published legal entity.
Three pool types: Classic (full-range), CLAMM (own range), Amplifi/ICHI (automated vault, extra contract risk).

## The decisive mechanic
Docs 4.1/4.5: *"On Nest, LP rewards come from emissions, not trading fees… LPs do not earn trading fees."*
100% of swap fees → **veNEST lockers**. LP reward = **NEST emissions**, vote-directed per epoch:
*"No votes = no emissions"* (an unvoted pool pays LPs **zero** that epoch, not less).

Emission schedule (docs 2.3): epoch 1 = 20M NEST/week, **+1.5%/epoch** through epoch 12 (peak ~23.4M),
then **−1%/epoch** (maturation). Epoch = 1 week, settles Thursday 00:00 UTC. LP position itself has **no lockup**
(withdraw anytime, needs HYPE for gas — docs 6.5); only veNEST locks.

## Numbers pulled live (27 Sep 2026)
| Metric | Value |
|---|---|
| Total TVL across 70 pools (own API) | $27,223,769 |
| DefiLlama `nest-cl` / `nest-amm` | $26.43M / $0.40M, 100% Hyperliquid L1 |
| CL TVL trend 30d | $17.15M → $26.43M (+54%) |
| Top pool WHYPE/USDC | TVL $10,511,388 (38.6% of TVL), 24h vol $4,162,059, fee 0.102% |
| Top-pool `curEpochEmissionRewardsUSD` | $126,703 → **62.7% emission APY** at spot NEST price |
| Sum of emissions, all pools, one epoch | $317,435 (36 of 70 pools get emissions; 34 get zero) |
| DefiLlama 30d fees (nest-cl) | $570,801 — **all to veNEST, none to LPs** |
| NEST | $0.0197 · mcap $5.08M · FDV $36.9M · circ 257.2M (total 1.87B) · 24h vol $185,550 · ATH $0.0438 → **−55%** |
| HYPE | $93.41, +15.5% 30d, ±20% swings inside a week |

### $250 scenario (computed, not quoted)
- Share of top pool = 0.00238% → emissions **$3.01/week ≈ $156.70/yr = 62.7% APY**, paid in NEST.
- NEST was +66%/7d and +97%/14d at review time → that APY is pump-inflated.
  Re-priced at the 30d average (~$0.011) it is **~35%**; at the mid-August level ($0.005) **~16%**. Always restate APR at the 30d-average price.
- IL, 50/50 pair, in dollars: ±20% divergence ≈ $1.04–1.55; ±50% ≈ $5–14.30 (i.e. **IL is not the risk at this size**).
- Exit: $250 = 0.0024% of a $10.5M pool → no exit-liquidity problem; HyperEVM gas is cents.

### Dilution check (the headline)
- Emissions ≈ $16.5M/yr vs **$5.08M mcap** → ~325% of mcap per year.
- One epoch of emissions ($317K) ≈ **12 days** of NEST's entire 24h volume ($185K/day).
- ⇒ Realising the "APY" requires selling printed NEST into thin liquidity; price has to hold for the APR to be real.

## Safety record
- Nest audits: **BailSec** (VE Core; report on GitHub) + **Hats Finance** competition on Thena/Fenix-derived legacy code (Blast era). **No tier-1 audit.** DefiLlama `hacks` empty (no recorded exploit).
- Governance: **3-of-5 multisig** for core functions + separate treasury multisig (docs 7.2).
- Chain-level context (distinct from Nest's own record): HyperEVM **Purrlend $1.5M, 25 Apr 2026** via 2/3 admin multisig; Hyperdrive **$21M** private-key exploit Oct 2025.
- Name collision: several unrelated "Nest" projects (Nest Protocol, Nest Credit on Plume, Nest vaults). Nest Exchange token = `0x07c57e32a3c29d5659bda1d3efc2e7bf004e3035` on HyperEVM — take addresses from the docs *Contracts* page only.

## Verdict given
- As a **yield destination for $200–300: 4/10** — not because it is fake (data is real and live) but because LPs are paid in a micro-cap token inflating ~6% of circulating supply **per week** while the fee yield they would normally earn is 0.
- As an **experiment: 6.5/10** — real tooling, growing TVL, easy exit, bounded max loss at this size.
- If the user actually wants Hyperliquid yield: HLP vault (market-making, drawdown risk) or HYPE staking/lending (Kinetiq kHYPE, HyperLend) — not an emission farm.

## Test plan handed over
$250 = ~$125 USDC + ~$125 HYPE (keep HYPE for gas) → WHYPE/USDC only (deepest pool; avoid the 300–500% APR pools that are thin + dump-prone) → 3–4 epochs → benchmark against simply **holding** the same 50/50 basket → claim and immediately sell emissions each epoch, logging NEST price at emission vs at sale → withdraw $50 in week 1 to prove the exit path → exit if it loses to hold two epochs running.
