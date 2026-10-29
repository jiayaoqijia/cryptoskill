<!-- INTERNAL WORKPAPER — not the user-facing deliverable. Keep this file; deliver a report template. Unfilled lines are findings. -->

# DeFi Workpaper — {{protocol_or_vault}}

**As of (UTC):** {{YYYY-MM-DD HH:MM}} · **Retrieval window:** {{first–last}}
**Decision lens:** {{screen | compare | deposit | hold | exit}}
**Horizon / benchmark / numeraire:** {{explicit values or labelled assumptions}}
**Exact target:** {{chain, contract, proxy, product, token, entity}}
**Investability gate:** {{pass | conditional | fail | insufficient evidence}} — {{which component}}
**Coverage:** {{checked / not checked / why}}

## 1. Asset and instrument map

- Protocol, version, product/market/vault/pool:
- Chain(s), chain ID(s), full contract address(es), proxy/implementation:
- Token(s), standard, supply and rights:
- Legal entity, jurisdiction, front end:
- Venues and quote assets:
- Peers selected and why:

## 2. Decision frame and suitability

- Decision requested, horizon, benchmark, numeraire:
- Constraints: drawdown, liquidity, currency, jurisdiction, existing exposure:
- If absent: `suitability not assessable — requires <inputs>`:
- Behavioral bias check (yield chasing, anchoring, sunk cost, recency, chain bias):

## 3. Claims converted into test questions

| Claim | Testable question | Evidence that confirms | Evidence that refutes |
|---|---|---|---|
| | | | |

## 4. Evidence ledger

| ID | Claim / metric | Type | Value, unit, as-of | Source, independence | Status |
|---|---|---|---|---|---|
| K1 | | | | | |

## 5. Data conflicts and freshness

| Metric | Source A | Source B | Difference | Chosen basis | Why |
|---|---|---|---|---|---|
| TVL | | | | | |
| Fees | | | | | |
| Revenue | | | | | |
| Supply/FDV | | | | | |
| APY | | | | | |

## 6. Five-layer stack

| Layer | Entity / contract | What it controls | Evidence |
|---|---|---|---|
| Venue protocol | | | |
| Vault / curator | | | |
| Underlying assets / counterparties | | | |
| Oracles / bridges / keepers | | | |
| Front end / distribution | | | |

## 7. Product and mechanism

{{What it does, who pays, why, substitutes, dependencies, failure modes.}}

## 8. Usage and demand quality

| Metric | Value | As-of | Source | Paid / incentive | Note |
|---|---:|---|---|---|---|
| Active users | | | | | |
| Retention | | | | | |
| Volume | | | | | |
| Utilization | | | | | |
| Top-10 concentration | | | | | |

## 9. TVL bridge

| Basis | Value | Definition | Source | Date | Difference explained |
|---|---:|---|---|---|---|
| Gross protocol TVL | | | | | |
| Excluding own token | | | | | |
| Excluding double counting | | | | | |
| Effective/productive TVL | | | | | |
| Withdrawable at size | | | | | |

## 10. Fee and revenue bridge

| Line | Value | Period | Definition | Source |
|---|---:|---|---|---|
| Gross fees | | | | |
| Supply-side revenue | | | | |
| Protocol revenue | | | | |
| Tokenholder revenue | | | | |
| Incentives | | | | |
| Earnings | | | | |

## 11. Yield decomposition

| Source | Share of APY | Organic / incentive | Cash / accrual | Denomination | Risk it pays for |
|---|---:|---|---|---|---|
| | | | | | |

**Gross → net:** {{fees, gas, slippage, exit}} · **Window:** {{...}} · **Size:** {{...}}

## 12. Unit economics and treasury

| Segment | Revenue/unit | Cost/unit | Gross margin | Note |
|---|---:|---:|---:|---|
| | | | | |

{{Treasury composition, stablecoin runway, token holdings, burn rate, who funds buybacks.}}

## 13. Supply bridge

| Basis | Value | Definition | Source | Date | Note |
|---|---:|---|---|---|---|
| Max supply | | | | | |
| Total supply | | | | | |
| Circulating | | | | | |
| Float | | | | | |
| Treasury-held | | | | | |
| Locked/vesting | | | | | |

## 14. Unlocks, emissions and burns

| Month | Tokens unlocking/emitted | % float | % 30d volume | Cumulative % | Beneficiary | Source |
|---|---:|---:|---:|---:|---|---|
| | | | | | | |

{{Emission schedule, buyback/burn funding source, net inflation.}}

## 15. Rights ladder and value capture

| Claimed right | Rung (1–7) | In code? | Function/state | Funding source | Enforceability |
|---|---|---|---|---|---|
| | | | | | |

## 16. Holder concentration and cohorts

| Holder/cohort | Share | Label | Locked/unlocked | Source | Basis |
|---|---:|---|---|---|---|
| | | | | | |

## 17. Staking, validator and keeper flows

{{Net stake/unstake, validator/operator concentration, slashing, keeper participation, rewards.}}

## 18. Protocol and treasury flows

| Period | Protocol buys | Treasury sells | User net | Bridge net | Net price change | Source |
|---|---:|---:|---:|---:|---:|---|
| | | | | | | |

## 19. Team, funding, governance and control

- Founders and core contributors, verified track record, key-person and conflicts:
- Funding rounds, cap table, treasury composition, stablecoin runway:
- Governance token distribution, delegates, quorum, proposal history:
- Team wallets, related entities and market maker/curator/oracle affiliations:

| Power | Holder | Threshold/delay | Can move user funds? | Evidence |
|---|---|---|---|---|
| Upgrade | | | | |
| Pause | | | | |
| Mint/burn | | | | |
| Oracle/collateral | | | | |
| Treasury | | | | |

## 20. Dependencies and systemic risk

| Dependency | What can fail | Exposure | Correlation | Exit impact | Source |
|---|---|---|---:|---|---|
| Bridge | | | | | |
| Oracle | | | | | |
| Stablecoin | | | | | |
| LST/LRT | | | | | |
| RWA wrapper | | | | | |
| Curator/keeper | | | | | |

## 21. Security and audits

| Audit | Firm | Date | Commit/scope | Critical/high | Remediation | Source |
|---|---|---|---|---|---|---|
| | | | | | | |

{{Source verification, formal verification, bug bounty, incidents, admin/upgrade path.}}

## 22. Incidents and postmortems

| Date | Loss | Root cause | Fix | Users made whole? | Still relevant? |
|---|---:|---|---|---|---|
| | | | | | |

## 23. Legal and regulatory

- Entity/jurisdiction:
- Token classification / MiCA / securities:
- KYC/AML, sanctions, eligible investors:
- Custody, segregation, insurance:
- Tax/transfer restrictions:
- Insurance/risk transfer:
- Counsel required:

## 24. Liquidity, exit and execution

| Venue | Pair | Depth ±2% | Slippage at size | Queue/cooldown | Exit days | Source |
|---|---|---:|---:|---|---:|---|
| | | | | | | |

- Wallet type, official domain/contract, calldata/spender/allowance:
- Transaction simulation and balance changes:
- RPC/MEV protection and unwind path:

## 25. Collateral, credit and liquidation

{{LTV/LLTV, liquidation threshold/bonus/close factor, oracle, keepers, bad debt, isolation/eMode, stress.}}

## 26. Market structure and technical

{{Price/volume, funding/basis, OI, volatility, drawdown, relative strength, correlations.}}

## 27. Community, news and catalysts

| Date | Event | Source | Confirmed? | Thesis impact |
|---|---|---|---|---|
| | | | | |

## 28. Valuation

{{Method, assumptions, P/F, P/S, P/E, reverse valuation, scenarios, expected return incl. total loss.}}

## 29. Risk matrix and pre-mortem

| Risk | Probability | Impact | Failure shape | Mitigation | Monitoring |
|---|---|---|---|---|---|
| | | | | | |

## 30. Decision and monitoring

- Gate:
- Verdict:
- Falsifiers:
- Monitoring dashboard:
- What would change the size:
- Checks not run:
