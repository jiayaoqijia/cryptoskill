# Methodology and Sources

## Research principles

This is an analyst workflow, not a universal scoring formula. Use primary evidence where possible, reconcile definitions and source dates, and distinguish measured facts from issuer claims, third-party estimates, and analyst inference. Cross-source confirmation is meaningful only when sources are independent; multiple dashboards may repeat one upstream dataset.

For token, protocol, subnet and DeFi-position work, `references/crypto-diligence.md` is the operative checklist; the asset-class table below is a selection index, not the procedure. Crypto is the primary track, and every other row remains available.

## Coverage map

| Lens | Reference |
|---|---|
| Decision, suitability, depth | `SKILL.md` |
| Business/product, market, asset-class lenses | this file |
| Demand, revenue, unit economics | `references/crypto-unit-economics.md` |
| Team, funding, cap table, related parties | `references/team-and-org.md` |
| Instrument rights, supply, unlocks, audits, incidents | `references/crypto-diligence.md` |
| Ownership, holders, staking, protocol flows, control | `references/crypto-onchain-flows.md` |
| Technical and market structure | `references/crypto-technical.md` |
| Risk, portfolio fit, suitability, macro | `references/portfolio-fit.md` |
| Community, news, sentiment, catalysts | `references/crypto-market-intelligence.md` |
| Legal, regulatory, security | `references/crypto-legal-security.md` |
| Valuation bridge, scenarios, expected return | `references/crypto-valuation.md` |
| PDF production | `references/pdf-report-production.md` |
| Output skeletons | `templates/investment-raporu-tr.md`, `templates/investment-report-full-tr.md`, `templates/investment-committee-tr.md`, `templates/investment-analysis.md` |

## Research basis

- **Public-company disclosures:** SEC Investor.gov explains that 10-K/10-Q filings include business descriptions, risk factors, management discussion, audited/unaudited financial statements, liquidity and material changes. EDGAR is a route to primary filings. A filing is issuer disclosure subject to regulatory rules, not an SEC guarantee of investment quality.
  - https://www.investor.gov/introduction-investing/getting-started/researching-investments/how-read-10-k
  - https://www.investor.gov/introduction-investing/getting-started/researching-investments/using-edgar-research-investments
- **Valuation:** CFA Institute covers present-value, multiple, and asset-based valuation families. Expected cash flows, growth, discount rates, and assumptions matter; multiples are not standalone proof of cheapness.
  - https://cfainstitute.org/insights/professional-learning/refresher-readings/2026/equity-valuation-concepts-basic-tools
  - https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/free-cash-flow-valuation
  - https://rpc.cfainstitute.org/blogs/enterprising-investor/2022/investings-first-principles-the-discounted-cash-flow-model
- **Portfolio risk and performance:** CFA Institute explains risk/return and evaluation methods, including assumptions and limitations. Match the measure to benchmark, horizon, asset liquidity, and data quality; do not infer skill from one ratio.
  - https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-risk-return-part-2
  - https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-performance-evaluation
  - https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/introduction-risk-management
- **Sector-specific financial analysis:** CFA Institute treats banks and insurers with distinct asset-quality, capital, liquidity/funding, market-risk, and loss-reserve considerations. Do not apply industrial-company metrics blindly to regulated financial institutions.
  - https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/analysis-of-financial-institutions
  - https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/equity-valuation-applications-and-processes
- **Bonds / credit:** FINRA's investor materials explain rate, duration, call, credit and yield-to-worst concepts; use primary offering terms and issuer data for a specific security.
  - https://www.finra.org/investors/investing/investment-products/bonds
  - https://www.finra.org/investors/insights/bond-yield-return
- **Funds / ETFs:** SEC Investor.gov explains NAV, market-price premiums/discounts, fees and other structural features. Read the actual prospectus and fund disclosures for mandate-specific analysis.
  - https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-24
  - https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/characteristics-mutual-funds-exchange-traded-funds
- **Private offerings:** SEC Investor.gov flags limited disclosure, illiquidity and total-loss risk in private placements. This does not replace jurisdiction-specific legal review or instrument-term analysis.
  - https://www.sec.gov/oiea/investor-alerts-and-bulletins/private-placements-under-regulation-d-investor-bulletin
- **Technical-analysis evidence:** Park and Irwin's literature review reports mixed evidence and recurring issues including data snooping, ex-post rule selection, and estimation of risk and trading costs. It is a dated review, not proof that any current signal works. Before claiming predictive edge, require execution costs, lagged execution, out-of-sample or walk-forward testing, the null and buy-and-hold comparison, and the number of variants tested.
  - https://ageconsearch.umn.edu/record/37487
  - https://doi.org/10.1111/j.1467-6419.2007.00519.x
- **Digital-asset/token diligence:** EY's 2024 framework groups diligence across strategic/reputational, technical, financial/tokenomics, legal/compliance, cybersecurity, and auditability. Use it as a checklist scaffold, not endorsement or assurance.
  - https://ey.com/content/dam/ey-unified-site/ey-com/en-us/insights/financial-services/documents/ey-token-due-diligence-a-structured-approach-to-evaluate-digital-asset-risk.pdf
- **Bittensor:** Emission documentation and runtime mechanics are version-sensitive. Official pages can differ across dates/versions. Check current official docs, runtime/source, network/version, and chain state rather than copying a remembered formula.
  - https://www.bittensor.com/docs/concepts/emissions
  - https://docs.bittensor.com/learn/emissions
  - https://github.com/opentensor/subtensor

## Asset-class and sector selection

Apply only the rows relevant to the instrument; do not force a universal ratio set or treat a checklist as proof of quality. If a key metric is unavailable, explain whether that prevents valuation or only lowers confidence.

| Instrument / business | Decision-critical checks to select |
|---|---|
| Public operating company | Business model and industry position; segment economics; earnings/cash conversion; debt, leases, guarantees and off-balance-sheet obligations; consensus revisions and short interest as positioning inputs; management/capital allocation; fit-for-sector multiples and cash-flow valuation. For banks and insurers, use regulatory capital, asset/credit quality, funding/liquidity, interest-rate sensitivity, reserves/combined ratio and solvency measures rather than mechanically applying industrial-company leverage or FCF ratios. |
| SaaS / software | ARR/revenue recognition, gross and net retention by cohort, churn/expansion, customer concentration, CAC/payback where measurable, stock-based compensation/dilution, cloud/infrastructure costs and monetization quality. |
| Biotech / pharmaceuticals | Clinical stage and trial design/endpoints, regulatory pathway and dated catalysts, patent/exclusivity, cash runway and financing dilution, commercial access, and explicit failure/downside case. Do not treat a trial result or approval probability as certain. |
| REIT / property company | Property-type and geography mix, occupancy/rent roll, same-property NOI, FFO/AFFO definitions and adjustments, leverage/debt maturities, cap-rate sensitivity, payout coverage and asset-level liquidity. |
| Retail / consumer | Comparable-store/same-customer sales, traffic vs ticket, gross margin/promotions, inventory age/markdowns, store economics, leases/working capital and brand/channel concentration. |
| Fixed income / credit | Seniority/security, issuer repayment capacity, covenants and recovery; maturity/refinancing, duration/convexity, calls/puts, credit-spread and default scenarios; compare yield-to-maturity and yield-to-worst as applicable, after fees/tax where known. A stated yield is not a guaranteed realized return. |
| Fund / ETF / private fund | Mandate and actual holdings; benchmark and net-of-fee returns; expense/carry and liquidity terms; concentration, leverage, tracking error, NAV methodology/premium-discount, manager/custody/valuation controls, redemption gates and tax/jurisdiction. |
| Private company / venture / project | Founder/team capability and role coverage, documented track record and key-person risk; evidence provenance (management claims vs verified records); capitalization table; security rights, preference/waterfall, dilution and follow-on needs; runway, financing access, governance/information rights, transfer restrictions, realistic exit path and total-loss case. |
| Real estate / infrastructure / real asset | Asset condition/title/permits, occupancy and lease/rent roll, normalized NOI/operating costs, maintenance and capex, financing/DSCR, comparable transactions, liquidity, environmental/insurance and jurisdiction risks. |
| Commodity producer / commodity exposure | Cost curve, reserves/resource quality and decline, sustaining/growth capex, inventory/supply response, benchmark basis, storage/carry/roll yield, hedging and geopolitical/permit exposure. Distinguish a producer's equity economics from the commodity's spot return. |
| Options / derivatives / structured products | Payoff at expiry and before expiry, notional/leverage, Greeks/path dependence, volatility/skew, margin/collateral, barrier/call features, counterparty, liquidation, liquidity, fees and loss bounds. If payoff cannot be reconstructed from terms, do not recommend or price it. |
| Token / protocol | Crypto is the primary track. Operate `references/crypto-diligence.md` Tier 1–2 for identity, supply truth, privileged control, claim chain, legal eligibility, rights, unlocks, governance, audits, incidents, treasury and exit; then `references/crypto-unit-economics.md` for revenue quality and unit economics; `references/crypto-valuation.md` for the business-vs-token bridge; `references/crypto-onchain-flows.md` for holders and flows; `references/crypto-technical.md` for market structure; `references/crypto-market-intelligence.md` for community/news/catalysts; `references/crypto-legal-security.md` for legal/security; and `references/team-and-org.md` for team/funding. This row is a summary, not the procedure. |

For cyclical, regulated, early-stage, or event-driven businesses, identify the cycle/stage and normalize across it; do not project a peak/trough period as a steady state. Relevant macro and policy inputs must enter through an explicit cash-flow, discount-rate, funding, or demand channel rather than a generic narrative.

## When financial statements do not exist

Use a fallback ladder rather than writing N/A, and state which step was used: (1) audited or reviewed financial statements; (2) regulatory filings and offering documents; (3) on-chain fee and treasury flows reconciled to addresses; (4) issuer-reported metrics with definition and period; (5) third-party estimates with method; (6) bottom-up reconstruction from observable unit data; (7) declared unknown with its effect on the conclusion. Steps 4–6 support a lower-confidence view, not an unqualified valuation. Step 7 caps the conclusion at `insufficient evidence` when the missing figure is gate-relevant.

## Report modes

- **Screen:** 1 page, 300–500 words; gate, business quality, valuation range, three risks, verdict.
- **Standard:** 3–5 pages; all core lenses, compressed technical/community, one chart per key lens.
- **Deep:** 8–15 pages PDF + 1-page IC summary + workpaper; all 14 lenses, charts, scenarios, risk matrix, monitoring dashboard.
- **Non-compressible minimum:** gate status, as-of timestamp, lens/horizon/numeraire, valuation range or scenario, liquidity/exit, top three risks, falsifiers, monitoring signal, sources.

## Source-use rules

1. Primary filings/chain state > issuer documents > independent research > media > social. A source that copies another is not independent.
2. Treat DeSearch and social output as discovery or sentiment unless the underlying claim is independently verified. Social following is not proof of quality.
3. Cite factual claims close to the claim; record publication/effective date, retrieval date, definition, unit and period.
4. Two dashboards sharing one upstream dataset count as one source.
5. If sources conflict (supply, price change, TVL, revenue), show both, choose the primary basis and explain the difference; never average silently.
6. Missing data is unknown, not zero. Never invent a metric, source, date or quote. A declared unknown is a valid result.
7. State jurisdiction, accounting regime, protocol/contract version and asset-right differences; do not universalize local rules.
8. Search snippets support only what they literally state; inspect the filing, page or code for material conclusions.
9. For PDF reports, follow `references/pdf-report-production.md`: A4, page numbers, chart source captions, embedded Turkish-capable font, no internal checklist.
