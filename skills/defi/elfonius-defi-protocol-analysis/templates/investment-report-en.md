<!-- INTERNAL TEMPLATE — deep DeFi report, 8–15 pages. Fill every placeholder; delete this comment, unused rows and empty sections. Pair with references/report-production.md. The one-page executive summary is mandatory. -->

# {{Protocol / vault}} — DeFi Investment Research

**Date (UTC):** {{YYYY-MM-DD HH:MM}} · **Decision:** {{deposit | buy | hold | exit | compare}}
**Chain / exact contract / product:** {{...}} · **Token:** {{...}}
**Prepared by:** {{name or team}} · **Data as of:** {{date}}

## Cover

- Title: {{protocol}} — {{one-sentence thesis}}
- Subtitle: {{real yield, weak token | good product, bad exit | ...}}
- Verdict: {{suitable | watch | avoid | insufficient evidence}}
- Four metrics: {{TVL}} · {{annualized fees}} · {{annualized revenue}} · {{market cap / FDV}}
- Contents: {{01 Identity · 02 Stack · ...}}

## Executive summary — one page

{{Four short paragraphs: what the product is and what the user owns; why now; where the yield comes from; the verdict and what would change it. Then the scorecard and "what to monitor".}}

| Dimension | State | Short evidence |
|---|---|---|
| Exact deployment | | |
| Product / mechanism | | |
| Market / competition | | |
| Usage / demand | | |
| Fees / revenue | | |
| Token / value capture | | |
| Liquidity / exit | | |
| Collateral / oracle | | |
| Security / audits | | |
| Admin / governance | | |
| Legal / eligibility | | |
| Portfolio fit | | |

**What to monitor:** {{four items}} · **Scope limit:** {{checks not run}}

## 01 · Decision frame and exact target

{{Decision, horizon, numeraire, benchmark, jurisdiction, loss tolerance, liquidity, existing exposure. Chain, version, product, full contract address, proxy/implementation, token, legal entity. Resolve name collisions/forks/bridged versions; block and UTC.}}

## 02 · Full stack and mechanism

{{Five layers: venue protocol, vault/curator, underlying assets/counterparties, oracles/bridges/keepers, front end. Who pays, what the wrapper adds, where the cash flow originates. Include a stack diagram or table.}}

## 03 · Product and real usage

{{Customer problem, product, pricing, distribution, retention, active users, volume, utilization, concentration. Paid vs incentivized, external vs related-party. Evidence: protocol API, dashboard, chain.}}

## 04 · Market and competition

{{Bottom-up market, 3–5 peers, share, fee/rate/latency/chain distribution, liquidity network effects, switching costs, moat, fork/price-war risk. Chart: market share or TVL/volume.}}

## 05 · Fees, revenue and unit economics

{{Activity → gross fees → supply-side revenue → protocol revenue → tokenholder revenue → earnings. Revenue/unit, cost/unit, margin, incentive intensity, treasury runway. Table plus stress test.}}

## 06 · Token and value capture

{{Rights ladder, supply bridge, float/FDV, emissions/unlocks, insider/VC allocation, buyback/burn funding, token-as-collateral reflexivity, governance. Table.}}

## 07 · Liquidity, exit, execution and stress

{{Depth at size, slippage, queue/cooldown, caps, utilization, bridge latency, CEX/DEX venues, lockups, realized exit cost. Wallet type, official domain/contract, calldata/spender/allowance, simulation, RPC/MEV protection and unwind path. Stress 25/50/100% exit. Chart: exit cost vs size.}}

## 08 · Collateral, credit and liquidation

{{LTV/LLTV, liquidation threshold/bonus/close factor, oracle, keeper incentives, bad debt, isolation/eMode, recursive collateral, rehypothecation, stablecoin depeg. Liquidation path at realistic gas/depth.}}

## 09 · Security and audits

{{Source/bytecode match, audit scope/date/commit/findings/remediation, formal verification, bug bounty, incident history, admin/upgrade/pause powers, multisig/timelock. Table.}}

## 10 · Team, governance, legal and regulatory

{{Founders, verified track record, funding, key-person, conflicts and contributor concentration. Token distribution/delegates/quorum, proposal history, treasury control and emergency powers. Entity, jurisdiction, MiCA/securities/sanctions/KYC-AML, custody, tax, insurance/risk transfer; counsel caveat.}}

## 11 · Dependencies and systemic risk

{{Bridges, oracles, stablecoins, LSTs/LRTs, RWA wrappers, curators, keepers, chains/RPCs. Correlation, contagion, double counting, composed positions. Cluster map.}}

## 12 · Market structure, technical and community

{{Price/volume, funding/basis, volatility, drawdown, relative strength, depth; social/GitHub/governance/news/catalysts. Label sentiment as signal. Technicals only if timing matters.}}

## 13 · Valuation

{{Method and why; P/F, P/S, P/E or scenario range; reverse valuation; fee-split adjustment; expected return including total-loss branch. Chart: valuation range.}}

| Scenario | Key assumption | Value / return | Versus current |
|---|---|---:|---:|
| Bear | | | |
| Base | | | |
| Bull | | | |

## 14 · Risk, stress and portfolio fit

{{Risk matrix (probability/impact), tail scenarios, correlations, drawdown, liquidity, jurisdiction, cluster exposure. No composite score. Suitability only with constraints.}}

## 15 · Decision and monitoring

{{Gate, conditional verdict, two or three falsifiers, monitoring dashboard (metric, current, threshold, source, frequency), what would change the size.}}

## Sources and methodology

{{Numbered sources, as-of dates, definitions (TVL, fees, revenue, tokenholder revenue, FDV), data conflicts, evidence classes, out of scope.}}
