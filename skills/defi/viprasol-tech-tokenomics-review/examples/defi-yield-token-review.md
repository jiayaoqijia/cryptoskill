# Example — DeFi Yield Token Review (Emissions-Funded Yield, Unlocked LP, Mintable)

> **Illustrative example.** "HyperYield Finance ($HYF)" and all figures below are
> fictional, used to demonstrate the skill's output format. Not a real token and
> not financial advice. DYOR.

## Header

| | |
|---|---|
| **Token** | HyperYield Finance ($HYF) (illustrative) |
| **Chain** | BNB Chain (BEP-20) |
| **Contract** | `0xHYF…illustrative` (verified, **owner not renounced**, **no audit**) |
| **Max supply** | **Unbounded** — `mint()` callable by owner |
| **Total / Circulating supply** | 50,000,000 / ~30,000,000 HYF |
| **Price / MC / FDV** | $0.10 · MC ≈ $3M · FDV ≈ n/a (uncapped) |
| **Advertised yield** | "Up to **900% APY**" staking, paid in HYF |
| **Team** | Anonymous |
| **Data sources** | Project site, contract bytecode/source, DEX pool, holders |
| **Not verified (ⓘ)** | Real protocol revenue (appears to be none) |

### Allocation & unlock schedule (illustrative)

| Bucket | % | Cliff | Vesting | Notable |
|---|---|---|---|---|
| Team (anon) | 20% | none | none | liquid at launch |
| "Marketing" wallet | 15% | none | none | liquid; mobile |
| Farming / staking rewards | 50% | none | **minted on demand** | emissions-funded |
| Liquidity | 15% | **none — LP NOT locked** | — | deployer holds LP |

There is no meaningful vesting; the reward pool is **minted**, not pre-allocated,
so supply is effectively uncapped.

## Risk Scorecard

| Metric | Value | Flag |
|---|---|---|
| Supply cap | **Unbounded (owner can mint)** | 🔴 |
| Insider (team + marketing) allocation | 35%, **no vesting** | 🔴 |
| FDV / MC | n/a — uncapped, dilution unlimited | 🔴 |
| Top-10 holders | ~71% (incl. deployer + reward contract) | 🔴 |
| Emission / inflation | "900% APY" in freshly minted HYF | 🔴 |
| Real utility / sinks | None — yield is reflexive (paid in own token) | 🔴 |
| Liquidity depth vs MC | ~6% | 🟡 |
| **LP lock / burn** | **NOT locked — deployer holds LP tokens** | 🔴 |
| Mint / pause / blacklist | **`mint`, `pause`, `setFee` all owner-callable; owner not renounced** | 🔴 |
| Transfer tax | **12% (and sell tax 18%)** | 🔴 |
| Team / audit | **Anonymous + unaudited** | 🔴 |

## Red-Flags Quick Scan

- 🔴 **Mintable / unbounded supply** — owner can print HYF at will.
- 🔴 **LP not locked or burned** — deployer can pull liquidity at any moment
  (textbook rug vector).
- 🔴 **Owner functions** — `mint`, `pause`, `setFee`, and ownership not renounced;
  pause + asymmetric tax = honeypot-capable.
- 🔴 **Transfer tax 12% buy / 18% sell** — well above 10% and asymmetric (sell
  penalty).
- 🔴 **Emissions-funded "900% APY"** — reflexive ponzi yield with no real revenue
  source; APR sustained only by new deposits + minting.
- 🔴 **Anonymous team + no audit** — no accountability, unverified safety.
- 🔴 **Top-10 ~71%** — extreme concentration.

## Top Risks (prioritized)

1. **🔴 Unlocked LP + non-renounced owner = active rug vector.** The deployer can
   pull liquidity and/or mint unlimited supply at any time — holders could be
   zeroed in a single transaction. *Evidence: LP tokens in deployer wallet;
   `mint()`/owner not renounced.*
2. **🔴 Honeypot/extraction mechanics.** Owner-callable `pause` plus an 18% sell
   tax can trap sellers and extract value asymmetrically. *Evidence: contract
   functions + tax variables.*
3. **🔴 Ponzi-style emissions.** "900% APY" is paid in newly minted HYF with no
   real revenue — structurally guaranteed to dilute toward zero once inflows
   slow. *Evidence: rewards minted on demand; no fee/burn sink.*
4. **🔴 Anonymous, unaudited, ~71% concentrated** — no accountability and trivial
   coordinated dumping.

## Verdict

**Likely-rug 🔴.** HyperYield Finance combines *every* Critical rug vector at
once: **unbounded mintable supply**, **LP that is not locked or burned** (held by
the deployer), **non-renounced owner** with `mint`/`pause`/`setFee` powers, an
**18% asymmetric sell tax**, an **anonymous team**, **no audit**, and a **"900%
APY" emissions-funded ponzi** yield with no real revenue. Any one of these would
cap the verdict; together they describe an economy designed to extract value from
buyers, with the deployer able to pull liquidity or dilute supply at will. This is
not a "watch it" situation — treat it as disqualifying absent verifiable,
on-chain mitigation of *all* of the above. *Illustrative; not financial advice —
DYOR.*
