# Example — Governance Token Review (Insider-Heavy, Big Cliff Unlock, High FDV/MC)

> **Illustrative example.** "MetaVault DAO ($MVD)" and all figures below are
> fictional, used to demonstrate the skill's output format. Not a real token and
> not financial advice. DYOR.

## Header

| | |
|---|---|
| **Token** | MetaVault DAO ($MVD) (illustrative) |
| **Chain** | Ethereum (ERC-20) |
| **Contract** | `0xMVD…illustrative` (verified source, 1 audit) |
| **Max / Total supply** | 1,000,000,000 MVD (fixed, no mint) |
| **Circulating supply** | ~120,000,000 MVD (12% of max) |
| **Price / MC / FDV** | $0.40 · MC ≈ $48M · **FDV ≈ $400M** |
| **Data sources** | Project docs, token + vesting contracts, explorer holders, unlock tracker |
| **Not verified (ⓘ)** | Exact CEX-omnibus split inside top holders; treasury denomination |

### Allocation & unlock schedule (illustrative, % of max supply)

| Bucket | % of supply | Cliff | Vesting | Notable unlock |
|---|---|---|---|---|
| Team | 22% | 6 mo | 18-mo linear after cliff | **cliff release at month 6** |
| Investors / VCs | 33% | 6 mo | 18-mo linear after cliff | **cliff release at month 6** |
| Community / airdrop | 12% | none | 40% at TGE, rest 12-mo | TGE |
| Treasury / DAO | 18% | none | DAO-controlled | — |
| Liquidity | 5% | locked 12 mo | — | — |
| Ecosystem / staking rewards | 10% | none | 4-yr emissions | ongoing |

**Insiders = Team 22% + Investors 33% = 55% of supply.** A combined **55% with
only a 6-month cliff** unlocks into the market starting month 6 — a large,
predictable supply wave against a $48M float.

## Risk Scorecard

| Metric | Value | Flag |
|---|---|---|
| Insider (team+investor) allocation | 55% | 🔴 |
| Vesting (cliff / linear) | 6-mo cliff, then 18-mo linear | 🟡 |
| FDV / MC | **15×** ($400M / $27M effective free float basis) | 🔴 |
| Top-10 holders (ex-LP/treasury) | ~46% | 🟡 |
| Unlock in next 30d (% of float) | 3% | 🟢 |
| Unlock at month-6 cliff (% of float) | **~25% of float in one step** | 🔴 |
| Emission / inflation (staking) | ~8%/yr, tapering over 4 yr | 🟡 |
| Liquidity depth vs MC | ~4% | 🟡 |
| LP lock / burn | Locked 12 mo | 🟢 |
| Mint / pause / blacklist | None; fixed supply; owner → 3-of-5 multisig + timelock | 🟢 |
| Transfer tax | 0% | 🟢 |

## Red-Flags Quick Scan

- 🔴 **Team + investors = 55% > 50%** — insider-dominated distribution.
- 🟡 **Short 6-month cliff** then a large step — not "no vesting", but the cliff
  is short and front-loaded for a 55% block.
- 🔴 **FDV/MC ≈ 15× > 10** — only ~12% of supply circulates; heavy overhang.
- 🔴 **~25% of float unlocks at the month-6 cliff** — far above the ~10%
  single-cliff guideline, into thin (~4% of MC) liquidity.
- 🟡 **Liquidity ~4% of MC** — thin; a modest sell moves price (LP is locked,
  so not a rug, but low depth amplifies the unlock impact).
- 🟢 Fixed supply, no mint/blacklist/pause, ownership behind multisig + timelock,
  0% tax, LP locked, audited & verified — **no Critical rug vector.**

## Top Risks (prioritized)

1. **🔴 Month-6 cliff dump risk.** ~25% of float unlocks in a single step for a
   55% insider block, into liquidity worth only ~4% of MC. Even partial selling
   could drive a large drawdown. *Evidence: 55% insider alloc, 6-mo cliff, ~4%
   liquidity/MC.*
2. **🔴 FDV/MC ≈ 15×.** Most value is unrealized supply; sustaining price requires
   demand to keep absorbing scheduled unlocks for 2+ years. *Evidence: $400M FDV
   vs $48M MC.*
3. **🟡 Holder concentration ~46% in top-10.** Concentrated float magnifies the
   unlock risk; verify how much is CEX-omnibus vs insider wallets. *Evidence:
   explorer top-10 (ex-LP/treasury).*
4. **🟡 Thin liquidity (~4% of MC).** Low depth means even non-cliff selling has
   outsized price impact.

## Verdict

**High-risk 🟠.** MetaVault DAO's *contract* is clean — fixed supply, no mint or
blacklist, ownership behind a multisig + timelock, LP locked, 0% tax — so this is
**not a likely-rug**. The risk is purely economic and scheduled: a **55% insider
allocation behind only a 6-month cliff**, an **FDV/MC of ~15×**, and a single
**month-6 unlock of ~25% of the float** into liquidity worth just ~4% of market
cap. That combination makes a large drawdown around the cliff the base case
unless real demand or further voluntary locks materialize first. Watch the
month-6 unlock date and liquidity depth closely. *Illustrative; not financial
advice — DYOR.*
