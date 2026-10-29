---
name: professional-investor-analysis
description: "Use when evaluating a token, protocol, company, fund or asset."
version: 0.4.1
author: Hermes Agent and contributors
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [investment, due-diligence, valuation, risk, crypto, technical, sentiment]
---

# Professional Investor Analysis

Evidence-led, multi-lens investment research for a crypto token, protocol, subnet or DeFi position — and for equities, credit, funds, private projects, real assets, commodities and derivatives. The standard is an investment-committee memo: every material lens is covered or explicitly excluded, every number has a source and date, and the conclusion is conditional and falsifiable. Crypto is the primary track; the other asset classes remain fully available. Not licensed investment, legal, tax or accounting advice. Never claim private information or a professional licence.

## When to Use

- The user asks whether a crypto token, protocol, subnet, DeFi position, company, fund, private project or other asset is worth buying, holding, comparing or exiting.
- The user asks for fundamental/technical analysis, tokenomics, valuation, due diligence, an investment memo or a full PDF report.
- A protocol is under stress (depeg, paused withdrawals, exploit) and the user needs a hold/exit/recovery judgment.

Not for a price lookup, a trade signal, or advice that depends on personal facts the user has not supplied.

## The Professional Standard — every lens

A professional investor does not look at one dimension. Cover each lens below, or mark it `not material` or `not assessable` with a reason. Silent omission is a defect.

| # | Lens | Core question | Reference |
|---|---|---|---|
| 1 | Decision and suitability | What decision, horizon, benchmark, constraints? | this file |
| 2 | Business/project quality | Real product, customer, moat, unit economics? | `references/crypto-unit-economics.md`; `references/methodology-and-sources.md` |
| 3 | Market and competition | Market structure, peers, share, pricing power, cycle/macro transmission? | `references/methodology-and-sources.md` |
| 4 | Demand, revenue and unit economics | Paid vs induced demand, retention, concentration, margin? | `references/crypto-unit-economics.md` |
| 5 | Team, organization and governance | Founders, key roles, funding, incentives, key-person? | `references/team-and-org.md` |
| 6 | Instrument rights | What does the holder own, and what claim is enforceable? | `references/crypto-diligence.md` |
| 7 | Token economics | Supply, emissions, unlocks, burns, value capture? | `references/crypto-diligence.md`; `references/crypto-valuation.md` |
| 8 | Ownership, on-chain flows and control | Who holds, who buys/sells, who can change the rules? | `references/crypto-onchain-flows.md` |
| 9 | Technical and market structure | Trend, relative strength, volatility, liquidity, derivatives? | `references/crypto-technical.md` |
| 10 | Community, news and catalysts | Narrative, sentiment, developer activity, dated events? | `references/crypto-market-intelligence.md` |
| 11 | Legal, regulatory and security | Jurisdiction, classification, audits, keys, incidents? | `references/crypto-legal-security.md` |
| 12 | Valuation | What is priced, what is it worth, what return? | `references/crypto-valuation.md` |
| 13 | Risk and portfolio fit | What can go wrong, correlation, liquidity, suitability, material ESG? | `references/portfolio-fit.md`; `references/crypto-technical.md` |
| 14 | Decision and monitoring | Verdict, conditions, KPIs, falsifiers? | this file |

## Deliverable modes

| Mode | Length | Use | Must contain |
|---|---|---|---|
| **Screen** | 1 page, 300–500 words | Quick filter, first look | Gate, business quality, valuation range, 3 risks, verdict |
| **Standard** | 3–5 pages | Ordinary analysis | All core lenses, compressed technical/community, one chart per key lens |
| **Deep** | 8–15 pages PDF + 1-page IC summary + workpaper | Buy/size/hold, full/every-angle request | All 14 lenses, charts, scenarios, risk matrix, monitoring dashboard, full sources |

- Crypto and token requests default to at least **standard**; a buy/size/hold decision defaults to **deep**.
- A request for "full", "every angle" or "professional report" activates **deep**; do not silently downgrade it.
- Report length constrains presentation, not diligence. A short note still requires the relevant workpaper.
- **Non-compressible minimum** in every mode: gate status, as-of timestamp, lens/horizon/numeraire, valuation range or scenario, liquidity/exit, top 3 risks, falsifiers, monitoring signal, sources.

**Report architecture (standard/deep):** cover → one-page executive summary (what, why now, verdict, three numbers) → business/product → market/competition → demand and unit economics → team/org → instrument and token economics → ownership/flows → technical/market structure → community/news/catalysts → legal/security → valuation → risks/stress tests → decision matrix and monitoring → sources/methodology. Deep mode adds charts and a 1-page IC summary.

**PDF production:** A4; 9.5–11 pt body; sans-serif headings; 1–2 charts per major section; every chart carries a source/date caption; page numbers; no internal checklist, placeholder or empty table in the delivered file. A one-page executive summary is mandatory in deep mode. Production details: `references/pdf-report-production.md`.

Templates: English `templates/investment-screen-en.md`, `templates/investment-memo-en.md`, `templates/investment-report-en.md`, `templates/investment-committee-en.md`, `templates/investment-analysis.md` (workpaper); Turkish equivalents `templates/investment-raporu-tr.md`, `templates/investment-report-full-tr.md`, `templates/investment-committee-tr.md`.

## Prerequisites

- Web search and page extraction for public sources; a browser or HTTP client for JS-rendered protocol state, dashboards and filings.
- Read-only chain/RPC access for contract state; no signing, custody or transaction execution.
- A citation discipline: record source, date, definition and independence for every material number.
- Never expose API keys. Record an inaccessible source as a gap; never fill it with a plausible number.

## Procedure

1. **Frame the decision.** Asset, decision (screen, compare, value, timing, hold/exit), horizon, benchmark/numeraire, jurisdiction if material, and the user's suitability inputs if offered. Missing facts become labelled assumptions; ask only when the answer changes the work or the authority.

2. **Map the asset and claims.** Issuer/entity, instrument rights, product, customer, revenue path, control/governance, venues, peers. Convert promotional claims into testable questions. Keep project quality separate from the value of its token or security. For non-crypto assets, map the equivalent: share class, fund terms, credit covenants, property leases, option payoff.

3. **Build the evidence ledger** in the workpaper. Per material claim: claim, type (fact / issuer claim / estimate / inference), value with unit and date, source and its independence, status. Primary sources first: filings, audited statements, contract state, protocol code, governance records. Crypto reads record chain + chain ID + full contract address + function/selector + block + retrieval time; resolve ticker → address before using any metric. Explorer labels, aggregator labels and issuer-reported supply are claims.

4. **Check freshness and comparability.** Align identity, contract/ticker, supply definition, accounting period, timezone, currency and timestamp before calculating. Market-data contract: venue, pair, quote currency, price type (last / mark / index / pool mid), UTC timestamp, provider, plus a second venue or the primary DEX pool; flag divergence. Use a series adjusted for splits, redenominations and token migrations. Never silently impute, mix market-cap conventions, present a token-denominated return as a USD return, or treat nominal volume as executable liquidity.

5. **Analyze the business/project.** Customer problem, willingness to pay, paid versus incentive-farmed activity, retention, pricing power, competition and substitutes, moat, market structure, concentration. Financial quality when statements exist: revenue recognition and composition, margins, operating cash flow versus earnings, working capital, capex, debt/maturities, off-balance-sheet obligations, leases and guarantees, accruals/capitalization and revenue-recognition red flags, dilution, auditor opinion, related parties. When statements do not exist, use the fallback ladder in `references/methodology-and-sources.md`; never write N/A by default. Unit economics when measurable (see `references/crypto-unit-economics.md`).

6. **Map the market and competition.** Size the market bottom-up where possible; state reachable share and the adoption constraint. Select 3–5 peers and compare product, price, latency, uptime, model/asset coverage, market share, liquidity and unit economics — not market cap alone. Test the moat: switching costs, network effects, integrations, data, licences, cost advantage, fork/copy risk. Place the market in its cycle; use macro/policy only through a named cash-flow, discount-rate, funding or demand channel.

7. **Analyze demand, revenue and unit economics.** Separate paid from incentive-farmed or related-party demand; customer concentration; prepaid/committed versus spot; churn/retention; revenue per unit (user, GPU, store, contract); cost per unit; gross margin; CAC/payback; miner/validator ROI where relevant. Revenue is not profit; TVL is not revenue; emissions are not revenue.

8. **Analyze the team, organization and governance.** Founders, critical roles, verified track record, prior failures, capital allocation, key-person dependence, retention/incentives, ownership, board, succession, funding runway, cap table and related entities. For crypto: doxxed or pseudonymous, insider allocation, vesting, control of treasury/contracts. Verify biographies; mark unverifiable claims. See `references/team-and-org.md`.

9. **Analyze the instrument and token economics.** Reconcile supply first — max, total, circulating, effective float, treasury, locked/vesting, unclaimed emissions — with source and date per row; state which basis backs market cap and which backs FDV. Then: rights ladder and where the right lives (code or documents only); vesting/unlock overhang by month against float and volume; emissions and burns with funding source; distribution and labeled holder concentration; governance execution; privileged control; audit scope bound to the deployed commit; claim chain and redeemability; incidents; venues/listing/liquidity; legal/transfer restrictions; exit paths. Use `references/crypto-diligence.md` and `references/crypto-onchain-flows.md`. For non-crypto instruments, use the matching row in `references/methodology-and-sources.md`: share class and rights, credit covenants/recovery, fund terms/liquidity, lease/NOI, or option payoff.

10. **Analyze ownership and on-chain flows.** Holder concentration and cohorts (team, foundation, treasury, investors, miners, validators, retail, CEX, bridges); net staking/unstaking; protocol buys/burns; root sells; cross-subnet flows; treasury outflows; miner/validator concentration and take rates; conviction locks and takeover cost. Explain who is buying and who is selling. For equities: insider ownership/transactions, institutional concentration, buybacks/dilution.

11. **Analyze technicals and market structure.** Always include a compressed market-structure paragraph in standard/deep, even when timing is not the question: trend, relative strength versus the natural benchmark, volatility, drawdown, volume, depth, slippage, venue concentration, and derivatives positioning where a perpetual exists. Label it descriptive context, not a valuation input. Pin conventions (daily UTC closes, 30d/90d/1y windows, annualisation). Use `references/crypto-technical.md`. Full technical section and backtest protocol only when timing or strategy evidence is requested.

12. **Analyze community, news and catalysts.** Community size/engagement, Discord/Telegram, GitHub contributors/issues/releases, governance forum activity, news flow, sentiment and dated catalysts. Social and news are **signals**, not evidence; verify material claims against primary sources and label each item. Build a catalyst calendar with dates, status and why it matters. Use `references/crypto-market-intelligence.md`.

13. **Analyze legal, regulatory and security.** Issuer entity/jurisdiction, token classification, securities/commodities law, MiCA/other regimes, KYC/AML, sanctions, transfer restrictions, tax, venue eligibility. Security: audits (scope, commit, findings, remediation, re-audit, bounty), admin/upgrade/pause/blacklist powers, oracle, bridge, custody, incident history, post-mortems. For non-crypto, replace token classification with the relevant regulatory/licensing regime and treat security as material only where the business depends on it. Use `references/crypto-legal-security.md`. This is analysis, not a legal opinion.

14. **Value the instrument.** State why each method fits or does not. Cash-flowing assets: DCF/FCF, comparable multiples and asset-based cross-checks, explicit assumptions, discount rate, terminal value, dilution/debt/cash, sensitivity, reverse valuation. Private projects: stage, terms, control, illiquidity, exit uncertainty. Tokens without enforceable cash flow to holders: do not force a DCF or P/E; use labelled anchors and name each distortion. State every valuation on float and fully diluted bases with the convention beside the number. Build a valuation bridge, scenario table and expected return; see `references/crypto-valuation.md`. For credit use yield/spread/recovery, rating and rating trajectory, covenants and duration; for funds use NAV, fees, track record and liquidity; for real assets use NOI/cap rate; for options use payoff/Greeks and implied volatility.

15. **Stress-test and red-team.** Risk matrix (likelihood/impact), pre-mortem, tail scenarios (revenue halved, TAO -30%, emissions +20%, liquidity -50%, exploit/key compromise), correlation and drawdown. Strongest counter-thesis; per driver: evidence, uncertainty, metric/source to monitor, timeframe, falsification condition. Separate fundamental, valuation and technical invalidation.

16. **Decide, monitor and deliver.** Report gate status separately from project quality, instrument attractiveness, timing and suitability. Use the dimension matrix, not a single composite score. Confidence with reasons, strongest counterargument, unresolved gaps, reversal conditions. Build the monitoring dashboard. Run the completeness check: every lens covered or excluded; every material claim sourced or marked unverified; units, dates and definitions aligned; no missing value became zero; activity not mislabelled revenue/profit; token rights/supply/dilution addressed; technicals not presented as fundamentals; liquidity executable at the stated size; report language/length/anatomy match the mode; no internal checklist in the delivered file. Fix or name as a limitation.

## Gates and standards

- **Investability gate (non-compensatory):** holder rights, identity/ownership, credible custody and exit, verifiability of critical claims. For tokens add contract identity on the stated chain, supply truth, privileged control, claim chain/redeemability, legal eligibility/transferability. Use `pass`, `conditional`, `fail`, `insufficient evidence`; a growth story, score or technical signal never offsets a failure. A critical unknown is `insufficient evidence`, not `conditional`. Render the gate in the report language (`uygun` / `koşullu` / `uygun değil` / `kanıt yetersiz`).
- **Depth gate:** screen, standard, deep. "Full/every angle" and buy/size/hold activate deep; do not silently substitute a quick screen.
- **No composite score by default.** A one-number score without criteria, weights, coverage, direction, sensitivity and validation is not a professional model. Use a dimension matrix; if the user insists on a score, show the full formula and sensitivity.
- **Suitability:** use the user's horizon, tolerable drawdown, liquidity needs, liability currency, jurisdiction/eligibility and existing concentration. If absent, write "suitability not assessable — requires <inputs>"; never assume or prescribe allocation.
- **Behavioral check:** if the user owns the asset or has a prior view, examine anchoring, sunk-cost, confirmation, recency, loss aversion and overconfidence. Never infer position size or suitability from the conversation.
- **Decision vocabulary:** `uygun` / `izle` / `kaçın` / `kanıt yetersiz` (asset-level; not a personal recommendation).

## Evidence rules

- Primary > issuer documents > independent research > media > social. Two pages copying one upstream dataset are one source.
- Label every claim: fact, issuer claim, third-party estimate, inference. Missing data is unknown, not zero. Never invent a metric, source, date or quote.
- If sources conflict (supply, price change, TVL, revenue), show both, pick the primary basis, explain the difference; never average silently.
- Date-stamp every market and on-chain metric; state the snapshot timezone.
- Do not cite a discovery snippet as if the underlying page was read.
- Do not treat an audit badge, a listing, a partnership announcement or a social following as proof of quality.

## Pitfalls

- Do not conflate project adoption, company revenue, accounting profit, protocol revenue, token burn or holder value accrual.
- Do not infer undervaluation from a small market cap, high TVL, request counts, staking yield or a burn event; decompose yield into emission-funded and fee-funded parts.
- Do not treat TVL as revenue or protocol-owned capital; state double-counting and incentive-adjusted figures.
- Do not treat an audit badge as proof of safety; bind scope/date to the deployed commit and check post-audit changes.
- Do not present a governance-only token as a residual claim, or a discretionary burn/buyback as enforceable value capture.
- Do not let a score, narrative, community size or momentum override a gate failure.
- Do not select only favourable periods, peers, benchmarks or sources; disclose null and conflicting evidence.
- Do not let a disclaimer substitute for uncertainty, falsifiers or evidence.
- Do not let a 1–2 page limit silently remove critical sections; use the non-compressible minimum.
- Do not ship a PDF without page numbers, source captions and a one-page executive summary.

## Verification

Reopen the final report and check every material number against its cited source, definition and date; recompute calculations with a tool and keep inputs, period and unit. For crypto, confirm the contract address, chain and block behind each state claim and that the price series is migration-adjusted. Confirm the report is in the requested language, matches the chosen mode, contains the non-compressible minimum, and is free of internal scaffolding. The repository validator confirms package structure only; it does not validate an investment conclusion.
