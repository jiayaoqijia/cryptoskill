---
name: collateral-quality
domain: crypto-trading/collateral-quality
trigger: evaluating stablecoin collateral types, comparing venue haircuts, auditing stablecoin issuer attestations, checking reserve backing
anti_trigger: trading perp positions, checking liquidation price math, venue selection, execution sizing
scope: What venues accept, haircuts, attestations vs audits, and the difference between a claim and a verified reserve.
status: seedling
---

## Standard
Stablecoin and digital asset collateral on perpetual futures exchanges forms the foundational layer of margin stability. Venue risk policies dictate which assets are accepted as margin, assigning specific haircuts that discount nominal value based on perceived liquidity and volatility risk. Stablecoins are not homogeneous; their structural backing varies from fiat reserves held in short-duration Treasury bills and cash equivalents to over-collateralized crypto assets and algorithmic models. Attestations are periodic point-in-time assertions issued by accounting firms, whereas audits involve comprehensive examinations of internal controls and financial statements over a full fiscal period. A claim by an issuer regarding asset backing differs fundamentally from a verified, on-chain or custodian-attested reserve that is independently auditable in real-time. Evaluating collateral quality requires examining the legal right of redemption, the liquidity profile of the underlying assets, and the jurisdictional framework governing the issuer. Publicly available reports such as the Tether Assurance Reports published at https://tether.to/en/transparency/ provide issuer-side breakdowns of commercial paper, US Treasuries, and cash equivalents. Similarly, Circle publishes monthly attestations regarding USD Coin reserves audited by independent accounting firms, accessible at https://www.circle.com/en/transparency/. Understanding the exact composition of collateral assets prevents miscalculating margin safety when venue haircut policies shift abruptly during market stress.

## Decision rules
- Rule 1: Never treat all stablecoins as equivalent to cash; classify collateral strictly by its redemption liquidity and regulatory backing.
- Rule 2: Treat an issuer attestation as a point-in-time snapshot rather than a continuous audit; do not rely solely on attestation summaries during high volatility.
- Rule 3: Apply an internal haircut buffer that exceeds the venue's stated margin haircut whenever underlying reserve assets include commercial paper or risk-weighted debt.
- Rule 4: Verify whether the venue permits direct redemption of collateral assets or if conversion is restricted to secondary market liquidity pools.
- Rule 5: Reject any stablecoin collateral whose issuer lacks transparent, publicly verifiable banking partners and independent third-party attestations.

## Procedure
1. Identify the exact list of collateral assets accepted by the trading venue through official risk documentation, such as the Binance collateral margins listed at https://www.binance.com/en/support/faq.
2. Review the most recent monthly reserve report or audit statement published by the stablecoin issuer, checking asset maturity profiles and liquidity.
3. Compare the venue's published margin haircut against the historical volatility and maximum drawdown observed in secondary market liquidity pools.
4. Verify whether the collateral asset maintains an active, deep secondary market order book across multiple independent venues to ensure convertibility.
5. Document the findings in a local risk ledger, noting any discrepancy between issuer claims and verified reserve data before depositing funds.

## Anti-patterns
- Assuming a stablecoin maintains a 1:1 risk profile with fiat currency simply because its secondary market price hovers near parity.
- Relying exclusively on marketing summaries provided by the stablecoin issuer without inspecting underlying reserve composition reports.
- Treating point-in-time attestations as proof of continuous solvency and unencumbered asset custody.
- Ignoring venue-imposed collateral concentration limits that restrict the proportion of alternative stablecoins eligible for margin calculation.

## Done checklist
- [ ] Stated collateral assets verified against official venue margin documentation.
- [ ] Issuer reserve reports and attestations reviewed for asset quality and liquidity.
- [ ] Venue haircuts compared against market-implied depeg risk.
- [ ] Secondary market liquidity and redemption pathways confirmed.
- [ ] Collateral quality assessment recorded without relying on unverified issuer claims.

## Sources
- Tether Transparency and Reserves Documentation: https://tether.to/en/transparency/
- Circle USD Coin Transparency and Audited Reserves: https://www.circle.com/en/transparency/
- Binance Margin Collateral and Haircut Guidelines: https://www.binance.com/en/support/faq
