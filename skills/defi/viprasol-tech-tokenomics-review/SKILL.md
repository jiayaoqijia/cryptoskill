---
name: tokenomics-review
description: Review a crypto token's economics for red flags — supply & FDV, insider allocation & vesting, emissions/inflation, unlock overhang, liquidity, and rug vectors. Outputs a risk scorecard and verdict. Use for token due diligence, launch review, or investment screening.
version: 1.0.0
---

# Tokenomics Review

A structured methodology for reviewing a crypto token's **economics** for red
flags. Given a token's supply schedule, allocation breakdown, vesting and unlock
calendar, emission model, liquidity, and contract permissions, this skill
produces a disciplined read of **supply & FDV, insider allocation & vesting,
emissions/inflation, unlock overhang, liquidity depth, and rug vectors** — and
returns a **risk scorecard** and a single **verdict**
(*Healthy / Caution / High-risk / Likely-rug*), grounded in standard token
due-diligence practice.

> **Not financial advice.** This is an educational analytical framework. Crypto
> is a high-risk asset class; tokens can go to zero, contracts can be exploited,
> and "tokenomics" can be designed to look healthy while extracting value. Always
> verify on-chain, read the audited contract, and **do your own research (DYOR)**.

For related Viprasol skills, see **`smart-contract-audit`** (Solidity/contract
vulnerability review) and **`defi-protocol-review`** (protocol-level economic and
mechanism review). Tokenomics review pairs naturally with both: this skill asks
"is the *token's economy* sound and non-predatory?", the contract audit asks "is
the *code* safe?", and the protocol review asks "is the *mechanism* sound?".

---

## When to Activate

Activate this skill when the user:

- Shares a token's tokenomics (supply, allocation, vesting, emissions, unlock
  schedule, contract address) and asks whether it's healthy, fair, risky, or a
  potential rug.
- Asks for token due diligence, launch review, allocation/vesting analysis,
  unlock-overhang analysis, or investment screening on a named token or pasted
  tokenomics.
- Asks "is this a rug?", "is the FDV too high?", "are insiders dumping?", "is the
  liquidity locked?", "is the supply inflationary?", or "are these tokenomics
  fair?".
- Is reviewing a presale, IDO/ICO/IEO, fair-launch, or airdrop allocation.

If only a fragment is given (e.g. just "price" or "market cap"), ask for the
minimum inputs needed (see Step 1) before scoring. **Do not fabricate supply,
allocation, or unlock numbers** — request the source (docs, token contract,
vesting contract, a tracker like a token-unlocks dashboard) or mark anything
derived as `(est.)`.

---

## Step 1: Scope & Data

Before any scoring, establish and restate the inputs so the review is anchored.
Pull these explicitly and flag whatever is missing or estimated:

| Field | Why it matters |
|---|---|
| **Token / ticker** | Identifies the asset; enables on-chain and tracker lookup. |
| **Chain(s)** | Determines tooling, standard (ERC-20/SPL/etc.), bridge & liquidity context. |
| **Contract address** | The ground truth. Everything else (supply, mint authority, taxes) is verifiable here. |
| **Total / Max / Circulating supply** | Total = minted; Max = hard cap (or "unbounded"); Circulating = liquid float. The gap is future dilution. |
| **FDV vs Market cap** | FDV = price × max/total supply; MC = price × circulating. A wide gap = large unlock overhang. |
| **Allocation breakdown** | Team, investors/VCs, community/airdrop, treasury/DAO, liquidity/LP, ecosystem/rewards — as % of total. |
| **Vesting, cliffs & unlock schedule** | When and how each bucket unlocks: cliff length, then linear/stepped release; % of float unlocking over the next 30/90/365 days. |
| **Emission schedule** | New tokens minted over time (staking/farming rewards, inflation rate %/yr) and whether it tapers. |
| **Utility / sinks** | What the token is *for* and what removes it from supply (fees, burns, buybacks, locked staking, collateral). |
| **Liquidity** | DEX/CEX liquidity depth ($) vs market cap; is the LP **locked or burned**, and for how long? |
| **Team & audit** | Doxxed vs anonymous team; reputable audit(s) vs none; verified source on the explorer. |

State each explicitly in the output header. If supply or allocation is unknown,
ask — a scorecard without supply and allocation is meaningless.

---

## Step 2: Severity Model

Grade each finding by severity. Use this table consistently:

| Severity | Icon | Meaning |
|---|---|---|
| **Critical** | 🔴 | Likely-rug or structurally insolvent economics — an active rug vector (unlocked LP, mint authority, blacklist/pause owner) or an extraction design that predictably transfers value from buyers to insiders. Treat as disqualifying absent strong mitigation. |
| **High** | 🟠 | Severe, value-destroying risk — e.g. insiders > 50% with weak vesting, FDV/MC > 10, a large near-term unlock cliff, ponzi-style emissions. Materially raises the odds of a large drawdown. |
| **Medium** | 🟡 | Notable concern that needs monitoring or context — elevated but not damning (moderate insider share, FDV/MC 3–10, thin-but-locked liquidity, gradual inflation). |
| **Low** | 🟢 | Minor / acceptable — within healthy benchmarks; note for completeness. |
| **Info** | ⓘ | Neutral context, assumption, or item that couldn't be verified (mark data gaps here, not as a pass). |

A single **Critical** rug vector caps the verdict at **Likely-rug** regardless of
how clean the rest looks. Severity reflects *economic harm × likelihood*, not
just presence of a feature.

---

## Step 3: Checklist

Work through every dimension below. For each: **what** it is, **how to check**
it, **why it matters**, and a **healthy benchmark**. Cover all of them — note
explicitly when a dimension can't be assessed (mark it ⓘ, don't skip silently).

### 3.1 Supply concentration & top-holder %
- **What:** how concentrated holdings are among the largest wallets.
- **How to check:** explorer "Holders" / top-100 list; net out known burn,
  bridge, LP, staking, and CEX-omnibus wallets before judging.
- **Why:** concentrated supply lets a few wallets crash the price or rug.
- **Healthy:** top-10 (ex-contract/LP/treasury) **< 30%**; no single non-team
  wallet dominating the float.

### 3.2 Insider (team + investor) allocation % and vesting structure
- **What:** combined team + VC/investor share and how it's locked.
- **How to check:** docs/token distribution + the on-chain vesting contract
  (cliff length, linear vs cliff-dump, total duration).
- **Why:** large insider allocations with weak vesting = sustained sell pressure
  and misaligned incentives.
- **Healthy:** insiders **< 35–40%** of supply; **≥ 12-month cliff** then
  **linear vesting over ≥ 24–48 months** (not a cliff-then-dump).

### 3.3 FDV / MC ratio & dilution overhang
- **What:** fully-diluted valuation vs current market cap.
- **How to check:** FDV = price × total/max supply; MC = price × circulating;
  ratio = FDV ÷ MC.
- **Why:** a high ratio means most supply isn't circulating yet — future unlocks
  must be absorbed by demand or price falls.
- **Healthy:** FDV/MC **< 3** is comfortable; **3–10** watch; **> 10** heavy
  overhang.

### 3.4 Emission / inflation rate vs demand sinks
- **What:** rate of new-supply issuance vs mechanisms that remove supply.
- **How to check:** annual emission ÷ circulating supply (= inflation %/yr);
  compare against burns/fees/locked-staking demand.
- **Why:** if emissions outrun real demand, price bleeds structurally
  ("emissions-funded yield").
- **Healthy:** inflation **< ~5–10%/yr** and **tapering**, with genuine sinks;
  uncapped/unbounded emission with no sinks is a red flag.

### 3.5 Upcoming unlock cliffs (% of float unlocking in next 30 / 90 days)
- **What:** scheduled near-term unlocks relative to circulating float.
- **How to check:** vesting calendar / unlock-tracker; compute unlocking amount ÷
  current circulating supply for 30d and 90d windows.
- **Why:** a large cliff into thin liquidity is a predictable dump.
- **Healthy:** **< 5%** of float unlocking in 30 days, **< 15%** in 90 days; no
  single cliff > ~10% of float at once.

### 3.6 Real utility vs reflexive / ponzi yield
- **What:** whether token demand is organic or self-referential.
- **How to check:** identify what the token *does*; is "yield" paid in real fees
  or in freshly minted tokens? Does APR depend on new deposits?
- **Why:** reflexive "X% APY in our own token" designs collapse when inflows
  stop — a classic ponzi pattern.
- **Healthy:** demand from real usage (fees, gas, collateral, governance over
  real value); yield sourced from **real revenue**, not pure emissions.

### 3.7 DEX liquidity depth vs market cap & LP lock/burn
- **What:** how much liquidity backs the token and whether it can be pulled.
- **How to check:** DEX pool TVL / depth ($) vs MC; check whether LP tokens are
  **locked** (time-locked) or **burned** (sent to dead address), and the lock
  expiry.
- **Why:** a "pull liquidity" rug is only possible if the deployer still holds
  LP; thin liquidity also means a small sell tanks price.
- **Healthy:** liquidity **≥ 5–10%** of MC and **LP locked (long) or burned**;
  unlocked LP held by deployer is a **Critical** rug vector.

### 3.8 Mint / pause / blacklist / owner admin functions (rug vectors)
- **What:** privileged contract functions the owner can call.
- **How to check:** read the verified contract: `mint`, owner-mintable supply,
  `pause`/`setTradingEnabled`, `blacklist`/`setMaxTx`, fee-setter, proxy
  upgradeability, owner not renounced or behind a timelock/multisig.
- **Why:** these let an owner print supply, freeze sells, or block specific
  wallets — direct rug/honeypot enablers.
- **Healthy:** no unbounded mint; ownership **renounced or behind a timelock +
  multisig**; no blacklist/arbitrary-pause; non-upgradeable or
  governance-gated. *(Cross-check with `smart-contract-audit`.)*

### 3.9 Transfer tax / honeypot patterns
- **What:** buy/sell taxes and asymmetric or sell-blocking logic.
- **How to check:** read tax variables; simulate a sell (honeypot checker / test
  swap); look for sell-only fees, max-tx limits applied only to sells, or
  hidden owner-only transfer paths.
- **Why:** high or asymmetric taxes extract value; honeypots let you buy but not
  sell.
- **Healthy:** **0% or low symmetric tax (≤ ~5%)**, no sell-blocking, sells
  confirmed to work. Tax **> 10%** is a red flag; un-sellable = honeypot.

### 3.10 Treasury runway & funding
- **What:** whether the project is funded to deliver without dumping its own
  token.
- **How to check:** treasury holdings (stables vs own-token), burn rate, raise
  size; is the treasury denominated in its own token (circular) or in
  stables/blue-chips?
- **Why:** a treasury that's only its own token must sell into the market to pay
  bills — structural sell pressure.
- **Healthy:** meaningful **non-native** runway (stables/blue-chips) covering
  development for 18+ months; transparent treasury wallet.

### 3.11 Governance centralization
- **What:** who actually controls upgrades, emissions, treasury, and parameters.
- **How to check:** multisig signer count/threshold, admin keys, proxy admin,
  voting-power distribution, whether insiders hold a governance majority.
- **Why:** "decentralized" governance where insiders hold the votes (or a 1-of-1
  admin key) can change the rules against holders.
- **Healthy:** **multisig (e.g. ≥ 3-of-5)** + **timelock** on sensitive actions;
  no single party holding a governance majority of the float.

> Aim to assess **at least 11 dimensions** (the list above). Add token-specific
> ones (e.g. rebasing, bridge-mint risk, oracle dependence, ve-token lock
> dynamics) where relevant.

---

## Step 4: Red-Flags Quick Scan

Fast triage — any hit warrants a deeper look; clusters of hits push the verdict
toward **High-risk** or **Likely-rug**:

- **Team + investors > 50% of supply** (insider-dominated distribution).
- **No vesting, or a very short cliff** (insiders can dump near launch).
- **FDV / MC > 10** (massive dilution overhang waiting to unlock).
- **> 10% of float unlocking within 30 days** (imminent cliff into the market).
- **Top-10 holders > 50%** of float (extreme concentration / dump risk).
- **Mintable or unbounded supply** (owner can print / dilute at will).
- **LP not locked or burned** (deployer can pull liquidity — classic rug).
- **Anonymous team + unaudited contract** (no accountability, unverified safety).
- **Transfer tax > 10%** (or asymmetric sell tax / honeypot pattern).

---

## Step 5: Output Format

Produce the report in this order:

### 1. Header
Token · ticker · chain(s) · contract address · total/max/circulating supply ·
price/MC/FDV (with units) · data sources · what couldn't be verified (ⓘ).

### 2. Risk scorecard table
One row per key metric; columns: **Metric · Value · Flag**, using 🔴 (Critical) /
🟡 (Watch — Medium/High) / 🟢 (Healthy):

| Metric | Value | Flag |
|---|---|---|
| Insider (team+investor) allocation | 55% | 🔴 |
| Vesting (cliff / linear) | 6-mo cliff, then 12-mo | 🟡 |
| FDV / MC | 15× | 🔴 |
| Top-10 holders (ex-LP/treasury) | 41% | 🟡 |
| Unlock in next 30d (% of float) | 4% | 🟢 |
| Emission / inflation | 6%/yr, tapering | 🟢 |
| Liquidity depth vs MC | 7% | 🟢 |
| LP lock / burn | Locked 12 mo | 🟢 |
| Mint / pause / blacklist | None; owner renounced | 🟢 |
| Transfer tax | 0% | 🟢 |

### 3. Allocation & unlock-schedule table
Allocation by bucket (% of total) plus each bucket's cliff/vesting and the
near-term unlock load:

| Bucket | % of supply | Cliff | Vesting | Notable unlock |
|---|---|---|---|---|
| Team | 20% | 12 mo | 36-mo linear | — |
| Investors | 25% | 6 mo | 24-mo linear | 6-mo cliff release |
| Community / airdrop | 20% | none | 50% at TGE | TGE |
| Treasury / DAO | 20% | none | DAO-controlled | — |
| Liquidity | 10% | locked | — | — |
| Ecosystem / rewards | 5% | none | emissions | ongoing |

### 4. Top risks (prioritized)
Most material first, each with the evidence (the numbers / contract finding)
behind it and its severity icon.

### 5. Verdict (one rating + one paragraph)
Conclude with exactly one rating and a one-paragraph justification:

- **Healthy 🟢** — fair distribution, insiders well-vested, FDV/MC low, manageable
  unlocks, real utility/sinks, deep & locked liquidity, no rug vectors.
- **Caution 🟡** — fundamentally workable but with one or two watch items
  (elevated FDV/MC, moderate insider share, gradual inflation) that need
  monitoring.
- **High-risk 🟠** — multiple serious concerns (insider-heavy + weak vesting,
  FDV/MC > 10, large near-term unlocks, emissions-funded yield) that make a large
  drawdown likely.
- **Likely-rug 🔴** — one or more **Critical** rug vectors (unlocked LP,
  mint/blacklist/pause owner, honeypot) or an extraction-by-design economy; treat
  as disqualifying absent strong, verifiable mitigation.

---

## Disclaimer

This skill provides **educational tokenomics analysis, not financial,
investment, legal, or tax advice.** Cryptocurrency is a **high-risk** asset class
— tokens can lose all value, smart contracts can be exploited, and tokenomics can
be engineered to appear sound while extracting value from buyers. The benchmarks
here are heuristics, not guarantees; passing this review does **not** make a token
safe, and a clean scorecard can still precede a collapse. Always verify every
figure **on-chain** against the token and vesting contracts, read any audit in
full, and **do your own research (DYOR)** before interacting with or investing in
any token. This skill is **not affiliated with or endorsed by Anthropic** or any
data provider, exchange, or project.
