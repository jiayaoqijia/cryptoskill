# 12 — Methodology and Sources

## Purpose

Make the analysis reproducible, source-bounded, and honest about what is not known.

## Inputs

- The question being answered and the asset/portfolio scope.
- The source matrix and access status.
- The evidence class required for the conclusion.
- The date, currency, and window.

## Method

1. Choose the narrowest source that answers the question.
2. Probe it in the current session; record the timestamp.
3. Cross-check material numbers with a second source.
4. Map the result to a formula or a named rule.
5. Label the evidence class and limitations.
6. If the source is unavailable, degrade; do not substitute a guess.


## Source matrix

Probed 2026-10-30 unless noted.

| Source | Endpoint / reference | Auth | What it proves | Status |
|---|---|---|---|---|
| DefiLlama protocols | `GET https://api.llama.fi/protocols` | None | Protocol list, TVL, chain | Probed: HTTP 200, 8,880 rows, 9.44 MB |
| DefiLlama protocol | `GET https://api.llama.fi/protocol/aave` | None | Protocol detail | Probed: HTTP 200, 10.87 MB |
| DefiLlama fees | `GET https://api.llama.fi/summary/fees/aave?dataType=dailyFees` | None | Fees/revenue | Probed: HTTP 200, 730 KB |
| DefiLlama yields | `GET https://yields.llama.fi/pools` | None | Pool yields/TVL | Probed: HTTP 200, 10.89 MB |
| Binance | `GET https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=2` | None | Price history | Probed: HTTP 200 |
| CoinGecko | `GET https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd` | None | Price cross-check | Probed: HTTP 200; rate-limited |
| Alternative.me | `GET https://api.alternative.me/fng/?limit=1` | None | Sentiment context | Probed: HTTP 200 |
| Taostats | `GET https://api.taostats.io/v1/accounts/{address}` | API key | Bittensor balances/alpha | Probed: HTTP 200 with key |
| Taostats identities | `GET https://api.taostats.io/v1/subnets/identities` | API key | Subnet names | Probed: HTTP 200 with key |
| DeBank | Public profile page | None | EVM positions | Cloudflare/JS risk; use extraction/browser fallback |
| Dune | API | API key | Custom SQL/on-chain | Not verified; key required |
| Token Terminal | API | Paid/enterprise | Fundaments/revenue | Not verified; key required |
| Glassnode | API | Paid | On-chain metrics | Not verified; key required |

**Rule:** a source that did not answer in the current session is not cited as live. A paid source is not “integrated” until an authenticated probe succeeds.

## Professional methodology sources

- CFA Institute, *Elements of an Investment Policy Statement for Individual Investors* (2010). https://rpc.cfainstitute.org/sites/default/files/-/media/documents/article/position-paper/investment-policy-statement-individual-investors.pdf
- CFA Institute, *Overview of the Global Investment Performance Standards* (2026). https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-of-the-global-investment-performance-standards
- CFA Institute, *Measuring and Managing Market Risk* (2026). https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/measuring-managing-market-risk
- CFA Institute, *Introduction to Risk Management* (2026). https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/introduction-risk-management
- CFA Institute, *Asset Allocation with Real-World Constraints* (2026). https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/asset-allocation-with-real-world-constraints
- FSB, *The Financial Stability Risks of Decentralised Finance* (2023). https://www.fsb.org/2023/02/the-financial-stability-risks-of-decentralised-finance/
- arXiv 2507.08915, *Quantifying Crypto Portfolio Risk* (2025). https://arxiv.org/html/2507.08915v1
- Chainalysis, *2025 Crypto Theft Reaches $3.4 Billion* (2025-12-18). https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2026/

## Method map

| Method | Where |
|---|---|
| IPS-lite, constraints, benchmark | `01-mandate-and-intake.md` |
| Fair-value hierarchy, reconciliation | `02-data-and-valuation.md` |
| Weights, HHI, TWR/MWR, attribution | `03-allocation-and-performance.md` |
| Volatility, drawdown, VaR/CVaR, beta, stress | `04-risk-and-correlation.md` |
| Exit days, queues, stress liquidity | `05-liquidity-and-exit.md` |
| Supply, emissions, value capture | `06-tokenomics-and-value-capture.md` |
| Lending/LP/staking, health factor, flows | `07-defi-and-onchain.md` |
| Regime, scenarios, reverse stress | `08-market-regime-and-scenarios.md` |
| Custody, keys, bridges, legal/tax | `09-security-counterparty-legal.md` |
| Risk budget, rebalancing, behavior | `10-portfolio-construction.md` |
| Report and decision record | `11-reporting.md` |

## Limitations

- Free APIs can rate-limit, change schema, or omit small assets.
- Long-tail token prices and liquidity may be unreliable.
- On-chain entity labels are probabilistic.
- DeFi positions require exact contract/market resolution; unsupported positions must be flagged.
- Cost basis and tax lots are often unavailable.
- VaR/CVaR are model-dependent and do not capture all tail or liquidity risk.
- No analysis can verify off-chain reserves without attestations.
- The skill is read-only and cannot execute, custody, or recover assets.

## Failure modes

- Citing a source that was not read or queried in this session.
- Treating a team claim as verified.
- Using a price without a timestamp.
- Hiding an unavailable source behind a generic “market data.”
- Averaging contradictory sources.
- Presenting a model output as observed data.

## Evidence rules

1. A material number needs source, date, definition, and evidence class.
2. Report claims are `REPORTED`, not `VERIFIED`.
3. Model outputs are `MODELED`; show assumptions.
4. Missing inputs are `not assessable`, not zero.
5. Contradictory sources are reported, not averaged.
6. No source is cited if it was not actually read or queried in this session.
