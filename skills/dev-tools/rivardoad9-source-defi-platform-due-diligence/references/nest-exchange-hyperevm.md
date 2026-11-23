# Nest Exchange (HyperEVM) — LP due diligence, 27 Sep 2026

Asked: "deepdive nest exchange, tempat LP di Hyperliquid — wise gak coba modal $200–300?"
Facts pulled from docs.usenest.xyz (`llms.txt` + `.md` pages), live API `app.usenest.xyz/api/blaze/liquidity-pools`,
DefiLlama (`nest`, `nest-cl`, `nest-amm`), CoinGecko (NEST, HYPE), NestBoard, SolBotRank.

## The one thing that changes the whole verdict

**Nest LPs earn 0% of trading fees.** Docs 4.1 & 4.5: *"On Nest, LP rewards come from emissions, not trading fees…
LPs do not earn trading fees."* 100% of fee value is allocated to veNEST lockers. So an LP's entire return is
NEST emissions — i.e. a token-price bet — and the dashboard "APY" for the top pool (~14.5%) is the **fee** APR
that LPs do *not* receive. Emissions are vote-directed: *"No votes = no emissions"* (a pool can pay LPs exactly
zero in a given epoch, not just less).

## Verified numbers (27 Sep 2026)

| metric | value |
|---|---|
| TVL (70 pools) | $27.22M, 100% on Hyperliquid L1 (HyperEVM), live since 15 Nov 2025 |
| TVL 30d trend | $17.15M → $26.43M |
| Top pool WHYPE/USDC | TVL $10.51M · 24h vol $4.16M · fee tier 0.102% |
| Emissions, top pool | $126.7k/epoch → ~62.7% APR *at current NEST price* |
| Emissions, all pools | $317.4k/epoch; only 36 of 70 pools incentivised |
| NEST | $0.0197 · mcap $5.08M · FDV $36.9M · circ 257M · 24h vol $185k · −55% from ATH |
| Emission schedule | epoch 1 = 20M NEST/wk, +1.5%/epoch to epoch 12, then −1%/epoch forever |

Structural read: one epoch of emissions ($317k) exceeds ~12 days of NEST's daily volume ($185k), and ~257M
circulating supply means roughly **6%/week dilution**. Emission APRs are therefore highly price-dependent —
the same pool is ~35% if NEST reverts to its 30d average and ~16% at its mid-August level.

## Pricing per position size (same coverage rule as Meteora)

$250 in WHYPE/USDC = 0.00238% of the pool → $3.01/week at the current NEST price. IL on a 50/50 pair with one
side moving ±20% ≈ −0.4…−0.6% of position (≈$1–1.5); ±50% ≈ −5.7% (≈$14). For $200–300 the gas and IL are
small in dollars — **the token risk, not the fees, is the whole bet.**

## Risk register

- Contract: audits = **BailSec (VE Core)** + **Hats Finance** (Thena/Fenix-derived, Blast era). No tier-1 audit.
  Governance = **3-of-5 multisig** (docs 7.2). No hacks recorded on DefiLlama.
- Chain: HyperEVM is young — Purrlend lost $1.52M (25 Apr 2026) via a compromised admin multisig; a Hyperdrive
  user lost $21M (Oct 2025) via a leaked private key. Admin-key risk is an ecosystem-level fact, not Nest-specific.
- Name collision: many unrelated "Nest" projects (Nest Protocol, Nest Credit on Plume, Nest vaults). Nest Exchange
  NEST = `0x07c57e32a3c29d5659bda1d3efc2e7bf004e3035` on HyperEVM. Docs themselves warn about lookalike domains.
- No published legal entity; angel round $670k at $20M FDV (below current FDV; mcap is far below the raise price).

## Verdict shape (how to answer this class of question)

Rate separately: *as a yield venue* (low — LP is paid in a micro-cap emission token, fees go elsewhere) vs *as a
small experiment* (acceptable — data is real, exit is easy at this size, max loss bounded by the position).
Then give the honest alternative for "stable yield on Hyperliquid": HLP vault (market making, has drawdown risk)
or staking/lending HYPE (Kinetiq kHYPE, HyperLend). Always end with a test plan: 3–4 epochs, benchmark against
holding the same 50/50 basket without LP, claim → sell emissions immediately to measure real slippage, and test a
small withdrawal before increasing size.

## Official links (bookmark these, not search results)

`app.usenest.xyz` (app) · `docs.usenest.xyz` (docs, `.md` suffix on any page for raw markdown) ·
`app.usenest.xyz/api/blaze/liquidity-pools` (public pool JSON: `tvlUSD`, `24hVolume`, `fee`, `curEpochEmissionRewardsUSD`)
