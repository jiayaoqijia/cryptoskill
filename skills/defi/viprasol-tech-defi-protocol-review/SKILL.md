---
name: defi-protocol-review
description: Due-diligence review of a DeFi protocol — admin-key & upgradeability risk, audit status, yield sustainability, liquidity/TVL quality, oracle dependency, and team transparency. Outputs a risk matrix and verdict. Use to vet a protocol before depositing, or to assess rug & exploit risk.
version: 1.0.0
---

# DeFi Protocol Review

A structured due-diligence methodology for assessing the **rug and exploit
risk** of a DeFi protocol before you deposit funds. Given a protocol's docs,
contracts, audits, token, and TVL, this skill works through seven review
dimensions — **smart-contract control, audits & track record, economic design,
liquidity & TVL, oracle dependency, team & transparency, and
composability/contagion** — runs a **red-flag quick scan**, and produces a
**risk matrix** with a single **Low / Moderate / High / Avoid** verdict.

> **Not financial advice.** This is an educational due-diligence framework, not
> an audit and not a recommendation. Smart-contract risk is real and total loss
> is possible — bugs, exploits, governance attacks, oracle manipulation, and
> rugs happen even to "reviewed" protocols. Never deposit more than you can
> afford to lose, and verify every claim on-chain and in the source yourself.

For deeper code-level work, cross-link the Viprasol **`smart-contract-audit`**
skill (line-by-line vulnerability review) and the **`tokenomics-review`** skill
(emission schedules, supply, incentive sustainability).

---

## When to Activate

Activate this skill when the user:

- Asks whether a DeFi protocol is **safe to deposit into**, "is this a rug?",
  "what's the risk of this farm/vault/pool?", or wants a due-diligence pass
  before allocating capital.
- Shares a protocol's **docs, GitHub, contract addresses, audit reports, token
  page, or a DeFiLlama/TVL link** and asks for a risk review.
- Wants to compare two protocols on risk, or to understand admin-key,
  upgradeability, oracle, or yield-sustainability risk specifically.
- Is evaluating a **new / high-APY** opportunity and wants a sanity check
  against rug and exploit red flags.

If the user gives only a name with no contracts/docs, ask for the minimum
inputs in Step 1 (at least: chain, contract address(es) or docs, and audit
status) before scoring. Do not invent findings — if data is missing, mark the
dimension **Unknown** and treat unknowns as risk, not as safety.

---

## Step 1: Scope & Data

Establish and restate the context before assessing anything:

| Field | Why it matters |
|---|---|
| **Protocol & version** | Identifies the entity; v1 vs v2 contracts differ in risk. |
| **Chain(s)** | Ethereum L1 vs a new L2/alt-L1 changes audit depth, bridge risk, and exit liquidity. |
| **Category** | DEX, lending, perps, stablecoin, or yield/aggregator — each has a different threat model (see Step 3). |
| **TVL & trend** | Size and *trend* (sticky vs a sudden spike) signal trust and mercenary capital. |
| **Token & contracts** | Governance/utility token, mint authority, and the exact deployed contract addresses to inspect. |
| **Docs & code** | Whitepaper/docs, public GitHub, verified source on the explorer. |
| **Audits** | Who audited, when, which contracts, and whether findings were fixed. |

State each explicitly in the output header. **Verify on-chain**, not just from
the docs: marketing pages routinely overstate decentralization, audit coverage,
and "locked" liquidity. If the deployed contracts differ from the audited
commit, that gap is itself a finding.

---

## Step 2: Severity Model

Rate each finding on this scale. The **highest** unresolved severity caps the
final verdict — one Critical that puts funds at immediate risk means **Avoid**
regardless of how good the rest looks.

| Severity | Meaning |
|---|---|
| **Critical** | Funds at **immediate** risk: a single key can drain/mint, an unaudited upgradeable proxy with no timelock, or an active known exploit. |
| **High** | Serious risk likely to cause loss under plausible conditions: single-source oracle, unsustainable emissions-only yield, concentrated/unlockable TVL, anon team with custody powers. |
| **Medium** | Material risk needing mitigation/monitoring: multisig with low threshold, partial audit, moderate oracle/composability dependency. |
| **Low** | Minor or well-mitigated risk: timelocked multisig, reputable audits with fixed findings, transparent team. |
| **Info** | Context/observation, no direct loss path. |

---

## Step 3: Review Dimensions

Cover **all seven** dimensions below. For each: **what to check**, **why it
matters**, and **good vs bad** signals. Assign each dimension a severity from
Step 2.

### (a) Smart-Contract Control — who can move or change things?

- **What to check:** Owner/admin of the core contracts — is it an **EOA**
  (single private key), a **multisig** (e.g. Gnosis Safe, note M-of-N), or a
  **timelock + multisig**? Is the protocol an **upgradeable proxy**
  (Transparent/UUPS) and if so, is upgrade gated by a timelock? What
  privileged powers exist: **pause, mint, blacklist, set fees, set oracle,
  emergency withdraw / sweep**, arbitrary `call`?
- **Why:** This is the #1 rug vector. An EOA owner or a no-timelock upgradeable
  proxy means the team (or a stolen key) can change logic or drain funds
  instantly with no warning. A timelock gives users time to exit before a
  malicious change executes.
- **Good:** Owner is a **timelocked multisig** (e.g. 48–72h timelock, 3-of-5+);
  immutable core or upgrades behind that timelock; powers minimized and
  documented; no admin `emergencyWithdraw` over user funds; renounced where
  appropriate.
- **Bad:** **EOA owner**; upgradeable proxy with **no timelock**; admin can
  mint the token or pull user deposits; hidden `onlyOwner` sweep; proxy admin
  same as deployer EOA.

### (b) Audits & Track Record — has it been reviewed and battle-tested?

- **What to check:** Audits by **reputable firms** (and how many), the audit
  **date vs current deployed code**, whether findings were **fixed**, presence
  of a funded **bug bounty** (e.g. Immunefi), and any **prior exploits,
  incidents, or paused events**. Time-in-market / TVL survived.
- **Why:** One audit is not a guarantee, but **zero** audits on a protocol
  holding real TVL is a major flag. Unfixed high findings, or audited code that
  no longer matches the deployment, negate the audit's value. Prior incidents
  reveal both the attack surface and how the team responded.
- **Good:** Multiple recent audits of the **deployed** contracts by known firms,
  findings resolved, active bug bounty, long incident-free track record (or a
  past incident handled transparently with users made whole).
- **Bad:** Unaudited, "audit in progress", audit of a **different** version,
  unfixed criticals, no bug bounty, prior exploit with no postmortem or
  reimbursement.

### (c) Economic Design — is the yield real and sustainable?

- **What to check:** **Where does the yield come from** — real protocol revenue
  (trading/lending/borrow fees, real demand) vs **native-token emissions**
  (printing the governance token)? Emission schedule and whether APY collapses
  as TVL grows. For **stablecoins:** the **peg mechanism** (fiat-backed,
  crypto-overcollateralized, or algorithmic), **collateralization ratio**,
  redemption path, and reserve transparency/attestations.
- **Why:** Emissions-only yield is a wealth transfer from later depositors and
  inevitably decays — "200% APY" almost always means token inflation, not real
  return. Under-collateralized or purely algorithmic stablecoins can
  **de-peg to zero** (see historical depeg collapses).
- **Good:** Yield backed by **real fees/revenue**, sustainable and transparent;
  stablecoin **over-collateralized** with audited/attested reserves and a clear
  redemption mechanism.
- **Bad:** Yield is only the native token; "**guaranteed**" or "**fixed** high
  APY"; ponzi-like reflexive tokenomics; algorithmic/under-collateralized
  stablecoin; opaque or unverifiable reserves.

### (d) Liquidity & TVL — can you actually get out?

- **What to check:** **Depth** of pools and **withdrawal capacity** (can large
  holders exit without breaking the peg/price?), **concentration** (is TVL a
  few whales or one address?), and whether TVL is **organic** vs
  **mercenary/incentivized** (chasing rewards, leaves when emissions stop). Is
  protocol-owned / LP liquidity **locked**, and verifiably so?
- **Why:** High TVL can be hollow. Concentrated or incentivized TVL can exit in
  hours, causing slippage, de-pegs, or bank-run dynamics — and you may be unable
  to withdraw at par.
- **Good:** Deep, **organic**, diversified TVL; sufficient idle/withdrawable
  liquidity; locked LP with on-chain proof; healthy utilization (for lending).
- **Bad:** TVL dominated by a **few addresses**; **mercenary** TVL propped up by
  emissions; thin exit liquidity; LP "locked" only by claim; a recent
  **unexplained TVL spike**.

### (e) Oracle Dependency — can the price feed be gamed?

- **What to check:** **Price source** (Chainlink/redundant feeds vs a single
  DEX spot pool vs an internal oracle), **manipulation resistance** (**TWAP**
  vs raw **spot**), and whether the oracle is a **single point of failure**.
  Fallbacks, staleness checks, and circuit breakers.
- **Why:** Oracle manipulation is one of the most common DeFi exploit classes —
  a single spot-price source on a thin pool can be flash-loaned to drain a
  lending market or mint bad debt. TWAP and multiple independent sources resist
  this; a single spot feed does not.
- **Good:** **Decentralized, redundant** feeds (e.g. Chainlink) with staleness
  and deviation checks; **TWAP** where spot is needed; documented fallback.
- **Bad:** **Single-source** oracle; raw **spot** price from one DEX pool;
  internal oracle the team controls; no staleness/deviation guards.

### (f) Team & Transparency — who is behind it, and can governance be trusted?

- **What to check:** Is the team **doxxed** or **anon**? Quality of **docs** and
  **comms** (clear, consistent, responsive vs hype-only). **Governance
  decentralization** — is voting power concentrated with the team/insiders? Vesting
  and treasury transparency.
- **Why:** Anonymity is not automatically disqualifying (much of DeFi is
  pseudonymous), but **anon + custody powers + no audit + no docs** is the
  classic rug profile. Concentrated governance means "decentralized" control is
  theater — insiders can pass any proposal.
- **Good:** Doxxed or long-reputable pseudonymous team; thorough docs; active,
  honest comms; meaningfully distributed governance with timelocked execution.
- **Bad:** Fully **anon** team with admin custody, thin/copy-paste docs,
  hype-only Telegram, governance tokens overwhelmingly held by insiders.

### (g) Composability / Contagion — what does it depend on?

- **What to check:** Dependencies on **other protocols** (oracles, bridges,
  lending markets, LSTs, wrapped/bridged assets, other yield sources it loops
  through). Bridge risk for cross-chain assets. What happens to this protocol if
  a **dependency** is exploited or de-pegs.
- **Why:** DeFi is composable, so risk is contagious — a vault built on another
  protocol inherits all of that protocol's risks plus bridge and integration
  risk. A safe-looking aggregator can be only as safe as its riskiest leg.
- **Good:** Few, **blue-chip** dependencies; isolated markets; no exotic
  bridged collateral; graceful handling of a dependency failure.
- **Bad:** Deep stack of dependencies; reliance on a **risky bridge** or thinly
  backed wrapped asset; leverage looping that amplifies a dependency de-peg.

---

## Step 4: Red-Flags Quick Scan

Run this fast checklist. Any hit warrants a dimension downgrade; several hits
together push toward **Avoid**:

- [ ] **EOA owner** / no multisig, or **no timelock** on privileged actions.
- [ ] **Upgradeable proxy** with no timelock (instant logic swap).
- [ ] Admin can **mint** the token or **emergency-withdraw** user funds.
- [ ] **Unaudited**, or audit covers a different version / has unfixed criticals.
- [ ] Yield paid **only in the native token** (emissions, not real revenue).
- [ ] **"Guaranteed" / "fixed" high APY** (e.g. triple-digit) marketing.
- [ ] **TVL highly concentrated** in a few addresses, or mercenary/incentive-only.
- [ ] **Single-source / spot** oracle (no TWAP, no redundancy).
- [ ] **Anon team + no docs** + custody powers (classic rug profile).
- [ ] **Recent unexplained TVL spike** or sudden APY pump.
- [ ] Stablecoin that is **algorithmic / under-collateralized** or has opaque reserves.
- [ ] Deployed contracts **don't match** the audited / GitHub source.

---

## Step 5: Output Format

Produce the report in this order:

### 1. Header
Protocol · version · chain(s) · category · TVL & trend · token · key contract
addresses · what was reviewed (docs/code/audits/on-chain).

### 2. Risk matrix (dimension × severity)
One row per dimension, with the assigned severity and the one-line evidence:

| Dimension | Severity | Key finding |
|---|---|---|
| (a) Smart-contract control | Critical / High / Medium / Low / Info | … |
| (b) Audits & track record | … | … |
| (c) Economic design | … | … |
| (d) Liquidity & TVL | … | … |
| (e) Oracle dependency | … | … |
| (f) Team & transparency | … | … |
| (g) Composability / contagion | … | … |

### 3. Top risks
The 2–4 most material findings, most severe first, each with the concrete
evidence (address, power, number, or missing data) behind it.

### 4. "If you still deposit" — risk-mitigation note
Practical mitigations for someone who proceeds anyway: size the position small
relative to net worth, use a fresh/segregated wallet, **revoke approvals** after
use, prefer the most-battle-tested pool, monitor governance/timelock queues and
TVL, and set an exit trigger. Mitigation reduces — never removes — the risk.

### 5. Verdict
Exactly one rating with a one-paragraph justification:

- **Low** — timelocked multisig (or immutable), multiple recent audits of the
  deployed code, real-revenue yield, deep organic TVL, redundant oracles,
  transparent team. Residual smart-contract risk always remains.
- **Moderate** — generally sound but with one or two High items to monitor
  (e.g. a single-source oracle, emissions-heavy yield, or a low-threshold
  multisig) that warrant caution and small sizing.
- **High** — multiple High findings or one near-Critical (e.g. upgradeable with
  weak timelock + emissions-only yield + concentrated TVL); deposit only with
  strong mitigations and capital you can lose.
- **Avoid** — any **Critical** funds-at-immediate-risk finding (EOA/no-timelock
  upgrade or mint, unaudited custody, active exploit) or the classic rug
  profile (anon + no audit + custody + "guaranteed" APY).

---

## Disclaimer

This skill provides **educational due-diligence analysis, not financial,
investment, legal, or security-audit advice.** A passing review here is **not**
a safety guarantee and does not replace a professional smart-contract audit.
**Smart-contract risk is real:** exploits, governance attacks, oracle
manipulation, de-pegs, and rug pulls cause total loss even in audited,
high-TVL protocols. Always verify contracts, ownership, and claims **on-chain**
yourself, read the actual source, and **never deposit more than you can afford
to lose.** This skill is **not affiliated with or endorsed by Anthropic** or any
protocol, auditor, or data provider.
