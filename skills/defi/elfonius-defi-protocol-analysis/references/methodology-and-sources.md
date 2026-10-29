# Methodology and Sources

This skill synthesises public DeFi risk and valuation frameworks with a non-compensatory investment-committee process. It is standalone: no other agent skill is required, and no source below is an endorsement.

## Research basis

| Source | What it informs |
|---|---|
| EEA *DeFi Risk Assessment Guidelines v1* (2024) | Software, oracle, governance, liquidity, credit, tokenomics, counterparty and regulatory risk categories |
| DefiLlama *Data Definitions* | TVL, fees, revenue, supply-side revenue, tokenholder revenue, earnings, incentives and FDV definitions |
| Token Terminal *Key Metrics FAQ* | Fees, revenue, earnings, P/F and P/S definitions |
| CryptoEQ *DeFi Token Valuation* | Network effects, MC/TVL, P/E analogs, fee-sharing and governance value |
| DeFi-native public skill (MIT) | Five-layer stack, yield decomposition, oracle classes, exit engineering, curator review, composed positions |
| Viprasol *DeFi Protocol Review* (MIT) | Admin/upgrade/audit/oracle/yield red flags and category-aware review |
| TeloSkills (MIT) | Non-compensatory red flags and source-tagged due diligence |
| truenorth *Crypto Project Security* (MIT) | Governance/admin, oracle, incident and on-chain verification workflow |
| Omnis *DeFi On-Chain Analytics* (MIT) | Read-only RPC workflow, proxy resolution, data-confidence tiers |
| Philidor *Vector Risk Framework* (public) | Asset, platform and governance risk decomposition |
| SkillHub DeFi examples | Confirmed demand for APY decomposition, risk scoring and audit-oriented skills; vendor-specific tools were not copied |
| ESMA *Decentralised Finance in the EU* (2023) | Regulatory risk context |
| Public DeFi due-diligence checklists | Operational prompts for lending, DEX, stablecoin and bridge reviews |

## Source URLs

Accessed 2026-10-28–29. These are evidence and design inputs, not endorsements or dependencies.

- EEA DeFi Risk Assessment Guidelines v1 — https://entethalliance.org/specs/defi-risks/
- DefiLlama Data Definitions — https://docs.llama.fi/analysts/data-definitions
- Token Terminal Key Metrics FAQ — https://tokenterminal.com/resources/articles/token-terminal-key-metrics-faq
- CryptoEQ DeFi Token Valuation — https://www.cryptoeq.io/articles/defi-fundamentals-valuation
- DeFi-native skill — https://github.com/emlai/defi-native-skill
- Viprasol DeFi Protocol Review — https://github.com/Viprasol-Tech/defi-protocol-review
- TeloSkills — https://github.com/Telos-Consilium/TeloSkills
- truenorth Crypto Project Security — https://github.com/truenorth-lj/crypto-project-security-skill
- Omnis DeFi On-Chain Analytics — https://github.com/Omnis-Labs/defi-onchain-analytics
- Philidor MCP / Vector Risk Framework — https://github.com/Philidor-Labs/philidor-mcp
- ESMA, Decentralised Finance in the EU — https://www.esma.europa.eu/sites/default/files/2023-10/ESMA50-2085271018-3349_TRV_Article_Decentralised_Finance_in_the_EU_Developments_and_Risks.pdf
- SkillHub marketplace — https://skillhub.club
- Blockchain Council, DeFi Due Diligence Checklist — https://blockchain-council.org/cryptocurrency/defi-due-diligence-checklist-smart-contract-liquidity-governance
- Railnet, Institutional DeFi Risk Framework — https://railnet.org/learn/institutional-defi-risk
- Curvance, DeFi Lending Risk Framework — https://blog.curvance.com/posts/defi-lending-risk-framework
- P2P, Institutional DeFi Infrastructure — https://p2p.org/economy/institutional-defi-infrastructure

### Practitioner checklists

The Blockchain Council, Railnet, Curvance and P2P checklists were used to test for missing prompts, especially front-end/operational risk, liquidation execution, off-chain operations and mandate validation. Their fixed thresholds (for example, TVL above a dollar figure or an audit younger than 12 months) were **not** adopted as universal rules; the skill reports the measurement and the risk instead.

## Coverage map

Use this map when revising the skill or auditing a report. A structural validator passing is not a content audit: every framework category must map to a lens and a depth file, or carry an explicit `not material` / `not assessable` reason. A missing category or an unmatched lens is a defect.

| Framework category | Primary lens | Depth file |
|---|---|---|
| Software and smart-contract risk | 12 Security | `references/defi-security.md` |
| Oracle and price integrity | 11 Oracles | `references/defi-security.md`, `references/defi-lending.md` |
| Governance, admin and upgrade control | 13 Admin/governance | `references/defi-governance-legal.md`, `references/defi-security.md` |
| Liquidity, exit and execution | 9 Liquidity/exit/execution | `references/defi-dex.md`, `references/wallet-operational-security.md` |
| Credit, collateral and liquidation | 10 Collateral/credit | `references/defi-lending.md` |
| Tokenomics and value capture | 8 Token economics | `references/defi-economics.md` |
| Market, competition and manipulation | 4 Market; 16 Technical | `references/defi-market-technical.md` |
| Demand, cohorts and distribution | 5 Usage/demand | `references/defi-economics.md` |
| Valuation and scenarios | 7 Valuation | `references/defi-economics.md` |
| Team, funding and key-person | 15 Team/legal | `references/team-and-org.md` |
| Counterparty, custody and off-chain operations | 14 Dependencies; 15 Team/legal | `references/team-and-org.md`, `references/defi-yield.md` |
| Legal, regulatory and compliance | 15 Team/legal | `references/defi-governance-legal.md` |
| Tax, accounting and reporting | 15 Team/legal | `references/defi-governance-legal.md` |
| Insurance and risk transfer | 15 Team/legal | `references/defi-governance-legal.md`, `references/portfolio-fit.md` |
| Front end, wallet and approval safety | 9 Execution; 12 Security | `references/wallet-operational-security.md`, `references/defi-security.md` |
| Portfolio fit, stress and monitoring | 1 Suitability; 17 Monitoring | `references/portfolio-fit.md` |

## What was adopted

- The gate is **non-compensatory**: a high APY, TVL or score cannot offset a broken control, oracle or exit.
- The **five-layer stack** prevents a single-venue view from hiding a curator, wrapper, bridge or counterparty.
- **Fees ≠ revenue ≠ tokenholder revenue ≠ earnings**; every report states the definition.
- **APY decomposition** on four axes plus four realization filters; no headline APY without a source.
- **Oracle class** and liquidation visibility are first-class findings.
- **Exit engineering** (queue, caps, depth, bridge) is part of the thesis, not an appendix.
- **Cluster exposure** counts one contract/oracle/curator/bridge exposure once.
- **Category-specific** checks for DEX, lending, CDP, perps, vaults, LST/LRT, bridges, RWA, options and insurance.
- **Front-end, wallet, approval and simulation** safety as part of execution, not an afterthought.
- **Data-room request list** so missing documents become findings rather than silent gaps.
- **Team/funding, tax/accounting/insurance** as explicit lenses, with counsel caveats.
- **Demand cohorts and macro transmission** only through a named channel; sentiment is not evidence.
- **Read-only** discipline and source-tagged evidence.

## What was rejected

- A single composite score or letter grade that hides dimensions; this skill reports dimension states and a conditional verdict.
- Fixed thresholds (“APY above X is unsafe”, “TVL below Y is a scam”) without a documented standard; report the measurement and the risk, not a universal cutoff.
- Vendor-specific MCPs/APIs as required dependencies; the method is tool-agnostic.
- Transaction execution, signing, bridging or deposit instructions; the skill is read-only.
- Copying one public skill's wording; the structure is synthesised and independently written.
- “Safe”, “guaranteed” or “risk-free” language; DeFi carries total-loss tails.

## Limitations

- Public data can be stale, self-reported or manipulated; primary chain reads and audited documents are preferred.
- An audit is not a guarantee; a new deployment or module needs new coverage.
- Legal/regulatory conclusions require counsel; this skill provides factual context and questions.
- A well-structured report can still be wrong; the method improves discipline, not predictive accuracy.
- Yield, TVL and prices age in days; every number needs an as-of date and a refresh plan.

## Currency

Refresh market, TVL, fee/revenue, unlock and governance data at the time of the analysis. Do not reuse a number from this reference as current.
