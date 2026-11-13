---
name: ac-stablecoin-collateral-risk
description: "Use when asking about stablecoin risk, collateral haircuts, depeg events, and margin safety on perpetual venues. Not for venue evaluation (ac-perp-venue-diligence), not for liquidation geometry in general (ac-liquidation-risk-management), not for the risk budget (ac-crypto-trading-discipline). Covers haircuts, redemption gates, cross-collateral contagion, and the depeg playbook, with the record as the deliverable."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# Stablecoin Collateral Risk

Stablecoin and digital asset collateral on perpetual futures exchanges forms the foundational layer of margin stability. Venue risk policies dictate which assets are accepted as margin, assigning specific haircuts that discount nominal value based on perceived liquidity and volatility risk. Stablecoins are not homogeneous; their structural backing varies from fiat reserves held in short-duration Treasury bills and cash equivalents to over-collateralized crypto assets and algorithmic models. Attestations are periodic point-in-time assertions issued by accounting firms, whereas audits involve comprehensive examinations of internal controls and financial statements over a full fiscal period. A claim by an issuer regarding asset backing differs fundamentally from a verified, on-chain or custodian-attested reserve that is independently auditable in real-time. Evaluating collateral quality requires examining the legal right of redemption, the liquidity profile of the underlying assets, and the jurisdictional framework governing the issuer. Publicly available reports such as the Tether Assurance Reports published at https://tether.to/en/transparency/ provide issuer-side breakdowns of commercial paper, US Treasuries, and cash equivalents. Similarly, Circle publishes monthly attestations regarding USD Coin reserves audited by independent accounting firms, accessible at https://www.circle.com/en/transparency/. Understanding the exact composition of collateral assets prevents miscalculating margin safety when venue haircut policies shift abruptly during market stress. Furthermore, cross-margin systems aggregate all account collateral and unrealized profits to support open positions across multiple trading pairs, creating efficiency at the cost of systemic contagion risk. When a portfolio holds mixed collateral types—such as pairing volatile crypto assets with stablecoins—a sharp price drop in one asset devalues the total account collateral pool, automatically endangering positions in entirely unrelated markets. Detailed references and institutional frameworks governing collateral evaluation, depeg mechanics, liquidation arithmetic, custody architecture, cross-margin contagion, monitoring systems, and crisis playbooks are indexed below to provide a rigorous foundation for risk management professionals.

## Subskills Index

| File | Domain | Scope |
|---|---|---|
| `subskills/collateral-quality.md` | `crypto-trading/collateral-quality` | What venues accept, haircuts, attestations vs audits, and the difference between a claim and a verified reserve. |
| `subskills/depeg-mechanics.md` | `crypto-trading/depeg-mechanics` | How a peg breaks: reserve runs, redemption gates, chain congestion, market-depth failure; the recurrent pattern from public episodes. |
| `subskills/haircuts-and-liquidation-distance.md` | `crypto-trading/haircuts-and-liquidation-distance` | How a haircut or a depeg moves your liquidation price; the arithmetic worked through. |
| `subskills/custody-vs-collateral.md` | `crypto-trading/custody-vs-collateral` | Where the collateral actually sits (venue omnibus, on-chain escrow, third-party custodian); the counterparty chain. |
| `subskills/cross-collateral-contagion.md` | `crypto-trading/cross-collateral-contagion` | Mixed collateral under cross margin; correlation and contagion; why the same asset on both legs is not diversification. |
| `subskills/collateral-monitoring.md` | `crypto-trading/collateral-monitoring` | Peg monitors, redemption status, issuer disclosures, venue haircut changes; the tripwires that force action. |
| `subskills/depeg-playbook.md` | `crypto-trading/depeg-playbook` | During a depeg: the decision order (reduce exposure, swap collateral, move venue), and what never to do (market orders into a gapped book). |

## Sources
- Tether Transparency and Reserves: https://tether.to/en/transparency/
- Circle USD Coin Transparency: https://www.circle.com/en/transparency/
- National Bureau of Economic Research: https://www.nber.org/
- Bank for International Settlements: https://www.bis.org/
- Investopedia Margin Guides: https://www.investopedia.com/
- Global Association of Risk Professionals: https://www.garp.org/
- Depository Trust and Clearing Corporation: https://www.dtcc.com/
- International Organization of Securities Commissions: https://www.iosco.org/
- CoinMarketCap Real-Time Data: https://coinmarketcap.com/
- U.S. Securities and Exchange Commission: https://www.sec.gov/
- Futures Industry Association: https://www.fia.org/
